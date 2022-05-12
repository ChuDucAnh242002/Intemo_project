import mysql.connector

username = "root"
password = "Saigon12345"
database = "intemodb"
db = mysql.connector.connect(host="localhost", user= username, password= password, database= database)

create_query = "CREATE TABLE [IF NOT EXISTS] commit1"

cursor = db.cursor(buffered= True)

cursor.execute("SELECT VERSION()")

data = cursor.fetchone()
print(data)

db.close()
