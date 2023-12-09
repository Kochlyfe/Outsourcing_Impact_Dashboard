import os


def csv_path(filename: str):
    dir_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(dir_path, "processed", f"{filename}.csv")


def geojson_path(filename: str):
    dir_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(dir_path, "processed", f"{filename}.geojson")
