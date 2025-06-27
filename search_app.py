import streamlit as st
import requests
from datetime import datetime, timedelta
import os

# App Config
st.set_page_config(page_title="24h News Search", layout="centered")
st.title("🗞️ 24-Hour News Search")
st.markdown("Search recent news articles by keyword using GNews API.")

# Keyword input
keyword = st.text_input("Enter a keyword", placeholder="e.g. Kpop, AI, elections")

if keyword:
    st.subheader(f"🔍 Recent News about '{keyword}'")

    # Date range setup
    today = datetime.utcnow()
    yesterday = today - timedelta(days=1)
    from_time = yesterday.strftime("%Y-%m-%dT%H:%M:%SZ")
    to_time = today.strftime("%Y-%m-%dT%H:%M:%SZ")

    # GNews API setup
    api_key = st.secrets["GNEWS_API_KEY"] if "GNEWS_API_KEY" in st.secrets else os.getenv("GNEWS_API_KEY")
    if not api_key:
        st.error("Missing GNews API key. Add it via Streamlit Secrets or a .env file.")
    else:
        url = f"https://gnews.io/api/v4/search"
        params = {
            "q": keyword,
            "from": from_time,
            "to": to_time,
            "lang": "en",
            "max": 10,
            "apikey": api_key,
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()
            articles = data.get("articles", [])

            if articles:
                for article in articles:
                    st.markdown(f"### [{article['title']}]({article['url']})")
                    st.write(article['description'])
                    st.caption(f"Source: {article['source']['name']} | Published: {article['publishedAt']}")
            else:
                st.info("No recent news found.")
        except Exception as e:
            st.error(f"Error retrieving news: {e}")
