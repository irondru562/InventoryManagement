'''

Author: Andrew Bell
Date: 5/13/2020


It has a front end GUI and uses a database to store all information needed to properly track inventory.

To convert py script to a exe run the following command at the command prompt where the script is located.

pyinstaller -wF [name of script].py

'''



import PySimpleGUI as gui
import cv2 as cv
from datetime import date
import inback, os



try:
    os.mkdir(os.getcwd() + '/pictures') # When program starts it will create a pictures folder in current directory and if exists it will continue.
    
except FileExistsError:
    pass

items = []    
item_info = ['Part Number: ', 'Description: ', 'Vendor: ', 'Price: ', 'Quantity on Hand: ', 'Quantity Needed: ']

add_tip = "Add new item to Inventory."
remove_tip = "Select an item to remove and press button."
add_item_tip = "Please use Vendor part number when adding an item."

# =============================================================================
# 
# 
# 
# Functions goes here
# 
# 
# 
# 
# =============================================================================

# create function that uses a python imaging library to convert any pictures into a .png. Going to use cv2.
def upload_img(image,name=' '):
    img = cv.imread(image) # Loads images to be modified.
    img = cv.resize(img,(250,250))
    
    cv.imwrite(os.getcwd() + f'\pictures\{name}.png', img)
    

    
def add_win(): # Creates a new window thats gets information for adding a new part.
    
    layout2 = [[gui.Text('Category: '),gui.Combo(inback.return_tables(),size= (30,1), readonly= True, key= 'categories2')]]
    layout2 += [[gui.Text('Item: '), gui.In(key= 'Item2')]]
    layout2 += [[gui.Text('Part Number: '), gui.In(key= 'Part Number: 2', tooltip= add_item_tip)]]
    layout2 += [[gui.Text(f'{info}'), gui.In(key= f'{info}2')] for info in item_info[1:]]
    layout2+= [[gui.FileBrowse(target= 'image_path'), gui.Text('(No Picture Selected)',key= 'image_path', size= (50,1))]]
    layout2 += [[gui.Button('OK')]]
    
    # Add some kind of browing button to get a image file path to be used.
    
    win2 = gui.Window('Add Item',layout2,element_justification= 'right', button_color= ('black','LightSkyBlue'))
    
    while True:
        events2, values2 = win2.read()
# Add some kind of error watch to see if numbers are inputted into price, qoh, qneed field.
        print(events2,values2)
        if events2 == None:
            break
        
        elif events2 == 'OK':
            try:
            # Gets the needed information to send back to add to database.
                cat = values2['categories2']
                item = values2['Item2'].title()
                pn = values2['Part Number: 2'].capitalize()
                des = values2['Description: 2'].capitalize()
                ven = values2['Vendor: 2'].capitalize()
                price = float(values2['Price: 2'])
                qoh = int(values2['Quantity on Hand: 2'])
                qneed = int(values2['Quantity Needed: 2'])
                
            # Gets a picture using the browse button and moves and renames image to a picture folder.    
                source_path = values2['Browse']
                
                if source_path.startswith('C:'): # Checks to see if a picture was selected of not.
                    upload_img(source_path,item)
                
                win2.close()
                return cat,item,pn,des,ven,price,qoh,qneed # Return statements will automatically break the loop and return values.
            
            except ValueError:
                gui.Popup('Please use a number for price, Quantity on hand or Quantity needed fields.', title= 'Error', button_color = ('white','red'))
                
    win2.close()
    
# =============================================================================
#     
#     
# a function that creates a new window called ordering that has information about ordered parts.
# 
# 
# 
# =============================================================================

