import os
import requests
import random
from collections import defaultdict

# Fetch the token from the environment variable
token = os.getenv("GITHUB_TOKEN")
if not token:
    raise ValueError(
        "GITHUB_TOKEN is not set. Please ensure the environment variable is configured."
    )

# GitHub API base URL
base_url = "https://api.github.com"
org = "hubverse-org"
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {token}",
}

# Fetch all repositories in the organization
repos_url = f"{base_url}/orgs/{org}/repos"
repos_response = requests.get(repos_url, headers=headers)
if repos_response.status_code != 200:
    raise ValueError(
        f"Failed to fetch repositories: {repos_response.status_code} - {repos_response.json()}"
    )

repos = [repo["name"] for repo in repos_response.json()]

# Dictionary to store contributors and their repositories
contributors = defaultdict(set)

# Fetch contributors for each repository
for repo in repos:
    url = f"{base_url}/repos/{org}/{repo}/contributors"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        continue  # Skip if request fails

    for contributor in response.json():
        login = contributor["login"]
        contributors[login].add(repo)

# Shuffle contributors randomly
contributor_list = list(contributors.items())
random.shuffle(contributor_list)

# Fetch user details and generate output
output_dir = "docs/source/overview"
os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
output_file = f"{output_dir}/contributors.md"

with open(output_file, "w") as file:
    file.write(
        "# Contributors to hubverse repositories\n\nThese are the contributors to hubverse repositories in random order.\n\n"
    )

    last_index = len(contributor_list) - 1  # Get last index to avoid trailing '---'

    for i, (login, repo_set) in enumerate(contributor_list):
        user_response = requests.get(f"{base_url}/users/{login}", headers=headers)
        if user_response.status_code != 200:
            file.write(
                f"- ![Avatar](https://dummyimage.com/50x50/3c88be/3c88be) "
                f"- [{login}](https://github.com/{login}) - "
                f"Failed to fetch additional details. (Error {user_response.status_code})\n"
            )
            continue  # Skip if user data fetch fails

        user_data = user_response.json()
        name = (user_data.get("name", login) or "").strip()
        github_name = (user_data.get("login") or "").strip()
        blog = (user_data.get("blog") or "").strip()
        bio = " ".join(
            (user_data.get("bio") or "").split()
        )  # Remove extra spaces inside bio
        location = (user_data.get("location", "") or "").strip()
        avatar_url = user_data.get("avatar_url", "")
        profile_url = user_data.get("html_url", "")

        # Only include square brackets around name if `blog` is not empty
        name_output = f"[{name}]" if name and blog else name

        # Only include the blog link if it's not empty
        if blog and not blog.startswith(("http://", "https://")):
            # If blog doesn't start with http:// or https://, prepend https://
            blog = f"https://{blog}"
        blog_output = (
            f"({blog})" if blog else ""
        )  # Don't include parentheses if `blog` is empty

        # Avoid adding period if `bio` or `location` is empty
        bio_output = f" {bio}." if bio else ""
        location_output = f" {location}." if location else ""
        repo_text = ", ".join(repo_set)

        file.write(
            f'<img src="{avatar_url}" alt="" class="avatar"> '
            f"- {name_output}{blog_output} ([{github_name}]({profile_url}))."
            f"{bio_output}{location_output}\n\n"
            f"Repositories contributed to: {repo_text}.\n\n"
        )

        # Add '---' separator only if it's NOT the last contributor
        if i != last_index:
            file.write("---\n\n")

print("Contributors list updated successfully.")
