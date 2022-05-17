from github import Github
import mysql.connector
import re
import csv
import sys
import os
from os import path
import shutil
from dotenv import load_dotenv
from textblob import TextBlob
import text2emotion as t
from ast import literal_eval
import pdb
#pdb.set_trace()
load_dotenv()
username = os.getenv("user")
password = os.getenv("password")
database = os.getenv("database")
db = mysql.connector.connect(host="localhost",user=username, password=password, database=database)
cursor = db.cursor(buffered=True)

date_fmt = "%m/%d/%Y"
check_query = "SECECT * FROM timeline WHERE repo_name = %s and issueid = %s and commitid = %s"
insert_query = "INSERT INTO timeline(repo_name, issueid, title, startdate, enddate, days_needed, commitid, commit_comments, commit_date) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"

join_query = "SELECT DISTINCT i.repo_name, i.issueid, i.title, i.startdate, i.enddate, i.days_needed, c.commitid, c.comments, c.date FROM issue i inner join commit c on (i.issueid = c.issue and i.repo_name = c.repo) ORDER BY i.repo_name, i.issueid"

def insert_timeline():
    """ 
    This function join issue and commit tables based on issueid and repo.
    Later on it save to timeline table.
    """

    cursor.execute(join_query)
    timeline_record = cursor.fetchall()
    for r in timeline_record:
        try:
            repo_name = r[0]
            issue_id = r[1]
            issue_title = r[2]
            startdate = r[3]
            enddate = r[4]
            days_needed = r[5]
            commit_id = r[6]
            commit_comments = r[7]
            commit_date = r[8]
            data = [repo_name, issue_id, issue_title, startdate, enddate, days_needed, commit_id, commit_comments, commit_date]
            cursor.execute(check_query, (repo_name, issue_id, commit_id))
            if( cursor.rowcount > 0 ):
                print("Issue already have this commit timeline")
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
    insert_timeline()