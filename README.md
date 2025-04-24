# 🗺️ Ulaşım Rota Planlama Sistemi (Kocaeli / İzmit)

Bu proje, Kocaeli Üniversitesi Bilgisayar Mühendisliği bölümü kapsamında **Programlama Laboratuvarı II** dersi için geliştirilmiş bir ulaşım rota planlama sistemidir. Kullanıcıdan alınan başlangıç ve hedef konumlara göre; **toplu taşıma (otobüs, tramvay)** ve **taksi** alternatiflerini değerlendirerek en uygun rotayı bulur.

## 🚀 Proje Amacı

Kocaeli ili İzmit ilçesi özelinde bir ulaşım sistemi geliştirerek;
- Enlem-boylam bilgileri ile **en uygun rotayı** bulmak
- **Süre, mesafe, maliyet, aktarma sayısı** gibi faktörlere göre farklı rota alternatifleri sunmak
- Farklı **yolcu tipleri** için (öğrenci, öğretmen, yaşlı vb.) **indirimli fiyatlandırma** uygulamak
- Hem metinsel hem görsel (harita tabanlı) çıktı sunmak

---

## 🧠 Kullanılan Teknolojiler

- **Python** (Ana programlama dili)
- **Tkinter** (Grafiksel kullanıcı arayüzü)
- **Folium** (HTML tabanlı harita görselleştirmesi)
- **JSON** (Durak ve ulaşım verisi)
- **OOP (Nesne Yönelimli Programlama)**
- **Dijkstra Algoritması** (En kısa yol hesaplama)

---

## 🛠️ Proje Özellikleri

- 🚍 Otobüs ve 🚋 Tramvay durakları arasında yönlü bağlantılar
- 🚖 Taksi ile hibrit ulaşım (3 km'den uzaksa taksi kullanımı)
- 👤 Yolcu tipine özel ücretlendirme
- 💳 Çoklu ödeme yöntemi (Nakit, Kredi Kartı, Kentkart, Mobil)
- 🧭 Alternatif rota senaryoları:
  - Sadece Otobüs
  - Sadece Tramvay
  - Otobüs + Tramvay aktarmalı
  - Taksi + Toplu taşıma

---

## 🧩 OOP Tasarımı

- `Durak`, `Konum`, `Yolcu`, `Araç`, `Cüzdan`, `RotaHesaplayici` gibi sınıflar
- `Yolcu`: Genel, Öğrenci, Yaşlı vb. (indirimli fiyatlandırma)
- `Araç`: Otobüs, Tramvay, Taksi (ücret yapıları farklı)
- `Factory` desenleriyle yeni yolcu/araç tipi kolayca eklenebilir
- SOLID prensiplerine uygun modüler yapı

---

## 📍 Örnek Kullanım Senaryosu

```text
Başlangıç Konumu: (40.765, 29.930)
Hedef Konum: (40.740, 29.980)
Yolcu Tipi: Öğrenci
Ödeme: Kentkart

💡 Rota:
1. Yürü → Otobüs Durağı (bus_otogar)
2. Otobüs → bus_sekapark
3. Transfer → tram_sekapark
4. Tramvay → tram_halkevi

🧾 Ücret: 4.0 TL   ⏱️ Süre: 20 dk   📏 Mesafe: 7.3 km
