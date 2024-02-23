import requests
import csv

def fetch_news(query):
    API_KEY = '63fd357c691246f9b084ddade6747223'  # Replace with your actual NewsAPI key
    API_ENDPOINT = "https://newsapi.org/v2/everything"
    parameters = {
        'q': query,  # User's search query
        'apiKey': API_KEY,
        'pageSize': 5,  # Limit to 5 articles
        'sortBy': 'publishedAt',  # Sort by publish date
        'language': 'en',  # Search for articles in English
    }
    response = requests.get(API_ENDPOINT, params=parameters)
    response.raise_for_status()  # Check for request errors
    return response.json().get('articles', [])

def save_to_csv(articles, filename='news_data.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['Title', 'Thumbnail', 'Date', 'Description', 'Author', 'URL']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for article in articles:
            writer.writerow({
                'Title': article.get('title', 'No Title'),
                'Thumbnail': article.get('urlToImage', 'No Thumbnail'),
                'Date': article.get('publishedAt', 'No Date'),
                'Description': article.get('description', 'No Description'),
                'Author': article.get('author', 'No Author'),
                'URL': article.get('url', 'No URL')
            })


# Main function to run the script
def main():
    query = input("Enter a company or topic to search for: ")
    articles = fetch_news(query)
    save_to_csv(articles)
    print(f"Top 5 articles about '{query}' have been saved to news_data.csv.")

if __name__ == "__main__":
    main()


