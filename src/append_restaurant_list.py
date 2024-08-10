import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse

restaurant_list_filepath = "../assets/restaurant_list.csv"
start_url = 'https://hellgatenyc.com/tag/20-dinner/'

def get_soup(url):
    print(f"Fetching content from: {url}")
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, 'html.parser')
    else:
        print(f"Failed to retrieve content from {url}, status code: {response.status_code}")
        return None

def extract_article_body(article_page):
    article_body = article_page.find('article', class_='post')
    if article_body:
        paragraphs = article_body.find_all('p')
        article_text = ' '.join([p.get_text(separator=' ', strip=True) for p in paragraphs])
        return article_text
    else:
        print("Article body not found")
        return ""

def parse_articles(soup):
    articles = []
    for post_card in soup.find_all('article', class_='post-card'):
        # Extract article link
        title_link_tag = post_card.find('h3', class_='outfit small').find('a')
        if title_link_tag:
            article_link = title_link_tag['href']
            # Ensure the article link is a valid URL
            if not urllib.parse.urlparse(article_link).scheme:
                article_link = urllib.parse.urljoin(start_url, article_link)
            # Extract headline
            headline = title_link_tag.get_text().strip()
            # Extract excerpt
            excerpt_tag = post_card.find('p', class_='excerpt mb-0')
            excerpt = excerpt_tag.get_text().strip() if excerpt_tag else ''
            # Extract author
            author_tag = post_card.find('span', class_='mr').find('a')
            author = author_tag.get_text().strip() if author_tag else ''
            # Extract date
            date_tag = post_card.find('time')
            date = date_tag.get_text().strip() if date_tag else ''
            # Get article details
            article_page = get_soup(article_link)
            if article_page:
                article_body = extract_article_body(article_page)
                articles.append({
                    'Headline': headline,
                    'Article Link': article_link,
                    'Excerpt': excerpt,
                    'Author': author,
                    'Date': date,
                    'Address': '',
                    'Restaurant Names and Links': '',
                    'Google Maps Address': '',
                    'Restaurant Name': '',
                    'Latitude': '',
                    'Longitude': '',
                    'Link': '',
                    'Unnamed: 10': '',
                    'Unnamed: 11': '',
                    'Unnamed: 12': '',
                    'Article Body': article_body
                })
            else:
                print(f"Failed to fetch article page: {article_link}")
        else:
            print(f"Title link tag not found in post card: {post_card}")
    return articles

def get_next_page(soup):
    next_button = soup.find('a', class_='next-posts')
    if next_button and 'disabled' not in next_button.get('class', []):
        next_page_url = next_button['href']
        if not urllib.parse.urlparse(next_page_url).scheme:
            next_page_url = urllib.parse.urljoin(start_url, next_page_url)
        return next_page_url
    else:
        return None

def scrape_articles(start_url):
    all_articles = []
    seen_urls = set()  # Set to keep track of seen article URLs
    url = start_url
    while url:
        soup = get_soup(url)
        if soup:
            articles = parse_articles(soup)
            if articles:
                for article in articles:
                    if article['Article Link'] not in seen_urls:
                        all_articles.append(article)
                        seen_urls.add(article['Article Link'])
            else:
                print("No articles found on this page.")
            url = get_next_page(soup)
            if url:
                print(f"Moving to the next page: {url}")
            else:
                print("No more pages to scrape.")
        else:
            break
    return all_articles


def new_articles_get_locations(scraped_df, old_list):
    stripped_list = old_list
    stripped_list['Article Link'] = old_list['Article Link'].str.rstrip('/')

    list_to_add = stripped_list
    for index, article in scraped_df.iterrows():
        link = article['Article Link'].rstrip('/')
        if link.rstrip('/') not in stripped_list['Article Link'].tolist() and link.rstrip('/') not in list_to_add['Article Link']:
            rest_name = input(f"What's the name of the restaurant contained in the link: {link}? Enter nothing if not a restaurant. \n")
            if rest_name:
                raw_address = input(
                    f"Using the format, 456 8th Avenue, Manhattan enter the address for {rest_name}, please:\n")
                socials_website = input(
                    f"Optional: Enter the social media or website for {rest_name} (leave blank if none):\n") or ""

                formatted_address = raw_address.replace(' ', '+')
                google_maps_address = formatted_address.replace(',', '%2C')

                article['Restaurant Name'] = rest_name
                article['Address'] = raw_address
                article['Google Maps Address'] = google_maps_address
                article['Restaurant Names and Links'] = rest_name + " (" + socials_website + ")"
                # TODO: SWAP OUT THIS MAPS KEY WITH YOUR OWN GOOGLE MAPS API KEY: EASY TO GET, JUST GOOGLE IT
                geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={google_maps_address}&key=YOUR_API_KEY_HERE"
                response = requests.get(geocode_url).json()

                if response['status'] == 'OK':
                    location = response['results'][0]['geometry']['location']
                    lat, lng = location['lat'], location['lng']

                    article['Latitude'] = lat
                    article['Longitude'] = lng

                    # Convert the Series article to a DataFrame and concatenate
                    article_df = pd.DataFrame([article])
                    list_to_add = pd.concat([list_to_add, article_df], ignore_index=True)
                else:
                    print(f"Failed to geocode address for restaurant in {link}. Response status: {response['status']}")
            else:
                print("Moving on: \n")
    return list_to_add


def main(url = start_url):
    articles = scrape_articles(url)
    scraped_articles = pd.DataFrame(articles)
    scraped_articles.to_csv('../scraped_articles.csv', index=False)
    master_list = pd.read_csv(restaurant_list_filepath)

    if scraped_articles.empty:
        print("The CSV is empty. Please check the scraping logic.")
    else:
        new_articles_get_locations(scraped_articles, master_list).to_csv(restaurant_list_filepath, index=False)
        #print(new_articles_get_locations(scraped_articles, master_list))
        print(f"Scraping complete. Data added to {restaurant_list_filepath}")
    return

if __name__ == "__main__":
    main()

