import os
from github import Github
from dotenv import load_dotenv

load_dotenv()

def get_pr_diff(pr_url):
    parts = pr_url.strip("/").split("/")
    owner = parts[-4]
    repo = parts[-3]
    pr_number = int(parts[-1])

    g = Github(os.getenv("GITHUB_TOKEN"))
    repository = g.get_repo(f"{owner}/{repo}")
    pr = repository.get_pull(pr_number)

    diff_text = ""
    for f in pr.get_files():
        diff_text += f"\n--- {f.filename} ---\n"
        diff_text += f.patch if f.patch else "(no diff available)"
    return diff_text

if __name__== "__main__":
    url = input("Paste a GitHub PR URL: ")
    diff = get_pr_diff(url)
    print(diff)

    