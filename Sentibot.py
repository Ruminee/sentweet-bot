import tweepy
from textblob import TextBlob
import requests
from bs4 import BeautifulSoup
import streamlit as st


def get_tweets(hashtag, count=100):
    auth = tweepy.OAuthHandler("0OpolP0BqVrGtQLryIkwURD6R", "RlMuTPzhCpdmYIuL4A74wKb0FXZsRbi494MuNzCZm8ZvaNQ5UF")
    auth.set_access_token("304900160-4f7XrVazNJ2RUlJWk1p9ZsJ5Y9xBpLYuhDOgAknq", "aRmc58zc7g1QY1WzInWYnac5F4sAyzyogaARI99c7STxn")
    api = tweepy.API(auth)

    tweets = tweepy.Cursor(api.search, q=hashtag, lang="en").items(count)
    return [(tweet.user.screen_name, tweet.text) for tweet in tweets]

# Fungsi untuk melakukan analisis sentimen menggunakan TextBlob
def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

# Fungsi untuk main page 1 (analisis sentimen hashtag)
def main_page_1():
    st.title("Sentiment Analysis App")

    hashtag = st.text_input("Masukkan hashtag (contoh: #Pilpres2024):")
    if st.button("Analyze"):
        if hashtag:
            tweets = get_tweets(hashtag, count=100)
            sentiment_scores = [analyze_sentiment(tweet[1]) for tweet in tweets]

            st.write("### Hasil Analisis Sentimen:")
            st.write(f"Hashtag: {hashtag}")
            st.write(f"Jumlah Tweet yang Dianalisis: {len(tweets)}")

            positive_tweets = sum(score > 0 for score in sentiment_scores)
            neutral_tweets = sum(score == 0 for score in sentiment_scores)
            negative_tweets = sum(score < 0 for score in sentiment_scores)

            st.write(f"Positif: {positive_tweets} tweets")
            st.write(f"Netral: {neutral_tweets} tweets")
            st.write(f"Negatif: {negative_tweets} tweets")

            st.write("### Rincian Sentimen:")
            st.table({"Nama Pengguna (ID)": [tweet[0] for tweet in tweets],
                      "Komentar": [tweet[1] for tweet in tweets],
                      "Hasil Sentimen": sentiment_scores})
        else:
            st.warning("Masukkan hashtag terlebih dahulu.")

# Fungsi untuk main page 2 (survey analisis sentimen produk)
def main_page_2():
    st.title("Product Sentiment Survey")

    marketplace = st.selectbox("Pilih Marketplace:", ["Tokopedia", "Shopee", "Bukalapak"])
    product_url = st.text_input("Masukkan URL Produk:")

    if st.button("Analyze"):
        if product_url:
            reviews = scrape_reviews(product_url, max_reviews=50)
            sentiment_scores = [analyze_sentiment(review) for review in reviews]

            st.write("### Hasil Analisis Sentimen:")
            st.write(f"Marketplace: {marketplace}")
            st.write(f"Jumlah Ulasan yang Dianalisis: {len(reviews)}")

            positive_reviews = sum(score > 0 for score in sentiment_scores)
            neutral_reviews = sum(score == 0 for score in sentiment_scores)
            negative_reviews = sum(score < 0 for score in sentiment_scores)

            st.write(f"Positif: {positive_reviews} ulasan")
            st.write(f"Netral: {neutral_reviews} ulasan")
            st.write(f"Negatif: {negative_reviews} ulasan")

            st.write("### Rincian Sentimen:")
            st.table({"Komentar": reviews, "Hasil Sentimen": sentiment_scores})
        else:
            st.warning("Masukkan URL produk terlebih dahulu.")

# Aplikasi Streamlit dengan multiple pages
def main():
    st.sidebar.title("Navigation")
    pages = {
        "Analisis Hashtag": main_page_1,
        "Survey Produk": main_page_2,
    }

    selection = st.sidebar.radio("Pilih Halaman", list(pages.keys()))
    pages[selection]()

if __name__ == "__main__":
    main()
