class Durak:
    """Bir durağı temsil eden sınıf."""

    def __init__(self, durak_id, ad, enlem, boylam, arac_tipi=None):
        self.durak_id = durak_id  # Durak kimliği
        self.ad = ad  # Durak adı
        self.enlem = enlem  # Enlem
        self.boylam = boylam  # Boylam
        self.komsular = []  # Bağlantılı duraklar (komşular)
        self.arac_tipi = arac_tipi  # Durak tipini belirler (bus, tramvay vb.)

    def ekle_komsu(self, komsu_durak, mesafe, sure, ucret, transfer_mi=False):
        """Durağa yeni bir komşu ekler. Transfer bağlantıları işaretlenebilir."""
        self.komsular.append((komsu_durak, mesafe, sure, ucret, transfer_mi))

    def __repr__(self):
        return f"{self.ad} ({self.durak_id})"


class UlasimGrafigi:
    """Toplu taşıma sistemini temsil eden graf."""

    def __init__(self):
        self.duraklar = {}  # Durakları saklayan sözlük (durak_id -> Durak nesnesi)

    def durak_ekle(self, durak):
        """Graf'a yeni bir durak ekler."""
        self.duraklar[durak.durak_id] = durak

    def baglanti_ekle(self, durak_id1, durak_id2, mesafe, sure, ucret, transfer_mi=False):
        """İki durak arasında yönlü bağlantı oluşturur."""
        if durak_id1 in self.duraklar and durak_id2 in self.duraklar:
            self.duraklar[durak_id1].ekle_komsu(
                self.duraklar[durak_id2],
                mesafe,
                sure,
                ucret,
                transfer_mi
            )

    def __repr__(self):
        return "\n".join([f"{durak}: {durak.komsular}" for durak in self.duraklar.values()])



