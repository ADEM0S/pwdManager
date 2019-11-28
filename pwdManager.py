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
yes = ['Yes', 'yes', 'YES', 'y', 'Y']
OS = sys.platform

def clear(OS):
    """clear the screen"""
    try:
        if OS=="windows":
            os.system("cls")
        elif OS=="linux":
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

def exist_serv(c, table, id):
    ret = c.execute(f"SELECT * FROM {table} WHERE service=? ", (id, )).fetchall()
    if ret == []:
        return False
    else:
        return True

def get_serv_pwd(c, table_name, service):
    """get pwd of a service"""
    try:
        pwd = c.execute(f"SELECT service_pwd FROM {table_name} WHERE service =?", (service,)).fetchall()[0][0]
        return pwd
    except:
        pass #occures an error wich will provoke the except msg

def del_pwd(c, table_name, service):
    """deletes a password and the service"""
    c.execute(f"DELETE FROM {table_name} WHERE service=?", (service,))

def update_pwd(c, table_name, service, password):
    """changes a password with the niewer one"""
    c.execute(f"UPDATE {table_name} SET service_pwd=? WHERE service=?", (password, service))

def open_pwd_gen():
    try:
        if OS == 'windows':
            os.system("python3 ./cmds/PasswordGenerator/windows/password_generator.py")
        elif OS == 'linux':
            os.system("python3 ./cmds/PasswordGenerator/linux/password_generator.py")
    except:
        input("Not abled to run the program.")

def main ():
    clear(OS)
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
        clear(OS)
        act = input("[q]uit or [c]ontinue ? \n" + prompt)
        clear(OS)
        if act == 'c':
        
            logged = False
            while not logged:
                clear(OS)
                act = input("login or register ? l/r \n" + prompt)
                clear(OS)

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
                        clear(OS)
                    else:
                        input("Not the same passwords.")
                        clear(OS)

                elif act == 'l':
                    print('Login')
                    user = input("User : ")
                    pwd = getpass.getpass('Password : ')

                    if check_pwd(c, user, pwd):
                        logged = True
            
            table_name = user + '_db'
            manRun = True
            while manRun:
                clear(OS)
                print(f"You are in the {user}'s manager.")
                print()
                print('***********************')
                print('COMMANDS:')
                print('@1 : disconnect')
                print('@2 : get password')
                print('@3 : register password')
                print('@4 : delete password')
                print('@5 : change password')
                print('@6 : generate pasword')
                print('***********************')

                act = input(prompt)

                if act == '1':
                    clear(OS)
                    manRun = False
                    input("disconnected.")

                elif act == '2':
                    clear(OS)
                    serv = input("Wich service do you want to get your password ?\n"+prompt)
                    try:
                        input("Password for " + serv + " : '" + get_serv_pwd(c, table_name, serv) + "\' \n")
                    except:
                        input("Password not assigned")

                elif act == '3':
                    clear(OS)
                    print("Register a password for a service.")
                    serv = input("Service : ")
                    pwd2reg1 = getpass.getpass("Password : ")
                    pwd2reg2 = getpass.getpass('Reapeat password : ')
                    if pwd2reg1 == pwd2reg2:
                        pwd2reg1
                        try:
                            store_pwd(c, table_name, serv, pwd2reg1)
                            db.commit()
                            clear(OS)
                            input('Password is stored.')
                        except Error as e:
                            if verb:
                                print(e)
                            input("Something went wrong, the password isn't stored.")
                    else:
                        clear(OS)
                        input("Not the same passwords.")
                
                elif act == '4':
                    clear(OS)
                    serv = input("service to delete the password :\n"+prompt)
                    print()
                    sure = input("Are you sure ??\n"+prompt)
                    if sure in yes:
                        rsure = input("Really sure ?!\nYou won't be able to get it back.\n"+prompt)
                        if rsure in yes:
                            clear(OS)
                            try:
                                del_pwd(c, table_name, serv)
                                input("Good job.")
                            except:
                                input("Not able to delete the password.\nMaybe you putted the wrong name or it doesn't exists")

                elif act == '5':
                    clear(OS)
                    print("Change the password of a service.")
                    serv = input("Service : ")
                    if exist_serv(c, table_name, serv):
                        exp_pwd = get_serv_pwd(c, table_name, serv)                   
                        old_pwd = getpass.getpass("Old password : ")
                        if exp_pwd == old_pwd:
                            new_pwd1 = getpass.getpass("New password : ")
                            new_pwd2 = getpass.getpass("Confirm new password : ")
                            if new_pwd1 == new_pwd2:
                                try:
                                    update_pwd(c, table_name, serv, new_pwd1)
                                    db.commit()
                                    input("Password has been updated.")
                                except:
                                    input('failed to update the password.')
                            else:
                                clear(OS)
                                input("Passwords aren't the same.")
                        else:
                            clear(OS)
                            input("Old password not correct.")
                    else:
                        clear(OS)
                        input(f"Service \'{serv}\' isn't known.")

                elif act == '6':
                    """generate a fully secured password"""
                    clear(OS)
                    print("Password generator.")
                    open_pwd_gen()

        elif act == 'q':
            swloop = False
            input("Leaving the program...\n")
            clear(OS)
                
    db.commit()
    db.close()
    del db


if __name__ == "__main__":
    main()