def order_win():
    
    rows2 = [[]]
    
    for table in inback.return_tables(): # Search all tables one at a time.
        if len(table) > 0: # If the table is empty dont do anything.
            
            table = table[0] # Unpack from tuple.
            for item in inback.Orders(table): # Look at each item in the current table.
                
                name = item[0]
                order_date = item[-1]
                
                if order_date != None: # If part has an order date run this code.
                    
                    rows2 += [[gui.Input(f'{name}', disabled= True), gui.CB('',default= True,key= f'{name}'), gui.Radio('Yes',f'{name}1',key= f'{name}_y', enable_events= True), gui.Radio('No',f'{name}1', default= True, key= f'{name}_n')]]
                
                else: # If part number does not have a order date then uncheck the ordered box
                    rows2 += [[gui.Input(f'{name}', disabled= True), gui.CB('', key= f'{name}'), gui.Radio('Yes',f'{name}1',key= f'{name}_y', enable_events= True), gui.Radio('No',f'{name}1', default= True, key= f'{name}_n')]]


    frame_order = [[gui.Output(size= (69,15))]]            
    main_col = [
            [gui.Text('Part Name'+(' '*55), font= ('Arial',11,'bold')), gui.Text('Ordered'+(' '*3), font= ('Arial',11,'bold')), gui.Text('Received', font= ('Arial',11,'bold'))],
            [gui.Column(rows2, element_justification="center")]
            ]
    
    layout3 = [
            [gui.Column(main_col, scrollable = True, vertical_scroll_only= True,size= (485,250))],
            [gui.Frame('Order List',frame_order, border_width= 4, font= ('Arial',11,'bold'))],
            [gui.Button('Order')]
                ]
    
    window3 = gui.Window('Orders', layout3)
    
    while True:
        event3, value3 = window3.read()
        
        if event3 == None:
            break
        
        elif event3 == "Order": # If Order button is pressed run this code.
            
            for table in inback.return_tables(): # Search all tables one at a time.
            
                if len(table) > 0: # If the table is empty dont do anything.
                    
                    table = table[0]
                    for item in inback.Orders(table): # Look at each item in the current table.
                        
                        name, pn, desc, ven, price,qoh, need = item[0:7] # unpack item into the following varibles.
                        now = item[-1]
                        
                        need = need - qoh # Subtract Quantity needed and Quantity on hand to see how much we need ordered.
                        
                        price = format(price,'.2f') # Converts floating numbers to .00 value.
                        
                        name1 = f'Item: {name}'
                        pn = f'Part number: {pn}'
                        desc = f'Description: {desc}'
                        ven = f'Vendor: {ven}'
                        price = f'Price: ${price}'
                        need = f'Quantity Needed: {need}'
                        
                        
                        if now == None: # Prints out information to send to supervisor only if date is not added.
                            
                            print(name1)
                            print(pn)
                            print(desc)
                            print(ven)
                            print(price)
                            print(need)
                            print('\n')
                            
                            now = date.today()
                            inback.Update_date(table, name, now)
                            window3[f"{name}"].Update(value= True)
        
        elif '_y' in event3:
            
            try:
                string = str(event3)
                string = string.split('_y')
                
                
                for table in inback.return_tables(): # Search all tables one at a time.
                
                    if len(table) > 0: # If the table is empty dont do anything.
                        
                        table = table[0]
                        for item in inback.Orders(table): # Look at each item in the current table.
                            
                            name, pn, desc, ven, price,qoh, need = item[0:7] # unpack item into the following varibles.
                            
                            if string[0] == name:
                                if item[-1] != None:
                                    new_need = need - qoh
                                    qoh += new_need
                                    
                                    inback.Update(table, name, price, qoh, need)
                                    inback.Update_date(table, name) # Resets time back to None.
                                    window3[f"{name}_y"].Update(disable= True)
                                    
                                else: # Runs if item was never ordered.
                                    
                                    window3[f"{name}_n"].Update(value= True)
                                    gui.Popup('Please send order to Supervisor.', title= 'Error', button_color = ('white','red'))
            except TypeError:
                pass
                        
                    
    window3.close()
# =============================================================================
#     
# 
# 
# =============================================================================


    
def return_list(items):
    temp = []
    for item in items:
        item = item[0] # Items is a list of tuples and this line unpacks the tuple.
        temp.append(item)
    return temp

# a function that returns True if qoh < qneeded.
def check_less(qoh, qneeded):
    
    qoh = int(qoh)
    qneeded = int(qneeded)
    
    if qoh < qneeded:
        return True
    else:
        return False

