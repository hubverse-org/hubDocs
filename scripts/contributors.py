import os
import requests
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

# Dictionary to store contributor commit counts
contributors = defaultdict(lambda: defaultdict(int))

# Dictionary to store contributor commit counts and last contribution date
contributors = defaultdict(lambda: {"repos": defaultdict(int), "last_commit": None})

# Fetch contributors for each repository
for repo in repos:
    url = f"{base_url}/repos/{org}/{repo}/contributors"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        for contributor in response.json():
            login = contributor["login"]
            contributors[login]["repos"][repo] += contributor["contributions"]

            # Fetch last commit date
            commits_url = (
                f"{base_url}/repos/{org}/{repo}/commits?author={login}&per_page=1"
            )
            commit_response = requests.get(commits_url, headers=headers)
            if commit_response.status_code == 200 and commit_response.json():
                last_commit_date = commit_response.json()[0]["commit"]["committer"][
                    "date"
                ]
                if (
                    not contributors[login]["last_commit"]
                    or last_commit_date > contributors[login]["last_commit"]
                ):
                    contributors[login]["last_commit"] = last_commit_date

# Sort contributors by total number of commits in descending order
sorted_contributors = sorted(
    contributors.items(), key=lambda x: sum(x[1]["repos"].values()), reverse=True
)

# Fetch user details and generate output
output_dir = "docs/source/overview"
os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
output_file = f"{output_dir}/contributors.md"

with open(output_file, "w") as file:
    file.write("# Contributors to hubverse GitHub repositories\n\n")
    for login, data in sorted_contributors:
        repo_commits = data["repos"]
        total_commits = sum(repo_commits.values())
        user_response = requests.get(f"{base_url}/users/{login}", headers=headers)
        if user_response.status_code == 200:
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
            last_commit = data["last_commit"]

            # Only include square brackets around name if `blog` is not empty
            if name:
                if blog:
                    name_output = f"[{name}]"
                else:
                    name_output = name  # No square brackets if `blog` is empty
            else:
                name_output = name  # Leave it as empty if `name` is blank

            # Only include the blog link if it's not empty
            if blog:
                # If blog doesn't start with http:// or https://, prepend https://
                if not blog.startswith(("http://", "https://")):
                    blog = f"https://{blog}"
                blog_output = f"({blog})"
            else:
                blog_output = ""  # Don't include parentheses if `blog` is empty

            # Avoid adding period if `bio` or `location` is empty
            bio_output = f" {bio}." if bio else ""
            location_output = f" {location}." if location else ""

            repo_commit_text = ", ".join(
                [f"{repo}: {count} commits" for repo, count in repo_commits.items()]
            )

            # Write to the file with conditional formatting
            file.write(
                f'<img src="{avatar_url}" alt="" class="avatar"> '
                f"- {name_output}{blog_output} ([{github_name}]({profile_url}))."
                f"{bio_output}{location_output}"
                f"\n\nTotal hubverse GitHub commits: {total_commits}."
                f"\n\n Last commit: {last_commit}."
                f"\n\n{repo_commit_text}.\n\n---\n\n"
            )

        else:
            file.write(
                f"- ![Avatar](https://dummyimage.com/50x50/3c88be/3c88be) "
                f"- [{contributor['login']}]({contributor['html_url']}) - "
                f"Failed to fetch additional details. (Error {user_response.status_code})\n"
            )

print("Contributors list updated successfully.")
