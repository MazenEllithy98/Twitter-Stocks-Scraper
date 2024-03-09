import tweepy
import time
import configparser
import datetime

# Read the Twitter API credentials from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

consumer_key = config['TWITTER']['consumer_key']
consumer_secret = config['TWITTER']['consumer_secret']
access_token = config['TWITTER']['access_token']
access_token_secret = config['TWITTER']['access_token_secret']

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Constant list of Twitter accounts
accounts = [
    'Mr_Derivatives',
    'warrior_0719',
    'ChartingProdigy',
    'allstarcharts',
    'yuriymatso',
    'TriggerTrades',
    'AdamMancini4',
    'CordovaTrades',
    'Barchart',
    'RoyLMattox'
]

def scrape_twitter_accounts(ticker, time_interval):
    while True:
        # Initialize an empty list to store the tweets
        stocks = []

        # Scrape the tweets from the specified Twitter accounts
        for account in accounts:
            tweets = tweepy.Cursor(api.user_timeline, screen_name=account, tweet_mode='extended').items()
            for tweet in tweets:
                # Check if the tweet contains the specified stock symbol
                if f'${ticker}' in tweet.full_text:
                    # Check if the tweet was created within the specified time interval
                    if (datetime.datetime.now(datetime.timezone.utc) - tweet.created_at).total_seconds() < time_interval * 60:
                        stocks.append(tweet.full_text)

        # Count the number of times the specified stock symbol is mentioned
        stock_count = len(stocks)

        # Print the output
        print(f"{ticker} was mentioned {stock_count} times in the last {time_interval} minutes.")

        # Wait for the next scraping session
        time.sleep(time_interval * 60)

def main():
    # Get the user inputs for ticker and time_interval
    ticker = input("Enter the stock ticker symbol: ")
    time_interval = int(input("Enter the time interval in minutes: "))

    # Start the scraping process
    scrape_twitter_accounts(ticker, time_interval)

if __name__ == "__main__":
    main()