# =============================================================================
# 
# Menu definition goes here
# 
# If a "&" sign is used behind a letter this means that the letter in front is used with Alt + Letter example: 'E&xit' = Alt + x
# Using a "!" behind a button disables it and greys it out. Used as a sort of place holder.
# 
# =============================================================================
menu_def = [
        ['File',['E&xit']],
        ['Edit',['Category',['Add::addCat','Remove::removeCat'], 'Item',['Add::addItem','Remove::removeItem']]]
        ]


# =============================================================================
# 
# This is the setup for the two column containers used to house the image and description texts and the dropdown and Listbox
# 
# =============================================================================


frame1 = [
        [gui.Combo(inback.return_tables(),default_value= '(Please Select Category)',size= (30,1), readonly= True, key= 'categories', enable_events= True)]
        ]

frame2 = [
        [gui.Button('Add',key= 'AddButton',tooltip= add_tip),gui.Button('Remove',key='RemoveButton', tooltip= remove_tip)],
        [gui.Listbox(items,size=(30,25), key= 'items',enable_events= True, pad= (3,5))]
        ]

# Change logo picture here.
frame3 = [[gui.Image(os.getcwd() + '\pictures\logo_test.png', size= (300,300), key='pic')]]
frame3 +=  [[gui.Text(f'{info}'), gui.In(key= f'{info}', disabled= True)] for info in item_info[0:3]]
frame3 +=  [[gui.Text(f'{info}'), gui.In(key= f'{info}')] for info in item_info[3:]]
frame3 += [[gui.Output(size= (60,15),key = '_output_', visible= False)],[gui.Button('Orders', key= 'Order'), gui.Button('Update', key= 'Update')]]

column1 = [
        [gui.Frame('Category',frame1, border_width= 4, font= ('Arial',11,'bold'))],
        [gui.Frame('Items',frame2, border_width= 4, font= ('Arial',11,'bold'))]
        ]

column2 =[[gui.Frame('Overview',frame3,element_justification= 'right', border_width= 4, font= ('Arial',11,'bold'))]]




# =============================================================================
# 
# 
# Main layout and program start here.
# 
# 
# =============================================================================
layout = [
        # This is the 1st row, below is the 2nd row, etc. Needs to be seperated by a comma.
        [gui.Menu(menu_def, key= 'menu')],
        [gui.Column(column1), gui.Column(column2)],
        ] # Create the layout for the application.

main_win = gui.Window('Inventory Management', layout,button_color= ('black','LightSkyBlue')) # Applies layout to window class called main_win.

while True:
    
    events, values = main_win.read() # Start main window and return as tuple (event,value).
    
# =============================================================================
#     
#     
#     When the exit button is pressed or the x on top right of window is pressed.
#     
#     
# =============================================================================
    if events == None or events == 'Exit': # If 'x' is pressed close application and stop loop.
        break
    
# =============================================================================
#     
#     When to add category button is pressed this will run.
#     
#     
# =============================================================================
    elif events == 'Add::addCat': # Run this if you go to Edit -> Add -> Category.
        
        text = gui.popup_get_text('Please Enter Category name','Add Category') # Get table name user wants to add.
        if text == None:
            pass
        else:
            inback.create_table(text) # Create a new table using the user input.
            main_win['categories'].Update(values= inback.return_tables()) # Update the main window to reflect change.
            
# =============================================================================
# 
#     When the remove category button is pressed this will run.
#     
# a statement that looks if the Edit -> Category -> Remove button is pressed and run the remove table function and update values for combo box.
# =============================================================================

    elif events == 'Remove::removeCat':
        
        inback.remove_table(values['categories'][0]) # Uses backend function to remove selected table.
        main_win['categories'].Update(values= inback.return_tables()) # Updates values list to reflect changes.
        
