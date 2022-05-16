from asyncio.windows_events import NULL
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

""" check_query = "SELECT * FROM timeline1"
update_commit_query = "update timeline1 set commitid=%s, date=%s where issueid = %s"
update_issue_query = "update timeline1 set title=%s where issueid=%s"
insert_query = "insert into timeline1(issueid, commitid, commitdate, title) values(%s,%s,%s,%s)"

commit_query = "SELECT issue, commitid, date from commit1 order by issue, date"
issue_query = "SELECT issueid, title from issue1 order by issueid" """

join_query = "select i.issueid, c.commitid, c.date, i.title from issue1 i inner join commit1 c on i.issueid = c.issue order by i.issueid, c.date;"
insert_query = "insert into timeline1(issueid, commitid, commitdate, title) value(%s, %s, %s, %s)"

def insert_timeline():
    """ cursor.execute(commit_query)
    commit_record = cursor.fetchall()
    for r in commit_record:
        try:
            issue = r[0]
            commit_id = r[1]
            commit_date = r[2]
            data = [issue, commit_id, commit_date, NULL]

            cursor.execute(insert_query, data)
            print("Row inserted {}".format(cursor.rowcount))
            db.commit()
        except Exception as e:
            print(e)

    cursor.execute(issue_query)
    issue_record = cursor.fetchall()
    for r1 in issue_record:
        try:
            issue_id = r1[0]
            issue_title = r1[1]
            cursor.execute(update_issue_query, (issue_title, issue_id))
            print("Row updated {} for {}".format(cursor.rowcount, issue_id))
            db.commit()
            
        except Exception as e:
            print(e)

    db.close()
    cursor.close() """

    cursor.execute(join_query)
    commit_record = cursor.fetchall()
    for r in commit_record:
        try:
            issue = r[0]
            commit_id = r[1]
            commit_date = r[2]
            issue_title = r[3]
            data = [issue, commit_id, commit_date, issue_title]
            cursor.execute(insert_query, data)
            print("Row inserted {}".format(cursor.rowcount))
            db.commit()

        except Exception as e:
            print(e)
    db.close()
    cursor.close() 
if __name__ == "__main__":
    insert_timeline()