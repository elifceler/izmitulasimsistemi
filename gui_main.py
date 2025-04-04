import tkinter as tk
from tkinter import messagebox, scrolledtext
from utils.factory import OdemeFactory, YolcuFactory

dosya_yolu = r"C:\Users\batus\PycharmProjects\moduler-ulasimsistemi2\data\stops_cift_yonlu.json"

# services klasöründen
from models.veri import VeriOkuyucu
from services.rota import RotaHesaplayici

# utils klasöründen
from utils.harita import haritada_goster

# models klasöründen
from models.yolcu import YolcuTipi, GenelYolcu, Ogrenci, Yasli, Ogretmen, SehitGaziYakini, Engelli
from models.odeme import Cuzdan, KentkartOdeme, MobilOdeme, KrediKartiOdeme, NakitOdeme
from models.arac import Taksi

global_harita_verisi = {}


def haritayi_ac():
    if "rota_adimlari" in global_harita_verisi and "ulasim_grafi" in global_harita_verisi:
        haritada_goster(global_harita_verisi["rota_adimlari"], global_harita_verisi["ulasim_grafi"])
    else:
        messagebox.showwarning("Uyarı", "Lütfen önce rota hesaplayın.")


def arayuzu_baslat():
    def girdileri_al():
        return {
            "baslat_lat": float(entry_baslat_lat.get()),
            "baslat_lon": float(entry_baslat_lon.get()),
            "hedef_lat": float(entry_hedef_lat.get()),
            "hedef_lon": float(entry_hedef_lon.get()),
            "isim": entry_isim.get(),
            "yas": int(entry_yas.get()),
            "yolcu_tipi": YolcuTipi[yolcu_var.get().upper()],
            "kentkart": float(entry_kentkart.get()),
            "mobil": float(entry_mobil.get()),
            "kredi": float(entry_kredi.get()),
            "nakit": float(entry_nakit.get())
        }

    def hesapla():
        global global_yolcu
        try:
            veri = girdileri_al()

            baslat_lat = veri["baslat_lat"]
            baslat_lon = veri["baslat_lon"]
            hedef_lat = veri["hedef_lat"]
            hedef_lon = veri["hedef_lon"]
            isim = veri["isim"]
            yas = veri["yas"]
            yolcu_tipi = veri["yolcu_tipi"]
            kentkart = veri["kentkart"]
            mobil = veri["mobil"]
            kredi = veri["kredi"]
            nakit = veri["nakit"]

            odeme_yontemleri = OdemeFactory.olustur(kentkart, mobil, kredi, nakit)

            if not odeme_yontemleri:
                messagebox.showerror("Hata", "En az bir ödeme yöntemi girilmelidir.")
                return

            cuzdan = Cuzdan(odeme_yontemleri)

            yolcu = YolcuFactory.olustur(yolcu_tipi, isim, yas, cuzdan)

            veri_okuyucu = VeriOkuyucu(dosya_yolu)
            ulasim_grafi = veri_okuyucu.grafigi_kur_jsondan()
            rota_hesaplayici = RotaHesaplayici(ulasim_grafi)

            bas_durak, bas_mesafe = rota_hesaplayici.en_yakin_durak_bul(baslat_lat, baslat_lon)
            hedef_durak, hedef_mesafe = rota_hesaplayici.en_yakin_durak_bul(hedef_lat, hedef_lon)

            _, rota_adimlari = rota_hesaplayici.en_kisa_yol_hesapla(bas_durak.durak_id, hedef_durak.durak_id)

            # Başlangıç durağına taksi gerekiyorsa, rota_adimlari'nın başına taksi adımı ekle
            if Taksi.taksi_gerekli_mi(bas_mesafe):
                rota_adimlari.insert(0, {
                    "tip": "taksi",
                    "sure": round(bas_mesafe / 0.8),
                    "mesafe": round(bas_mesafe, 2),
                    "ucret": Taksi.ucret_hesapla_static(bas_mesafe),
                    "koordinatlar": [(baslat_lat, baslat_lon), (bas_durak.enlem, bas_durak.boylam)]
                })

            # Hedef durağa taksi gerekiyorsa, rota_adimlari'nın sonuna taksi adımı ekle
            if Taksi.taksi_gerekli_mi(hedef_mesafe):
                rota_adimlari.append({
                    "tip": "taksi",
                    "sure": round(hedef_mesafe / 0.8),
                    "mesafe": round(hedef_mesafe, 2),
                    "ucret": Taksi.ucret_hesapla_static(hedef_mesafe),
                    "koordinatlar": [(hedef_durak.enlem, hedef_durak.boylam), (hedef_lat, hedef_lon)]
                })

            # 🔁 Harita için rota ve grafik bilgisini sakla
            global_harita_verisi["rota_adimlari"] = rota_adimlari
            global_harita_verisi["ulasim_grafi"] = ulasim_grafi

            text_output.delete('1.0', tk.END)

            text_output.tag_config("baslik", foreground="blue", font=("Arial", 10, "bold"))
            text_output.tag_config("alt_baslik", foreground="darkgreen", font=("Arial", 10, "bold"))
            text_output.tag_config("normal", font=("Arial", 10))
            text_output.tag_config("odeme", foreground="green", font=("Arial", 10))
            text_output.tag_config("toplam", foreground="red", font=("Arial", 10, "bold"))
            text_output.tag_config("taksi", foreground="darkorange", font=("Arial", 10, "bold"))
            text_output.tag_config("alternatif", foreground="purple", font=("Arial", 10, "bold"))
            text_output.tag_config("taksi_kelime", foreground="darkorange", font=("Arial", 10, "bold"))
            text_output.tag_config("taksi_blok", foreground="darkorange", font=("Arial", 10))

            text_output.insert(tk.END, f"📍 Başlangıç Durağı: {bas_durak.ad} ➝ {hedef_durak.ad} (En Ekonomik)\n",
                               "alt_baslik")

            toplam_sure = sum([step['sure'] for step in rota_adimlari])
            toplam_mesafe = sum([step['mesafe'] for step in rota_adimlari])

            text_output.insert(tk.END, f"📏 Tahmini Mesafe: {toplam_mesafe:.2f} km\n", "normal")
            text_output.insert(tk.END, f"⏳ Tahmini Süre: {toplam_sure:.0f} dk\n\n", "normal")
            if Taksi.taksi_gerekli_mi(bas_mesafe):
                text_output.insert(tk.END,
                                   f"🚖 Başlangıç durağına taksiyle gitmeniz gerekiyor. Uzaklık: {bas_mesafe:.2f} km\n",
                                   "taksi")
            if Taksi.taksi_gerekli_mi(hedef_mesafe):
                text_output.insert(tk.END,
                                   f"🚖 Hedef durağa ulaşmak için taksi gerekebilir. Uzaklık: {hedef_mesafe:.2f} km\n",
                                   "taksi")

            toplam_ucret = 0
            for i, adim in enumerate(rota_adimlari, start=1):
                if "kaynak" in adim and "hedef" in adim:
                    kaynak = ulasim_grafi.duraklar[adim["kaynak"]]
                    hedef = ulasim_grafi.duraklar[adim["hedef"]]
                    ucret = adim["ucret"]
                    indirimli_ucret = yolcu.ucret_indirimi(ucret, arac_tipi="toplu_tasima")
                    odeme_sonucu = yolcu.cuzdan.odeme_yap(indirimli_ucret)
                    toplam_ucret += indirimli_ucret

                    text_output.insert(tk.END, f"{i}. {kaynak.ad} ➔ {hedef.ad} ({adim['sure']} dk, {ucret:.2f} TL)\n",
                                       "normal")
                    if ucret != indirimli_ucret:
                        text_output.insert(tk.END, f"   🎫 İndirimli: {indirimli_ucret:.2f} TL\n", "odeme")
                    text_output.insert(tk.END, f"   💳 {odeme_sonucu}\n", "odeme")

                    # ✅ Teşvik varsa mesajı göster
                    if ucret == 0.00:
                        text_output.insert(tk.END, "   🔄 Aktarma teşviki uygulanmıştır.\n", "normal")

                    text_output.insert(tk.END, "\n")


                elif adim.get("tip") == "taksi":
                    # Taksi adımı ayrı işleniyor
                    mesafe = adim["mesafe"]
                    sure = adim["sure"]
                    ucret = adim["ucret"]
                    odeme_sonucu = yolcu.cuzdan.odeme_yap(ucret, arac_tipi="taksi")
                    toplam_ucret += ucret

                    text_output.insert(tk.END, f"🚖 Taksi ile {mesafe:.2f} km, Süre: {sure} dk\n", "taksi")
                    text_output.insert(tk.END, f"   💸 Ücret: {ucret:.2f} TL\n", "taksi")
                    text_output.insert(tk.END, f"   💳 {odeme_sonucu}\n\n", "taksi")

            # Alternatif rotaları al
            alternatifler = rota_hesaplayici.rota_alternatifleri((baslat_lat, baslat_lon), (hedef_lat, hedef_lon))

            # En az aktarmalı rotayı bul
            en_az_aktarma_sayisi = float('inf')

            for baslik, adimlar in alternatifler.items():
                onceki_tip = None
                aktarma_sayisi = 0

                for adim in adimlar:
                    if "kaynak" in adim and "hedef" in adim:
                        hedef = ulasim_grafi.duraklar[adim["hedef"]]
                        mevcut_tip = hedef.arac_tipi  # veya kaynak.arac_tipi de kullanılabilir

                        if onceki_tip is not None and mevcut_tip != onceki_tip:
                            aktarma_sayisi += 1

                        onceki_tip = mevcut_tip

                if aktarma_sayisi < en_az_aktarma_sayisi:
                    en_az_aktarma_sayisi = aktarma_sayisi

            # Alternatif rotaları yazdır*
            text_output.insert(tk.END, "\nAlternatif Rotalar:\n", "alternatif")

            rota_ozetleri = {}
            for baslik, adimlar in alternatifler.items():
                if "Taksi" in baslik:
                    # Taksi rotasında direkt 0 aktarma sayısı
                    aktarma_sayisi = 0
                    taksi_mesafe = 0
                    for a in adimlar:
                        if "Taksi ile:" in a:
                            try:
                                taksi_mesafe = float(a.split(":")[1].strip().split()[0])
                            except:
                                taksi_mesafe = 3
                            break
                    mesafe = taksi_mesafe
                    sure = round(Taksi(None).seyahat_suresi_hesapla(mesafe))
                else:
                    # Burada gerçek hesaplama yapılır
                    aktarma_sayisi = hesapla_gercek_aktarma(adimlar, ulasim_grafi)
                    mesafe = sum(1 for a in adimlar if "➝" in a)
                    sure = mesafe * 3

                rota_ozetleri[baslik] = {
                    "aktarma": aktarma_sayisi,
                    "mesafe": round(mesafe, 2),
                    "sure": sure
                }

            min_aktarma = min(rota_ozetleri.items(), key=lambda x: x[1]['aktarma'])[0]
            min_mesafe = min(rota_ozetleri.items(), key=lambda x: x[1]['mesafe'])[0]
            min_sure = min(rota_ozetleri.items(), key=lambda x: x[1]['sure'])[0]

            for baslik, adimlar in alternatifler.items():
                etiket = []
                if "Taksi" not in baslik and baslik == min_aktarma:
                    etiket.append("En Az Aktarmalı")
                if baslik == min_mesafe:
                    etiket.append("En Kısa")
                if baslik == min_sure:
                    etiket.append("En Hızlı")

                etiket_str = f" ({', '.join(etiket)})" if etiket else ""
                tag_to_use = "taksi_blok" if "Taksi" in baslik else "normal"

                if "Sadece Tramvay" in baslik:
                    baslik_gosterim = f"{baslik} Rota (Rahat ve Dengeli Bir Ulaşım Seçeneği)"
                else:
                    baslik_gosterim = f"{baslik} Rota"

                text_output.insert(tk.END, f"\n→ {baslik_gosterim}{etiket_str}:\n", "alternatif")

                for i, adim in enumerate(adimlar, start=1):
                    text_output.insert(tk.END, f"  {i}. {adim}\n", tag_to_use)

                    # 0 TL'lik aktarma teşvikini yakala
                    if "0.00" in adim or "aktarma" in adim.lower() or "transfer" in adim.lower():
                        text_output.insert(tk.END, "    🔄 Aktarma teşviki uygulanmıştır.\n", tag_to_use)

                # Özeti göster
                ozet = rota_ozetleri[baslik]
                text_output.insert(tk.END,
                                   f"    ⏳ Süre: {ozet['sure']} dk, 📏 Mesafe: {ozet['mesafe']} km, 🔁 Aktarma: {ozet['aktarma']}\n",
                                   "normal")

            text_output.insert(tk.END, f"\n💰 Toplam Ulaşım Ücreti: {toplam_ucret:.2f} TL\n", "toplam")

            if isinstance(yolcu, Yasli):
                text_output.insert(tk.END, f"🎁 Kalan ücretsiz hak: {yolcu.kalan_ucretsiz_hak}\n", "odeme")

            text_output.insert(tk.END, "\n💼 Güncel Cüzdan Durumu:\n", "odeme")

            for yontem in yolcu.cuzdan.odeme_yontemleri:
                sinif_adi = yontem.__class__.__name__
                ikon = {
                    "NakitOdeme": "💵",
                    "KrediKartiOdeme": "💳",
                    "KentkartOdeme": "🚌",
                    "MobilOdeme": "📱"
                }.get(sinif_adi, "💰")
                text_output.insert(tk.END, f"{ikon} {sinif_adi}: {yontem.bakiye:.2f} TL\n", "odeme")


        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def hesapla_gercek_aktarma(adimlar, ulasim_grafi):
        onceki_tip = None
        aktarma = 0
        for adim in adimlar:
            if "kaynak" in adim and "hedef" in adim:
                kaynak = ulasim_grafi.duraklar[adim["kaynak"]]
                hedef = ulasim_grafi.duraklar[adim["hedef"]]
                mevcut_tip = hedef.arac_tipi
                if onceki_tip is not None and mevcut_tip != onceki_tip:
                    aktarma += 1
                onceki_tip = mevcut_tip
        return aktarma

    pencere = tk.Tk()
    pencere.title("🗺️ Ulaşım Rota Planlayıcı")
    pencere.configure(bg="#f0f0f0")

    # Ana Başlık
    tk.Label(pencere, text="Ulaşım Rota Planlayıcı", font=("Helvetica", 16, "bold"), bg="#f0f0f0").grid(row=0, column=0,
                                                                                                        columnspan=2,
                                                                                                        pady=(10, 20))

    # Giriş Alanları (LabelFrame ile gruplandırma)
    frame_input = tk.LabelFrame(pencere, text="📌 Giriş Bilgileri", padx=10, pady=10, bg="#f0f0f0")
    frame_input.grid(row=1, column=0, columnspan=2, padx=10, sticky="we")

    labels = ["Başlangıç Enlem:", "Başlangıç Boylam:", "Hedef Enlem:", "Hedef Boylam:",
              "İsim:", "Yaş:", "Kentkart Bakiye:", "Mobil Bakiye:", "Kredi Kartı:", "Nakit:"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(frame_input, text=label, anchor="w", width=20, bg="#f0f0f0").grid(row=i, column=0, sticky="e", pady=2)
        entry = tk.Entry(frame_input, width=30)
        entry.grid(row=i, column=1, pady=2)
        entries.append(entry)

    (entry_baslat_lat, entry_baslat_lon, entry_hedef_lat, entry_hedef_lon,
     entry_isim, entry_yas, entry_kentkart, entry_mobil, entry_kredi, entry_nakit) = entries

    # Yolcu Tipi Seçimi
    tk.Label(frame_input, text="Yolcu Tipi:", anchor="w", width=20, bg="#f0f0f0").grid(row=10, column=0, sticky="e",
                                                                                       pady=5)
    yolcu_var = tk.StringVar()
    yolcu_var.set("GENEL")
    yolcu_tipleri = [t.name for t in YolcuTipi]
    tk.OptionMenu(frame_input, yolcu_var, *yolcu_tipleri).grid(row=10, column=1, sticky="w")

    # Rota Hesapla Butonu
    btn = tk.Button(pencere, text="🚀 Rota Hesapla", command=hesapla, bg="#4CAF50", fg="white",
                    font=("Arial", 11, "bold"), padx=10, pady=5)
    btn.grid(row=2, column=0, padx=(20, 10), pady=15, sticky="e")

    btn_harita = tk.Button(pencere, text="🗺️ Haritada Göster", command=haritayi_ac, bg="#2196F3", fg="white",
                           font=("Arial", 11, "bold"), padx=10, pady=5)
    btn_harita.grid(row=2, column=1, padx=(10, 20), pady=15, sticky="w")

    # Sonuç Kutusu
    frame_output = tk.LabelFrame(pencere, text="📋 Sonuçlar", padx=10, pady=10, bg="#f0f0f0")
    frame_output.grid(row=3, column=0, columnspan=2, padx=10, pady=(0, 15), sticky="we")

    text_output = scrolledtext.ScrolledText(frame_output, width=80, height=25, font=("Courier New", 10))
    text_output.pack()

    pencere.mainloop()

if __name__ == "__main__":
    arayuzu_baslat()