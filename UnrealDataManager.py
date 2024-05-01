import pandas as pd
import time


class UnrealDataManager:
    def __init__(self):
        self.all_data = None

    def set_data(self, all_data):
        self.all_data = all_data

    def save_data(self, title, save_type):
        df = pd.DataFrame(data=self.all_data)

        current_date = time.strftime("%Y-%m-%d") + "_MDT"
        if save_type == "bulk":
            df.to_csv(
                f"C:/Users/Dilshaansan/PycharmProjects/APCSPProject/output/bulk/forum_data_bulk_{title}_{current_date}.csv",
                index=False)
        elif save_type == "specific":
            df.to_csv(
                f"C:/Users/Dilshaansan/PycharmProjects/APCSPProject/output/specific/forum_data_specific_{title}_{current_date}.csv",
                index=False)
