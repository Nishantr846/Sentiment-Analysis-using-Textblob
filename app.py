import streamlit as st
import tweepy
import time
import plotly.express as px
import re
from transformers import pipeline

# Twitter API Credentials (Replace with actual credentials)
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAJYt0AEAAAAAhb4tSRgUfmAYzIw%2BdIdzqUc7wCE%3DNuxeGwCLPfrHzhfBKbxE0U7AbeJFtUli50cX9haXylh4IF8bvL"

# Initialize Tweepy Client (Twitter API v2)
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Initialize Sentiment Analysis Model
sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Cache dictionary to store recent query results
cache = {}

def clean_text(text):
    """Cleans tweet text by removing URLs, mentions, and special characters."""
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'@[A-Za-z0-9_]+', '', text)  # Remove mentions
    text = re.sub(r'#[A-Za-z0-9_]+', '', text)  # Remove hashtags
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)  # Remove special characters
    return text.strip()

def fetch_tweets(query, num_tweets):
    """Fetches recent tweets based on query, with caching to minimize API calls."""
    current_time = time.time()
    if query in cache and (current_time - cache[query]["timestamp"] < 900):
        return cache[query]["data"]
    try:
        response = client.search_recent_tweets(query=query, max_results=num_tweets, tweet_fields=["text"])
        tweets = [clean_text(tweet.text) for tweet in response.data] if response and response.data else []
        cache[query] = {"data": tweets, "timestamp": current_time}
        return tweets
    except tweepy.errors.TooManyRequests:
        st.error("Rate limit exceeded. Please try again later.")
        return []
    except Exception as e:
        return [f"Error: {str(e)}"]

def analyze_sentiment(text):
    """Analyzes sentiment of a given text using the Transformer model."""
    result = sentiment_model(text)[0]
    return result['label'], result['score']

# Streamlit UI
st.set_page_config(page_title="Twitter Sentiment Analysis", layout="wide")

st.title("🐦 Twitter Sentiment Analysis")
st.write("Analyze sentiment of tweets based on a keyword, hashtag, or copy-pasted tweet text.")

col1, col2 = st.columns([1, 1])

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
                st.error(tweets[0])
            else:
                sentiment_counts = {"POSITIVE": 0, "NEGATIVE": 0}
                categorized_tweets = {"POSITIVE": [], "NEGATIVE": []}
                
                for tweet in tweets:
                    sentiment, confidence = analyze_sentiment(tweet)
                    sentiment_counts[sentiment] += 1
                    categorized_tweets[sentiment].append((tweet, confidence))
                
                st.write("### Sentiment Analysis Summary")
                fig = px.pie(
                    names=list(sentiment_counts.keys()),
                    values=list(sentiment_counts.values()),
                    title="Sentiment Distribution",
                    color=list(sentiment_counts.keys()),
                    color_discrete_map={"POSITIVE": "green", "NEGATIVE": "red"},
                )
                st.plotly_chart(fig, use_container_width=True)
                
                with st.expander("📢 **View Tweets by Sentiment**"):
                    for category, tweets in categorized_tweets.items():
                        if tweets:
                            st.subheader(f"{category} Tweets:")
                            for tweet, score in tweets:
                                st.write(f"- {tweet} (Confidence: {score:.2f})")

with col2:
    st.subheader("📝 Analyze a Copied Tweet Text")
    tweet_text = st.text_area("Paste the tweet text here:")
    
    if st.button("Analyze Sentiment", key="text_button"):
        if not tweet_text.strip():
            st.warning("Please enter a valid tweet text.")
        else:
            sentiment, confidence = analyze_sentiment(clean_text(tweet_text))
            st.write("### Tweet Content:")
            st.info(tweet_text)
            st.write(f"### Sentiment Analysis: **{sentiment}** (Confidence: {confidence:.2f})")
            if sentiment == "POSITIVE":
                st.success("This tweet expresses a **positive sentiment**. 😊")
            else:
                st.error("This tweet expresses a **negative sentiment**. 😠")
