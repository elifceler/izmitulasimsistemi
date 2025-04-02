from enum import Enum
from abc import ABC, abstractmethod

class YolcuTipi(Enum):
    GENEL = "Genel"
    OGRENCI = "Öğrenci"
    YASLI = "Yaşlı"
    OGRETMEN = "Öğretmen"
    SEHIT_GAZI_YAKINI = "Şehit & Gazi Yakını"
    ENGELLI = "Engelli"


class Yolcu(ABC):
    def __init__(self, isim, yas, tipi: YolcuTipi, cuzdan):
        self.isim = isim
        self.yas = yas
        self.tipi = tipi  # Yolcu tipini belirtiyoruz
        self.cuzdan = cuzdan

    @abstractmethod
    def ucret_indirimi(self, ucret, arac_tipi=None):
        pass


# **Alt sınıflar (Tüm yolcu tipleri)**
class GenelYolcu(Yolcu):
    def __init__(self, isim, yas, cuzdan):
        super().__init__(isim, yas, YolcuTipi.GENEL, cuzdan)

    def ucret_indirimi(self, ucret, arac_tipi=None):
        return ucret

class Ogrenci(Yolcu):
    INDIRIM_ORANI = 0.50

    def __init__(self, isim, yas, cuzdan):
        super().__init__(isim, yas, YolcuTipi.OGRENCI, cuzdan)

    def ucret_indirimi(self, ucret, arac_tipi=None):
        if arac_tipi == "taksi":
            return ucret  # Takside indirim yok
        return ucret * (1 - self.INDIRIM_ORANI)


class Yasli(Yolcu):
    INDIRIM_ORANI = 0.20
    UCRETSIZ_HAK_SAYISI = 20

    def __init__(self, isim, yas, cuzdan):
        super().__init__(isim, yas, YolcuTipi.YASLI, cuzdan)
        self.kalan_ucretsiz_hak = self.UCRETSIZ_HAK_SAYISI

    def ucret_indirimi(self, ucret, arac_tipi=None):
        if arac_tipi != "taksi" and self.kalan_ucretsiz_hak > 0:
            self.kalan_ucretsiz_hak -= 1
            return 0  # Ücretsiz geçiş
        return ucret * (1 - self.INDIRIM_ORANI)


class Ogretmen(Yolcu):
    INDIRIM_ORANI = 0.20

    def __init__(self, isim, yas, cuzdan):
        super().__init__(isim, yas, YolcuTipi.OGRETMEN, cuzdan)

    def ucret_indirimi(self, ucret, arac_tipi=None):
        if arac_tipi == "taksi":
            return ucret
        return ucret * (1 - self.INDIRIM_ORANI)


class SehitGaziYakini(Yolcu):
    def __init__(self, isim, yas, cuzdan):
        super().__init__(isim, yas, YolcuTipi.SEHIT_GAZI_YAKINI, cuzdan)

    def ucret_indirimi(self, ucret, arac_tipi=None):
        if arac_tipi == "taksi":
            return ucret
        return 0


class Engelli(Yolcu):
    def __init__(self, isim, yas, cuzdan):
        super().__init__(isim, yas, YolcuTipi.ENGELLI, cuzdan)

    def ucret_indirimi(self, ucret, arac_tipi=None):
        if arac_tipi == "taksi":
            return ucret
        return 0
