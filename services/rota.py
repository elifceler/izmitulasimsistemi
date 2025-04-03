from models.arac import Taksi

class RotaHesaplayici:
    """
    Kullanıcının belirttiği başlangıç ve hedef konumuna göre en uygun ulaşım rotalarını hesaplar.
    """

    def __init__(self, ulasim_grafi):
        """
        Başlangıçta toplu taşıma grafını alır.
        :param ulasim_grafi: Durakları içeren ulaşım ağı (graf yapısı).
        """
        self.ulasim_grafi = ulasim_grafi

    def en_yakin_durak_bul(self, enlem, boylam, arac_tipi=None):
        en_yakin_durak, mesafe = None, float('inf')

        for durak in self.ulasim_grafi.duraklar.values():
            if arac_tipi and durak.arac_tipi != arac_tipi:
                continue  # Yalnızca istenen tipteki durakları dikkate al

            uzaklik = Taksi.haversine_mesafe_km(enlem, boylam, durak.enlem, durak.boylam)
            if uzaklik < mesafe:
                mesafe = uzaklik
                en_yakin_durak = durak

        return en_yakin_durak, mesafe

    def en_kisa_yol_hesapla(self, baslangic_durak_id, hedef_durak_id, arac_tipi=None):
        """
        Dijkstra algoritması ile en kısa yolu hesaplar ve her adım için detaylı bilgi döndürür.
        :param baslangic_durak_id: Başlangıç durağının ID'si.
        :param hedef_durak_id: Hedef durağın ID'si.
        :param arac_tipi: 'otobus' veya 'tramvay' (Opsiyonel).
        :return: (Toplam mesafe, rota_adimlari: {kaynak, hedef, mesafe, sure, ucret, transfer_mi} listesi)
        """

        mesafeler = {durak_id: float('inf') for durak_id in self.ulasim_grafi.duraklar}
        onceki_duraklar = {durak_id: None for durak_id in self.ulasim_grafi.duraklar}
        mesafeler[baslangic_durak_id] = 0

        ziyaret_edilmemis = list(self.ulasim_grafi.duraklar.keys())

        while ziyaret_edilmemis:
            mevcut_durak_id = min(ziyaret_edilmemis, key=lambda durak: mesafeler[durak])

            if mevcut_durak_id == hedef_durak_id:
                break

            for komsu, mesafe, _, _, _ in self.ulasim_grafi.duraklar[mevcut_durak_id].komsular:
                print(f"🔍 İncelenen komşu: {komsu.durak_id}, türü: {komsu.arac_tipi}")

                if arac_tipi and (komsu.arac_tipi is None or komsu.arac_tipi != arac_tipi):

                    continue  # Uygun tip değilse atla

                yeni_mesafe = mesafeler[mevcut_durak_id] + mesafe
                if yeni_mesafe < mesafeler[komsu.durak_id]:
                    mesafeler[komsu.durak_id] = yeni_mesafe
                    onceki_duraklar[komsu.durak_id] = mevcut_durak_id

            ziyaret_edilmemis.remove(mevcut_durak_id)

        # En kısa yolun durak ID'lerini bul
        en_kisa_yol_ids = []
        mevcut_durak = hedef_durak_id
        while mevcut_durak is not None:
            en_kisa_yol_ids.insert(0, mevcut_durak)
            mevcut_durak = onceki_duraklar[mevcut_durak]

        # Rota adımlarının detaylarını topla
        rota_adimlari = []
        for i in range(len(en_kisa_yol_ids) - 1):
            kaynak_id = en_kisa_yol_ids[i]
            hedef_id = en_kisa_yol_ids[i + 1]
            komsular = self.ulasim_grafi.duraklar[kaynak_id].komsular

            for komsu, mesafe, sure, ucret, transfer_mi in komsular:
                if komsu.durak_id == hedef_id:
                    rota_adimlari.append({
                        "kaynak": kaynak_id,
                        "hedef": hedef_id,
                        "mesafe": mesafe,
                        "sure": sure,
                        "ucret": ucret,
                        "transfer_mi": transfer_mi
                    })
                    break

        return mesafeler[hedef_durak_id], rota_adimlari

    def otobus_tramvay_aktarma_hesapla(self, baslangic_durak_id, hedef_durak_id):
        """
        Otobüs ve tramvay arasındaki en uygun aktarma noktalarını hesaplar.
        :return: En kısa mesafe ve aktarma duraklarını içeren güzergah listesi.
        """

        en_kisa_mesafe = float('inf')
        en_iyi_aktarma = None

        for durak in self.ulasim_grafi.duraklar.values():
            if "tram" in durak.ad:
                mesafe1, yol1 = self.en_kisa_yol_hesapla(baslangic_durak_id, durak.durak_id, arac_tipi="otobus")
                mesafe2, yol2 = self.en_kisa_yol_hesapla(durak.durak_id, hedef_durak_id, arac_tipi="tramvay")

                toplam_mesafe = mesafe1 + mesafe2
                if toplam_mesafe < en_kisa_mesafe:
                    en_kisa_mesafe = toplam_mesafe
                    en_iyi_aktarma = yol1 + yol2

        return en_kisa_mesafe, en_iyi_aktarma

    def rota_alternatifleri(self, baslangic_konum, hedef_konum):
        bas_durak, bas_mesafe = self.en_yakin_durak_bul(*baslangic_konum)
        hedef_durak, hedef_mesafe = self.en_yakin_durak_bul(*hedef_konum)

        rota_sonuclari = {}

        print(f"\n🔰 Başlangıç konumuna en yakın durak: {bas_durak.ad}")
        print(f"Uzaklık: {bas_mesafe:.2f} km")
        print("➡️ Taksi gerekiyor:", "Evet" if Taksi.taksi_gerekli_mi(bas_mesafe) else "Hayır")

        print(f"\n🎯 Hedef konuma en yakın durak: {hedef_durak.ad}")
        print(f"Uzaklık: {hedef_mesafe:.2f} km")
        print("➡️ Taksi gerekiyor:", "Evet" if Taksi.taksi_gerekli_mi(hedef_mesafe) else "Hayır")

        def rota_olustur(yol, rota_adi, beklenen_tur=None):
            # 🚫 Beklenen araç türü kontrolü
            if beklenen_tur:
                for adim in yol:
                    if not adim['transfer_mi']:  # ⛔ Sadece gerçek ulaşım adımlarında kontrol et
                        kaynak_tur = self.ulasim_grafi.duraklar[adim['kaynak']].arac_tipi
                        hedef_tur = self.ulasim_grafi.duraklar[adim['hedef']].arac_tipi
                        if kaynak_tur != beklenen_tur or hedef_tur != beklenen_tur:
                            print(f"⛔ Uygunsuz adım: {kaynak_tur} → {hedef_tur}")
                            return

            rota = []
            ilk_durak = self.ulasim_grafi.duraklar[yol[0]['kaynak']]
            son_durak = self.ulasim_grafi.duraklar[yol[-1]['hedef']]

            ilk_mesafe = Taksi.haversine_mesafe_km(*baslangic_konum, ilk_durak.enlem, ilk_durak.boylam)
            son_mesafe = Taksi.haversine_mesafe_km(son_durak.enlem, son_durak.boylam, *hedef_konum)

            if ilk_mesafe > 3:
                rota.append(f"Başlangıç konum ➝ {ilk_durak.ad} (🚖 Taksi ile {ilk_mesafe:.2f} km)")

            for adim in yol:
                kaynak_ad = self.ulasim_grafi.duraklar[adim['kaynak']].ad
                hedef_ad = self.ulasim_grafi.duraklar[adim['hedef']].ad
                rota.append(f"{kaynak_ad} ➝ {hedef_ad}")

            if son_mesafe > 3:
                rota.append(f"{son_durak.ad} ➝ Hedef konum (🚖 Taksi ile {son_mesafe:.2f} km)")

            rota_sonuclari[rota_adi] = rota

        # 1️⃣ Sadece Otobüs (yeni mantıkla)
        en_yakin_bus_bas, mesafe_bus_bas = self.en_yakin_durak_bul(*baslangic_konum, arac_tipi="bus")
        en_yakin_bus_hedef, mesafe_bus_hedef = self.en_yakin_durak_bul(*hedef_konum, arac_tipi="bus")

        if en_yakin_bus_bas.arac_tipi == "bus" and en_yakin_bus_hedef.arac_tipi == "bus":
            mesafe_otobus, yol_otobus = self.en_kisa_yol_hesapla(
                en_yakin_bus_bas.durak_id, en_yakin_bus_hedef.durak_id, arac_tipi="bus"
            )

            if yol_otobus:
                rota = []

                # Başlangıçtan en yakın otobüs durağına yürüyüş
                yurume_mesafe_bas = Taksi.haversine_mesafe_km(
                    *baslangic_konum, en_yakin_bus_bas.enlem, en_yakin_bus_bas.boylam
                )
                if yurume_mesafe_bas > 0.05:
                    rota.append(
                        f"Başlangıç ➝ {en_yakin_bus_bas.ad} (🚶 Yürüyerek {yurume_mesafe_bas:.2f} km)"
                    )

                # Otobüs güzergahı
                for adim in yol_otobus:
                    kaynak_ad = self.ulasim_grafi.duraklar[adim['kaynak']].ad
                    hedef_ad = self.ulasim_grafi.duraklar[adim['hedef']].ad
                    rota.append(f"{kaynak_ad} ➝ {hedef_ad}")

                # Hedef durağından hedef konuma yürüyüş
                yurume_mesafe_hedef = Taksi.haversine_mesafe_km(
                    en_yakin_bus_hedef.enlem, en_yakin_bus_hedef.boylam, *hedef_konum
                )
                if yurume_mesafe_hedef > 0.05:
                    rota.append(
                        f"{en_yakin_bus_hedef.ad} ➝ Hedef (🚶 Yürüyerek {yurume_mesafe_hedef:.2f} km)"
                    )

                rota_sonuclari["Sadece Otobüs"] = rota

        # 2️⃣ Sadece Tramvay (yeni mantıkla)
        en_yakin_tram_bas, mesafe_tram_bas = self.en_yakin_durak_bul(*baslangic_konum, arac_tipi="tram")
        en_yakin_tram_hedef, mesafe_tram_hedef = self.en_yakin_durak_bul(*hedef_konum, arac_tipi="tram")

        if en_yakin_tram_bas.arac_tipi == "tram" and en_yakin_tram_hedef.arac_tipi == "tram":
            mesafe_tramvay, yol_tramvay = self.en_kisa_yol_hesapla(
                en_yakin_tram_bas.durak_id, en_yakin_tram_hedef.durak_id, arac_tipi="tram"
            )

            if yol_tramvay:
                rota = []

                # 🚖 Başlangıç konumu tramvay durağına 3 km'den uzaksa taksi
                if mesafe_tram_bas > 3:
                    rota.append(f"Başlangıç ➝ {en_yakin_tram_bas.ad} (🚖 Taksi ile {mesafe_tram_bas:.2f} km)")
                elif mesafe_tram_bas > 0.05:
                    rota.append(f"Başlangıç ➝ {en_yakin_tram_bas.ad} (🚶 Yürüyerek {mesafe_tram_bas:.2f} km)")

                # 🚋 Tramvayla yolculuk
                for adim in yol_tramvay:
                    kaynak_ad = self.ulasim_grafi.duraklar[adim['kaynak']].ad
                    hedef_ad = self.ulasim_grafi.duraklar[adim['hedef']].ad
                    rota.append(f"{kaynak_ad} ➝ {hedef_ad}")

                # 🚶 Hedef tramvay durağından hedefe yürüyüş (her zaman yürüyerek)
                if mesafe_tram_hedef > 0.05:
                    rota.append(f"{en_yakin_tram_hedef.ad} ➝ Hedef (🚶 Yürüyerek {mesafe_tram_hedef:.2f} km)")

                rota_sonuclari["Sadece Tramvay"] = rota

        # 3️⃣ Karma sistem için zaten beklenen_tur yok, olduğu gibi kalabilir:
        mesafe_karma, yol_karma = self.otobus_tramvay_aktarma_hesapla(bas_durak.durak_id, hedef_durak.durak_id)
        if yol_karma:
            rota_olustur(yol_karma, "Otobüs + Tramvay Aktarması")

        taksi_mesafe, taksi_ucret = Taksi.taksi_ucreti_hesapla(*baslangic_konum, *hedef_konum)
        sure = Taksi(None).seyahat_suresi_hesapla(taksi_mesafe)
        rota_sonuclari["Sadece Taksi"] = [
            f"Başlangıç konum ➝ Hedef konum",
            f"🚖 Taksi ile: {taksi_mesafe:.2f} km",
            f"🕒 Süre: {sure:.0f} dk",
            f"💰 Ücret: {taksi_ucret:.2f} TL"
        ]

        return rota_sonuclari