import sqlite3
from sqlite3 import Error
import os
import sys

run = True
verb = None

try:
    verb = argv[0]
except:
    pass

def clear():
    """clear the screen"""

    try:
        if sys.platform=="windows":
            os.system("cls")
        elif sys.platform=="linux":
            os.system("clear")
            
    except Error as e:
        if verb:
            print(e)



def check_master_pass(user, master_pass):
    pwd = c.execute(f"SELECT user_pwd FROM 'users' WHERE name='{user}'")
    if verb:
        print(pwd)
    pwd = pwd.fetchall()
    if verb:
        print(pwd)

    if master_pass == pwd:
        return True
    else:
        return False

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None

    try:
        conn = sqlite3.connect(db_file)
        if verb:
            print(sqlite3.version)
        return conn

    except Error as e:
        if verb:
            print(e)


def close_connection(db_file):
    """ close the connection with a database """
    db_file.close()

def create_table(cursor, table, args):
    """create the table """
    command = "CREATE TABLE " + table + ' ' + args
    
    try:
        cursor.execute(command)
    except Error as e :
        if verb:
            print(e)


def store_new_pwd(service, pwd, user):
    c1 = sqlite3.connect('users.db').cursor()
    sql = "INSERT INTO {}(service, servpassword) VALUES({},{})".format(user, service, pwd)
    try:
        c1.execute(sql)
        print(f"{service} inserted")
        input()
    except Error as e:
        print(e)
    




if __name__ == '__main__':


    # create the database connection
    data = create_connection('database.db')
    # data cursor 
    c = data.cursor()
    # create manager table
    create_table(c, 'manager', '(domain text, stored_password text)')
    # create identification table
    
    create_table(c, 'users', '(name string, user_password string)')
    
    loop = True
    while loop:
        act = input("[q]uit or [c]ontinue ? \n")
        if act == 'c':
    
            logged = False
            while not logged:

                clear()
                print("login or register ? l/r")
                act = input('$ ')

                clear()
                if act == 'l':
                    user = input("User: ")
                    master_password = input("Password: ")
            
                    if check_master_pass(user, master_password):
                        logged = True

                elif act == 'r':
                    user = input("new user: ")
                    pwd = input("new password: ")

                    c.execute("INSERT INTO users VALUES ( ?, ?)", (user, pwd))
                    data.commit()
                    logged = True
                    
                    try:
                        create_table(c, user, "(service TEXT, servpassword TEXT)")
                        print("table created")
                    except:
                        print("Error creating the table")
                    
                    
                    
                    print(f"Welcome {user} !")
                    input('')
            
            data.commit()

    
    #software loop
    
            while run:
        
    
                clear()
                print(f"You are in the {user}'s manager.")
                print()
                print('****************')
                print('commands:')
                print('q : quit')
                print('gp : get password')
                print('rp : register password')
                print('****************')
        
                act = input("$ ")

                if act == 'q':
                    run = False
            
                elif act == 'gp':
                    service = input('Service : ')
            
            
                elif act == 'rp':
                    """register a password for a service"""
                    clear()
                    print("Register a password for a service\n")
                    service = input("New service: ")
                    pwd_to_store = input("Password: ")
                    store_new_pwd(service, pwd_to_store, user)
                    try:
                        pass
                    except:
                        pass





            data.commit()
            data.close()
            del data
            
        elif act == 'q':
            
            loop = False
