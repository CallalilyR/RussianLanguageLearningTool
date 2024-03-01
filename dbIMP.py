# Written by: Calla Robison
# 4/24/2023
# This file's purpose was to import and connect to a mariaDb database and implement SQL
# queries in a python environment and through user inputted actions and information
# CRUD operations can be found in the functions addOp, delOp, editOp, and displayOptions 
# paired with the functions querying the tables the funtions translationTable, nounsOnly,
# verbsOnly, etc. The user interface was created using 'pick' and I was going to display
# the tables using the panda plugin, but was crunched on time in this project and will 
# implement in the future.

import mysql.connector as sql
from mysql.connector import Error
import mariadb
import pandas as pd
from sqlOps import AddingOperations, DeletingOperations, EditingOperations, RetrieveOperations
from pick import pick
import os

def createConnection(host_name, user_name, password, database):
    db = None
    try:
        db = mariadb.connect(host=host_name,
                user=user_name,
                password=password,
                database = database) #adjust to your DB setup
        print("MariaDB Database connection successful")
    except ValueError as err:
        print(f"Error: '{err}'")

    return db

def createDatabase(db, query):
    cursor = db.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except ValueError as err:
        print(f"Error: '{err}'") 

def executeQuery(db, query):
    cursor = db.cursor()
    try:
        cursor.execute(query)
        db.commit() #implements SQL queries
        print("Query Successful")
        print(db)
    except ValueError as err:
        print(f"Error: '{err}'") 

def executeQuerywInput(db, query, *args):
    cursor = db.cursor()
    try:
        cursor.execute(query, args)
        db.commit() #implements SQL queries
        print("Query Successful")
        print(db)
    except ValueError as err:
        print(f"Error: '{err}'") 

#Customize terminal print statements
def esc(code):
    return f'\033[{code}m'

#Validate user input for verb type
def get_verb_type():
    while True:
        try: 
            verbType = input("imperf or perf: ")
            if verbType == "imperf" or verbType == "perf":
                return verbType
            else:
                print("Should be imperf or perf")
        except:
            continue

#validate user input for Id
def get_properId(cursor):

    cursor.execute('SELECT MAX(id) from russianWords')
    maxId = cursor.fetchone()[0]
    
    while True:
        try:
            id = int(input("Input Word ID: "))
            if id <= maxId:
                return id
            else:
                print("Value does not exist. Try again")
        except ValueError:
            print("Invalid value: please enter a valid integer")

# ------------------------------------------------------------------------------------------------------------------------------------------------
# CRUD Operation implementations           

#Add rows to a table
def addOp():

    ops = AddingOperations()

    #Intialize user entries
    r_word = input('Russian word: ')
    e_word = input('English word: ')
    print('Grammar type list: adj, adv, noun, prep, conj, verb, pronoun \n')
    gramType = input('Grammar Type: ')

    if gramType == 'verb':
        verbType = input('imperf or perf: ')
        gramCase =''
    if gramType == 'pronoun' or gramType =='prep' or gramType == 'conj':
        print('Grammar case list: nom, gen, dative, acc, instr, prep \n')
        gramCase = input('Case: ')
        verbType = ''

    #add to english and russian table first
    executeQuerywInput(db, ops.pop_russianWords, r_word, gramType)
    executeQuerywInput(db, ops.pop_englishWords, e_word, gramType)

    #Execute query to add to verb table if grammar type is verb, pronoun, prep, or conj
    if gramType == 'verb':
        executeQuerywInput(db, ops.pop_verb, r_word , gramType, verbType)
        executeQuery(db, ops.update_verbId) #Update ID in verb table to match the word in russian parent table
    if gramType == 'pronoun':
        executeQuerywInput(db, ops.pop_pronoun, r_word, gramType, gramCase)
        executeQuery(db, ops.update_pronounId) #Update ID in pronoun table to match the word in russian parent table
    if gramType == 'prep' or gramType == 'conj':
        executeQuerywInput(db, ops.pop_prep_conj, r_word, gramType, gramCase)
        executeQuery(db, ops.update_prepConjId) #Update ID in prep_conj table to match the word in russian parent table
 
