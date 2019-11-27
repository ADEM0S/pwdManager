#!/bin/python3

import sqlite3 as sq
from sqlite3 import Error
import getpass #password inputs
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
        input("User not known")
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

def no_double(c, table, id):
    """returns true if the id already exists and false else """
    
    ret = c.execute(f"SELECT * FROM {table} WHERE name=? ", (id, )).fetchall()
    if ret == []:
        return True
    else:
        return False

def get_serv_pwd(c, table_name, service):
    """get pwd of a service"""
    try:
        pwd = c.execute(f"SELECT service_pwd FROM {table_name} WHERE service =?", (service,)).fetchall()[0][0]
        return pwd
    except:
        pass



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
                    pwd1 = getpass.getpass('Password : ')
                    pwd2 = getpass.getpass("Confirm password : ")
                    if pwd1 == pwd2:
                        pwd = pwd1
                        #creates user's table
                        try:
                            table_name = user + '_db'
                            args = '(service TEXT, service_pwd TEXT)'
                            create_table(c, table_name, args)
                        except:
                            print("Error creating {}'s database".format(user))
                        
                        #inserts users login infos into users
                        try:
                            if no_double(c, 'users', user):
                                c.execute("INSERT INTO users VALUES ( ?, ?)", (user, pwd))
                                input('inserted')
                                logged = True
                            else:
                                input("id already exists\n")
                        except Error as e:
                            print(e)
                            print("Error inserting {}'s values".format(user))
                        db.commit()
                        clear()
                    else:
                        input("Not the same passwords.")
                        clear()

                elif act == 'l':
                    print('Login')
                    user = input("User : ")
                    pwd = getpass.getpass('Password : ')

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
                    clear()
                    serv = input("Wich service do you want to get your password ?\n")
                    try:
                        input("Password for " + serv + " : '" + get_serv_pwd(c, table_name, serv) + "\' \n")
                    except:
                        input("Password not assigned")

                elif act == 'rp':
                    clear()
                    print("Register a password for a service.")
                    serv = input("Service : ")
                    pwd2reg1 = getpass.getpass("Password : ")
                    pwd2reg2 = getpass.getpass('Reapeat password : ')
                    if pwd2reg1 == pwd2reg2:
                        pwd2reg1
                        try:
                            store_pwd(c, table_name, serv, pwd2reg1)
                            db.commit()
                            clear()
                            input('Password is stored.')
                        except Error as e:
                            if verb:
                                print(e)
                            input("Something went wrong, the password isn't stored.")
                    else:
                        clear()
                        input("Not the same passwords.")



        elif act == 'q':
            swloop = False
            input("Leaving the program...\n")
            clear()
                
    db.commit()
    db.close()
    del db


if __name__ == "__main__":
    main()