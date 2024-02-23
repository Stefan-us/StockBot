import requests
from bs4 import BeautifulSoup

# Define a list of websites to scrape
websites = [
    "https://news.sky.com/story/lloyds-banks-record-profits-but-sets-aside-450m-to-cover-car-finance-probe-13078045",
    "https://www.bloomberg.com/news/articles/2024-02-21/private-equity-payouts-at-major-firms-plummet-49-in-two-years?leadSource=uverify%20wall",
    "https://www.ft.com/content/7ef97342-48fa-4969-b3ee-bc7419b69e65"
]

# Define the function to extract links from the HTML content
def extract_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = []
    for a_tag in soup.findAll('a', href=True):
        href = a_tag['href']
        # Here, you might want to filter and process the href value as needed
        links.append(href)
    return links

# Define a function to perform a search query and fetch the results
def perform_search(query):
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(search_url, headers=headers)
    return response.text

# Now, use the functions defined above
query = "Lloyds Bank news"
search_results_html = perform_search(query)  # Perform the search

# Use the previously defined function to extract links from the search results
article_links = extract_links(search_results_html)

# Print the extracted links
for link in article_links:
    print(link)

# Function to fetch content from a URL
def fetch_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        return response.text
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

# Function to save websites to a file
def save_websites_to_file(websites, file_path):
    with open(file_path, 'w') as file:
        for website in websites:
            file.write(website + "\n")

# Function to read websites from a file
def read_websites_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

# Save the list of websites to a text file
file_path = 'websites.txt'
save_websites_to_file(websites, file_path)

# Read the list back (to demonstrate it works)
saved_websites = read_websites_from_file(file_path)
print(saved_websites)

# Example function to parse and print the title of an article
def parse_and_print_title(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    title = soup.find('title').text  # This assumes <title> tag contains the article title
    print(title)

def fetch_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

def parse_article(html_content):
    soup = BeautifulSoup(html_content, 'lxml')

    title = soup.find('h1').text if soup.find('h1') else 'Title not found'
    publication_date = soup.find('span', class_='date').text if soup.find('span', class_='date') else 'Date not found'
    article_body = soup.find('div', class_='article-content').text if soup.find('div', class_='article-content') else 'Content not found'

    return {
        'title': title,
        'publication_date': publication_date,
        'article_body': article_body
    }



# Fetch and print the content of each website
saved_websites = read_websites_from_file('websites.txt')  # Assuming this function reads URLs from a file

# Function to save article information to a file
def save_article_info(article_info, file_path='extracted_articles.txt'):
    with open(file_path, 'a') as file:
        file.write(f"Title: {article_info['title']}\n")
        file.write(f"Publication Date: {article_info['publication_date']}\n")
        file.write(f"Article Body: {article_info['article_body'][:100]}... (truncated)\n")  # Truncate for brevity
        file.write("\n-----------------------------------\n\n")

# Loop through saved websites, fetch their content, parse the articles, and save the info
for website in saved_websites:
    html_content = fetch_content(website)
    if html_content:
        article_info = parse_article(html_content)
        print(article_info)  # Optionally, keep this line to also see the output in the console
        save_article_info(article_info)




