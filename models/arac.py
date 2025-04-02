from abc import ABC, abstractmethod

class Arac(ABC):
    """
    Soyut araç sınıfı.
    Otobüs, Tramvay ve Taksi bu sınıftan türetilir.
    """

    def __init__(self, yolcu):
        """
        Yolcu nesnesi alınır, artık ödeme yöntemi araçta değil yolcunun cüzdanında saklanır.
        """
        self.yolcu = yolcu

    @abstractmethod
    def seyahat_suresi_hesapla(self, mesafe):
        """Aracın belirli bir mesafeyi ne kadar sürede gideceğini hesaplar."""
        pass

    @abstractmethod
    def ucret_hesapla(self, mesafe):
        """Aracın belirli bir mesafedeki ücretini hesaplar."""
        pass

    def seyahat_ve_odeme_yap(self, mesafe):
        """
        Seyahat süresi hesaplanır, ücret belirlenir ve yolcunun cüzdanı üzerinden ödeme yapılır.
        """
        sure = self.seyahat_suresi_hesapla(mesafe)
        tam_ucret = self.ucret_hesapla(mesafe)
        indirimli_ucret = self.yolcu.ucret_indirimi(tam_ucret)

        # 🚀 Ödeme yolcunun cüzdanı üzerinden gerçekleştirilir
        odeme_sonucu = self.yolcu.cuzdan.odeme_yap(indirimli_ucret)

        return f"🚗 Seyahat Süresi: {sure:.2f} dakika\n💰 {odeme_sonucu}"


class Otobus(Arac):
    """
    Otobüs sınıfı.
    """

    ORTALAMA_HIZ = 40  # km/h
    KM_BASI_UCRET = 2  # TL

    def __init__(self, yolcu):
        super().__init__(yolcu)

    def seyahat_suresi_hesapla(self, mesafe):
        """Otobüs ile tahmini süre hesaplama (dakika cinsinden)."""
        return (mesafe / self.ORTALAMA_HIZ) * 60

    def ucret_hesapla(self, mesafe):
        """Otobüs için mesafeye göre ücret hesaplama."""
        return mesafe * self.KM_BASI_UCRET


class Tramvay(Arac):
    """
    Tramvay sınıfı.
    """

    ORTALAMA_HIZ = 50  # km/h
    KM_BASI_UCRET = 2.5  # TL

    def __init__(self, yolcu):
        super().__init__(yolcu)

    def seyahat_suresi_hesapla(self, mesafe):
        """Tramvay ile tahmini süre hesaplama (dakika cinsinden)."""
        return (mesafe / self.ORTALAMA_HIZ) * 60

    def ucret_hesapla(self, mesafe):
        """Tramvay için mesafeye göre ücret hesaplama."""
        return mesafe * self.KM_BASI_UCRET


class Taksi(Arac):
    """
    Taksi sınıfı.
    """

    TAKSI_ACILIS_UCRETI = 10  # TL
    KM_BASI_UCRET = 4         # TL
    MIN_TAKSI_MESAFE = 3      # km

    def __init__(self, yolcu):
        super().__init__(yolcu)

    def seyahat_suresi_hesapla(self, mesafe):
        """
        Taksi ile tahmini süre hesaplama (dakika cinsinden).
        """
        ORTALAMA_HIZ = 60  # km/h
        return (mesafe / ORTALAMA_HIZ) * 60

    # Arac sınıfının beklentisini karşılayan override metot (self'li)
    def ucret_hesapla(self, mesafe):
        return self.TAKSI_ACILIS_UCRETI + (mesafe * self.KM_BASI_UCRET)

    # Koordinat bazlı ya da nesne oluşturmadan hesaplama için static versiyon
    @staticmethod
    def ucret_hesapla_static(mesafe):
        return Taksi.TAKSI_ACILIS_UCRETI + (mesafe * Taksi.KM_BASI_UCRET)

    @staticmethod
    def haversine_mesafe_km(enlem1, boylam1, enlem2, boylam2):
        """
        Haversine formülü ile iki koordinat arasındaki mesafeyi kilometre cinsinden hesaplar.
        """
        from math import radians, sin, cos, sqrt, atan2

        R = 6371  # Dünya yarıçapı (km)
        enlem1, boylam1, enlem2, boylam2 = map(radians, [enlem1, boylam1, enlem2, boylam2])
        d_enlem = enlem2 - enlem1
        d_boylam = boylam2 - boylam1

        a = sin(d_enlem / 2) ** 2 + cos(enlem1) * cos(enlem2) * sin(d_boylam / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return R * c  # Mesafe (km)

    @classmethod
    def taksi_ucreti_hesapla(cls, enlem1, boylam1, enlem2, boylam2):
        """
        Başlangıç ve hedef koordinatlara göre taksi mesafesini ve toplam ücretini hesaplar.
        """
        mesafe_km = cls.haversine_mesafe_km(enlem1, boylam1, enlem2, boylam2)
        toplam_ucret = cls.TAKSI_ACILIS_UCRETI + (mesafe_km * cls.KM_BASI_UCRET)
        return mesafe_km, toplam_ucret

    @classmethod
    def taksi_gerekli_mi(cls, mesafe):
        """
        Eğer mesafe belirlenen eşik değerinden büyükse taksi zorunludur.
        """
        return mesafe > cls.MIN_TAKSI_MESAFE

