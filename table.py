# importing psycopg2
import psycopg2

# conn=psycopg2.connect(
# 	database="d2kq6ba278qupb",
# 	user="rpiefrkjxxncgz",
# 	password="38a33ed0eb25a13b7f4f1d5bd02fee72bad4fc86cbd9d07df6d2bf1e35561890",
# 	host="ec2-44-199-143-43.compute-1.amazonaws.com",
# 	port="5432"
# )
conn=psycopg2.connect(
	database="my_db",
	user="postgres",
	password="8566",
	host="127.0.0.1", 
	port = "5433"
)

# Creating a cursor object using the cursor()
# method
cursor = conn.cursor()

# drop table accounts
sql =  """ SELECT * FROM vendor
			"""

# Executing the query
cursor.execute(sql)
print("Table created !")

# Commit your changes in the database
conn.commit()

# Closing the connection
conn.close()
