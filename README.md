# Twitter Sentiment Analysis

## Overview

A Machine Learning-based web application that analyzes sentiments of live tweets fetched from Twitter. The sentiment of tweets is categorized as Positive, Neutral, or Negative using TextBlob.

### Features

- Fetches live tweets based on user input (keyword or hashtag)

- Analyzes sentiment of fetched tweets in real-time

- Allows users to manually input a tweet for sentiment analysis

- Displays sentiment summary and categorized tweets

- Implements caching to minimize redundant API calls

## Installation

### Prerequisites

- Ensure you have Python installed (version 3.7 or later). Then, install dependencies using: requirements.txt

### How to Run

- Clone this repository to your local machine:

- Run the Streamlit app: streamlit run app.py (https://sentiment-analysis-minor-project-kiit.streamlit.app/)

- This will start a local server and open the application in your browser.

### How It Works

- The user enters a keyword or hashtag to fetch tweets.

- The system retrieves the latest tweets using the Twitter API.

- Sentiment analysis is performed using TextBlob.

- The application displays sentiment summaries and categorized tweets.

- Users can also paste a tweet manually for analysis.

## Error Handling

- Displays an error message if the Twitter API rate limit is exceeded.

- Handles exceptions and alerts the user if tweets cannot be retrieved.

## Technologies Used

- **Python** - Core programming language

- **Streamlit** - Web framework for creating an interactive UI

- **Tweepy** - Python wrapper for Twitter API v2

- **TextBlob** - Sentiment analysis library

# License

This project is open-source and available under the MIT License.

### Contact : 
- Nishant Kumar
- nishantr846@gmail.com
- https://www.linkedin.com/in/nishantr846/

