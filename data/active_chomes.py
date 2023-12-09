import pandas as pd

from utils import csv_path

active_chomes = pd.read_csv(
    "https://raw.githubusercontent.com/BenGoodair/childrens_social_care_data/main/Final_Data/outputs/active_chomes_2023.csv",
    encoding="ISO-8859-1",
)

active_chomes.to_csv(
    csv_path("active_chomes"), index=False, header=True, encoding="ISO-8859-1"
)
