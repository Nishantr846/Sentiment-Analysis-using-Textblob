import streamlit as st
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Function to preprocess text
def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)  # Remove URLs
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = re.sub(r'@\w+', '', text)  # Remove mentions
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove special characters
    return text.strip()

# Function to analyze sentiment
def analyze_sentiment(text, positive_keywords, negative_keywords):
    text = preprocess_text(text)  # Clean the text
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)  # Get sentiment scores

    # Check for keyword-based sentiment adjustment
    for word in positive_keywords:
        if word.lower() in text:
            scores['compound'] += 0.3  # Increase positivity bias

    for word in negative_keywords:
        if word.lower() in text:
            scores['compound'] -= 0.3  # Increase negativity bias

    # Debugging: Display raw sentiment scores
    st.write(f"🔍 **Sentiment Scores:** {scores}")

    if scores['compound'] >= 0.2:  
        return "Positive", "😊", "success"
    elif scores['compound'] <= -0.2:  
        return "Negative", "😠", "error"
    else:
        return "Neutral", "😐", "warning"

# Streamlit UI
st.title("📑 Analyze a Copied Tweet Text")
st.write("Paste the tweet text here:")

# User input text area
tweet_text = st.text_area("", height=150)

# Keyword input for sentiment correction
st.write("🔹 **Enter keywords to refine sentiment analysis**")
positive_keywords = st.text_input("Positive Keywords (comma-separated)", "").split(',')
negative_keywords = st.text_input("Negative Keywords (comma-separated)", "").split(',')

# Analyze button
if st.button("Analyze Sentiment", help="Click to analyze sentiment"):
    if tweet_text.strip():
        sentiment, emoji, status = analyze_sentiment(tweet_text, positive_keywords, negative_keywords)

        # Display tweet content
        st.subheader("Tweet Content:")
        st.info(tweet_text)

        # Display sentiment result
        st.subheader(f"Sentiment Analysis: {sentiment} {emoji}")
        getattr(st, status)(f"This tweet expresses a **{sentiment.lower()} sentiment**. {emoji}")
    else:
        st.warning("⚠️ Please enter some text to analyze!")
