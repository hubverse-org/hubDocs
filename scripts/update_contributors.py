import os
import requests

# Fetch the token from the environment variable
token = os.getenv("GITHUB_TOKEN")

if token is None:
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
    with open("docs/source/overview/contributors.md", "w") as file:
        file.write("# Contributors\n\n")
        for contributor in contributors:
            # Fetch detailed user info for the contributor
            user_response = requests.get(contributor['url'], headers=headers)
            if user_response.status_code == 200:
                user_data = user_response.json()
                name = user_data.get('name', contributor['login'])  # Use name if available, else login
            else:
                name = contributor['login']  # Fallback if user details fail
            
            file.write(
                f"- [{name} ({contributor['login']})]({contributor['html_url']})\n"
            )
    print("Contributors list updated successfully.")
else:
    print(f"Failed to fetch contributors: {response.status_code} - {response.json()}")
