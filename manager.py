import sqlite3
from sqlite3 import Error
import os

run = True

def check_master_pass(user, master_pass):
    pwd = c.execute(f"SELECT user_password FROM 'users' WHERE name='{user}'")
    print(pwd)
    pwd = c.fetchall()[0][0]
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

if __name__ == '__main__':



    # create the database connection
    data = create_connection('db.sq3')
    # data cursor 
    c = data.cursor()
    # create manager table
        # create_table(c, 'manager', '(domain text, stored_password text)')
    # create identification table

    create_table(c, 'users', '(name string, user_password string)')


    logged = False
    while not logged:

        os.system('cls')
        print("login or register ? l/r")
        act = input('$ ')

        os.system('cls')
        if act == 'l':
            user = input("User: ")
            master_password = input("Password: ")
            
            if check_master_pass(user, master_password):
                logged = True
            else :
                print("WRONG PASSWORD")

        elif act == 'r':
            user = input("new user: ")
            pwd = input("new password: ")

            c.execute("INSERT INTO users VALUES ( ?, ?)", (user, pwd))
            data.commit()
            logged = True
            print(f"Welcome {user} !")
            input('')
            



    # user verification:


    data.commit()

    while run:
        os.system("cls")
        print("Successfully logged in !")
        print(f"You are in the {user}'s manager.")
        print()
        print('****************')
        print('commands:')
        print('q : quit')
        print('gp : get password')
        print('****************')
        
        act = input("$ ")

        if act == 'q':
            run = False
        


    data.close()
    del data 