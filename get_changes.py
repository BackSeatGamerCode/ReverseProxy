import urllib.request
import json

OWNER = "BackSeatGamerCode"
REPO = "ReverseProxy"

print("Pulling latest release tag...")
response = urllib.request.urlopen("https://api.github.com/repos/{}/{}/releases/latest".format(OWNER, REPO))
tag_name = json.loads(response.read().decode("utf8"))["tag_name"]

print("Latest release tag is {}".format(tag_name))

print("Fetching commits since tag... {}".format(tag_name))

response = urllib.request.urlopen(
    "https://api.github.com/repos/{}/{}/compare/{}...main".format(OWNER, REPO, tag_name)
)
commits = json.loads(response.read().decode("utf8"))["commits"]

print("\nCommit messages since last tag:")
for commit in commits:
    commit = commit["commit"]
    print(commit["message"])
