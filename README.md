Twitter Sentiment Analysis

Overview

This project is a web application built using Streamlit that performs sentiment analysis on live tweets fetched from Twitter. The sentiment of tweets is analyzed using TextBlob, categorizing them as Positive, Neutral, or Negative.

Features

Fetches live tweets based on user input (keyword or hashtag)

Analyzes sentiment of fetched tweets

Allows users to manually input a tweet for sentiment analysis

Displays sentiment summary and categorized tweets

Implements caching to minimize redundant API calls

Technologies Used

Python: Core programming language

Streamlit: Web framework for creating interactive UI

Tweepy: Python wrapper for Twitter API v2

TextBlob: Sentiment analysis library

Installation

Prerequisites

Ensure you have Python installed (version 3.7 or later). Install dependencies using:

Usage

1. Obtain Twitter API Credentials

Replace the BEARER_TOKEN variable in the script with your own Twitter API credentials.

2. Run the Application

Execute the following command in the terminal:

This will start the Streamlit application, which can be accessed in a browser.

3. Analyze Tweets

Enter a keyword/hashtag and select the number of tweets to fetch.

Click Analyze Sentiment to fetch and analyze the tweets.

View sentiment summary and categorized tweets.

Alternatively, paste a tweet text for sentiment analysis.

Error Handling

Displays an error message if the Twitter API rate limit is exceeded.

Handles exceptions and alerts the user if tweets cannot be retrieved.

License

This project is open-source and available under the MIT License.

Author

Nishant

