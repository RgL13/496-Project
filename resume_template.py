import pandas as pd

names = pd.read_csv("names.csv")

names["full_name"] = names["first_name"] + " " + names["last_name"]

for name in names["full_name"]:
    resume = f"""
    Name: {name}
    Education: BS in Statistics
    Experience: Data Analyst Intern
    GPA: 3.8
    """
    
    print(resume)


