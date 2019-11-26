#!/bin/python3

import sqlite3 as sq
from sqlite3 import Error
import sys
import os

"""Variables """
#verbose 
verb = None
try :
    if argv[0] == "verb":
        verb = True
except:
    pass

prompt = "~ $ "


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

def check_pwd(c, user, pwd):
    """checks the password"""
    true_pwd = None

    try:
        true_pwd = c.execute("""SELECT usr_pwd FROM 'users' WHERE name=?""", (user,))
        true_pwd = true_pwd.fetchall()[0][0]
        if verb:
            print(true_pwd)
        if pwd == true_pwd:
            if verb:
                print("login success")
                input()
            return True
    except:
        print("User not known")
        return False


def create_connection(db):
    """create connection"""
    conn = None

    try:
        conn = sq.connect(db)
        return conn
    except:
        if verb :
            print("Error during database connection") 

def create_table(c, id, args):
    """creates <id> table with <args> for arguments"""
    cmd = "CREATE TABLE " + id + ' ' + args
    try:
        c.execute(cmd)
        if verb:
            print("table {id} created")
    except:
        if verb:
            print(f"problem creating the {id} table")

def store_pwd(c, table_name, service, password):
    """store new password for new service"""
    cmd = "INSERT INTO {} (service, service_pwd) VALUES( ?, ?)".format(table_name)

    c.execute(cmd, (service, password))


def main ():
    clear()
    db =  create_connection('database.db')
    c = db.cursor()

    #'users' table
    try:
        create_table(c, 'users', '(name TEXT, usr_pwd TEXT)')
        db.commit()
    except:
        print('table user already exists')

    swloop = True
    while swloop:
        clear()
        act = input("[q]uit or [c]ontinue ? \n" + prompt)
        clear()
        if act == 'c':
        
            logged = False
            while not logged:
                #clear()
                act = input("login or register ? l/r \n" + prompt)
                clear()

                if act == 'r':
                    print("Register")
                    user = input('User : ')
                    pwd = input('Password : ')

                    #creates user's table
                    try:
                        table_name = user + '_db'
                        args = '(service TEXT, service_pwd TEXT)'
                        create_table(c, table_name, args)
                    except:
                        print("Error creating {}'s database".format(user))
                    
                    #inserts users login infos into users
                    try:
                        c.execute("INSERT INTO users VALUES ( ?, ?)", (user, pwd))
                    except Error as e:
                        print(e)
                        print("Error inserting {}'s values".format(user))
                    db.commit()

                elif act == 'l':
                    print('Login')
                    user = input("User : ")
                    pwd = input('Password : ')

                    if check_pwd(c, user, pwd):
                        logged = True
            
            table_name = user + '_db'
            manRun = True
            while manRun:
                clear()
                print(f"You are in the {user}'s manager.")
                print()
                print('****************')
                print('commands:')
                print('d : disconnect')
                print('gp : get password')
                print('rp : register password')
                print('****************')

                act = input(prompt)

                if act == 'd':
                    clear()
                    manRun = False
                    input("disconnected.")

                elif act == 'gp':
                    pass
                
                elif act == 'rp':
                    clear()
                    print("Register a password for a service.")
                    serv = input("Service : ")
                    pwd2reg = input("Password : ")
                    try:
                        store_pwd(c, table_name, serv, pwd2reg)
                        db.commit()
                    except Error as e:
                        if verb:
                            print(e)
                        print("Something went wrong")



        elif act == 'q':
            swloop = False
            input("Leaving the program...\n")
                
    db.commit()
    db.close()
    del db


if __name__ == "__main__":
    main()