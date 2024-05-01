import time

from selenium import webdriver
from selenium.webdriver.common.by import By


class UnrealTextScraper:
    def __init__(self):
        self.all_data = []
        self.links_scrape = None
        self.driver = None
        self.post_data = {}

    def set_links(self, links):
        self.links_scrape = links

    def run(self):

        options = webdriver.ChromeOptions()
        options.add_argument(r"user-data-dir=C:\Users\Dilshaansan\AppData\Local\Google\Chrome\User Data")
        options.add_argument('--profile-directory=Profile 6')

        self.driver = webdriver.Chrome(options=options)

        for link in self.links_scrape:
            self.post_data = {}
            self.driver.get(link)
            self.scrape_post()

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

    def scrape_post(self):
        post_title = self.driver.find_element(By.CLASS_NAME, "fancy-title").text

        post_topic = self.driver.find_elements(By.CLASS_NAME, "custom-topic-status-bar")
        if not post_topic:
            post_topic = "NA"
        else:
            post_topic = post_topic[0].text

        post_time = self.driver.find_element(By.CLASS_NAME, "relative-date").get_attribute("title") + " MDT"

        post_last_reply_time = self.driver.find_elements(By.CLASS_NAME, "last-reply")

        if not post_last_reply_time:
            post_last_reply_time = "NA"
        else:
            post_last_reply_time = post_last_reply_time[0].find_element(By.CLASS_NAME, "relative-date").get_attribute(
                "title") + " MDT"

        post_categories = [tag.text for tag in self.driver.find_elements(By.CLASS_NAME, "badge-category__name")]

        post_m_category = post_categories[0]
        post_s_category = post_categories[1]

        post_tags = [tag.text for tag in
                     self.driver.find_element(By.CLASS_NAME, "discourse-tags").find_elements(By.TAG_NAME, "a")]

        post_secondary_users = self.driver.find_elements(By.CLASS_NAME, "map")

        if not post_secondary_users:
            post_secondary_users = 1
        else:
            post_secondary_users = int(
                post_secondary_users[0].find_elements(By.CLASS_NAME, "users")[0].find_element(By.CLASS_NAME,
                                                                                              "number").text) + 1

        post_vote_count = self.driver.find_elements(By.CLASS_NAME, "list-vote-count")
        if not post_vote_count:
            post_vote_count = 0
        else:
            post_vote_count = post_vote_count[0].text.replace("votes", "").strip()

        self.post_data["title"] = post_title
        self.post_data["topic"] = post_topic
        self.post_data["post time"] = post_time
        self.post_data["last reply time"] = post_last_reply_time
        self.post_data["main category"] = post_m_category
        self.post_data["sub category"] = post_s_category
        self.post_data["tags"] = post_tags
        self.post_data["user count"] = post_secondary_users
        self.post_data["vote count"] = post_vote_count
        self.post_data["post data"] = None
        self.post_data["reply data"] = []

    def scrape_replies(self):

        all_reply_posts = self.driver.find_elements(By.CLASS_NAME, "topic-post")

        if all_reply_posts:

            for raw_reply_post in all_reply_posts:
                reply_author = raw_reply_post.find_element(By.CLASS_NAME, "ue-badges-for-post__username ").text
                reply_author_post_num = raw_reply_post.find_element(By.CLASS_NAME,
                                                                    "post-user-topic-count").text.replace("posts",
                                                                                                          "").strip()
                reply_author_answers_num = raw_reply_post.find_element(By.CLASS_NAME,
                                                                       "post-user-answers-count").text.replace(
                    "answers", "").strip()
                reply_post_date = raw_reply_post.find_element(By.CLASS_NAME, "relative-date").get_attribute(
                    "title") + " MDT"

                reply_edit_num = raw_reply_post.find_elements(By.CLASS_NAME, "edits")

                if not reply_edit_num:
                    reply_edit_num = 0
                else:
                    reply_edit_num = reply_edit_num[0].text

                reply_post_likes = raw_reply_post.find_elements(By.CLASS_NAME, "regular-likes")

                if not reply_post_likes:
                    reply_post_likes = 0
                else:
                    reply_post_likes = reply_post_likes[0].text
                reply_post_text = raw_reply_post.find_element(By.CLASS_NAME, "cooked").text

                reply_soln = raw_reply_post.find_elements(By.CLASS_NAME, "solution")
                if not reply_soln:
                    reply_post_accepted = False
                else:
                    reply_post_accepted = True

                reply_data = {
                    "author": reply_author,
                    "author post num": reply_author_post_num,
                    "author answers num": reply_author_answers_num,
                    "post date": reply_post_date,
                    "edit num": reply_edit_num,
                    "post likes": reply_post_likes,
                    "post text": reply_post_text,
                    "post accepted": reply_post_accepted
                }

                if not self.post_data["post data"]:
                    self.post_data["post data"] = reply_data
                    all_reply_posts = [post for post in all_reply_posts if not post.find_elements(By.ID, "post_1")]
                else:
                    self.post_data["reply data"].append(reply_data)

        self.post_data["reply data"] = list({v['post text']: v for v in self.post_data["reply data"]}.values())

    def get_data(self):
        return self.all_data