#Delete rows from a table
def delOp():

    ops = DeletingOperations()
    executeQuery(db, ops.fk1)
    executeQuery(db, ops.fk2)
    executeQuery(db, ops.fk3)

    translationTable(cursor) #Display current table of all english words in database with russian translation and grammar type

    #Intialize user entries
    e_word = input('Input english word: ')

    #store tuple that is being deleted
    cursor.execute(f"""
        -- SELECT * FROM englishWords WHERE engWord = '{e_word}'
        SELECT * 
        FROM englishWords
        JOIN russianWords ON englishWords.id = russianWords.id
        LEFT JOIN proNouns ON englishWords.id = proNouns.id
        LEFT JOIN verbs ON englishWords.id = verbs.id
        WHERE englishWords.engWord = '{e_word}' ;
    """)
    deletedRows = cursor.fetchall()

    #Deletes from all tables where id is used as a foreign key to connect all the tables
    executeQuerywInput(db, ops.delete_query_reg, e_word)

    #Show user the row that was deleted
    for row in deletedRows:
            print(row)
            #print("\n")
    
    #Supposed to reset the ID number count but doesn't  
    #executeQuery(db, ops.reset_auto_incrementEng)
    #executeQuery(db, ops.reset_auto_incrementRuss)

    executeQuery(db, ops.dropFk1)
    executeQuery(db, ops.dropFk2)
    executeQuery(db, ops.dropFk3)
    
#Edit/update rows
def editOp(cursor):

    ops = EditingOperations()

    print('Which row would you like to edit?')
    translationTable(cursor) #Display current table of all english words in database with russian translation and grammar type
    id = get_properId(cursor) #Only takes valid integers

    print('Select a column')
    #only takes valid selctions
    while True:
        try:
            print(esc('31;1;4') + 'English Word' + esc(0) + ', ' + esc('31;1;4') + 'Russian Word' + esc(0) + ', ' + esc('31;1;4') + 'Verb Type ' + esc(0) + ', ' + esc('31;1;4') + 'Grammar Case' + esc(0))
            edit_Inp = input('Selection: ')
            if edit_Inp == "english word" or edit_Inp == "russian word" or edit_Inp == "verb type" or edit_Inp == "grammar case":
                break
            else:
                print("Invalid entry: try again")
        except:
            print("Invalid entry: try again")
            

    if edit_Inp == "english word":
        e_word = input('Edit english word: ')
        executeQuerywInput(db, ops.update_engWord, e_word, id)

    if edit_Inp == "russian word":
        r_word = input('Edit russian word: ')
        print("Grammar type list: adj, adv, noun, prep, conj, verb, pronoun \n")
        gramType = input('Enter grammar type: ')
        map = ["adj", "adv", "noun"]

        if gramType in map:
            executeQuerywInput(db, ops.update_russWord, r_word, id)
        if gramType == "prep" or gramType == "conj":
            executeQuerywInput(db, ops.update_russWord, r_word, id)
            executeQuerywInput(db, ops.update_russWordPrepConj, r_word, id)
        if gramType == "verb":
            executeQuerywInput(db, ops.update_russWord, r_word, id)
            executeQuerywInput(db, ops.update_russWordVerb, r_word, id)
        if gramType == "pronoun":
            executeQuerywInput(db, ops.update_russWord, r_word, id)
            executeQuerywInput(db, ops.update_russWordProNouns, r_word, id)
        

    #Show user the row that was updated
    cursor.execute(f"""
        SELECT englishWords.id, englishWords.engWord, russianWords.russWord, englishWords.gramType
        FROM englishWords
        JOIN russianWords ON englishWords.id = russianWords.id
        WHERE englishWords.id = '{id}'
     """)
    updatedRow = cursor.fetchall()
        
    # Convert the tuple to a string
    updatedRowString = str(updatedRow)

    # Concatenate the string and print
    print("UPDATED ROW: " + updatedRowString)
    

    # get_verb_type()

#Displaying table/database information
def translationTable(cursor):
    
    ops = RetrieveOperations()

    #Display translate view table
    try:
        cursor.execute(ops.create_translateView)
        cursor.execute(ops.show_translateView)
        tableView = cursor.fetchall()

        #print rows
        print("TRANSLATION VIEW")
        for row in tableView:
            print(row)
            #print("\n")
        input("press enter to continue...")
    
    except Exception as e:
        print(e)

