import sqlite3

def create_table(name):
    
    name = name.title()
    name = name.split()
    name = ''.join(name)
    with sqlite3.connect('supplies.db') as conn:
        cur = conn.cursor()
        cur.execute(f'CREATE TABLE IF NOT EXISTS {name} (Item TEXT, Part Number TEXT, Description TEXT, Vendor TEXT, Price REAL, QOH INT, QNeed INT, Ordering TEXT, Ordered DATE)')
        
def remove_table(name):
    
    with sqlite3.connect('supplies.db') as conn:
        cur = conn.cursor()
        cur.execute(f'DROP TABLE IF EXISTS {name}')
        

def return_tables():
    with sqlite3.connect('supplies.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT name from sqlite_master WHERE type= "table" ORDER BY name ASC')
        return cur.fetchall()
    
# Create a return items Function.
def return_allitems(table):
    with sqlite3.connect('supplies.db') as conn:
        cur = conn.cursor()
        cur.execute(f'SELECT Item from {table} ORDER BY Item ASC')
        return cur.fetchall()
    
def return_allinfo(table, item):
    with sqlite3.connect('supplies.db') as conn:
        cur = conn.cursor()
        cur.execute(f'SELECT * from {table} WHERE Item= ? ORDER BY Item ASC', (item,))
        return cur.fetchall()

# Create a insert items function.
def add_items(table,item,pn,des,ven,price,qoh,qneed,order= "FALSE", ordered= None):
    with sqlite3.connect('supplies.db') as conn:
        cur = conn.cursor()
        cur.execute(f'INSERT INTO {table} VALUES (?,?,?,?,?,?,?,?,?)', (item,pn,des,ven,price,qoh,qneed,order, ordered))
        conn.commit()
        

# Create a remove items function.
def remove_items(table, item):
    with sqlite3.connect('supplies.db') as conn:
        cur = conn.cursor()
        cur.execute(f'DELETE FROM {table} WHERE Item= ?', (item,))
        conn.commit()
        
# Create a Update function that updates the price of selected item.
def Update(table, item, price, qoh, qneeded, order= 'FALSE'):
    with sqlite3.connect('supplies.db') as conn:
        cur = conn.cursor()
        cur.execute(f'UPDATE {table} SET Price= ?, QOH = ?, QNeed= ?, Ordering= ? WHERE Item= ?', (price, qoh, qneeded, order, item))
        conn.commit()
        
def Update_date(table, item, date= None):
    with sqlite3.connect('supplies.db') as conn:
        cur = conn.cursor()
        cur.execute(f'UPDATE {table} SET Ordered = ? WHERE Item= ?', (date, item))
        conn.commit()
        
def Orders(table):
        with sqlite3.connect('supplies.db') as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM {table} WHERE Ordering= 'TRUE' ")
            return cur.fetchall()
        

