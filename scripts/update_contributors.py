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
                bio = " ".join(bio.split())  # Remove extra spaces inside bio
                location = (user_data.get('location', '') or "").strip()
                commit_count = contributor.get('contributions', 0)
                
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
                    if not blog.startswith(('http://', 'https://')):
                        blog = f"https://{blog}"
                    blog_output = f"({blog})"
                else:
                    blog_output = ""  # Don't include parentheses if `blog` is empty

                # Avoid adding period if `bio` or `location` is empty
                bio_output = f"{bio}." if bio else ""
                location_output = f" {location}." if location else ""
                
                # Write to the file with conditional formatting
                file.write(
                    f"- {name_output}{blog_output} ([{contributor['login']}]({contributor['html_url']})) - "
                    f"{bio_output}{location_output} {commit_count} commits.\n"
                )
            else:
                file.write(
                    f"- [{contributor['login']}]({contributor['html_url']}) - "
                    f"Failed to fetch additional details. (Error {user_response.status_code})\n"
                )
    print("Contributors list updated successfully.")
else:
    print(f"Failed to fetch contributors: {response.status_code} - {response.json()}")
