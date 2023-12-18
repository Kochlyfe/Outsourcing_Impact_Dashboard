import os
from typing import NamedTuple
import pandas as pd
import geopandas as gpd
from dataclasses import dataclass


@dataclass(frozen=True)
class DataContainer:
    la_df: pd.DataFrame
    nobs_final: pd.DataFrame
    exitdata: pd.DataFrame
    merged2: gpd.GeoDataFrame
    active_chomes: pd.DataFrame
    outcomes_df: pd.DataFrame
    placements_df: pd.DataFrame
    expenditures_df: pd.DataFrame

    @classmethod
    def load_data(cls):
        # Get the directory of the current script
        dir_path = os.path.dirname(os.path.abspath(__file__))
        processed_path = os.path.join(dir_path, "..", "data", "processed")

        # Define the paths to the CSV files relative to the script directory
        la_df_path = os.path.join(processed_path, "la.csv")
        nobs_final_path = os.path.join(processed_path, "nobs.csv")
        exitdata_path = os.path.join(processed_path, "exits.csv")
        merged2_path = os.path.join(processed_path, "merged.geojson")
        active_chomes_path = os.path.join(processed_path, "active_chomes.csv")
        outcomes_df_path = os.path.join(processed_path, "outcomes.csv")
        placements_df_path = os.path.join(processed_path, "placements.csv")
        expenditures_df_path = os.path.join(processed_path, "expenditures.csv")

        # Read the CSV files
        la_df = pd.read_csv(la_df_path)
        nobs_final = pd.read_csv(nobs_final_path)
        exitdata = pd.read_csv(exitdata_path)
        active_chomes = pd.read_csv(active_chomes_path)
        outcomes_df = pd.read_csv(outcomes_df_path)
        placements_df = pd.read_csv(placements_df_path)
        expenditures_df = pd.read_csv(expenditures_df_path)

        # Read geojson file
        merged2 = gpd.read_file(merged2_path)

        return cls(
            la_df,
            nobs_final,
            exitdata,
            merged2,
            active_chomes,
            outcomes_df,
            placements_df,
            expenditures_df,
        )

    def get_dataframes_as_namedtuple(self) -> NamedTuple:
        DataFramesTuple = NamedTuple(
            "DataFramesTuple",
            [
                ("la_df", pd.DataFrame),
                ("nobs_final", pd.DataFrame),
                ("exitdata", pd.DataFrame),
                ("merged2", gpd.GeoDataFrame),
                ("active_chomes", pd.DataFrame),
                ("outcomes_df", pd.DataFrame),
                ("placements_df", pd.DataFrame),
                ("expenditures_df", pd.DataFrame),
            ],
        )

        return DataFramesTuple(
            self.la_df,
            self.nobs_final,
            self.exitdata,
            self.merged2,
            self.active_chomes,
            self.outcomes_df,
            self.placements_df,
            self.expenditures_df,
        )
