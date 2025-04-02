from math import radians, sin, cos, sqrt, atan2

def haversine_mesafe_km(enlem1, boylam1, enlem2, boylam2):
    R = 6371
    enlem1, boylam1, enlem2, boylam2 = map(radians, [enlem1, boylam1, enlem2, boylam2])
    d_enlem = enlem2 - enlem1
    d_boylam = boylam2 - boylam1

    a = sin(d_enlem / 2) ** 2 + cos(enlem1) * cos(enlem2) * sin(d_boylam / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

def yurume_suresi_hesapla(mesafe_km):
    return (mesafe_km / 5) * 60  # 5 km/h hızla yürüyüş

class EnYakinDurakHesaplayici:
    """
    Kullanıcının belirttiği enlem ve boylam bilgilerine göre en yakın durağı bulan sınıf.
    """

    @staticmethod
    def mesafe_hesapla(enlem1, boylam1, enlem2, boylam2):
        """
        Haversine formülü ile iki koordinat arasındaki mesafeyi kilometre cinsinden hesaplar.
        """
        R = 6371  # Dünya yarıçapı (km)

        enlem1, boylam1, enlem2, boylam2 = map(radians, [enlem1, boylam1, enlem2, boylam2])
        d_enlem = enlem2 - enlem1
        d_boylam = boylam2 - boylam1

        a = sin(d_enlem / 2) ** 2 + cos(enlem1) * cos(enlem2) * sin(d_boylam / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return R * c  # Mesafe (km)

    @staticmethod
    def en_yakin_durak(konum_enlem, konum_boylam, duraklar):
        """
        Kullanıcının belirttiği koordinata en yakın durağı bulan fonksiyon.
        """
        en_yakin = None
        min_mesafe = float('inf')

        for durak in duraklar:
            lat, lon = durak.get("lat"), durak.get("lon")

            if lat is None or lon is None:
                continue

            mesafe = EnYakinDurakHesaplayici.mesafe_hesapla(konum_enlem, konum_boylam, lat, lon)

            if mesafe < min_mesafe:
                min_mesafe = mesafe
                en_yakin = durak

        return en_yakin, min_mesafe