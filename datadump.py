from github import Github
import csv
import mysql.connector
from dotenv import load_dotenv
import os
from collections import defaultdict
from typing import Dict
import datetime as dt
import pdb
#pdb.set_trace()
import argparse
load_dotenv()
username = os.getenv("user")
password = os.getenv("password")
database = os.getenv("database")
token = os.getenv("token")
print(database)
db = mysql.connector.connect(host="localhost",user=username, password=password, database=database)
cursor = db.cursor(buffered=True)
def insert_data(**data):
    """ This function inserts data sent by fetch_gitIssues function into a MYSQL table
        #Input: 
            #argument1: keyword argument dictionary of named arguments
    """
    query = ""
    check_query = ""
    update_query = ""
    for k, v in data.items():
        if k == "table" and v == "issue_comment":
            query = "INSERT INTO issue_comment(COMMENTID,COMMENT,USER,REACTIONS)" \
                    "VALUES(%s,%s,%s,%s)"
            continue
        elif k == "table" and v == "issue":
            query = "INSERT INTO issue(ISSUEID,REPO_NAME,COMMENTID,TITLE,STARTDATE,ENDDATE," \
                    "DAYS_NEEDED,ISSUETYPE,ASSIGNEE)" \
                    "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            continue
        elif k == "table" and v == "contribution":
             query = "INSERT INTO contribution(DEVELOPER,ISSUE_COUNT,REPO_NAME) VALUES(%s,%s,%s)"
             check_query = "select * from contribution where developer=%s  and repo_name=%s"
             continue
    vals = data.values()
    vals = list(vals)[1:]
    vals = tuple(vals)
    chk_vals = (tuple(vals)[0],tuple(vals)[2])
    upd_vals = (tuple(vals)[1],tuple(vals)[0],tuple(vals)[2])
    if check_query:
       cursor.execute(check_query,chk_vals)
       if cursor.rowcount > 0:
          row = cursor.fetchone()
          if row[1] == tuple(vals)[1]:
             print("Contribution Record already exists")
             pass
          else:
               update_query = "update contribution set issue_count=%s where developer=%s and repo_name=%s"
               cursor.execute(update_query,upd_vals)
               db.commit()
       else:
            try:
                cursor.execute(query, vals)
                print("{} record(s) inserted".format(cursor.rowcount))
                db.commit()
            except Exception as e:
                   print(e)
                   pass

             
    else:
         try:
             cursor.execute(query, vals)
             print("{} record(s) inserted".format(cursor.rowcount))
             db.commit()
         except Exception as e:
                print(e)
                pass
    


def fetch_gitdetails(org_repo):
    """ This function calls GitHub API to fetch closed issues from a GitHub Repository and extract details from them. Further it calls
    the database insertion function too
    #Input:
     argument 1: org_repo or repository name (str)
    """
    g_repo = Github(login_or_token=token).get_repo(org_repo)
    assignee = ''
    reactions = []
    label = []
    resource_utilized = 0
    issue_user: Dict[str, int] = defaultdict(int)
    try:
        for issue in g_repo.get_issues(state="closed"):
            number = issue.number
            if issue.closed_at and issue.user.name:
               issue_user[issue.user.name] += 1

            if issue.assignee:
               assignee = issue.assignee.name
            comments_no = issue.comments
            start_date = issue.created_at
            end_date = issue.closed_at
            interval = end_date - start_date
            days , seconds = interval.days , interval.seconds
            hours = days * 24 + seconds // 3600
            label = ''.join([str(l.name) for l in issue.get_labels()])


            if comments_no > 0 and number == issue.number:
               for comment in issue.get_comments():
                   commenter = comment.user.name
                   if commenter == assignee:
                      commenter = assignee
                   if comment.get_reactions().totalCount > 0:
                      reactions = ''.join([str(c.content) for c in comment.get_reactions()])
                      insert_data(table="issue", issueid=number,repo=org_repo,commentid=comment.id,\
                                  title=issue.title, start_date=start_date, end_date=end_date,\
                                  days_needed=hours,issuetype=label, assignee=assignee)
                      insert_data(table="issue_comment", commentid=comment.id,\
                                  comment=comment.body, user=commenter, reactions=reactions)
                   else:
                           insert_data(table="issue", issueid=number,repo=org_repo,commentid=comment.id,\
                                       title=issue.title, start_date=start_date, end_date=end_date,\
                                       days_needed=hours, issuetype=label, assignee=assignee)
                           insert_data(table="issue_comment", commentid=comment.id,\
                                    comment=comment.body, user=commenter, reactions=0)

    finally:
            issue_stat_user = {k: v for k, v in sorted(issue_user.items(), key=lambda item: item[1])}
            if issue_stat_user:
               for key,value in issue_stat_user.items():
                   insert_data(table="contribution", developer=key,\
                            issues_resolved=value, repo=org_repo)
            else:
                 print("No data for issue contribution")


if __name__ == "__main__":
    # fetch_gitDetails()
    # db.close()
    parser = argparse.ArgumentParser()
    parser.add_argument("-r","--repo",help="Pass the Opensource repository name with path e.g.; apache/maven")
    args = parser.parse_args()
    if args.repo:
       fetch_gitDetails(args.repo)
    db.close()
    cursor.close()
