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

load_dotenv()
username = "root"
password = "Saigon12345"
database = "intemodb"
token = "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"
url = "https://github.com/ChuDucAnh2402/hello-world.git"
db = mysql.connector.connect(host="localhost", user=username, password=password, database=database)
cursor = db.cursor(buffered=True)

date_fmt = "%m/%d/%Y"
source_file ="commit.csv"
destination = "/group1/"
query = "select * from commit"

def save_gitcommits():
    sentiment = 0
    emotion = ""
    emotion_value = ""
    f = open("/home/xvnisa/commit.csv","w",encoding="utf-8",newline='')
    commit_header = ['commit_id','commit_comments','commit_sentiment','commit_subjectivity','commit_emotion','author','commit_date','no_files_changed','no_of_lines_changed','issue#','repo_name']
    writer = csv.writer(f)
    writer.writerow(commit_header)
    cursor.execute(query)
    record = cursor.fetchall()
    for r in record:
        try:
            sentiment = TextBlob(r[1]).sentiment.polarity
            subjectivity = TextBlob(r[1]).sentiment.subjectivity
            emotion = t.get_emotion(r[1])
            max_number=max(emotion.values())
            # Text2emotion returns multiple emotion for same comments
            # To avoid such confusion, the sentiment of the comment needs to be checked
            # If sentiment is positive and returned emotion has "Happy" or "Joy", the emotion should be set as either of them.
            # If sentiment is positive and emotion is of negative, the first negative emotion is taken from the dictionary.
            # same applies for other cases.
            d=dict((key,value) for key, value in emotion.items() if value == max_number)
            print(d)
            if len(d) > 1 and ('Happy' in d.keys() or 'Surprise' in d.keys() )and sentiment > 0:
               emotion_value = 'Happy'
            elif len(d) > 1 and ('Happy'  in d.keys() or 'Surprise' in d.keys() )  and sentiment < 0:
                 emotion_value = list(d.keys())[0]
                 if emotion_value == 'Happy' or emotion_value == 'Surprise':
                    emotion_value = list(d.keys())[1]
                 else:
                       emotion_value = list(d.keys())[0]
            list_of_files = literal_eval(r[4])
            print(len(list_of_files))
            data = [r[0],r[1],sentiment,subjectivity,emotion_value,r[2],r[3],len(list_of_files),r[5],r[6],r[7]]
            writer.writerow(data)
        except Exception as e:
               print(e)
               continue
           
    db.close()
    cursor.close()
    f.close()

if __name__ == "__main__":
    save_gitcommits()