# =============================================================================
#     
#     When the add item button is pressed this will run.
#     
#     
# =============================================================================
    elif events == 'Add::addItem' or events == 'AddButton':
        part_info = add_win()
        if part_info == None:
            pass
        
        else:
            table, item, pn, des, ven, price, qoh, qneed = part_info # Gets user input from other window and unpacks results to be added to list.
            
            if check_less(qoh,qneed):
                
                inback.add_items(table[0],item,pn,des,ven,price,qoh,qneed, order= "TRUE")
            else:
                inback.add_items(table[0],item,pn,des,ven,price,qoh,qneed)


# =============================================================================
# 
#     When the remove item is pressed this will run.
#     
#     
# =============================================================================
    elif events == 'Remove::removeItem' or events == 'RemoveButton':
        try:
            cat = values['categories'][0]
            temp_item = values['items'][0]
            inback.remove_items(cat, temp_item) # Removes item from table.
            
            temp_items = return_list(inback.return_allitems(cat)) # Returns updated list of category.
            main_win['items'].Update(temp_items) # Update listbox with new list.
            
        except:
            pass
            
# =============================================================================
# 
#     When a category is selected from the category list this will run.
#     
#     
# =============================================================================
    elif events == 'categories':
        
        cat = values['categories'][0]
        items = return_list(inback.return_allitems(cat)) # Returns list of items.
        main_win['items'].Update(items) # Updates item listbox.
        
# =============================================================================
#         
# 
#     This event happens when a item is clicked.
# 
#     
# =============================================================================
    elif events == 'items':
        try:
            # When a item is clicked all information will appear on right hand side.
            cat = values['categories'][0]
            item = values['items'][0]
            infos = inback.return_allinfo(cat,item)[0][1:]
            qoh = infos[4]
            qneeded = infos[5]
            
            main_win["_output_"].Update('', visible= False)
            
            try: # If there's no picture use default picture
                main_win['pic'].Update(os.getcwd() + f'\pictures\{item}.png')
            except:
                main_win['pic'].Update(os.getcwd() + r'\pictures\no_image.png')
                
            
            for info, inputbox in zip(infos,item_info): # Put item information in respective field.
                main_win[inputbox].Update(info)
                
            if check_less(qoh,qneeded): # Check to see if quanity on hand is lower than quanity needed.
                main_win['Quantity on Hand: '].Update(background_color= 'Red')
            else:
                main_win['Quantity on Hand: '].Update(background_color= 'white')
                
        except IndexError: # Just skip if no information is returned back.
            pass
        
# =============================================================================
#         
# 
# 
# 
# 
# 
# =============================================================================
            
# =============================================================================
#                  
# 
#     When the Update button is pressed this will run.
# 
#       
# =============================================================================
    elif events == 'Update':
        try:
            cat = values['categories'][0]
            item = values['items'][0]
            price = float(values['Price: '])
            qoh = int(values['Quantity on Hand: '])
            qneed = int(values['Quantity Needed: '])
            
            if check_less(qoh,qneed):
                
                main_win['Quantity on Hand: '].Update(background_color= 'Red')
                inback.Update(cat, item, price, qoh, qneed, order= 'TRUE')
            else:
                
                main_win['Quantity on Hand: '].Update(background_color= 'white')
                inback.Update(cat, item, price, qoh, qneed)
                inback.Update_date(cat, item)
            
            # Gets the information for the updated item and updates the window.
            
            infos = inback.return_allinfo(cat,item)[0][1:]
            for info, inbox in zip(infos,item_info):
                main_win[inbox].Update(info)
                
            gui.popup_timed('Item Updated', font= ('Arial',12))
        
        except ValueError:
            gui.Popup('Please use a number for price, quantity on hand or quantity needed fields.', title= 'Error', button_color = ('white','red'))
        
        except IndexError:
            gui.popup_timed('Please select an item first before updating.', title= 'Error', font= ('Arial',11,'bold'))
            
# =============================================================================
#             
# 
# 
# 
# 
# =============================================================================
        
# a feature event listener that puts all items with a True in Ordering column in Database (return_allinfo(Table, Item)[0][-1]) and puts it into a word document to send to boss.
            
    elif events == "Order": # When order button is pressed.
        
        order_win()
        
main_win.close()
    