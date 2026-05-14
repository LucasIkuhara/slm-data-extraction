# %%
import pandas as pd
import numpy as np


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
    "../slm/results/prompts_2.xlsx",
)
ext_df = split_multi_field_rows(ext_df)
ext_df["BC_CMP"] = ext_df["Bacia"].str.upper() + ":" + ext_df["Campo"].str.upper()
ext_df["BC_CMP"] = ext_df["BC_CMP"].str.strip()
ext_df.drop([f for f in ext_df.columns if "_src" in f], axis="columns", inplace=True)

# Cast -1 to 0
text_fields = ["Bacia", "Campo", "Document", "empresa", "BC_CMP"]
for c in ext_df:
    if c in text_fields:
        continue
    ext_df[c] = ext_df[c].apply(lambda x: max(0, x))

# Modulate qnt found based on existence flag
ext_df["qtd_manifold"] = ext_df["qtd_manifold"] * ext_df["manifold"]
ext_df["qtd_skid"] = ext_df["qtd_skid"] * ext_df["skid"]

ext_df.head()

# %%
# Read and format Ground Truth Df
gt_df = pd.read_excel("ground_truth.xlsx", sheet_name="Data", header=2)

# Column mapping
col_map = {
    "BASIN": "Bacia",
    "FIELD": "Campo",
    # "COAST_DIST": "distancia",
    "MANIFOLD _QNT": "qtd_manifold",
    "SKIDS_QNT": "qtd_skid",
    # "LDA": "lamina",
    "Contract": "empresa",
    "CABO ELÉTRICO ": "cabo_elet",
    "MANIFOLD": "manifold",
    "DR": "duto_rig",
    "DF": "duto_flex",
}
non_text_fields = [x for x in col_map.values() if x not in text_fields]

gt_df = gt_df.rename(columns=col_map)
gt_df.drop(
    [x for x in gt_df.columns if x not in col_map.values()],
    inplace=True,
    axis="columns",
)
gt_df = split_multi_field_rows(gt_df)

gt_df["Bacia"] = gt_df["Bacia"].str.replace("BACIA DE", "").str.replace("BACIA", "")
gt_df["BC_CMP"] = gt_df["Bacia"] + ":" + gt_df["Campo"]
gt_df["BC_CMP"] = gt_df["BC_CMP"].str.strip()
gt_df.head()


# %%
# Row-wise Validation
def get_diff_dict(extracted: dict, ground: dict) -> dict:
    diff = {
        "Bacia": extracted["Bacia"],
        "Campo": extracted["Campo"],
        "Documento": extracted["Document"],
        "K": extracted["K"],
    }

    for key in non_text_fields:
        diff[key] = int(extracted[key]) == int(ground[key])

    # Label, simply create a str
    diff["empresa"] = f"R: {ground['empresa']}; E: {extracted['empresa']}"
    return diff


results = []

# Iterate through extracted and compare
k_values = [k for k in ext_df["K"].unique()]
for k in k_values:
    for field in ext_df["BC_CMP"].unique():

        # Get Ground Truth dict filtered by a specific extraction field
        gt = gt_df[gt_df["BC_CMP"] == field.strip()]
        if not len(gt):
            print(f"[WARN]: field {field} not found in Ground Truth dataset.")
            continue
        field_ground_truth = gt.iloc[0].to_dict()

        # Get extracted dict for a specific extraction field and K value
        field_extracted = (
            ext_df[(ext_df["BC_CMP"] == field) & (ext_df["K"] == k)].iloc[0].to_dict()
        )

        compared = get_diff_dict(field_extracted, field_ground_truth)
        results.append(compared)

    compared_df = pd.DataFrame(results)

out_path = "validation.xlsx"
compared_df.to_excel(out_path, index=False)
compared_df.head()

# %%
# Format Results and Export latex
excluded = ["Documento", "Bacia"]
printed_fields = [x for x in col_map.values() if x not in excluded]


def to_formatted_latex(df: pd.DataFrame, name: str):
    df.style.hide(axis="index").format(precision=2).relabel_index(
        [x.replace("_", " ") for x in df.columns], axis="columns"
    ).to_latex(name, hrules=False)


# Only include extraction fields with results
fmt_ext = ext_df[ext_df["Campo"].isin(compared_df["Campo"].unique())]

# Exclude duplicate Tambaú
fmt_ext = fmt_ext.reset_index()
fmt_ext = fmt_ext[fmt_ext.Campo != "Tambaú"]
fmt_ext.loc[fmt_ext["Campo"] == "Uruguá", "Campo"] = "Tambaú/Uruguá"

results_numeric = []
for k in k_values:
    k_df = fmt_ext[fmt_ext["K"] == k]
    for f in non_text_fields:
        acc = 1 - np.sum(k_df[f]) / len(k_df[f])

        results_numeric.append(
            {
                "Variável": f,
                "K": k,
                "Accuracy": acc,
            }
        )

metrics = pd.DataFrame(results_numeric)

# Switch _'s for spaces for latex printing
metrics["Variável"] = [x.replace("_", " ") for x in metrics["Variável"]]

to_formatted_latex(metrics, "metrics.tex")
metrics.pivot(index="K", columns=["Variável"]).style.to_latex(
    "consolidated.tex", hrules=False
)

# %%
