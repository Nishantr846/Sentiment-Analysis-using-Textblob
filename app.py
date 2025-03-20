 import streamlit as st
 import tweepy
 from textblob import TextBlob
 import time
 
 # Twitter API Credentials (Replace with actual credentials)
 BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAJYt0AEAAAAAhb4tSRgUfmAYzIw%2BdIdzqUc7wCE%3DNuxeGwCLPfrHzhfBKbxE0U7AbeJFtUli50cX9haXylh4IF8bvL"
 BEARER_TOKEN = "YOUR_BEARER_TOKEN_HERE"
 
 # Initialize Tweepy Client (Twitter API v2)
 # Initialize Tweepy Client
 client = tweepy.Client(bearer_token=BEARER_TOKEN)
 
 # Cache dictionary to store recent query results
 # Cache to store recent query results
 cache = {}
 
 def fetch_tweets(query, num_tweets):
     """Fetches recent tweets based on query, with caching to minimize API calls."""
     """Fetches recent tweets based on a query, with caching to minimize API calls."""
     current_time = time.time()
     if query in cache and (current_time - cache[query]["timestamp"] < 900):
         return cache[query]["data"]
 
     try:
         response = client.search_recent_tweets(query=query, max_results=num_tweets, tweet_fields=["text"])
         tweets = [tweet.text for tweet in response.data] if response and response.data else []
 @@ -40,67 +39,56 @@
         return "Neutral", "😐"
 
 # Streamlit UI
 st.set_page_config(page_title="Twitter Sentiment Analysis", layout="wide")
 st.title("🐦 Twitter Sentiment Analysis")
 st.write("Analyze sentiment of tweets based on a keyword, hashtag, or copy-pasted tweet text.")
 
 # **LEFT COLUMN: Keyword/Hashtag Search**
 st.markdown(
     """
     <style>
         .stColumns { gap: 50px; }
     </style>
     """,
     unsafe_allow_html=True
 )
 
 col1, spacer, col2 = st.columns([20, 5, 20])  # Adjusted spacing
 # Define Columns for Layout
 col1, col2 = st.columns([1, 1])
 
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
                 st.error(tweets[0])  # Display error messages
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
     st.subheader("📝 Analyze a Copied Tweet Text")
     tweet_text = st.text_area("Paste the tweet text here:")
 
     
     if st.button("Analyze Sentiment", key="text_button"):
         if not tweet_text.strip():
             st.warning("Please enter a valid tweet text.")
 @@ -109,3 +97,12 @@
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
