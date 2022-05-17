from asyncio.windows_events import NULL
from github import Github
import mysql.connector
import re
#import pdb
#import sys
#import os
from os import path
#import shutil
from dotenv import load_dotenv
load_dotenv()
username = "root"
password = "Saigon12345"
database = "intemodb"
token = "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"
url = "https://github.com/ChuDucAnh2402/hello-world.git"
db = mysql.connector.connect(host="localhost", user=username, password=password, database=database)
cursor = db.cursor(buffered=True)
commit_author = ""
date_fmt = "%m/%d/%Y"

check_query = "SELECT * FROM commit1 WHERE commitid = %s"
update_query = "UPDATE commit1 SET author=%s, no_line_changes= %s WHERE commitid = %s"
insert_query = "INSERT INTO commit1(commitid,comments,author,date,no_line_changes,issue,repo) values(%s,%s,%s,%s,%s,%s,%s)"

def insert_gitcommits(repo):
    """
    This function takes the repository name as an argument then connects to it. Later, it fetches all the commits(successful ones)
    and stores it in Commit table.
    #Input:
      argument1: repo (str)
    """
    g = Github(login_or_token=token)
    g_repo = g.get_user().get_repo(repo)
    for commit in g_repo.get_commits():
        sum_commit =0
        commit_comments = commit.commit.message
        if commit.author:
            if commit.committer and commit.author.name == commit.committer.name:
                commit_author = commit.committer.name
            elif commit.committer and commit.author.email == commit.committer.email:
                commit_author = commit.committer.email
            else:
                commit_author = commit.author.name
        commit_date = commit.last_modified.format()
        commit_files = str([f.filename for f in commit.files])
        commit_changes = [l.changes for l in commit.files]
        for ch in commit_changes:
            sum_commit += ch
        commit_id = commit.sha
        
        try:
            if commit_comments:
                print(commit_comments)
                first_index = re.search("\(#[0-9]+\)",commit_comments).start()
                last_index = re.search("\(#[0-9]+\)",commit_comments).end()
                issue = commit_comments[first_index+2:last_index-1]
            print("Commit {} has comments {} by {} on {} with files {} for issue {} with {} changes".format(
                                        commit_id, commit_comments, commit_author, commit_date, commit_files, issue, sum_commit))
            data = (commit_id, commit_comments, commit_author, commit_date, sum_commit, issue, repo)
            cursor.execute(check_query, (commit_id,))
            if cursor.rowcount> 0:
                cursor.execute(update_query, (commit_author, sum_commit, commit_id))
                print("Rows updated {} for {}".format(cursor.rowcount, commit_id))
                db.commit()
            else:
                cursor.execute(insert_query, data)
                print("Row inserted {}".format(cursor.rowcount))
                db.commit()
        except Exception as e:
            print(e)
            continue
    db.close()
    cursor.close()    

if __name__ == "__main__":
    insert_gitcommits("hello-world")