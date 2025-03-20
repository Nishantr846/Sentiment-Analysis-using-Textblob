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
def analyze_sentiment(text):
    text = preprocess_text(text)  # Clean the text
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)  # Get sentiment scores

    # Display raw sentiment scores for debugging
    st.write(f"🔍 **Sentiment Scores:** {scores}")

    if scores['compound'] >= 0.2:  # Adjusted threshold
        return "Positive", "😊"
    elif scores['compound'] <= -0.2:  # Adjusted threshold
        return "Negative", "😠"
    else:
        return "Neutral", "😐"

# Streamlit UI
st.title("📑 Analyze a Copied Tweet Text")
st.write("Paste the tweet text here:")

# User input text area
tweet_text = st.text_area("", height=150)

# Analyze button
if st.button("Analyze Sentiment", help="Click to analyze sentiment"):
    if tweet_text.strip():
        sentiment, emoji = analyze_sentiment(tweet_text)

        # Display tweet content
        st.subheader("Tweet Content:")
        st.info(tweet_text)

        # Display sentiment result
        st.subheader(f"Sentiment Analysis: {sentiment} {emoji}")
        if sentiment == "Positive":
            st.success("This tweet expresses a **positive sentiment**. 😊")
        elif sentiment == "Negative":
            st.error("This tweet expresses a **negative sentiment**. 😠")
        else:
            st.warning("This tweet expresses a **neutral sentiment**. 😐")
    else:
        st.warning("⚠️ Please enter some text to analyze!")
