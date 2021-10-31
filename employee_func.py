#Broke many lines in two parts cuz pylint loves it
"""This module will be used for functionalities of the employee"""
import PySimpleGUI as sg
import mysql.connector as sqltor
import settings as st

mycon= sqltor.connect(host=st.host,user=st.user,passwd=st.password,database=st.database)
cursor = mycon.cursor()
def employee_screen():
    """This Function is responsible for the display of Employee Screen"""
    sg.theme('DarkAmber')
    font = ("Arial", 11)
    layout = [
        [sg.Text("Welcome",font=font)],
        [sg.Text('')],
        [sg.Text('Please choose the function')],
        [sg.Button("Update Stock Data",key = 'Update'),
            sg.Button("Show Profit Analysis"),sg.Button("See Customer Details")],
        [sg.Text("")]
    ]
    window = sg.Window('Welcome',layout)
    while True:
        event = window.read(close = True)[0] #Values variable was getting wasted
        if event is None:
            window.close()
            break
        if event == 'Update':
            update_stock()

def update_stock():
    """This function is responsible for handling update related functions"""
    def display_stock():
        """This displays the products"""
        cursor.execute("SELECT * FROM PRODUCTS")
        data = cursor.fetchall()
        for i in range(len(data)):
            data[i] = list(data[i])
            for j in range(len(data[i])):
                if isinstance(data[i][j],str):
                    data[i][j] = str(data[i][j])
        heading = ['ID','Name','Brand','Size','Quantity','Cost_Price','Selling_Price']
        layout1 = [[sg.Text('Product List')],
        [sg.Table(data,headings = heading,key = 'Table',justification='left'
        ,auto_size_columns=False,def_col_width=10)],
        [sg.Button('Add',key = 'Add'),sg.Button('Update Stock',key = 'Update'),
        sg.Button('Go Back',key = 'GB')],
        ]
        win = sg.Window('Product List',layout1,finalize=True)
        while True:
            event,value = win.read()
            #print(event,value)
            if event == 'Update':
                try:
                    update_data(value['Table'][0]+1)
                    cursor.execute("SELECT * FROM PRODUCTS")
                    data = cursor.fetchall()
                    win['Table'].update(data)
                except IndexError:
                    sg.popup( "Warning: No Product Selected",title = "WARNING")
            if event == 'Add':
                win['GB'].update(disabled = True)
                add_stock()
                cursor.execute("SELECT * FROM PRODUCTS")
                data = cursor.fetchall()
                win['Table'].update(data)
                win['GB'].update(disabled = False)
            if event == 'GB':
                win.close()
                employee_screen()
            elif event is None:
                break

    def add_stock():
        """This function enables the employee to add new products in stock"""
        lay = [[sg.Text('Enter Product ID',size = (18,1)),sg.Input(key = 'id')],
        [sg.Text('Enter Product Name',size = (18,1)),sg.Input(key = 'name')],
        [sg.Text('Enter Product Brand',size = (18,1)),sg.Input(key = 'brand')],
        [sg.Text('Enter Product Size',size = (18,1)),sg.Input(key = 'size')],
        [sg.Text('Quantity of Product',size = (18,1)),sg.Input(key = 'quantity')],
        [sg.Text('Cost Price of Product',size = (18,1)),sg.Input(key = 'cost_price')],
        [sg.Text('Selling Price of Product',size = (18,1)),sg.Input(key ='selling_price')]
        ]
        layout = [[sg.Frame("Add New Stock",lay)],
        [sg.Button('Go Back'),sg.Button('Confirm')]
        ]
        window = sg.Window("New Product",layout=layout)
        while True:
            event,value = window.read()
            #print(event,value)
            if event == 'Confirm':
                sg.popup('Stock Added to Database')
                window.close()
                insert_prod = """INSERT INTO PRODUCTS
                (ID,Name,Brand,Size,Quantity,Cost_Price,Selling_Price)
                Values(%s,%s,%s,%s,%s,%s,%s)"""
                upd_value = [list(value.values())]
                cursor.executemany(insert_prod,upd_value)
                print(upd_value)
                break
            if event in (None, "Go Back"):
                window.close()
                break
    def update_data(ID):
        """This function allows employee to modify the details of existing stock"""
        lay = [[sg.Text('Product ID',size = (18,1)),
            sg.Input(default_text = ID, key = 'ID',readonly=True,tooltip = "It's Read Only")],
        [sg.Text('Product Name',size = (18,1)),sg.Input(key = 'Name')],
        [sg.Text('Product Brand',size = (18,1)),sg.Input(key = 'Brand')],
        [sg.Text('Product Size',size = (18,1)),sg.Input(key = 'Size')],
        [sg.Text('Quantity of Product',size = (18,1)),sg.Input(key = 'Quantity')],
        [sg.Text('Cost Price of Product',size = (18,1)),sg.Input(key = 'Cost_Price')],
        [sg.Text('Selling Price of Product',size = (18,1)),sg.Input(key ='Selling_Price')]
        ]
        layout=[[sg.Text("Instructions: The data which is not to be updated shall be left blank")],
            [sg.Frame("Add New Stock",lay)],
        [sg.Button('Go Back'),sg.Button('Confirm')]
        ]
        win = sg.Window('Update Data',layout,finalize=True)
        while True:
            event,value = win.read()
            if event == 'Confirm':
                for i in value:
                    if value[i] != '' and i!= 'ID':
                        print(i,value[i])
                        cursor.execute(f"""UPDATE PRODUCTS SET {i} = {value[i]}
                        WHERE ID = {int(ID)}""")
                        print('Meow Testing')
                sg.popup('Data Updated')
                win.close()
            print(event,value)
            if event is None:
                break
    display_stock()
mycon.commit()
#Run the code only if the current file run
if __name__=='__main__':
    employee_screen()