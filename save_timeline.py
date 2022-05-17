from github import Github
import mysql.connector
import re
import csv
import sys
import os
from os import path
import shutil
from dotenv import load_dotenv
#from textblob import TextBlob
#import text2emotion as t
#from ast import literal_eval
#import pdb
#pdb.set_trace()
load_dotenv()
username = os.getenv("user")
password = os.getenv("password")
database = os.getenv("database")
db = mysql.connector.connect(host="localhost",user=username, password=password, database=database)
cursor = db.cursor(buffered=True)

date_fmt = "%m/%d/%Y"
source_file = "timeline.csv"
destination = "/group1/"
query = "select * from timeline"

def save_timeline():
    """ 
        Import the timeline from database to the timeline.csv file
    """

    f = open("/home/xvnisa/timeline.csv","w",encoding="utf-8",newline='')
    timeline_header = ['repo_name', 'issue#', 'title', 'startdate', 'enddate', 'days_needed', 'commit_id', 'commit_comments','commit_date']
    writer = csv.writer(f)
    writer.writerrow(timeline_header)
    cursor.execute(query)
    record = cursor.fetchall()
    for r in record:
        try:
            data = [r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8]]
            writer.writerow(data)
        except Exception as e:
            print(e)
            continue

if __name__ == "__main__":
    save_timeline()
    dest_path = destination + source_file
    if(path.exists(dest_path)):
        os.remove(dest_path)
        dest_path = shutil.move(source_file, destination)
        print("File {} is moved to {}".format(source_file,dest_path))

    else:
        dest_path = shutil.move(source_file,destination)
        print("File {} is moved to {}".format(source_file,dest_path))