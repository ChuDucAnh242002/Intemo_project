from github import Github
import mysql.connector

import sys
import os
from os import path

from dotenv import load_dotenv
load_dotenv()
username = "root"
password = "Saigon12345"
database = "intemodb"
token = "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"
url = "https://github.com/ChuDucAnh2402/hello-world.git"
db = mysql.connector.connect(host="localhost", user=username, password=password, database=database)
cursor = db.cursor(buffered=True)

check_query = ""
insert_query = ""

def insert_gitcommits(repo):
    """
    This function takes the repository name as an argument then connects to it. Later, it fetches all the commits(successful ones)
    and stores it in Commit table.
    #Input:
      argument1: repo (str)
    """
    g = Github(login_or_token= token)
    g_repo = g.get_user().get_repo(repo)
    for commit in g_repo.get_commits():
        commit_comments = commit.commit.message
        try:
            print("Commit has commet: {}".format(commit_comments))
        except Exception as e:
            print(e)
            continue
    


if __name__ == "__main__":
    insert_gitcommits("hello-world")