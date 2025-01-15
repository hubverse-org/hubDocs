import os
import requests

# Fetch the token from the environment variable
token = os.getenv("GITHUB_TOKEN")

if not token:
    raise ValueError("GITHUB_TOKEN is not set. Please ensure the environment variable is configured.")

# GitHub API URL for contributors
url = "https://api.github.com/repos/hubverse-org/hubDocs/contributors"
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {token}"  # Optional if repo is public
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    contributors = response.json()
    output_dir = "docs/source/overview"
    output_file = f"{output_dir}/contributors.md"
    
    # Ensure the directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    with open(output_file, "w") as file:
        file.write("# Contributors\n\n")
        for contributor in contributors:
            user_response = requests.get(contributor['url'], headers=headers)
            if user_response.status_code == 200:
                user_data = user_response.json()
                name = (user_data.get('name', contributor['login']) or "").strip()
                blog = (user_data.get('blog') or "").strip()
                bio = (user_data.get('bio') or "").strip()
                location = (user_data.get('location', '') or "").strip()
                commit_count = contributor.get('contributions', 0)
                
                file.write(
                    f"- [{name}]({blog}) ([{contributor['login']}]({contributor['html_url']})) - "
                    f"{bio}. {location}. {commit_count} commits.\n"
                )
            else:
                file.write(
                    f"- [{contributor['login']}]({contributor['html_url']}) - "
                    f"Failed to fetch additional details. (Error {user_response.status_code})\n"
                )
    print("Contributors list updated successfully.")
else:
    print(f"Failed to fetch contributors: {response.status_code} - {response.json()}")
