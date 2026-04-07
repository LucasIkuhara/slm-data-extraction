# %%
import pandas as pd

# %%
ext_df = pd.read_csv("../slm/results/latest.csv")
print(ext_df.head())

# %%
gt_df = pd.read_excel("ground_truth.xlsx", sheet_name="Data (2)", header=2)

# Column mapping
col_map = {
    "BASIN": "Bacia",
    "FIELD": "Campo",
    "COAST_DIST": "distancia",
    "MANIFOLD _QNT": "qtd_manifold",
    "SKIDS_QNT": "qtd_skid",
    "LDA": "lamina",
}

gt_df = gt_df.rename(columns=col_map)
gt_df["Bacia"] = gt_df["Bacia"].str.replace("BACIA DE", "").str.replace("BACIA", "")
print(gt_df.head())


# %%


# %%
