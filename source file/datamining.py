from time import sleep
from github import Github
import csv
# import pdb
# pdb.set_trace()

token = "XXXXXXXXX"
# repo = "https://github.com/apache/trafficcontrol"
# url = f"https://api.github.com/repos/apache/{repo}/issues"
org_repo = "apache/airflow"



def print_gitIssues():
    g_repo = Github(login_or_token="", password="").get_repo(org_repo)
    assignee = ''
    contributed = 'N'
    label = 'Yes'
    fp = open("/home/xvnisa/airflow_data.csv", "w", encoding="utf-8")
    git_header = ['id','label', 'text']
    writer = csv.writer(fp,delimiter=';')
    writer.writerow(git_header)
    for issue in g_repo.get_issues(state="closed"):
        number = issue.number
        if issue.assignee:
            assignee = issue.assignee.name
        comments_no = issue.comments
        start_date = issue.created_at
        end_date = issue.closed_at
        interval = end_date - start_date

        if comments_no > 0 and number == issue.number:
            for comment in issue.get_comments():
                commenter = comment.user.name
                if commenter == assignee or str(comment).find(assignee) >= 0:
                    contributed = 'Y'
                    data = [number,label,comment.title, comment.id,comment.body, comment.user.name, start_date,end_date,interval,assignee]
                    writer.writerow(data)
                    #print(
                    #"Issue Number {}, Label{} , Title{},CommentID {} , Issue Comments {},  User {}, "
                    #"StartDate {}, EndDate {}, Days spent {} AssignedTo {} Contributor_Status {}".format(
                     #   number,label, comment.title, comment.id, comment.body, commenter, start_date, end_date,
                      #  interval, assignee, contributed))
                    #sleep(20)


if __name__ == "__main__":
    print_gitIssues()

