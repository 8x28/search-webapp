import streamlit as st
import requests
import snscrape.modules.twitter as sntwitter
from datetime import datetime, timedelta
import os

# Streamlit App Config
st.set_page_config(page_title="24h Web + Social Search", layout="centered")

# App title
st.title("🔍 24-Hour Keyword Search")
st.markdown("Search for the most recent posts and news across Google and Twitter/X.")

# User input
keyword = st.text_input("Enter a keyword", placeholder="e.g. Taylor Swift, AI trends, BINI")

# Run if keyword is provided
if keyword:
    st.subheader(f"🌐 Google News (Past 24 Hours)")
    
    # SerpApi setup
    api_key = st.secrets["SERPAPI_API_KEY"] if "SERPAPI_API_KEY" in st.secrets else os.getenv("SERPAPI_API_KEY")
    if not api_key:
        st.error("Missing SerpApi API key. Set it in Streamlit secrets or environment variables.")
    else:
        params = {
            "engine": "google",
            "q": keyword,
            "api_key": api_key,
            "tbs": "qdr:d",  # past 24 hours
        }
        try:
            response = requests.get("https://serpapi.com/search", params=params)
            results = response.json().get("organic_results", [])
            if results:
                for result in results:
                    st.markdown(f"- [{result.get('title')}]({result.get('link')})")
            else:
                st.info("No recent web results found.")
        except Exception as e:
            st.error(f"Error fetching results: {e}")

    st.subheader(f"🐦 Twitter/X Posts (Past 24 Hours)")
    
    # Twitter search using snscrape
    try:
        since_date = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')
        query = f"{keyword} since:{since_date}"

        tweets = list(sntwitter.TwitterSearchScraper(query).get_items())
        if tweets:
            for tweet in tweets[:10]:
                tweet_url = f"https://twitter.com/{tweet.user.username}/status/{tweet.id}"
                st.markdown(f"- [{tweet.content[:100]}...]({tweet_url})")
        else:
            st.info("No recent tweets found.")
    except Exception as e:
        st.error(f"Error scraping tweets: {e}")
