from models.yolcu import YolcuTipi, GenelYolcu, Ogrenci, Yasli, Ogretmen, SehitGaziYakini, Engelli
from models.odeme import Cuzdan, KentkartOdeme, MobilOdeme, KrediKartiOdeme, NakitOdeme


class OdemeFactory:
    @staticmethod
    def olustur(kentkart, mobil, kredi, nakit):
        yontemler = []
        if kentkart > 0:
            yontemler.append(KentkartOdeme(kentkart))
        if mobil > 0:
            yontemler.append(MobilOdeme(mobil))
        if kredi > 0:
            yontemler.append(KrediKartiOdeme(kredi))
        if nakit > 0:
            yontemler.append(NakitOdeme(nakit))
        return yontemler


class YolcuFactory:
    global_yolcu = None  # sadece Yasli tipi için tutulur

    @staticmethod
    def olustur(tip, isim, yas, cuzdan):
        if tip == YolcuTipi.YASLI:
            if YolcuFactory.global_yolcu and isinstance(YolcuFactory.global_yolcu, Yasli):
                yolcu = YolcuFactory.global_yolcu
                yolcu.cuzdan = cuzdan
                return yolcu
            else:
                yolcu = Yasli(isim, yas, cuzdan)
                YolcuFactory.global_yolcu = yolcu
                return yolcu

        # Diğer yolcu tipleri için sadeleştirilmiş yapı
        siniflar = {
            YolcuTipi.GENEL: GenelYolcu,
            YolcuTipi.OGRENCI: Ogrenci,
            YolcuTipi.OGRETMEN: Ogretmen,
            YolcuTipi.SEHIT_GAZI_YAKINI: SehitGaziYakini,
            YolcuTipi.ENGELLI: Engelli
        }

        if tip in siniflar:
            return siniflar[tip](isim, yas, cuzdan)
        else:
            raise ValueError(f"Tanımsız yolcu tipi: {tip}")
