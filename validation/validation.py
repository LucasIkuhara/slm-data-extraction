# %%
import pandas as pd

# %%
gt_df = pd.read_excel("ground_truth.xlsx", sheet_name="Data (2)", header=2)
print(gt_df.head())

# %%
ext_df = pd.read_csv("out.csv")
print(ext_df.head())

# %%
# Column mapping
col_map = {
    "BASIN": "Bacia",
    "FIELD": "Campo",
}

# %%
