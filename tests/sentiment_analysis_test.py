'''''
SENTIMENT ANALYSIS TEST
'''
# tests/sentiment_analysis_test.py
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

# Adjust the path to find the src directory for importing
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from sentiment_analysis import add_sentiment_columns


def plot_sentiment_distribution(data):
    # Calculate the count of sentiment labels
    counts = data['label'].value_counts()

    # Drawing a bar chart
    plt.figure(figsize=(8, 5))
    plt.bar(counts.index, counts.values, color=['green', 'blue', 'red'])
    plt.title('Distribution of Sentiments')
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.show()

    # Save the chart
    screenshots_dir = '../screenshots'
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)
    plt.savefig(os.path.join(screenshots_dir, 'sentiment_distribution.png'))


def test_sentiment_analysis():
    # Assuming the preprocessed data file is in the 'data' directory
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'your_preprocessed_data.csv')
    data = pd.read_csv(data_path)

    # Check if the clean_text column exists
    if 'clean_text' in data.columns:
        # Apply sentiment analysis and add columns
        data_with_sentiment = add_sentiment_columns(data, 'clean_text')

        # Print the first five rows to verify the results
        print(data_with_sentiment[['clean_text', 'polarity', 'label']].head())

        # Optional: Save the updated DataFrame to a new CSV file
        output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'data_with_sentiment.csv')
        data_with_sentiment.to_csv(output_path, index=False)

        # Plot and save the sentiment distribution
        plot_sentiment_distribution(data_with_sentiment)
    else:
        print("The 'clean_text' column was not found. Please verify the column names.")


if __name__ == "__main__":
    test_sentiment_analysis()