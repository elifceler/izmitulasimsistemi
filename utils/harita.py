import folium
import webbrowser
import os

def haritada_goster(rota_adimlari, ulasim_grafi, harita_dosyasi="rota_haritasi.html"):
    if not rota_adimlari:
        print("❗ Görselleştirilecek rota bulunamadı.")
        return

    # Harita başlat
    ilk_adim = rota_adimlari[0]
    if "koordinatlar" in ilk_adim:
        bas_coord = ilk_adim["koordinatlar"][0]
    elif "kaynak" in ilk_adim:
        kaynak_durak = ulasim_grafi.duraklar[ilk_adim["kaynak"]]
        bas_coord = (kaynak_durak.enlem, kaynak_durak.boylam)
    else:
        print("❗ Rota başlangıç bilgisi eksik.")
        return

    harita = folium.Map(location=bas_coord, zoom_start=13)

    # Ulaşım türlerine göre renkler
    renkler = {
        "otobus": "blue",
        "tram": "green",
        "tramvay": "green",
        "taksi": "orange"
    }

    for adim in rota_adimlari:
        # Taksi adımı özel işlenir
        if "koordinatlar" in adim:
            koordinatlar = adim["koordinatlar"]
            tip = adim.get("tip", "taksi")
            folium.PolyLine(
                locations=koordinatlar,
                color=renkler.get(tip, "gray"),
                weight=5,
                opacity=0.8
            ).add_to(harita)

            folium.Marker(
                location=koordinatlar[0],
                popup="Taksi Başlangıç",
                icon=folium.Icon(color="orange", icon="taxi", prefix='fa')
            ).add_to(harita)

            folium.Marker(
                location=koordinatlar[1],
                popup="Taksi Bitiş",
                icon=folium.Icon(color="orange", icon="flag", prefix='fa')
            ).add_to(harita)
            continue

        # Eğer kaynak-hedef adımı ise
        if "kaynak" in adim and "hedef" in adim:
            kaynak = ulasim_grafi.duraklar[adim["kaynak"]]
            hedef = ulasim_grafi.duraklar[adim["hedef"]]
            tip = kaynak.arac_tipi.lower() if kaynak.arac_tipi else "bilinmiyor"

            folium.PolyLine(
                locations=[(kaynak.enlem, kaynak.boylam), (hedef.enlem, hedef.boylam)],
                color=renkler.get(tip, "gray"),
                weight=5,
                opacity=0.8
            ).add_to(harita)

            folium.Marker(
                location=(kaynak.enlem, kaynak.boylam),
                popup=f"{kaynak.ad} ({tip})",
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(harita)

            folium.Marker(
                location=(hedef.enlem, hedef.boylam),
                popup=f"{hedef.ad} ({tip})",
                icon=folium.Icon(color="green" if hedef.durak_id == adim["hedef"] else "red")
            ).add_to(harita)

    harita.save(harita_dosyasi)
    print(f"🗺️ Harita kaydedildi: {harita_dosyasi}")
    webbrowser.open("file://" + os.path.abspath(harita_dosyasi))
