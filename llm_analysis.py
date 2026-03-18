import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests
import numpy as np

# Load datasets
gpt41_reply = pd.read_csv('results_gpt41mini.csv')
gemini25_reply = pd.read_csv('results_gemini25.csv')
resumes = pd.read_csv('resumes.csv')

# Construct accepted datasets
accepted_ids_gpt41 = gpt41_reply['resume_id'].unique()
accepted_ids_gemini25 = gemini25_reply['resume_id'].unique()

accepted_df_gpt41 = pd.DataFrame({
    'resume_id': accepted_ids_gpt41,
    'decision': 1
})

accepted_df_gemini25 = pd.DataFrame({
    'resume_id': accepted_ids_gemini25,
    'decision': 1
})

# Merge with resumes
merged_gpt41 = pd.merge(resumes, accepted_df_gpt41, on='resume_id', how='left')
merged_gpt41['decision'] = merged_gpt41['decision'].fillna(0).astype(int)

merged_gemini25 = pd.merge(resumes, accepted_df_gemini25, on='resume_id', how='left')
merged_gemini25['decision'] = merged_gemini25['decision'].fillna(0).astype(int)



# Summary by Race
def create_summary(df):
    summary = df.groupby('race').agg(
        total_resumes=('resume_id', 'count'),
        accepted=('decision', 'sum')
    )
    summary['rejected'] = summary['total_resumes'] - summary['accepted']
    summary['acceptance_rate'] = summary['accepted'] / summary['total_resumes']
    summary['rejection_rate'] = summary['rejected'] / summary['total_resumes']

    total_accepted = summary['accepted'].sum()
    total_rejected = summary['rejected'].sum()


    summary['%_of_accepted_pool'] = (
        summary['accepted'] / total_accepted if total_accepted > 0 else 0
    )
    summary['%_of_rejected_pool'] = (
        summary['rejected'] / total_rejected if total_rejected > 0 else 0
    )

    return summary


# Logistic Regression
model_41 = smf.logit(
    'decision ~ C(race, Treatment(reference="black")) * C(gender, Treatment(reference="male")) + C(job_title)',
    data=merged_gpt41
).fit(cov_type='HC3')


model_25 = smf.logit(
    'decision ~ C(race, Treatment(reference="black")) * C(gender, Treatment(reference="male")) + C(job_title)',
    data=merged_gemini25
).fit(cov_type='HC3')

# Adjust p-values for multiple comparisons
pvals = model_41.pvalues
adjusted = multipletests(pvals, method='fdr_bh')[1]

results_table_41 = model_41.summary2().tables[1]
results_table_41.to_csv("logit_results_gpt41.csv")

results_table_25 = model_25.summary2().tables[1]
results_table_25.to_csv("logit_results_gemini25.csv")

# Combine datasets for visualization
merged_gpt41['model'] = 'GPT-4.1'
merged_gemini25['model'] = 'Gemini 2.5'
combined = pd.concat([merged_gpt41, merged_gemini25])
race_map = {
    'asian': 'Asian',
    'black': 'Black',
    'white': 'White',
    'hispanic': 'Hispanic'
}
combined['race'] = combined['race'].map(race_map)

# Bar Chart for Acceptance Rates by Race
sns.barplot(
    data=combined,
    x='race',
    y='decision',
    hue='model'
)

plt.title('Acceptance Rate by Race')
plt.xlabel('Race')
plt.ylabel('Acceptance Rate')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Bias Chart
g = sns.catplot(
    data=combined,
    x='race',
    y='decision',
    hue='gender',
    col='model',
    kind='bar',
    palette='muted',
    height=5,
    aspect=1
)

g.set_axis_labels("Race", "Acceptance Rate")
g.set_titles("{col_name}")

for ax in g.axes.flat:
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

g._legend.set_title("Gender")
g.fig.suptitle("Acceptance Rate by Race and Gender", y=1.05)

plt.show()