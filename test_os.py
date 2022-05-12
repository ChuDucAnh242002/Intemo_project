import os
import sys
from dotenv import load_dotenv
from github import Github
load_dotenv()

token = "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"
url = "https://github.com/ChuDucAnh2402/hello-world.git"

def insert_gitcommits():
    g = Github(login_or_token=token)
    g_repo = g.get_user().get_repo("hello-world")
    for commit in g_repo.get_commits():
        commit_comments = commit.commit.message
        print(commit_comments)

if __name__ == "__main__":
    insert_gitcommits()