def nounsOnly(cursor):
    ops = RetrieveOperations()

    #Display noun selection query
    try:
        cursor.execute(ops.select_nouns)
        tableView = cursor.fetchall()

        #print rows
        print("SELECT NOUNS")
        for row in tableView:
            print(row)
            #print("\n")
        input("press enter to continue...")
    
    except Exception as e:
        print(e)
    
def verbsOnly(cursor):
    ops = RetrieveOperations()

    #Display noun selection query
    try:
        cursor.execute(ops.select_verbs)
        tableView = cursor.fetchall()

        #print rows
        print("SELECT VERBS")
        for row in tableView:
            print(row)
            #print("\n")
        input("press enter to continue...")
    
    except Exception as e:
        print(e)

def adjOnly(cursor):
    ops = RetrieveOperations()

    #Display noun selection query
    try:
        cursor.execute(ops.select_adj)
        tableView = cursor.fetchall()

        #print rows
        print("SELECT ADJ")
        for row in tableView:
            print(row)
            #print("\n")
        input("press enter to continue...")
    
    except Exception as e:
        print(e)

def prepOnly(cursor):
    ops = RetrieveOperations()

    #Display noun selection query
    try:
        cursor.execute(ops.select_prep)
        tableView = cursor.fetchall()

        #print rows
        print("SELECT PREP")
        for row in tableView:
            print(row)
            #print("\n")
        input("press enter to continue...")
    
    except Exception as e:
        print(e)

def conjOnly(cursor):
    ops = RetrieveOperations()

    #Display noun selection query
    try:
        cursor.execute(ops.select_conj)
        tableView = cursor.fetchall()

        #print rows
        print("SELECT CONJ")
        for row in tableView:
            print(row)
            #print("\n")
        input("press enter to continue...")
    
    except Exception as e:
        print(e)

def advOnly(cursor):
    ops = RetrieveOperations()

    #Display noun selection query
    try:
        cursor.execute(ops.select_adv)
        tableView = cursor.fetchall()

        #print rows
        print("SELECT ADVERBS")
        for row in tableView:
            print(row)
            #print("\n")
        input("press enter to continue...")
    
    except Exception as e:
        print(e)

def proNounsOnly(cursor):
    ops = RetrieveOperations()

    #Display noun selection query
    try:
        cursor.execute(ops.select_pronouns)
        tableView = cursor.fetchall()

        #print rows
        print("SELECT PRONOUNS")
        for row in tableView:
            print(row)
            #print("\n")
        input("press enter to continue...")
    
    except Exception as e:
        print(e)

def displayOptions(cursor):
    while True:
        title = 'Choose an option below'
        options = ['All words in database', 'All nouns', 'All verbs', 'All adjectives', "All prepositions", "All conjunctions", "All adverbs", "All pronouns", "Exit"]

        option, index = pick(options, title, indicator='=>', default_index=2)

        print(f"You chose {option} at index {index}")
        os.system("cls")
        if index == 0:
            translationTable(cursor)
        if index == 1:
            nounsOnly(cursor)
        if index == 2:
            verbsOnly(cursor)
        if index == 3:
            adjOnly(cursor)
        if index == 4:
            prepOnly(cursor)
        if index == 5:
            conjOnly(cursor)
        if index == 6:
            advOnly(cursor)
        if index == 7:
            proNounsOnly(cursor)
        if index ==8:
            break


#Main function
def main():
    

 
    while True:
        title = 'Choose an option below'
        options = ['Add to database', 'Delete from databse', 'Edit entries in database', 'Displays', "Exit"]

        option, index = pick(options, title, indicator='=>', default_index=2)

        print(f"You chose {option} at index {index}")
        os.system("cls")
        if index == 0:
            addOp()
        if index == 1:
            delOp()
        if index == 2:
            editOp(cursor)
        if index == 3:
            displayOptions(cursor)
        if index == 4:
            break


#run main fucntion
if __name__ == '__main__':
    db = createConnection("localhost", "root", "root", "russLangTool")
    cursor = db.cursor()
    main()
    db.close()


















