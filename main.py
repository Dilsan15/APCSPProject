import os

# Importing the custom classes for managing, scraping links, and scraping text from Unreal Engine forums
from UnrealDataManager import UnrealDataManager
from UnrealLinkScraper import UnrealLinkScraper
from UnrealTextScraper import UnrealTextScraper

# Instantiate the scraper and manager objects
link_scraper = UnrealLinkScraper()
post_scraper = UnrealTextScraper()
data_manager = UnrealDataManager()

def input_validation(l_lim=1, t_lim=5):
    """ Input validation function
    Verifies user input is within a specified range, defaults to 1-5
    Repeatedly prompts the user until a valid integer within the range is provided

    # Parameters:
    l_lim (int): The lower limit of the range, defaults to 1
    t_lim (int): The upper limit of the range, defaults to 5

    Returns: user_c_input (int): Validated user input
    """

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

    """Function to scrape bulk forum posts
    Prompts the user for the number of posts to scrape from different categories
    Uses the UnrealLinkScraper to fetch links and UnrealTextScraper to scrape posts
    Saves the scraped data to a CSV file through UnrealDataManager
    """

    print("Note: there is a 10,000 forum scraping limit (for each category)\n")

    # Get user inputs for different forum categories with limits
    print("How many forum posts would you like to scrape for the General category (max 10000)?")
    general_limit = input_validation(0, 10000)

    # Repeat for other categories
    print("How many forum posts would you like to scrape for the Development category?")
    development_limit = input_validation(0, 10000)

    print("How many forum posts would you like to scrape for the Community category?")
    programming_limit = input_validation(0, 10000)

    print("How many forum posts would you like to scrape for the International category?")
    asset_creation_limit = input_validation(0, 10000)

    print("How many forum posts would you like to scrape for the Legacy category?")
    legacy_limit = input_validation(0, 10000)

    # Instantiate a new UnrealLinkScraper with category limits
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

#
def scrape_s_forum_posts():
    """
    Function to scrape specific forum posts
    Prompts the user to enter links to specific forum posts
    Scrapes the posts and saves the data to a named CSV file
    """

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
    """
     Function to delete a CSV file
     Lists all CSV files in the specified directories and allows the user to choose one for deletion
    """


    directories = [
        "output/bulk/",
        "output/specific/"
    ]

    all_files = []

    # Collect all CSV files from the specified directories
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
        print("Error! Please try again")
        return

# Main program loop
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
