import mysql.connector 
from datetime import datetime
conn= mysql.connector.connect(
    host="localhost",
    user="root",
    password="Happykid@05"
)
cursor = conn.cursor()
cursor.execute("create database if not exists restaurant_management")
# print("Database created successfully")

cursor.execute("use restaurant_management")
cursor.execute("""create table if not exists customers(id int auto_increment primary key,
name varchar(100), email varchar(100), phone varchar(15))""")
# print("table created successfully")

cursor.execute("""
create table if not exists restaurant_tables(table_number varchar(10) primary key,
capacity int,status varchar(50))""")
# print ("table created successfully")
table =[("t1", 4, "available"),
       ("t2", 2, "full"),
       ("t3", 6, "available"),
       ("t4", 4, "available"),
       ("t5", 2, "full"),
       ("t6", 4, "full"),
       ("t7", 6, "available"),
       ("t8", 2, "available")]
for t in table:
    cursor.execute("insert ignore into restaurant_tables(table_number,capacity,status) values(%s,%s,%s)",(t[0],t[1],t[2]))
cursor.execute("select *from restaurant_tables")
rows = cursor.fetchall() 
# for i in rows:
#     print(i)
cursor.execute("""create table if not exists bookings(id int Auto_increment primary key,
customer_id int, customer_name varchar(50),table_number varchar(10), booking_date date,
booking_time time,capacity int, status varchar(50))""")   
print("welcome to Syberviz Restaurant")
customer_name= input("enter customer Name:")
customer_email=input("enter customer email:")
customer_phone= (input("enter customer phone:"))
cursor.execute("""insert into customers(name,email,phone)
values(%s,%s,%s)""",( customer_name,customer_email,customer_phone))
customer_id = cursor.lastrowid
     
# print("data inserted successfully") 
bookings= input("do you want to book a table? (yes/no):")
if bookings.lower()=="no":
    table_number="none"
if bookings.lower()=="yes":
    booking_date=(input("enter booking date():"))
    booking_time= (input("enter booking time()"))
    capacity= int(input("enter capacity:"))

    cursor.execute("select * from restaurant_tables where status='available' and capacity>=%s",(capacity,))
    rows= cursor.fetchall()
    for i in rows:
        print(i)
    if rows:
        table_number= input("enter table number to book:")
        table_found=False
        for i in rows:
            if i[0]==table_number:
                table_found=True  
                cursor.execute("""insert into bookings(customer_id,customer_name,table_number,booking_date,booking_time,capacity,status) 
                values(%s,%s,%s,%s,%s,%s,'confirmed')""",(customer_id,customer_name,table_number,booking_date,booking_time,capacity))
                conn.commit()
                print("table booked successfully")
        if table_found== False:
            print("table number not available for the selected capacity")  
else:
    cursor.execute(""" create table if not exists menu(id int primary key,
name varchar(100),price decimal(10,2))""")
# print("table created successfully")
table=[("1", "chicken biryani", 250.00),
       ("2", "mutton biryani", 300.00),
       ("3", "veg biryani", 200.00),
       ("4", "chicken fry", 150.00),
       ("5", "mutton fry", 200.00),
       ("6", "veg fry", 100.00)]
for t in table:
    cursor.execute("insert ignore into menu(id,name,price) values(%s,%s,%s)",(t[0],t[1],t[2]))
cursor.execute('select* from menu')
rows = cursor.fetchall()
menu = input("do you want to see the menu? (yes/no):")
if menu.lower()=="yes":
    cursor.execute("select * from menu")
    rows = cursor.fetchall()
    for i in rows:
        print(i)
else:
    print("Thank you for visiting our restaurant. Have a great day!")
    exit()
# print("table created successfully")

order_items = input("do you want to order food?:")
if order_items.lower()=="yes":
    menu_item_id= input("enter menu item id:")
    quantity= input("enter quantity:")
    menu_item_id=[int(i)for i in menu_item_id.split(",")]
    quantity=[int(i) for i in quantity.split(",")]
    final_total=0
    for i in range(len(menu_item_id)):
        menu_item = menu_item_id[i]
        quanty = quantity[i]
        cursor.execute("select name,price from menu where id=%s",(menu_item,))
        result= cursor.fetchone()
        if result:     
            item_name=result[0]
            price= result[1] 
            total = quanty *price
            final_total = final_total+total
        if bookings =="yes":
            print("table_number:",table_number)
            print("customer Name:",customer_name)
        else:
            print("item:",item_name)
            print("quantity:",quanty)
            print("price:",price)
    print("total bill:",final_total) 
    confirmation = input("do you want to confirm order?(yes/no):")  
    if confirmation == "yes":
        print("your orders confirmed")

        cursor.execute("""create table if not exists orders(id int auto_increment primary key,
        customer_id int, table_number varchar(10), 
        order_date date, order_time time, total_amount decimal(10,2), status varchar(50))""") 

        order_date= datetime.now().date()
        order_time= datetime.now().time()

        cursor.execute("""insert into orders(customer_id,table_number,
        order_date,order_time,total_amount,status)values(%s,%s,%s,%s,%s,%s)
        """,(customer_id,table_number, order_date, order_time,final_total,'confirmed'))
        order_id=cursor.lastrowid

        cursor.execute("""create table if not exists order_items(id int auto_increment primary key,order_id int,
        menu_item_id int, quantity int, price decimal(10,2))""")
        
        for i in range(len(menu_item_id)):
            menu_item = menu_item_id[i]
            quanty = quantity[i]
            cursor.execute("select name,price from menu where id=%s",(menu_item,))
            result= cursor.fetchone()
            if result:
                item_name= result[0]
                price=result[1]
                cursor.execute("""insert into order_items(order_id,menu_item_id,quantity,price)
                values(%s,%s,%s,%s)""",(order_id,menu_item,quanty,price))
        conn.commit()
          
    print("Thank you visit Again")
     
else:
    print("Thank you for visiting our restaurant. Have a great day!") 


# cursor.execute("select * from customers")
# rows = cursor.fetchall()
# for i in rows:
#     print(i)
