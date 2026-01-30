import pandas as pd

data = pd.read_csv("llm_reply.csv")
total = data["decision"].value_counts()
total_percent = data["decision"].value_counts(normalize=True) * 100


race_decision_counts = (
    data.groupby(["name_origin_category", "decision"])
      .size()
      .unstack(fill_value=0)
)

race_decision_percent = (
    race_decision_counts
    .div(race_decision_counts.sum(axis=1), axis=0)
    * 100
)

accepted_race_percent = (
    data[data["decision"] == "accept"]["name_origin_category"]
    .value_counts(normalize=True)
    * 100
)

rejected_race_percent = (
    data[data["decision"] == "reject"]["name_origin_category"]
    .value_counts(normalize=True)
    * 100
)


print("total_percent:", total_percent)
print("race_decision_counts:", race_decision_counts)
print("race_decision_percent:", race_decision_percent)
print("accepted_race_percent:", accepted_race_percent)
print("rejected_race_percent:", rejected_race_percent)