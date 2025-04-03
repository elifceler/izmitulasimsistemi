import os
import json
from models.durak import Durak, UlasimGrafigi

# 📌 Proje kök dizinini al
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dosya_yolu = os.path.join(BASE_DIR, "data", "stops.json")


class VeriOkuyucu:
    """
    JSON dosyasını okuyan ve doğrulayan sınıf.
    """

    def __init__(self, dosya_yolu):
        """
        Sınıf başlatılırken dosya yolunu alır ve veriyi yüklemeye çalışır.
        """
        self.dosya_yolu = dosya_yolu
        self.veri = self.json_verisini_oku()

    def json_verisini_oku(self):
        """
        JSON dosyasını okur, doğrular ve 'duraklar' anahtarını kontrol eder.
        """
        try:
            with open(self.dosya_yolu, "r", encoding="utf-8") as dosya:
                veri = json.load(dosya)  # JSON dosyasını oku

            # 🚀 JSON yapısını kontrol et
            if not isinstance(veri, dict):
                raise ValueError("JSON hatalı! Beklenen format: dict")

            if "duraklar" not in veri or not isinstance(veri["duraklar"], list):
                raise KeyError("'duraklar' listesi eksik veya yanlış formatta!")

            print(f"✅ JSON geçerli! Durak sayısı: {len(veri['duraklar'])}")
            return veri

        except json.JSONDecodeError as e:
            print(f"🚨 JSON Hatası: Dosya bozuk veya yanlış formatta! Hata: {e}")
        except FileNotFoundError:
            print("🚨 Dosya bulunamadı! JSON dosyanızın yolunu kontrol edin.")
        except (ValueError, KeyError) as e:
            print(f"🚨 Veri Hatası: {e}")
        except Exception as e:
            print(f"🚨 Beklenmeyen Hata: {e}")

        return {}  # Hata olursa boş sözlük döndür

    def get_duraklar(self):
        """
        JSON içindeki 'duraklar' listesini döndürür.
        """
        return self.veri.get("duraklar", [])

    def grafigi_kur_jsondan(self):
        """
        JSON dosyasındaki durak, bağlantı ve transfer verilerine göre ulaşım grafiğini kurar.
        """
        ulasim_grafi = UlasimGrafigi()

        # 1️⃣ Durakları oluştur ve ekle
        for d in self.veri.get("duraklar", []):
            durak = Durak(
                durak_id=d["id"],
                ad=d["name"],
                enlem=d["lat"],
                boylam=d["lon"],
                arac_tipi=d.get("type", "").lower() if d.get("type") else None
            )

            ulasim_grafi.durak_ekle(durak)

        # 2️⃣ nextStops ile bağlantıları ekle (çift yönlü!)
        for d in self.veri.get("duraklar", []):
            kaynak_id = d["id"]
            for next_stop in d.get("nextStops", []):
                hedef_id = next_stop["stopId"]
                mesafe = next_stop["mesafe"]
                sure = next_stop["sure"]
                ucret = next_stop["ucret"]
                # ✅ Artık bağlantılar çift yönlü olarak ekleniyor
                ulasim_grafi.baglanti_ekle(kaynak_id, hedef_id, mesafe, sure, ucret)
                ulasim_grafi.baglanti_ekle(hedef_id, kaynak_id, mesafe, sure, ucret)

        # 3️⃣ Transfer bağlantılarını ekle (negatif ücretli olabilir)
        for d in self.veri.get("duraklar", []):
            kaynak_id = d["id"]
            transfer = d.get("transfer")
            if transfer:
                hedef_id = transfer["transferStopId"]
                sure = transfer["transferSure"]
                ucret = transfer["transferUcret"]  # Burada negatif ücret olabilir
                mesafe = 0.05  # Semboliktir
                ulasim_grafi.baglanti_ekle(
                    kaynak_id, hedef_id, mesafe, sure, ucret, transfer_mi=True
                )

        return ulasim_grafi
