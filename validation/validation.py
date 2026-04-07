# %%
import pandas as pd

# %%
# Read and format Extracted Df
ext_df = pd.read_csv("../slm/results/latest.csv")
ext_df["BC_CMP"] = ext_df["Bacia"].str.upper() + ":" + ext_df["Campo"].str.upper()
ext_df["BC_CMP"] = ext_df["BC_CMP"].str.strip()

print(ext_df.head())

# %%
# Read and format Ground Truth Df
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
gt_df["BC_CMP"] = gt_df["Bacia"] + ":" + gt_df["Campo"]
gt_df["BC_CMP"] = gt_df["BC_CMP"].str.strip()
print(gt_df.head())


# %%
# Iterate through extracted and compare
for field in ext_df["BC_CMP"].unique():
    gt = gt_df[gt_df["BC_CMP"] == field.strip()]

    if not len(gt):
        print(f"[WARN]: field {field} not found in Ground Truth dataset.")
        continue

    print(field, len(gt))
results = []

# %%
