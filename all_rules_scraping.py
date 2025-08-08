import requests
import csv

# Replace with your actual SonarQube token
TOKEN = "squ_5d910e07d0110f860308776c294fc9e6dd85ca11"
BASE_URL = "http://localhost:9000/api/rules/search"
PAGE_SIZE = 500

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

all_rules = []
page = 1

while True:
    print(f" Fetching page {page}...")
    response = requests.get(BASE_URL, headers=headers, params={"p": page, "ps": PAGE_SIZE})

    if response.status_code != 200:
        print(f" Error {response.status_code}: {response.text[:300]}")
        break

    data = response.json()
    rules = data.get("rules", [])
    total = data.get("total", 0)

    if not rules:
        break

    for rule in rules:
        all_rules.append({
            "key": rule.get("key"),
            "repo": rule.get("repo"),
            "name": rule.get("name")
        })

    if page * PAGE_SIZE >= total:
        break

    page += 1

with open("all_sonarqube_rules.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["key", "repo", "name"])
    writer.writeheader()
    writer.writerows(all_rules)

print(f"\n Saved {len(all_rules)} rules to 'all_sonarqube_rules.csv'")
