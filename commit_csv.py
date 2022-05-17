import csv

import mysql.connector

username = "root"
password = "Saigon12345"
database = "intemodb"
#token = "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"
url = "https://github.com/ChuDucAnh2402/hello-world.git"
db = mysql.connector.connect(host="localhost", user=username, password=password, database=database)
cursor = db.cursor(buffered=True)
query = "SELECT * FROM commit1"
def save_commit():
    path = "csv/commit.csv"
    f = open(path, "w", encoding="utf-8", newline="")
    writer = csv.writer(f)
    header = ['commit_id', 'commit_comments', 'author', 'commit_date', 'no_of_lines_changed', 'issue#', 'repo_name']
    writer.writerow(header)

    cursor.execute(query)
    record = cursor.fetchall()
    for r in record:
        try:
            data = [r[0], r[1], r[2], r[3], r[4], r[5], r[6]]
            writer.writerow(data)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    save_commit()