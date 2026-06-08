import requests
import psycopg2

conn = psycopg2.connect(
    database="github_trends",
    user="postgres",
    password="bandhav1",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

url = "https://api.github.com/search/repositories"

params = {
    "q": "stars:>10000",
    "sort": "stars",
    "order": "desc",
    "per_page": 20
}

response = requests.get(url, params=params)
data = response.json()

for repo in data["items"]:

    repo_name = repo["name"]
    owner = repo["owner"]["login"]
    language = repo["language"]
    stars = repo["stargazers_count"]
    forks = repo["forks_count"]
    watchers = repo["watchers_count"]
    created_at = repo["created_at"][:10]
    updated_at = repo["updated_at"][:10]

    cursor.execute("""
        INSERT INTO repositories
        (repo_name, owner, language, stars, forks, watchers, created_at, updated_at)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        repo_name,
        owner,
        language,
        stars,
        forks,
        watchers,
        created_at,
        updated_at
    ))

conn.commit()

print("Data Inserted Successfully!")

cursor.close()
conn.close()
