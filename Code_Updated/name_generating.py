import pandas as pd
import itertools

name_pool = {
    "white": {
        "male": ["John", "James", "Michael", "Matthew"],
        "female": ["Emily", "Mary", "Jennifer", "Lisa"],
        "last": ["Anderson", "Thompson", "Smith", "Wilson"]
    },
    "black": {
        "male": ["King", "Malik", "Levi", "Jayden"],
        "female": ["Naya", "Nova", "Maya", "Naomi"],
        "last": ["Washington", "Jefferson", "Jackson", "Robinson"]
    },
    "asian": {
        "male": ["Wei", "Jin", "Hiroshi", "Min"],
        "female": ["Yuna", "Mei", "Soo", "Aiko"],
        "last": ["Zhang", "Kim", "Wang", "Lee"]
    },
    "hispanic": {
        "male": ["Carlos", "Luis", "Benjamin", "Sebastian"],
        "female": ["Maria", "Sofia", "Isabella", "Lucia"],
        "last": ["Garcia", "Martinez", "Lopez", "Rodriguez"]
    }
}


def generate_balanced_names(n_per_group=5):
    data = []
    
    for race in name_pool:
        for gender in ["male", "female"]:
            
            combinations = list(itertools.product(
                name_pool[race][gender],
                name_pool[race]["last"]
            ))
            
            selected = combinations[:n_per_group]
            
            for first, last in selected:
                data.append({
                    "first_name": first,
                    "last_name": last,
                    "full_name": f"{first} {last}",
                    "race": race,
                    "gender": gender
                })
    
    return pd.DataFrame(data)


names_df = generate_balanced_names(n_per_group=5)

names_df.to_csv("names.csv", index=False)

# print(len(names_df))  
