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
    def ucret_indirimi(self, ucret):
        """Alt sınıflar tarafından uygulanması gereken soyut metod."""
        pass


# **Alt sınıflar (Tüm yolcu tipleri)**
class GenelYolcu(Yolcu):
    def __init__(self, isim, yas, cuzdan):
        super().__init__(isim, yas, YolcuTipi.GENEL, cuzdan)

    def ucret_indirimi(self, ucret):
        return ucret  # İndirim yok


class Ogrenci(Yolcu):
    INDIRIM_ORANI = 0.50

    def __init__(self, isim, yas, cuzdan):
        super().__init__(isim, yas, YolcuTipi.OGRENCI, cuzdan)

    def ucret_indirimi(self, ucret):
        return ucret * (1 - self.INDIRIM_ORANI)


class Yasli(Yolcu):
    INDIRIM_ORANI = 0.20

    def __init__(self, isim, yas, cuzdan):
        super().__init__(isim, yas, YolcuTipi.YASLI, cuzdan)

    def ucret_indirimi(self, ucret):
        return ucret * (1 - self.INDIRIM_ORANI)


class Ogretmen(Yolcu):
    INDIRIM_ORANI = 0.20

    def __init__(self, isim, yas, cuzdan):
        super().__init__(isim, yas, YolcuTipi.OGRETMEN, cuzdan)

    def ucret_indirimi(self, ucret):
        return ucret * (1 - self.INDIRIM_ORANI)


class SehitGaziYakini(Yolcu):
    def __init__(self, isim, yas, cuzdan):
        super().__init__(isim, yas, YolcuTipi.SEHIT_GAZI_YAKINI, cuzdan)

    def ucret_indirimi(self, ucret):
        return 0  # Ücretsiz


class Engelli(Yolcu):
    def __init__(self, isim, yas, cuzdan):
        super().__init__(isim, yas, YolcuTipi.ENGELLI, cuzdan)

    def ucret_indirimi(self, ucret):
        return 0  # Ücretsiz*