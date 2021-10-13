import mysql.connector
from mysql.connector import Error
from mysql.connector import connection
from sql import create_connection


#creating connection to mysql database
conn = create_connection("cis3368fall21.ckt6dnygzu82.us-east-2.rds.amazonaws.com", "admin", "chase234", "cis3368fall21")
mycursor = conn.cursor()

# Here I created the menu where you select how you want to manage the shopping list
# Once you run the program the menu will show and you input the selection you want.

def menu():
    mymenu = []
    while True:
        selection = input('''
            MENU
a - Add item
d - Remove item
u - Update item Details
r1 - Output all items in alphabetical order
r2 - Output all items sorted by quantity (ascending)
q - quit

''')

        # When you select 'a' from the menu it prompts you to enter the item description and quantity,
        # then the code inserts them into the query and runs the sql statement. Then the item is added to the shopping list
        # this is the source I used to help with this section https://www.w3schools.com/python/python_mysql_insert.asp

        if selection == 'a':
            itemd = input("Enter the item description: ")
            quantity = int(input("Enter the item quantity: "))

            query = "INSERT INTO shoppinglist (itemdescription, quantity, dateadded) VALUES (%s, %s, now())"
            val = (itemd, quantity)
            mycursor.execute(query,val)
            conn.commit()

        # When you select 'd' from the menu it prompts you to enter the item description of the item 
        # you want to delete and then the code runs sql statement with the inputs and deletes the item from the shopping list.
        # this is the source I used to help with this section https://www.w3schools.com/python/python_mysql_delete.asp

        elif selection == 'd':
            item_to_be_deleted = input("Name of item to be deleted: ")
            query = "DELETE FROM shoppinglist WHERE itemdescription = %s"
            val = (item_to_be_deleted, )
            mycursor.execute(query,val)
            conn.commit()

        # When you select 'u' from the menu it prompts you to enter the item description you want to update and the updated description
        # then the program run sql statement runs with the inputs and updates the table.
        # this is the source I used to help with this section https://www.w3schools.com/python/python_mysql_update.asp 

        elif selection == 'u':
            itemd = input("Enter item description you would like to change: ")
            updated_itemd = input("Enter the updated item description: ")


            query1 = "UPDATE shoppinglist SET itemdescription = %s WHERE itemdescription = %s "
            val1 = (updated_itemd, itemd)
            mycursor.execute(query1,val1)
            conn.commit()
        
        # When you enter 'r1' it runs the sql statement, then prints the table alphabetically by the item description
        # this is the source I used to help with this section https://www.w3schools.com/python/python_mysql_orderby.asp      
        elif selection == 'r1':
            output_alpha = "SELECT * FROM shoppinglist ORDER BY itemdescription"
            mycursor.execute(output_alpha)
            myresult = mycursor.fetchall()
            for x in myresult:
                print(x)

        # When you enter 'r2' it runs the sql statement , then prints the table by the quantity ascending
        # this is the source I used to help with this section https://www.w3schools.com/python/python_mysql_orderby.asp
        elif selection == 'r2':
                output_ascending = "SELECT * FROM shoppinglist ORDER BY quantity ASC"
                mycursor.execute(output_ascending)
                myresult = mycursor.fetchall()
                for x in myresult:
                    print (x)
    
        # when you select 'q' the program stops
        elif selection == 'q':
            break

menu()