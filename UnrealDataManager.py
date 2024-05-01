import pandas as pd
import time

# UnrealDataManager class for handling the storage and file output of scraped data
class UnrealDataManager:
    def __init__(self):
        # Initializes the UnrealDataManager with no data
        self.all_data = None


    def set_data(self, all_data):
        """Method to set the data inside the manager
            Parameter:
            all_data (list or dict): The data that has been scraped and is to be managed
        """
        self.all_data = all_data

    #
    def save_data(self, title, save_type):
        """
        Method to save the managed data to a CSV file
        Parameters:
        title (str): A string used to title and uniquely identify the file
        save_type (str): Determines the folder in which the file is saved ('bulk' or 'specific')
        """

        # Convert the data into a pandas DataFrame
        df = pd.DataFrame(data=self.all_data)

        # Get the current date and time, formatted as YYYY-MM-DD, append time zone
        current_date = time.strftime("%Y-%m-%d") + "_MDT"

        # Check the save_type and choose the directory accordingly
        if save_type == "bulk":
            # Save the DataFrame to a CSV file in the 'bulk' directory
            df.to_csv(
                f"C:/Users/Dilshaansan/PycharmProjects/APCSPProject/output/bulk/forum_data_bulk_{title}_{current_date}.csv",
                index=False)
        elif save_type == "specific":
            # Save the DataFrame to a CSV file in the 'specific' directory
            df.to_csv(
                f"C:/Users/Dilshaansan/PycharmProjects/APCSPProject/output/specific/forum_data_specific_{title}_{current_date}.csv",
                index=False)
