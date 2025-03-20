import streamlit as st
import tweepy
import time
import plotly.express as px
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Twitter API Credentials (Replace with actual credentials)
BEARER_TOKEN = "YOUR_TWITTER_BEARER_TOKEN"

# Initialize Tweepy Client (Twitter API v2)
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Cache dictionary to store recent query results
cache = {}

# Initialize Sentiment Analyzer (VADER)
analyzer = SentimentIntensityAnalyzer()

def fetch_tweets(query, num_tweets):
    """Fetches recent tweets based on query, with caching to minimize API calls."""
    current_time = time.time()
    if query in cache and (current_time - cache[query]["timestamp"] < 900):
        return cache[query]["data"]

    try:
        response = client.search_recent_tweets(query=query, max_results=num_tweets, tweet_fields=["text"])
        tweets = [tweet.text for tweet in response.data] if response and response.data else []
        cache[query] = {"data": tweets, "timestamp": current_time}
        return tweets
    except tweepy.errors.TooManyRequests:
        st.error("Rate limit exceeded. Please try again later.")
        return []
    except Exception as e:
        return [f"Error: {str(e)}"]

def analyze_sentiment(text):
    """Analyzes sentiment of a given text using VADER."""
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']

    if compound >= 0.05:
        return "Positive", "😊"
    elif compound <= -0.05:
        return "Negative", "😠"
    else:
        return "Neutral", "😐"

# Streamlit UI
st.set_page_config(page_title="Twitter Sentiment Analysis", layout="wide")

st.title("🐦 Twitter Sentiment Analysis")
st.write("Analyze sentiment of tweets based on a keyword, hashtag, or copy-pasted tweet text.")

# **LEFT COLUMN: Keyword/Hashtag Search**
col1, col2 = st.columns([1, 1])  # Balanced column layout

# **LEFT COLUMN: Search Tweets by Keyword**
with col1:
    st.subheader("🔍 Analyze Tweets by Keyword/Hashtag")
    query = st.text_input("Enter a keyword or hashtag (e.g., #AI, Tesla, Python):")
    num_tweets = st.slider("Select number of tweets:", min_value=10, max_value=100, step=10, value=20)

    if st.button("Analyze Sentiment", key="keyword_button"):
        if not query:
            st.warning("Please enter a valid keyword or hashtag.")
        else:
            st.write(f"Fetching {num_tweets} tweets for: **{query}**")
            tweets = fetch_tweets(query, num_tweets)

            if not tweets:
                st.warning("No tweets found for this query.")
            elif "Error" in tweets[0]:
                st.error(tweets[0])  # Display error messages
            else:
                sentiment_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
                categorized_tweets = {"Positive": [], "Neutral": [], "Negative": []}

                for tweet in tweets:
                    sentiment, _ = analyze_sentiment(tweet)
                    sentiment_counts[sentiment] += 1
                    categorized_tweets[sentiment].append(tweet)

                # **Pie Chart Visualization**
                st.write("### Sentiment Analysis Summary")
                fig = px.pie(
                    names=list(sentiment_counts.keys()),
                    values=list(sentiment_counts.values()),
                    title="Sentiment Distribution",
                    color=list(sentiment_counts.keys()),
                    color_discrete_map={"Positive": "green", "Neutral": "gray", "Negative": "red"},
                )
                st.plotly_chart(fig, use_container_width=True)

                # **Show Sentiment Counts**
                st.success(f"**Positive Tweets:** {sentiment_counts['Positive']}")
                st.warning(f"**Neutral Tweets:** {sentiment_counts['Neutral']}")
                st.error(f"**Negative Tweets:** {sentiment_counts['Negative']}")

                # **Display Tweets Categorized by Sentiment**
                with st.expander("📢 **View Tweets by Sentiment**"):
                    for category, tweets in categorized_tweets.items():
                        if tweets:
                            st.subheader(f"{category} Tweets:")
                            for tweet in tweets:
                                st.write(f"- {tweet}")

# **RIGHT COLUMN: Analyze Single Tweet**
with col2:
    st.subheader("📝 Analyze a Copied Tweet Text")
    tweet_text = st.text_area("Paste the tweet text here:")

    if st.button("Analyze Sentiment", key="text_button"):
        if not tweet_text.strip():
            st.warning("Please enter a valid tweet text.")
        else:
            sentiment, emoji = analyze_sentiment(tweet_text)
            st.write("### Tweet Content:")
            st.info(tweet_text)
            st.write(f"### Sentiment Analysis: **{sentiment} {emoji}**")
            if sentiment == "Positive":
                st.success("This tweet expresses a **positive sentiment**. 😊")
            elif sentiment == "Negative":
                st.error("This tweet expresses a **negative sentiment**. 😠")
            else:
                st.warning("This tweet expresses a **neutral sentiment**. 😐")
