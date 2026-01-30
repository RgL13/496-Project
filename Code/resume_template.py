from google.colab import drive
drive.mount("/content/drive")
import pandas as pd
from pathlib import Path

# Paths
DATA_DIR = Path("/content/drive/MyDrive/stat496-Capstone/pipeline/data")
NAMES_PATH = DATA_DIR / "names.csv"
OUT_PATH = DATA_DIR / "resume.csv"

# Safety checks
if not NAMES_PATH.exists():
    raise FileNotFoundError(f"Cannot find file: {NAMES_PATH}")

names = pd.read_csv(NAMES_PATH)

required_cols = {"first_name", "last_name"}
missing = required_cols - set(names.columns)
if missing:
    raise ValueError(f"Missing required columns: {missing}. Found columns: {list(names.columns)}")

# Build full_name
names["full_name"] = (
    names["first_name"].astype(str).str.strip()
    + " "
    + names["last_name"].astype(str).str.strip()
)

# Loop + template
resumes = []

for _, row in names.iterrows():
    name = row["full_name"]

    resume = f"""
Name: {name}
Education: BS in Statistics
Experience: Data Analyst Intern
GPA: 3.8
""".strip()

    resumes.append({
        "id": row.get("id", None),
        "first_name": row.get("first_name", None),
        "last_name": row.get("last_name", None),
        "name_origin_category": row.get("name_origin_category", None),
        "gender_label": row.get("gender_label", None),
        "full_name": name,
        "resume_text": resume
    })
# Save
resume_df = pd.DataFrame(resumes)
resume_df.to_csv(OUT_PATH, index=False, encoding="utf-8")

print(f"Successful Saved resume.csv to: {OUT_PATH}")
display(resume_df.head(10))
