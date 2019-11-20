import sqlite3
from sqlite3 import Error
import os
import sys

run = True
prompt = '$ '
verbose = False


try:
    arg1 = sys.argv[0]
    if arg1 == "verbose":
        verbose = True
except:
    pass

def clear():
    """clear the screen"""

    try:
        if sys.platform == 'win32':
            os.system('cls')
        elif sys.platform == 'linux':
            os.system('clear')
    except Error as e:
        if verbose:
            print(e)

def check_master_pass(user, master_pass):
    pwd = c.execute(f"SELECT user_password FROM 'users' WHERE name='{user}'")
    if verbose :
        print(pwd)
    pwd = c.fetchall()[0][0]
    if verbose:
        print(pwd)
    input()

    if master_pass == pwd :
        return True
    else:
        return False

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None

    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn

    except Error as e:
        if verbose :
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
        print(e)


def store_new_pwd(service, pwd, user):
    c1 = sqlite3.connect('user.db').cursor()
    sql = "INSERT INTO {}(service, servpassword) VALUES({},{})".format(user, service, pwd)
    c1.execute(sql)
    print("well inserted")


if __name__ == '__main__':



    # create the database connection
    data = create_connection('users.db')
    # data cursor 
    c = data.cursor()
    # create manager table
        # create_table(c, 'manager', '(domain text, stored_password text)')
    # create identification table

    create_table(c, 'users', '(name string, user_password string)')


    logged = False
    while not logged:

        clear()
        print("login or register ? l/r")
        act = input(prompt)

        clear()
        if act == 'l':
            user = input("User: ")
            master_password = input("Password: ")
            
            try :
                if check_master_pass(user, master_password):
                    logged = True
                else :
                    print("WRONG PASSWORD")
            except Error as e:
                print("Error occured:")
                print(e)

        elif act == 'r':
            user = input("new user: ")
            pwd = input("new password: ")

            c.execute("INSERT INTO users VALUES ( ?, ?)", (user, pwd))

            user_table = user
            create_table(c, user_table, "(service TEXT, servpassword TEXT)")
            print("table created")

            data.commit()
            logged = True
            print(f"Welcome {user} !")
            input('')
            



    # user verification:


    data.commit()

    while run:
        clear()
        print("Successfully logged in !")
        print(f"You are in the {user}'s manager.")
        print()
        print('****************')
        print('commands:')
        print('q : quit')
        print('gp : get password')
        print('rg')
        print('****************')
        
        act = input("$ ")

        if act == 'q':
            run = False
        
        elif act == 'rp':
            """register a password for a service"""
            clear()
            print("registering a new password:\n")
            service = input("New service: ")
            pwd_to_store = input('New password: ')

            store_new_pwd(service, pwd_to_store, user)

            try:
                pass
            except:
                pass


    data.close()
    del data 
