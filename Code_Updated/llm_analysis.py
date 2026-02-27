import pandas as pd
import matplotlib.pyplot as plt

llm_reply = pd.read_csv('llm_reply.csv')
resumes = pd.read_csv('resumes.csv')

accepted_ids = llm_reply['resume_id'].unique()
accepted_df = pd.DataFrame({'resume_id': accepted_ids, 'decision': 1})

# Merge
merged = pd.merge(resumes, accepted_df, on='resume_id', how='left')
merged['decision'] = merged['decision'].fillna(0).astype(int)

# Calculate acceptance/rejection rates by race
summary = merged.groupby('race').agg(
    total_resumes=('resume_id', 'count'),
    accepted=('decision', 'sum')
)

summary['rejected'] = summary['total_resumes'] - summary['accepted']
summary['acceptance_rate'] = summary['accepted'] / summary['total_resumes']
summary['rejection_rate'] = summary['rejected'] / summary['total_resumes']

# Race percentage within accepted and rejected groups
total_accepted = summary['accepted'].sum()
total_rejected = summary['rejected'].sum()

summary['%_of_accepted_pool'] = summary['accepted'] / total_accepted
summary['%_of_rejected_pool'] = summary['rejected'] / total_rejected

print(summary)

# Acceptance Rate by Race
plt.figure()
plt.bar(summary.index, summary['acceptance_rate'], color='skyblue')
plt.title('Acceptance Rate by Race')
plt.xlabel('Race')
plt.ylabel('Acceptance Rate')
plt.xticks(rotation=45)
plt.show()

# Accepted Pool
plt.figure()
plt.bar(summary.index, summary['%_of_accepted_pool'], color='lightgreen')
plt.title('Race Percentages in Accepted Pool')
plt.xlabel('Race')
plt.ylabel('Percentage of Accepted Pool')
plt.xticks(rotation=45)
plt.show()

# Rejected Pool
plt.figure()
plt.bar(summary.index, summary['%_of_rejected_pool'], color='orange')
plt.title('Race Percentages in Rejected Pool')
plt.xlabel('Race')
plt.ylabel('Percentage of Rejected Pool')
plt.xticks(rotation=45)
plt.show()
