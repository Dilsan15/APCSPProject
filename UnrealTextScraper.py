import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# UnrealTextScraper class uses Selenium to scrape detailed text data from Unreal Engine forum posts
class UnrealTextScraper:
    def __init__(self):
        # Initial empty list to hold all scraped data and setup for links and Selenium driver
        self.all_data = []
        self.links_scrape = None
        self.driver = None
        self.post_data = {}

    # Method to set the links for scraping
    def set_links(self, links):
        self.links_scrape = links

    # Main method to execute the scraping process
    def run(self):
        # Chrome driver options to use specific user profile data
        options = webdriver.ChromeOptions()
        options.add_argument(r"user-data-dir=C:\Users\Dilshaansan\AppData\Local\Google\Chrome\User Data")
        options.add_argument('--profile-directory=Profile 6')
        self.driver = webdriver.Chrome(options=options)

        # Iterate through each link provided to scrape data
        for link in self.links_scrape:
            self.post_data = {}
            self.driver.get(link)
            self.scrape_post()

            # Infinite loop to scroll through and scrape replies until no new data is loaded
            while True:
                self.scrape_replies()
                last_height = self.driver.execute_script("return document.body.scrollHeight")
                time.sleep(1)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
            self.all_data.append(self.post_data)

        self.driver.close()

    # Method to scrape the main post data
    def scrape_post(self):
        # Extracting various data from the post using specific CSS class names
        post_title = self.driver.find_element(By.CLASS_NAME, "fancy-title").text
        post_topic = self.driver.find_elements(By.CLASS_NAME, "custom-topic-status-bar")
        post_topic = post_topic[0].text if post_topic else "NA"
        post_time = self.driver.find_element(By.CLASS_NAME, "relative-date").get_attribute("title") + " MDT"
        post_last_reply_time = self.driver.find_elements(By.CLASS_NAME, "last-reply")
        post_last_reply_time = post_last_reply_time[0].find_element(By.CLASS_NAME, "relative-date").get_attribute("title") + " MDT" if post_last_reply_time else "NA"
        post_categories = [tag.text for tag in self.driver.find_elements(By.CLASS_NAME, "badge-category__name")]
        post_tags = [tag.text for tag in self.driver.find_element(By.CLASS_NAME, "discourse-tags").find_elements(By.TAG_NAME, "a")]
        post_secondary_users = self.driver.find_elements(By.CLASS_NAME, "map")
        post_secondary_users = int(post_secondary_users[0].find_elements(By.CLASS_NAME, "users")[0].find_element(By.CLASS_NAME, "number").text) + 1 if post_secondary_users else 1
        post_vote_count = self.driver.find_elements(By.CLASS_NAME, "list-vote-count")
        post_vote_count = post_vote_count[0].text.replace("votes", "").strip() if post_vote_count else 0

        # Storing scraped data into a dictionary
        self.post_data.update({
            "title": post_title, "topic": post_topic, "post time": post_time, "last reply time": post_last_reply_time,
            "main category": post_categories[0], "sub category": post_categories[1] if len(post_categories) > 1 else 'NA',
            "tags": post_tags, "user count": post_secondary_users, "vote count": post_vote_count, "post data": None, "reply data": []
        })

    # Method to scrape replies to the main post
    def scrape_replies(self):
        all_reply_posts = self.driver.find_elements(By.CLASS_NAME, "topic-post")
        if all_reply_posts:
            for raw_reply_post in all_reply_posts:
                # Extracting details about each reply
                reply_author = raw_reply_post.find_element(By.CLASS_NAME, "ue-badges-for-post__username ").text
                reply_author_post_num = raw_reply_post.find_element(By.CLASS_NAME, "post-user-topic-count").text.replace("posts", "").strip()
                reply_author_answers_num = raw_reply_post.find_element(By.CLASS_NAME, "post-user-answers-count").text.replace("answers", "").strip()
                reply_post_date = raw_reply_post.find_element(By.CLASS_NAME, "relative-date").get_attribute("title") + " MDT"
                reply_edit_num = raw_reply_post.find_elements(By.CLASS_NAME, "edits")
                reply_edit_num = reply_edit_num[0].text if reply_edit_num else 0
                reply_post_likes = raw_reply_post.find_elements(By.CLASS_NAME, "regular-likes")
                reply_post_likes = reply_post_likes[0].text if reply_post_likes else 0
                reply_post_text = raw_reply_post.find_element(By.CLASS_NAME, "cooked").text
                reply_soln = raw_reply_post.find_elements(By.CLASS_NAME, "solution")
                reply_post_accepted = True if reply_soln else False

                reply_data = {
                    "author": reply_author, "author post num": reply_author_post_num, "author answers num": reply_author_answers_num,
                    "post date": reply_post_date, "edit num": reply_edit_num, "post likes": reply_post_likes,
                    "post text": reply_post_text, "post accepted": reply_post_accepted
                }

                # Determining if the reply is the main post or a subsequent reply
                if not self.post_data["post data"]:
                    self.post_data["post data"] = reply_data
                    all_reply_posts = [post for post in all_reply_posts if not post.find_elements(By.ID, "post_1")]
                else:
                    self.post_data["reply data"].append(reply_data)

        # Remove duplicate replies based on post text
        self.post_data["reply data"] = list({v['post text']: v for v in self.post_data["reply data"]}.values())

    # Method to retrieve all scraped data
    def get_data(self):
        return self.all_data
