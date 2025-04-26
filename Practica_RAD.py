import streamlit as st
import requests

# API keys (meglio mettere nei secrets in produzione)
WEATHER_API_KEY = '64cd71cfda1d4f27bd3150724250904'
NEWS_API_KEY = '58c4cd2e6f01dbcf396267600723d514'
PEXELS_API_KEY = 'KVvWFXLJMdHs5vuq72VmhLA9KrB8nqtb6vZh2IE2CsAYTuTJWDrCdb1O'

CITIES = ['Amsterdam', 'Bari', 'Chicago', 'Rome', 'Matera']

st.set_page_config(page_title="Previsioni Meteo e Notizie", layout="centered")

st.title("☁️ Previsioni Meteo e 📰 Notizie")
st.subheader("Scegli una città per visualizzare il meteo, le notizie e un'immagine rappresentativa")

selected_city = st.selectbox("Seleziona una città", CITIES)

def fetch_data(city):
    try:
        weather_url = f"https://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={city}&days=8&lang=it"
        news_url = f"https://gnews.io/api/v4/search?q={city}&lang=it&max=4&apikey={NEWS_API_KEY}"
        image_url = f"https://api.pexels.com/v1/search?query={city}&per_page=1"

        weather_res = requests.get(weather_url)
        news_res = requests.get(news_url)
        image_res = requests.get(image_url, headers={"Authorization": PEXELS_API_KEY})

        weather_data = weather_res.json()
        news_data = news_res.json()
        image_data = image_res.json()

        return weather_data, news_data, image_data

    except Exception as e:
        st.error(f"Errore durante il recupero dei dati: {e}")
        return None, None, None

if st.button("🔍 Mostra dati"):
    with st.spinner("Caricamento in corso..."):
        weather, news, image = fetch_data(selected_city)

        if not weather or 'error' in weather:
            st.error("⚠️ Impossibile ottenere i dati meteo.")
        else:
            # Immagine
            if image.get("photos"):
                img_url = image["photos"][0]["src"]["landscape"]
                st.image(img_url, caption=f"Immagine di {selected_city}", use_column_width=True)

            # Meteo attuale
            current = weather["current"]
            location = weather["location"]
            st.markdown(f"### ☁️ Meteo attuale a {location['name']}")
            st.write(f"**Temperatura:** {current['temp_c']}°C")
            st.write(f"**Condizione:** {current['condition']['text']}")
            st.write(f"**Umidità:** {current['humidity']}%")
            st.write(f"**Vento:** {current['wind_kph']} km/h")

            # Previsioni prossimi giorni
            st.markdown("### 📆 Previsioni prossimi giorni")
            for day in weather["forecast"]["forecastday"][1:]:
                st.write(f"**{day['date']}** - {day['day']['condition']['text']} ({day['day']['avgtemp_c']}°C)")
                st.image("https:" + day["day"]["condition"]["icon"], width=40)

            # Notizie
            if news.get("articles"):
                st.markdown("### 📰 Notizie recenti")
                for article in news["articles"]:
                    st.markdown(f"- [{article['title']}]({article['url']})")
            else:
                st.warning("Nessuna notizia trovata per questa città.")