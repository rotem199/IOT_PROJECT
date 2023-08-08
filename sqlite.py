import sqlite3
import random


conn = sqlite3.connect('airConditioners.db')
conn2 = sqlite3.connect('boilers.db')
c=conn.cursor()
c2=conn2.cursor()

c.execute("""CREATE TABLE airConditionersData (
          airConditionerNumber integer,
          open_close text
           )""")

c2.execute("""CREATE TABLE boilersData (
           boilersNumber integer,
           open_close text
           )""")
conn.commit()
conn2.commit()


def insert_airConditioners(airConditionerNumber, open_close):
    with conn:
        c.execute("INSERT INTO airConditionersData VALUES (:airConditionerNumber, :open_close)",{'airConditionerNumber':airConditionerNumber, 'open_close':open_close})

def update_airConditioners(airConditionerNumber, open_close):
    with conn:
        c.execute("""UPDATE from airConditionersData SET open_close = :open_close WHERE airConditionerNumber =:airConditionerNumber""",{'airConditionerNumber':airConditionerNumber, 'open_close':open_close})

def get_status_by_number(airConditionerNumber):
    c.execute("SELECT * FROM airConditionersData WHERE airConditionerNumber=:airConditionerNumber", {'airConditionerNumber': airConditionerNumber})
    return c.fetchall()

def insert_boilers(boilersNumber, open_close):
    with conn2:
        c2.execute("INSERT INTO boilersData VALUES (:boilersNumber, :open_close)",{'boilersNumber':boilersNumber, 'open_close':open_close})

def update_window(boilersNumber, open_close):
    with conn2:
        c2.execute("""UPDATE from boilersData SET open_close = :open_close WHERE boilersNumber =:boilersNumber""",{'boilersNumber':boilersNumber, 'open_close':open_close})

def get_status_by_number(boilersNumber):
    c.execute("SELECT * FROM boilersData WHERE boilersNumber=:boilersNumber", {'boilersNumber': boilersNumber})
    return c.fetchall()

for x in range(21):
    
    mylist1 = ['open', 'close']
    insert_airConditioners(x+1,random.choice(mylist1)) 
    insert_boilers(x+1,random.choice(mylist1)) 
    
conn.close()
conn2.close()