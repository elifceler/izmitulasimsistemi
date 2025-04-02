from abc import ABC, abstractmethod

class Cuzdan:
    def __init__(self, odeme_yontemleri):
        """
        odeme_yontemleri: OdemeYontemi nesnelerinden oluşan liste
        """
        self.odeme_yontemleri = odeme_yontemleri

    def odeme_yap(self, tutar, arac_tipi=None):
        """
        Tutar kadar ödeme yapabilecek ilk uygun yöntemi bulup ödemeyi gerçekleştirir.
        'arac_tipi' belirtilirse, sadece o araçla uyumlu yöntemler denenir.
        """
        for yontem in self.odeme_yontemleri:
            # Taksi için Kentkart geçerli değil
            if arac_tipi == "taksi" and isinstance(yontem, KentkartOdeme):
                continue

            if yontem.bakiye >= tutar:
                return yontem.odeme_yap(tutar)

        return f"❌ Ödeme başarısız! {tutar:.2f} TL için yeterli bakiye bulunamadı."

    def odeme_yontemi_sec_ve_odeme_yap(self, tutar):
        while True:
            print("\n💳 Kullanılabilir ödeme yöntemleri:")
            for i, yontem in enumerate(self.odeme_yontemleri, start=1):
                sinif_adi = yontem.__class__.__name__
                ikon = {
                    "NakitOdeme": "💵",
                    "KrediKartiOdeme": "💳",
                    "KentkartOdeme": "🚌",
                    "MobilOdeme": "📱"
                }.get(sinif_adi, "💰")
                print(f"{i}. {ikon} {sinif_adi} (Bakiye: {yontem.bakiye:.2f} TL)")

            secim = int(input("Lütfen ödeme yönteminizi seçiniz (1-{}): ".format(len(self.odeme_yontemleri))))
            if 1 <= secim <= len(self.odeme_yontemleri):
                secilen_yontem = self.odeme_yontemleri[secim - 1]
                sonuc = secilen_yontem.odeme_yap(tutar)
                if "yetersiz" in sonuc:
                    print(f"⚠️ {sonuc}")
                    print("Başka bir yöntem seçin.")
                else:
                    return sonuc
            else:
                print("🚫 Geçersiz seçim! Lütfen tekrar deneyin.")

    def __str__(self):
        """
        Cüzdandaki tüm ödeme yöntemlerini ve bakiyelerini yazdırır.
        """
        bilgiler = "💼 Cüzdan Bakiyeleri:\n"
        for yontem in self.odeme_yontemleri:
            sinif_adi = yontem.__class__.__name__
            ikon = {
                "NakitOdeme": "💵",
                "KrediKartiOdeme": "💳",
                "KentkartOdeme": "🚌",
                "MobilOdeme": "📱"
            }.get(sinif_adi, "💰")
            bilgiler += f"{ikon} {sinif_adi}: {yontem.bakiye:.2f} TL\n"
        return bilgiler


class OdemeYontemi(ABC):
    """
    Ödeme yöntemleri için soyut sınıf.
    Her ödeme yöntemi kendine özgü `odeme_yap` metodunu uygulayacaktır.
    """

    def __init__(self, bakiye=0):
        self.bakiye = bakiye  # her yöntemin kendine ait bakiyesi olur

    @abstractmethod
    def odeme_yap(self, tutar):
        """Ödeme işlemini gerçekleştirir."""
        pass


class NakitOdeme(OdemeYontemi):
    def __init__(self, bakiye=0):
        super().__init__(bakiye)

    def odeme_yap(self, tutar):
        if self.bakiye >= tutar:
            self.bakiye -= tutar
            return f"💵 {tutar:.2f} TL nakit olarak ödendi. Kalan bakiye: {self.bakiye:.2f} TL"
        else:
            return f"🚫 Yetersiz nakit bakiye! Gerekli: {tutar:.2f} TL, Mevcut: {self.bakiye:.2f} TL"


class KrediKartiOdeme(OdemeYontemi):
    def __init__(self, bakiye=0):
        super().__init__(bakiye)

    def odeme_yap(self, tutar):
        if self.bakiye >= tutar:
            self.bakiye -= tutar
            return f"💳 {tutar:.2f} TL kredi kartı ile ödendi. Kalan limit: {self.bakiye:.2f} TL"
        else:
            return f"🚫 Kredi kartı limit yetersiz! Gerekli: {tutar:.2f} TL, Kalan: {self.bakiye:.2f} TL"


class KentkartOdeme(OdemeYontemi):
    def __init__(self, bakiye=0):
        super().__init__(bakiye)

    def odeme_yap(self, tutar):
        if self.bakiye >= tutar:
            self.bakiye -= tutar
            return f"🚌 {tutar:.2f} TL Kentkart ile ödendi. Kalan bakiye: {self.bakiye:.2f} TL"
        else:
            return f"🚫 KentKart bakiyesi yetersiz! Gerekli: {tutar:.2f} TL, Mevcut: {self.bakiye:.2f} TL"


class MobilOdeme(OdemeYontemi):
    def __init__(self, bakiye=0):
        super().__init__(bakiye)

    def odeme_yap(self, tutar):
        if self.bakiye >= tutar:
            self.bakiye -= tutar
            return f"📱 {tutar:.2f} TL mobil ödeme ile ödendi. Kalan bakiye: {self.bakiye:.2f} TL"
        else:
            return f"🚫 Mobil ödeme bakiyesi yetersiz! Gerekli: {tutar:.2f} TL, Mevcut: {self.bakiye:.2f} TL"
