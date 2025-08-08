import requests
import csv
import pandas as pd
TOKEN = "squ_5d910e07d0110f860308776c294fc9e6dd85ca11"
BASE_URL = "http://localhost:9000/api/issues/search"


headers = {
    "Authorization": f"Bearer {TOKEN}"
}
repo_name=input("enter the repo for which u want to pull the bugs : ")
params = {
    "componentKeys": repo_name,
    "ps": 500,
    "resolved": "false"
}

response = requests.get(BASE_URL, headers=headers, params=params)

if response.status_code != 200:
    print(f"Error {response.status_code}")
    print(response.text[:300])
    exit(1)

data = response.json()
issues = data.get("issues", [])

# Extract only rule and component
results = [{"rule": issue["rule"], "file_name": issue["component"].split(":")[-1]} for issue in issues]

# Save to CSV
with open("unresolved_issues.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["rule", "file_name"])
    writer.writeheader()
    writer.writerows(results)

print(f"Saved {len(results)} unresolved issues to 'unresolved_issues.csv'")
import pandas as pd

# Load the CSV files
df1 = pd.read_csv('all_sonarqube_rules.csv')
df2 = pd.read_csv('unresolved_issues.csv')
print("df1:", df1.columns)
print("df2:", df2.columns)
merged_df = pd.merge(df1, df2, left_on='key', right_on='rule', how='inner')
merged_df.drop(columns=['key', 'rule'], inplace=True)
merged_df = merged_df.rename(columns={
    'repo': 'code_language',
    'file_name': 'file_name',
    'name': 'bug_description'
})[['code_language', 'file_name', 'bug_description']]
merged_df = merged_df.drop_duplicates()
merged_df.to_csv('./bug_fixes.csv', index=False)
print("Merge completed. Saved to bug_fixes.csv")