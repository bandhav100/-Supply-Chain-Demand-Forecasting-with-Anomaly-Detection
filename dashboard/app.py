import streamlit as st
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(
    page_title="GitHub Developer Trend Analytics",
    layout="wide"
)

# ---------------------------------
# DATABASE CONNECTION
# ---------------------------------
conn = psycopg2.connect(
    database="github_trends",
    user="postgres",
    password="bandhav1",  # nee actual password
    host="localhost",
    port="5432"
)

# ---------------------------------
# LOAD DATA
# ---------------------------------
query = """
SELECT
    repo_name,
    owner,
    language,
    stars,
    forks,
    watchers,
    created_at,
    updated_at
FROM repositories
"""

df = pd.read_sql(query, conn)

# ---------------------------------
# TITLE
# ---------------------------------
st.title("GitHub Developer Trend Analytics Dashboard")
st.markdown("---")

# ---------------------------------
# KPI CARDS
# ---------------------------------
total_repos = len(df)
total_stars = int(df["stars"].sum())
total_languages = df["language"].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("Repositories", total_repos)
col2.metric("Total Stars", f"{total_stars:,}")
col3.metric("Languages", total_languages)

st.markdown("---")

# ---------------------------------
# SIDEBAR FILTER
# ---------------------------------
st.sidebar.header("Filters")

languages = sorted(
    [lang for lang in df["language"].dropna().unique()]
)

selected_language = st.sidebar.selectbox(
    "Select Language",
    ["All"] + languages
)

filtered_df = df.copy()

if selected_language != "All":
    filtered_df = filtered_df[
        filtered_df["language"] == selected_language
    ]

# ---------------------------------
# SEARCH
# ---------------------------------
search = st.text_input("Search Repository")

if search:
    filtered_df = filtered_df[
        filtered_df["repo_name"]
        .str.contains(search, case=False, na=False)
    ]

# ---------------------------------
# TOP REPOSITORIES
# ---------------------------------
st.subheader("Top Repositories")

top_repos = filtered_df.sort_values(
    by="stars",
    ascending=False
)

st.dataframe(
    top_repos[
        [
            "repo_name",
            "language",
            "stars",
            "forks",
            "watchers"
        ]
    ],
    use_container_width=True
)

# ---------------------------------
# LANGUAGE POPULARITY
# ---------------------------------
st.subheader("Language Popularity")

language_df = (
    filtered_df
    .groupby("language")
    .size()
    .reset_index(name="repo_count")
    .sort_values(
        by="repo_count",
        ascending=False
    )
)

st.bar_chart(
    language_df.set_index("language")
)

# ---------------------------------
# TOP STARRED REPOSITORIES
# ---------------------------------
st.subheader("Top Starred Repositories")

chart_df = (
    filtered_df
    .sort_values(
        by="stars",
        ascending=False
    )
    .head(10)
)

st.bar_chart(
    chart_df.set_index("repo_name")["stars"]
)

# ---------------------------------
# LANGUAGE DISTRIBUTION
# ---------------------------------
st.subheader("Language Distribution")

fig, ax = plt.subplots()

ax.pie(
    language_df["repo_count"],
    labels=language_df["language"],
    autopct="%1.1f%%"
)

st.pyplot(fig)

# ---------------------------------
# REPOSITORY DETAILS
# ---------------------------------
st.subheader("Repository Details")

selected_repo = st.selectbox(
    "Choose Repository",
    filtered_df["repo_name"]
)

repo_info = filtered_df[
    filtered_df["repo_name"] == selected_repo
].iloc[0]

st.write(f"Owner: {repo_info['owner']}")
st.write(f"Language: {repo_info['language']}")
st.write(f"Stars: {repo_info['stars']:,}")
st.write(f"Forks: {repo_info['forks']:,}")
st.write(f"Watchers: {repo_info['watchers']:,}")
st.write(f"Created: {repo_info['created_at']}")
st.write(f"Updated: {repo_info['updated_at']}")

# ---------------------------------
# INSIGHTS
# ---------------------------------
st.subheader("Key Insights")

if len(language_df) > 0:
    top_language = language_df.iloc[0]["language"]
    st.success(f"Most Popular Language: {top_language}")

if len(top_repos) > 0:
    top_repo = top_repos.iloc[0]["repo_name"]
    st.info(f"Highest Starred Repository: {top_repo}")

# ---------------------------------
# CLOSE CONNECTION
# ---------------------------------
conn.close()
