# %%
import pandas as pd


def split_multi_field_rows(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Campo"] = df["Campo"].str.split("/")
    df = df.explode("Campo")
    df = df[~df["Campo"].str.contains("/")]
    df.reset_index()
    return df


# %%
# Read and format Extracted Df
ext_df = pd.read_excel(
    "../slm/results/latest.xlsx",
)
ext_df = split_multi_field_rows(ext_df)
ext_df["BC_CMP"] = ext_df["Bacia"].str.upper() + ":" + ext_df["Campo"].str.upper()
ext_df["BC_CMP"] = ext_df["BC_CMP"].str.strip()
ext_df.drop([f for f in ext_df.columns if "_src" in f], axis="columns", inplace=True)

ext_df.head()

# %%
# Read and format Ground Truth Df
gt_df = pd.read_excel("ground_truth.xlsx", sheet_name="Data", header=2)

# Column mapping
col_map = {
    "BASIN": "Bacia",
    "FIELD": "Campo",
    "COAST_DIST": "distancia",
    "MANIFOLD _QNT": "qtd_manifold",
    "SKIDS_QNT": "qtd_skid",
    "LDA": "lamina",
    # "EC": "cabo_elet",
    "EQ": "manifold",
    "DR": "duto_rig",
    "DF": "duto_flex",
}
gt_df = gt_df.rename(columns=col_map)
gt_df = split_multi_field_rows(gt_df)

gt_df["Bacia"] = gt_df["Bacia"].str.replace("BACIA DE", "").str.replace("BACIA", "")
gt_df["BC_CMP"] = gt_df["Bacia"] + ":" + gt_df["Campo"]
gt_df["BC_CMP"] = gt_df["BC_CMP"].str.strip()
print(gt_df.head())


# %%
# Row-wise Validation
def get_diff_dict(extracted: dict, ground: dict) -> dict:
    not_matched = ["Bacia", "Campo"]
    keys = [x for x in col_map.values() if x not in not_matched]
    diff = {
        "Bacia": extracted["Bacia"],
        "Campo": extracted["Campo"],
        "Documento": extracted["Document"],
    }

    for key in keys:
        extracted_val = max(0, extracted[key])
        diff[key] = extracted_val - ground[key]

    return diff


results = []

# Iterate through extracted and compare
for field in ext_df["BC_CMP"].unique():
    gt = gt_df[gt_df["BC_CMP"] == field.strip()]

    if not len(gt):
        print(f"[WARN]: field {field} not found in Ground Truth dataset.")
        continue

    field_gt = gt.iloc[0].to_dict()
    field_ext = ext_df[ext_df["BC_CMP"] == field].iloc[0].to_dict()

    compared = get_diff_dict(field_ext, field_gt)
    results.append(compared)

compared_df = pd.DataFrame(results)

out_path = "validation.osv"
print()
print(compared_df.head())

# %%
