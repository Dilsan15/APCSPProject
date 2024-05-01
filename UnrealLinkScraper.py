import time

from selenium import webdriver
from selenium.webdriver.common.by import By


class UnrealLinkScraper:
    def __init__(self, categories=None):
        self.categories = categories
        self.links = []

    def run(self):

        options = webdriver.ChromeOptions()
        options.add_argument(r"user-data-dir=C:\Users\Dilshaansan\AppData\Local\Google\Chrome\User Data")
        options.add_argument('--profile-directory=Profile 6')

        self.driver = webdriver.Chrome(options=options)

        base_url = "https://forums.unrealengine.com"
        self.driver.get(base_url)
        self.driver.implicitly_wait(10)

        site_links = [raw_site_link.get_attribute("href") for raw_site_link in
                      self.driver.find_elements(By.CLASS_NAME, "category-title-link") if
                      raw_site_link.get_attribute("href").count("/") == 5]

        time.sleep(1.5)

        for cat in self.categories.keys():
            cat = cat.replace(" ", "-")

            for link in site_links:
                if cat in link:
                    time.sleep(1)
                    self.driver.get(link)
                    self.scrape_links(self.categories[cat])

        self.driver.close()

    def scrape_links(self, limit):

        cat_links = []
        while len(cat_links) < limit:
            link_count = len(cat_links)

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            raw_posts = self.driver.find_elements(By.CLASS_NAME, "topic-list-body")
            for raw_post in raw_posts:

                if link_count == limit:
                    break

                post_link = raw_post.find_element(By.TAG_NAME, "a").get_attribute("href")
                cat_links.append(post_link)

        self.links.extend(cat_links)

    def get_links(self):

        print(f"Total links scraped: {len(self.links)}")
        return self.links
