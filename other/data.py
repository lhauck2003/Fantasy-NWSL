import pandas as pd

JSON = "nwsl_2025_season.json"

nwsl_df = pd.read_json(JSON)

print(nwsl_df)