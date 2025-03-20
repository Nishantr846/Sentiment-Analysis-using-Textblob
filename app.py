import streamlit as st
import tweepy
from textblob import TextBlob
import time

# Twitter API Credentials (Replace with actual credentials)
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAJYt0AEAAAAAhb4tSRgUfmAYzIw%2BdIdzqUc7wCE%3DNuxeGwCLPfrHzhfBKbxE0U7AbeJFtUli50cX9haXylh4IF8bvL"

# Initialize Tweepy Client (Twitter API v2)
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Cache dictionary to store recent query results
cache = {}

def fetch_tweets(query, num_tweets):
    """Fetches recent tweets based on a query, with caching to minimize API calls."""
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
    """Analyzes sentiment of a given text using TextBlob."""
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0:
        return "Positive", "😊"
    elif polarity < 0:
        return "Negative", "😠"
    else:
        return "Neutral", "😐"

# Streamlit UI
st.markdown("""
    <h2 style="text-align: center;">🐦 X (formerly Twitter) Sentiment Analysis</h2>
""", unsafe_allow_html=True)

# Layout Columns
col1, spacer, col2 = st.columns([20, 10, 20])  # Increased spacing between columns

# **LEFT COLUMN: Search Tweets by Keyword**
with col1:
    st.subheader("🔍 Analyze Tweets by Keyword/Hashtag")
    query = st.text_input("Enter a keyword or hashtag (e.g., #AI, Tesla, Python):")
    num_tweets = st.slider("Select number of tweets:", min_value=10, max_value=100, step=2, value=20)

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
                sentiment_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
                categorized_tweets = {"Positive": [], "Neutral": [], "Negative": []}

                for tweet in tweets:
                    sentiment, _ = analyze_sentiment(tweet)
                    sentiment_counts[sentiment] += 1
                    categorized_tweets[sentiment].append(tweet)

                st.write("### Sentiment Analysis Summary")
                st.success(f"**Positive Tweets:** {sentiment_counts['Positive']}")
                st.warning(f"**Neutral Tweets:** {sentiment_counts['Neutral']}")
                st.error(f"**Negative Tweets:** {sentiment_counts['Negative']}")

                with st.expander("📢 **View Tweets by Sentiment**"):
                    for category, tweets in categorized_tweets.items():
                        if tweets:
                            st.subheader(f"{category} Tweets:")
                            for tweet in tweets:
                                st.write(f"- {tweet}")

# **Add Vertical Space Between Sections**
st.markdown("<br><br>", unsafe_allow_html=True)

# **RIGHT COLUMN: Analyze Single Tweet**
with col2:
    st.subheader("📝 Analyze a single Tweet Text")
    tweet_text = st.text_area("Paste the tweet text here:")

    if st.button("Analyze Sentiment", key="text_button"):
        if not tweet_text.strip():
            st.warning("Please enter a valid tweet text.")
        else:
            sentiment, emoji = analyze_sentiment(tweet_text)
            st.write("### Tweet Content:")
            st.info(tweet_text)
            st.write(f"### Sentiment Analysis: **{sentiment} {emoji}**")

# **Styling**
st.markdown("""
    <style>
        .stButton>button { width: 100%; }
        .stTextInput>div>div>input { font-size: 16px; }
        .stTextArea>div>textarea { font-size: 16px; }
    </style>
""", unsafe_allow_html=True)
