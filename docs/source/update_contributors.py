import requests

# GitHub API URL for contributors
url = "https://api.github.com/repos/hubverse-org/hubDocs/contributors"
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": "Bearer YOUR_PERSONAL_ACCESS_TOKEN"  # Optional if repo is public
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    contributors = response.json()
    with open("contributors.md", "w") as file:
        file.write("# Contributors\n\n")
        for contributor in contributors:
            file.write(
                f"- [{contributor['login']}]({contributor['html_url']})\n"
            )
else:
    print(f"Failed to fetch contributors: {response.status_code}")
