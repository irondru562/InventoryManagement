# InventoryManagement
Simple Desktop Application for inventory management.

## About
A very simple inventory managment program as a desktop application. This program uses the **PySimpleGUI** library to create the GUI and **sqlite3** on the backend as the database.

## Setup

Install the following libraries:

``` pip install PySimpleGUI```

and

``` pip install opencv-python ```

## How to Use

### Selecting Category
If a category exists in your database it will show up in the dropdown when clicked.

![Selecting Cateroy](https://github.com/irondru562/InventoryManagement/tree/main/images/sel_cat.png?raw=true)

### Adding Categories
If you want to add a new category that doesnt already exists.

**Add pictrue here**

1. Click on Edit.
2. Hover over Category.
3. Select Add.
4. Type name of category.

### Removing Category
Same path as adding a category, just have category you wish removed already selected from the dropdown menu the remove.

### Selecting Item

Once a category is selected.

If items are present within that category they will appear in the item box.

Select the item to view an overview about the item to the right.

### Adding Item

1. Within the **Items** box click on the **Add** button.
2. Fill out information on *Add Inventory* window.
3. Click **Ok**

**Add picture here**

### Removing Item

With the item selected. Click the remove button.

### Updating Item

With the desired item selected.

Under the overview box. Make the necessary changes to the inventory. **Keep in mind Part Number, Description, and Vendor cannot be changed**

Once changes are made click the **Update** button.

``` NOTE: As the inventory on hand goes below the inventory needed, the field will be highlighted red to indicate that the item needs to be ordered. ```

### Orders

Pressing the **Orders** button will open up a new window.

**Add picture here**

Pressing the **Order** button at the bottom will produce a list of items that need to be ordered. If item has already been ordered (order button already pressed) then a checkmark will appear in the *Ordered* field. If you have recieved the item alread, then click yes on *recieved* and database will be updated.

**Add picture here**