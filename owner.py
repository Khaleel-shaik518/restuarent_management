import mysql.connector
conn= mysql.connector.connect(
    host="localhost",
    user="root",
    password="Happykid@05"
)
cursor=conn.cursor()
cursor.execute("use restaurant_management")
all_tables=input("Do you want see all tables?(yes/no)")
if all_tables.lower()=="yes":
    cursor.execute("select *from restaurant_tables")
    rows=cursor.fetchall()
    for i in rows:
        print(i)
    available = input("Do you want to see all available tables? (yes/no)")
    if available.lower()=="yes":
        cursor.execute("select * from restaurant_tables where status='available'")
        rows=cursor.fetchall()
        for i in rows:
            print(i)
            print("see you again")
else:
    available = input("Do you want to see all available tables? (yes/no)")
    if available.lower()=="yes":
        cursor.execute("select * from restaurant_tables where status='available'")
        rows=cursor.fetchall()
        for i in rows:
            print(i)
orderss=input("Do you want to see customer orders?(yes/no)")
if orderss.lower()=="yes":
    cursor.execute("select * from orders")
    rows=cursor.fetchall()
    for i in rows:
        print(i)
customer_details=input("do you want to see customer details?(yes/no)")
if customer_details=="yes":
    cursor.execute("select * from customers")
    rows=cursor.fetchall()
    for i in rows:
        print(i)
else:
    print("see you again")