import tweepy
from textblob import TextBlob
import requests
from bs4 import BeautifulSoup
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# Fungsi untuk mendapatkan tweet dengan hashtag tertentu
def get_tweets(hashtag, count=100):
    auth = tweepy.OAuthHandler("0OpolP0BqVrGtQLryIkwURD6R", "RlMuTPzhCpdmYIuL4A74wKb0FXZsRbi494MuNzCZm8ZvaNQ5UF")
    auth.set_access_token("304900160-4f7XrVazNJ2RUlJWk1p9ZsJ5Y9xBpLYuhDOgAknq", "aRmc58zc7g1QY1WzInWYnac5F4sAyzyogaARI99c7STxn")
    api = tweepy.API(auth)

    tweets = tweepy.Cursor(api.search_tweets, q=hashtag, lang="id").items(count)
    return [(tweet.user.screen_name, tweet.text, tweet.created_at) for tweet in tweets]

# Fungsi untuk melakukan analisis sentimen menggunakan TextBlob
def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    # Mengonversi skor sentimen menjadi kategori
    if polarity > 0:
        return f"Positif ({polarity:.2f})"
    elif polarity == 0:
        return f"Netral ({polarity:.2f})"
    else:
        return f"Negatif ({polarity:.2f})"

# Fungsi untuk membuat donut chart
def create_donut_chart(positive, neutral, negative):
    fig, ax = plt.subplots()
    width = 0.35

    # Outer circle
    outer_circle = Circle((0, 0), 0.6, color='white')
    ax.add_patch(outer_circle)

    # Inner circles
    colors = ['#66ff66', '#99ccff', '#ff6666']
    labels = ['Positif', 'Netral', 'Negatif']
    data = [positive, neutral, negative]

    for i, (col, lab) in enumerate(zip(colors, labels)):
        inner_circle = Circle((0, 0), 0.4, color='white')
        ax.add_patch(inner_circle)

        ax.text(0, 0, f"{data[i]:.1%}\n{lab}", ha='center', va='center', fontsize=12, color='black')

    ax.set_aspect('equal', adjustable='box')
    ax.axis('off')

    return fig

# Fungsi untuk main page 1 (analisis sentimen hashtag)
def main_page_1():
    st.title("Sentiment Analysis App")

    hashtag = st.text_input("Masukkan hashtag (contoh: #Pilpres2024):")
    if st.button("Analyze"):
        if hashtag:
            tweets = get_tweets(hashtag, count=100)
            sentiment_results = [analyze_sentiment(tweet[1]) for tweet in tweets]

            st.write("### Donut Chart Analisis Sentimen:")
            positive_tweets = sum("Positif" in result for result in sentiment_results)
            neutral_tweets = sum("Netral" in result for result in sentiment_results)
            negative_tweets = sum("Negatif" in result for result in sentiment_results)

            fig = create_donut_chart(positive_tweets, neutral_tweets, negative_tweets)
            st.pyplot(fig)

            st.write("### Hasil Analisis Sentimen:")
            st.write(f"Hashtag: {hashtag}")
            st.write(f"Jumlah Tweet yang Dianalisis: {len(tweets)}")

            st.write(f"Positif: {positive_tweets} tweets")
            st.write(f"Netral: {neutral_tweets} tweets")
            st.write(f"Negatif: {negative_tweets} tweets")

            st.write("### Rincian Sentimen:")
            st.table({"Tanggal": [tweet[2] for tweet in tweets],
                      "Nama Pengguna (ID)": [tweet[0] for tweet in tweets],
                      "Komentar": [tweet[1] for tweet in tweets],
                      "Hasil Sentimen": sentiment_results})
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
            sentiment_results = [analyze_sentiment(review) for review in reviews]

            st.write("### Donut Chart Analisis Sentimen:")
            positive_reviews = sum("Positif" in result for result in sentiment_results)
            neutral_reviews = sum("Netral" in result for result in sentiment_results)
            negative_reviews = sum("Negatif" in result for result in sentiment_results)

            fig = create_donut_chart(positive_reviews, neutral_reviews, negative_reviews)
            st.pyplot(fig)

            st.write("### Hasil Analisis Sentimen:")
            st.write(f"Marketplace: {marketplace}")
            st.write(f"Jumlah Ulasan yang Dianalisis: {len(reviews)}")

            st.write(f"Positif: {positive_reviews} ulasan")
            st.write(f"Netral: {neutral_reviews} ulasan")
            st.write(f"Negatif: {negative_reviews} ulasan")

            st.write("### Rincian Sentimen:")
            st.table({"Tanggal": [review[2] for review in reviews],
                      "Komentar": reviews,
                      "Hasil Sentimen": sentiment_results})
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
