import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Class UnrealLinkScraper uses Selenium to scrape links from Unreal Engine forums
class UnrealLinkScraper:
    def __init__(self, categories=None):
        # Initializes with optional categories dictionary and empty list for storing links
        self.categories = categories
        self.links = []
        self.driver = None

    def run(self):
        # Setup Chrome options to use specific user data and profile
        options = webdriver.ChromeOptions()
        options.add_argument(r"user-data-dir=C:\Users\Dilshaansan\AppData\Local\Google\Chrome\User Data")
        options.add_argument('--profile-directory=Profile 6')

        # Initialize the Chrome webdriver with specified options
        self.driver = webdriver.Chrome(options=options)

        # Base URL for Unreal Engine forums
        base_url = "https://forums.unrealengine.com"
        self.driver.get(base_url)
        # Wait for elements to load on the page
        self.driver.implicitly_wait(10)

        # Extract links from the page that match specific criteria
        site_links = [raw_site_link.get_attribute("href") for raw_site_link in
                      self.driver.find_elements(By.CLASS_NAME, "category-title-link") if
                      raw_site_link.get_attribute("href").count("/") == 5]

        time.sleep(1.5)

        # Loop through each category to find specific links
        for cat in self.categories.keys():
            cat = cat.replace(" ", "-")

            for link in site_links:
                if cat in link:
                    time.sleep(1)
                    self.driver.get(link)
                    self.scrape_links(self.categories[cat])

        self.driver.close()

    def scrape_links(self, limit):
        # Function to scrape individual links within a category until a specified limit is reached
        cat_links = []
        while len(cat_links) < limit:
            link_count = len(cat_links)

            # Scroll to the bottom of the page to load more posts
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            raw_posts = self.driver.find_elements(By.CLASS_NAME, "topic-list-body")
            for raw_post in raw_posts:

                if link_count == limit:
                    break

                # Extract the hyperlink from the post and add it to the list
                post_link = raw_post.find_element(By.TAG_NAME, "a").get_attribute("href")
                cat_links.append(post_link)

        self.links.extend(cat_links)

    def get_links(self):
        # Returns the total number of scraped links
        print(f"Total links scraped: {len(self.links)}")
        return self.links
