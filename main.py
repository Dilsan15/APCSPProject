import os

from UnrealDataManager import UnrealDataManager
from UnrealLinkScraper import UnrealLinkScraper
from UnrealTextScraper import UnrealTextScraper

link_scraper = UnrealLinkScraper()
post_scraper = UnrealTextScraper()
data_manager = UnrealDataManager()

# input validation

# method used to verify user input is within the range either passed in or by default [1 to 5]
# prompts user to enter a valid number if the input is not within the range, or if the input is not a number
# returns the user input if it is valid, which is later used to determine the action to take

# Parameters:
# l_lim (int) - lower limit of the range (default 1)
# t_lim (int) - upper limit of the range (default 5)

# Returns:
# user_c_input (int) - user input number if it is valid


def input_validation(l_lim=1, t_lim=5):
    while True:
        try:
            user_c_input = int(input("Enter your choice: "))
            if user_c_input in range(l_lim, t_lim + 1):
                print("\n")
                return user_c_input
            else:
                print("Please enter a valid number from " + str(l_lim) + " to " + str(t_lim))
        except ValueError:
            print("Please enter a valid number from " + str(l_lim) + " to " + str(t_lim))

def scrape_b_forum_posts():
    print("Note: there is a 10 000 forum scraping limit (for each category)\n")

    print("How many forum posts would you like to scrape for the General category (max 10000)?")
    general_limit = input_validation(0, 10000)

    print("How many forum posts would you like to scrape for the Development category?")
    development_limit = input_validation(0, 10000)

    print("How many forum posts would you like to scrape for the Community category?")
    programming_limit = input_validation(0, 10000)

    print("How many forum posts would you like to scrape for the International category?")
    asset_creation_limit = input_validation(0, 10000)

    print("How many forum posts would you like to scrape for the Legacy category?")
    legacy_limit = input_validation(0, 10000)

    link_scraper = UnrealLinkScraper({
        "general": general_limit,
        "development": development_limit,
        "community": programming_limit,
        "international": asset_creation_limit,
        "legacy": legacy_limit
    })

    print(
        f"Scraping {general_limit + development_limit + programming_limit + asset_creation_limit + legacy_limit} posts ...\n")

    link_scraper.run()

    post_scraper.set_links(link_scraper.get_links())
    post_scraper.run()

    data_manager.set_data(post_scraper.get_data())
    data_manager.save_data("bulk", "bulk")
    print("Data has been scraped and saved to a CSV file\n")


def scrape_s_forum_posts():
    print("Please enter the number of posts you would like to scrape (1-10000):")
    single_forum_scrapes = input_validation(1, 10000)

    input_link_list = []
    for i in range(single_forum_scrapes):

        while True:
            input_link = input("\bPlease enter the link to the forum post you would like to scrape: ")

            if "https://forums.unrealengine.com/" not in input_link:
                print("Please enter a valid link\n")
                continue
            else:
                input_link_list.append(input_link)
                break

    post_scraper.set_links(input_link_list)
    post_scraper.run()
    data_manager.set_data(post_scraper.get_data())

    title = input("Please enter a title for the CSV file: ")

    data_manager.save_data(title, "specific")
    print("Data has been scraped and saved to a CSV file\n")


def delete_csv_file():
    directories = [
        "output/bulk/",
        "output/specific/"
    ]

    all_files = []

    for directory in directories:
        all_files.extend([os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".csv")])

    if not all_files:
        print("No CSV files available for deletion!")
        return

    print("The following CSV files are available for deletion:\n")
    for idx, file in enumerate(all_files, 1):
        print(f"{idx}. {file.split('/')[-1]}")
    try:
        file_number = int(input("\nPlease enter the number corresponding to the file you would like to delete: "))
        os.remove(all_files[file_number - 1])
        print("File has been deleted\n")

    except ValueError:
        print("Error!, please try again")
        return


while True:

    print("\nHello!, welcome to the Unreal Engine Forum Scraper\n")
    print("Please enter the number corresponding to the action you would like to take: ")
    print("1. Scrape forum posts and save to CSV")
    print("2. Scrape specific forum posts and save to a CSV")
    print("3. Delete specific CSV file")
    print("4. Exit\n")

    user_input = input_validation(1, 4)

    if user_input == 1:
        print("You have chosen to scrape forum posts and save to CSV\n")
        scrape_b_forum_posts()
    elif user_input == 2:
        print("You have chosen to scrape specific forum posts and save to a CSV file\n")
        scrape_s_forum_posts()
    elif user_input == 3:
        print("You have chosen to delete a specific CSV file\n")
        delete_csv_file()
    else:
        print("Goodbye!")
        break
