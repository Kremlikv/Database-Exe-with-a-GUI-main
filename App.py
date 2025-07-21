
"""
This is a simple school project by Vitezslav Kremlik
contact: kremlik@seznam.cz

It is a database management app with a Graphic User Interface.
It uploads and administers a csv file.

The left frame is used to display a table, the right frame is used to input data.
All changes are stored to a temporary working dataframe.
Users have to open a file first, otherwise a warning message is shown.

The code has comments.
The file exists in a virtual environment. (python -m venv myvenv) (.\myvenv\scripts\activate)
It is backed up at GitHub.

***

PyInstaller is used to convert the programme into a single .exe file.

pyinstaller --onefile --windowed --add-data "blue_banner.png;." --add-data "brand.png;." --icon=myicon.ico app.py

pyinstaller add-data problem solved:
https://www.youtube.com/watch?v=p3tSLatmGvU 
https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file

Since the Exe file uses a sys import, the exit function must be sys.exit() not just exit().

"""

from tkinter import *
import tkinter as tk
from pandastable import Table 
import pandas as pd
import numpy as np
from PIL import Image, ImageTk
from tkinter.filedialog import asksaveasfile 


# We define the resource_path so the Pyinstaller can create an exe file
# It allows pyinstaller to find png files in the temporary _MEIPASS directory
# Paths to png files must be changed in the whole code appropriately 
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


global id_entry, surname_entry, name_entry, suffix_entry, email_entry, phone_entry
global id1, surname1, name1, suffix1, email1, phone1
global validate_adding

# LOGIN WINDOW
logapp = tk.Tk()
logapp.title("Login App")
logapp.geometry("300x350")
logapp.configure(bg='DeepSkyBlue2')
bg = PhotoImage(file = resource_path("blue_banner.png")) 
label1 = Label(logapp, image = bg) 
label1.place(x = 0, y = 0) 

# LOGIN FRAME
login_frame = tk.Frame(logapp, bg='lightblue', width=220, height=220)
login_frame.place(x = 40, y = 40) 
#login_frame.pack(side="bottom", padx=10, pady=10)

# pre-defined username and password
username = "User" 
password = "12345" 

# Prepare a function to clear a frame
def clear_login_frame():
    for widgets in login_frame.winfo_children():
        widgets.destroy()

# START
# What happens after you successfully log in 
def start_program():
    if user_entry.get() != username or user_pass.get() != password: 
        tk.messagebox.showinfo(title="Attention", 
                    message="Incorret password of user name")
    else:
        # Close the login window
        logapp.destroy()      
        # ROOT - create the main loop with the menu bar
        root = tk.Tk()
        root.title("ERGOSOL *** Employee Database Administration")
        root.geometry("1100x500")
        root.configure(bg='DeepSkyBlue2')           
               
        bg = PhotoImage(file = resource_path("blue_banner.png")) 
        label1 = Label( root, image = bg) 
        label1.place(x = 0, y = 0) 

        # FRAME1 and FRAME2
        frame1 = tk.Frame(root, bg='lightblue', width=400, height=350)
        frame1.pack(side="left", padx=10, pady=10)   
        frame2 = tk.Frame(root, bg='lightblue', width=400, height=350)
        frame2.pack(side="right", padx=10, pady=10)   

        # LOGO
        image = Image.open(resource_path('brand.png'))           
        image = ImageTk.PhotoImage(image)
        image_label = tk.Label(frame1, image=image)
        image_label.pack(side = "top", padx=20, pady=20)

        # When we log we want to see just Frame1 with a logo
        # We do not want to see Frame2 now       
        frame2.pack_forget()

        # Prepare functions to hide frames when necessary 
        def clear_frame1():
            for widgets in frame1.winfo_children():
                widgets.destroy() 

        def clear_frame2():
            for widgets in frame2.winfo_children():
                widgets.destroy()     
                 
        # DO NOTHIGN DUMMY WIDGET
        # Used during coding before replacing it with real functions
        def donothing():
            filewin = Toplevel(root)
            button = Button(filewin, text="Do nothing button")
            button.pack()
                
        # MENU - OPEN ANY        
        def open():
            # Wipe the Frames so we can display something new
            frame1.pack_forget() 
            frame2.pack_forget()    
            clear_frame1()
            clear_frame2()
            # Open a dialogue allowing to select a file from any directory
            file_path = tk.filedialog.askopenfilename(defaultextension=".csv",
                                                    filetypes=[("csv file", ".csv")],
                                                    )    
            # Upload the file into the working dataframe
            global df_working
            df = pd.read_csv(file_path)
            global df_working
            df_working = df
                   
            # Display the table in a new pop-up window            
            class ModifiedData:
                def __init__(self, frame1):
                    self.frame = tk.Frame(frame1) 
                    self.frame.pack(padx=10, pady=10)
                    self.table = Table(self.frame, dataframe=df_working, height = 140, width = 680)
                    self.table.show()
            frame1.pack(side="left", padx=10, pady=10)
            a = tk.Label (frame1, text = "Dataframe viewer", fg='white', bg='gray23', font=("Helvetica", 16))
            a.pack(padx=10, pady=10)
            tk.Label(frame1, text= "Modified data: ").pack()
            ModifiedData(frame1) 
            # We have nothing to display in Frame2 now so we can hide it
            frame2.pack_forget()

        # MENU - EXPORT TO CSV
        
        def export_validation():
            try: 
                df_working != None 
            except:
                tk.messagebox.showwarning(title="Attention", message="Open a file first.")
            else: 
                export()
        
        def export():
            # Load the working dataframe with the recent changes
            global df_working
            frame1.pack_forget() 
            frame2.pack_forget()   
            # Open the dialogue allowing to save into any directory
            file_path = tk.filedialog.asksaveasfilename(defaultextension=".csv",
                                                    filetypes=[("csv file", ".csv")],
                                                    )
            df_working.to_csv(file_path, index = False)
            # Write a message about the performed operation
            tk.messagebox.showinfo("Info", "Changes saved to CSV") 

        # MENU - QUITTING 
        def quitting():            
            sys.exit()

        def sorting_validation():
            try: 
                df_working != None 
            except:
                tk.messagebox.showwarning(title="Attention", message="Open a file first.")
            else: 
                sorting()

        # OPTION 1 - SORTING 
        def sorting():                  
            
            # Unhide Frame2 and wipe both frames clean
            frame1.pack(side="left", padx=10, pady=10)
            frame2.pack(side="right", padx=10, pady=10)
            clear_frame1()
            clear_frame2()           
            
            # Create a table to display the latest working data
            class OriginalData:
                def __init__(self, frame1):
                    self.frame = tk.Frame(frame1) 
                    self.frame.pack(padx=10, pady=10)
                    self.table = Table(self.frame, dataframe=df_working, height = 140, width = 680)
                    self.table.show()
            a = tk.Label (frame1, text = "Dataframe viewer", fg='white', bg='gray23', font=("Helvetica", 16))
            a.pack(padx=10, pady=10)
            tk.Label(frame1, text= "Data in active memory").pack()
            OriginalData(frame1)    
                                      
            # In Frame 2 Ask the user to select one of the columns
            sv1 = tk.StringVar(),tk.IntVar()
            tk.Label(frame2, text= "Write the column by which to sort the data:").pack(padx=10, pady=10)
            sorting_entry = tk.Entry(frame2, textvariable=sv1, width=35)
            sorting_entry.pack(padx=10, pady=10)

            # Extract the user-entered data from the Entry object
            # Then show the sorted data in a new pop-up window
            def get_sorted():
                sortie=sorting_entry.get()
                class SortedData:
                    def __init__(self, frame1):
                        self.frame = tk.Frame(frame1)
                        self.frame.pack(padx=10, pady=10)
                        self.table = Table(self.frame, dataframe=df_sorted, height = 140, width = 680)
                        self.table.show() 
                global df_working  
                df_sorted = df_working.sort_values(by= sortie)
                tk.Label(frame1, text= "Sorted data: ").pack()
                clear_frame1()                
                a = tk.Label (frame1, text = "Dataframe viewer", fg='white', bg='gray23', font=("Helvetica", 16))
                a.pack(padx=10, pady=10)                
                tk.Label(frame1, text= "Modified data").pack()
                SortedData(frame1)
                # Export the sorted dataframe into the working dataframe for later use
                df_working = df_sorted
                
            # This button confirms which column to sort by 
            # It displays the resulting sorted table
            sort_button = tk.Button(frame2, text= "Save", command = get_sorted,fg='white', bg='gray23', font=("Helvetica", 11)) 
            sort_button.pack(padx=10, pady=10)             
       
            
        # ADDING

        def adding_validation():
            try: 
                df_working != None 
            except:
                tk.messagebox.showwarning(title="Attention", message="Open a file first.")
            else: 
                adding()

        def adding():
            # Wipe both frames clean
            frame1.pack(side="left", padx=10, pady=10)
            clear_frame2() 
            clear_frame1()
            # Display the table with the lastest working data in Frame1    
            class WorkingData:
                def __init__(self, frame1):
                    self.frame = tk.Frame(frame1) 
                    self.frame.pack(padx=10, pady=10)
                    self.table = Table(self.frame, dataframe=df_working, height = 140, width = 680)
                    self.table.show()
            a = tk.Label (frame1, text = "Dataframe viewer", fg='white', bg='gray23', font=("Helvetica", 16))
            a.pack(padx=10, pady=10)
            tk.Label(frame1, text= "Working data: ").pack()
            WorkingData(frame1)
            
            # Disappear the Add Button in Frame2
            # Replace it with a form to input the employee data
            frame2.pack(side="right", padx=10, pady=10)

            iv1 = tk.IntVar()
            sv1 = tk.StringVar()
            sv2 = tk.StringVar()
            sv3 = tk.StringVar()
            sv4 = tk.StringVar()
            iv2 = tk.IntVar()   
        
            tk.Label(frame2, text= "id:").pack()
            id_entry = tk.Entry(frame2, textvariable=iv1, width=35)
            id_entry.pack(padx=10, pady=10)    

            tk.Label(frame2, text= "surname:").pack()
            surname_entry = tk.Entry(frame2, textvariable=sv1, width=35)
            surname_entry.pack(padx=10, pady=10) 

            tk.Label(frame2, text= "name:").pack()
            name_entry = tk.Entry(frame2, textvariable=sv2, width=35)
            name_entry.pack(padx=10, pady=10)

            tk.Label(frame2, text= "suffix:").pack()
            suffix_entry = tk.Entry(frame2, textvariable=sv3, width=35)
            suffix_entry.pack(padx=10, pady=10)  

            tk.Label(frame2, text= "email:").pack()
            email_entry = tk.Entry(frame2, textvariable=sv4, width=35)
            email_entry.pack(padx=10, pady=10)  

            tk.Label(frame2, text= "phone:").pack()
            phone_entry = tk.Entry(frame2, textvariable=iv2, width=35)
            phone_entry.pack(padx=10, pady=10)    

            # Define what happens after successful validation.
            # Updated table is shown
            def display_added():
        
                id1=id_entry.get()
                surname1=surname_entry.get()
                name1=name_entry.get()
                suffix1=suffix_entry.get()
                email1=email_entry.get()  
                phone1=phone_entry.get()
                # Define new row with user-input data
                new_row = {'id': id1,'surname': surname1, 'name': name1, 'suffix': suffix1, 'email':email1, 'phone':phone1} 
                df_new_row = pd.DataFrame.from_dict([new_row]) # must confert dict to df before concat
                df_new_row = df_new_row.astype({'id': int, 'phone': int})
                
                # Add the new row to the table
                global df_added 
                global df_working
                df_added = pd.concat([df_working, df_new_row]) # .append is deprecated
                class AfterAdding:
                    def __init__(self, frame1):
                        self.frame = tk.Frame(frame1)
                        self.frame.pack(padx=10, pady=10)
                        self.table = Table(self.frame, dataframe=df_added,height = 140, width = 680)
                        self.table.show()
                clear_frame1()
                a = tk.Label (frame1, text = "Dataframe viewer", fg='white', bg='gray23', font=("Helvetica", 16))
                a.pack(padx=10, pady=10)
                tk.Label(frame1, text= "Table with added data: ").pack()
                AfterAdding(frame1)
                # Update the working dataframe with the added row
                df_working = df_added

            # Validation happens after Adding, before Displaying 
            def validate_adding():
                # Examine user-input data extracted from the Entry object
                id1=id_entry.get()
                surname1=surname_entry.get()
                name1=name_entry.get()
                suffix1=suffix_entry.get()
                email1=email_entry.get()  
                phone1=phone_entry.get()
                if len(id1)<1 or len(surname1)<1 or len(name1)< 1 or len(suffix1)<1 or len(email1)<1 or len(phone1)<1: 
                    tk.messagebox.showwarning(title="Attention", message="All fields must be filled in!")
                    adding()
                else:
                    display_added()                     

            # A button that saves the new values a
            # It displays an updated table with added data   
            adding_button = tk.Button(frame2, text= "Add", command = validate_adding, fg='white', bg='gray23', font=("Helvetica", 11))
            adding_button.pack(padx=10, pady=10) 
 

        # DELETE

        def deletion_validation():
            try: 
                df_working != None 
            except:
                tk.messagebox.showwarning(title="Attention", message="Open a file first.")
            else: 
                deletion()

        def deletion():
            # Unhide Frame2 if necessary 
            frame1.pack(side="left", padx=10, pady=10)
            frame2.pack(side="right", padx=10, pady=10)
            # Display the latest working data for reference
            class WorkingData:
                def __init__(self, frame1):
                    self.frame = tk.Frame(frame1) 
                    self.frame.pack(padx=10, pady=10)
                    self.table = Table(self.frame, dataframe=df_working, height = 140, width = 680)
                    self.table.show()
            # Display the table tk.Label(frame1, text= "These default data cannot be overwritten. ").pack()
            clear_frame1()
            a = tk.Label (frame1, text = "Dataframe viewer", fg='white', bg='gray23', font=("Helvetica", 16))
            a.pack(padx=10, pady=10)   
            tk.Label(frame1, text = "Data before deletion").pack()
            WorkingData(frame1)        
            
            # Ask the user to select a row ID 
            clear_frame2()
            vv = tk.IntVar()
            tk.Label(frame2, text= "Write ID of the row you wish to delete:").pack(padx=10, pady=10)
            e = tk.Entry(frame2, textvariable=vv, width=35)
            e.pack(padx=10, pady=10)
            
            # Define what happens after pushing the Confirm Deletion button
            def show_after_deletion():
                
                # Get the user-input value from the Entry object
                e_text=e.get()
                # Drop the row containing a specific ID defined in Entry:
                global df_working
                df_after_drop = df_working.drop(df_working[df_working['id'] == int(e_text)].index) 
                
                # Display the updated table after dropping/deletion of data
                class TableAfterDrop:
                    def __init__(self, frame1):
                        self.frame = tk.Frame(frame1)
                        self.frame.pack(padx=10, pady=10)
                        self.table = Table(self.frame, dataframe=df_after_drop, height = 140, width = 670)
                        self.table.show()
                clear_frame1()
                a = tk.Label (frame1, text = "Dataframe viewer", fg='white', bg='gray23', font=("Helvetica", 16))
                a.pack(padx=10, pady=10)
                tk.Label(frame1, text= "Table after deletion:").pack()
                TableAfterDrop(frame1)
                # Update the working dataframe with post-deletion data
                df_working = df_after_drop
                    
            # This confirmation button shows the table after deletion
            w = tk.Button(frame2, text= "Confirm deletion", command = show_after_deletion, fg='white', bg='gray23', font=("Helvetica", 11)) 
            w.pack(padx=10, pady=10) 


        # EDIT        
        
        def editing_validation():
            try: 
                df_working != None 
            except:
                tk.messagebox.showwarning(title="Attention", message="Open a file first.")
            else: 
                editing()
        
        def editing():
            # Unhide Frame2 if necessary 
            frame1.pack(side="left", padx=10, pady=10)
            frame2.pack(side="right", padx=10, pady=10)
            # Display the latest working data
            class WorkingData:
                def __init__(self, frame1):
                    self.frame = tk.Frame(frame1) 
                    self.frame.pack(padx=10, pady=10)
                    self.table = Table(self.frame, dataframe=df_working, height = 140, width = 680)
                    self.table.show()
            # Display the table 
            clear_frame1()
            a = tk.Label (frame1, text = "Dataframe viewer", fg='white', bg='gray23', font=("Helvetica", 16))
            a.pack(padx=10, pady=10)
            a = tk.Label (frame1, text = "Working data")
            a.pack(padx=10, pady=10)
            WorkingData(frame1)
                    
            # In Frame 2 the user shall write a surnameand confirm with a button
            clear_frame2()
            vv = tk.IntVar()
            tk.Label(frame2, text= "Write surname of the person to edit:").pack(padx=10, pady=10)
            e = tk.Entry(frame2, textvariable=vv, width=35)
            e.pack(padx=10, pady=10) 

            
            # Define what happens after a button confirms the input surname
            def get_person_value():        
                # Get the user input surname from the Entry object
                e_text=e.get()
                # Find a row containing the entered surname
                # Extract the row into a separate tiny dataframe df_find
                df_find = df_working.loc[df_working["surname"] == e_text]
                # Identify the row number
                global row_number
                row_number = df_working.index.get_loc(df_working[df_working['surname'] == e_text].index[0])
                # Construct a table showing only the one person   
                clear_frame1()
                class TableFind:
                    def __init__(self, frame1):
                        self.frame = tk.Frame(frame1)
                        self.frame.pack(padx=10, pady=10)
                        self.table = Table(self.frame, dataframe=df_find, height = 140, width = 680)
                        self.table.show()
                # Display the table with the one selected person                
                a = tk.Label (frame1, text = "Dataframe viewer", fg='white', bg='gray23', font=("Helvetica", 16))
                a.pack(padx=10, pady=10)
                tk.Label(frame1, text= "Selected person:").pack()
                TableFind(frame1)
                            
                # Wipe Frame2 clean
                # Then ask the user to input new values for the employee (name, surname, phone...)                             
                clear_frame2()
                # What the user inputs in the Entry object is interpreted by the Textvariable
                # Later, user input values will have to be extracted by a .get method
                iv0 = tk.IntVar()
                sv1 = tk.StringVar()
                sv2 = tk.StringVar()        
                sv3 = tk.StringVar()        
                sv4 = tk.StringVar()
                iv2 = tk.IntVar()    
                
                tk.Label(frame2, text= "id:").pack()
                id2_entry = tk.Entry(frame2, textvariable=iv0, width=35)
                id2_entry.pack(padx=10, pady=10)

                tk.Label(frame2, text= "surname:").pack()
                surname2_entry = tk.Entry(frame2, textvariable=sv1, width=35)
                surname2_entry.pack(padx=10, pady=10)
                        
                tk.Label(frame2, text= "name:").pack()
                name2_entry = tk.Entry(frame2, textvariable=sv2, width=35)
                name2_entry.pack(padx=10, pady=10)

                tk.Label(frame2, text= "suffix:").pack()
                suffix2_entry = tk.Entry(frame2, textvariable=sv3, width=35)
                suffix2_entry.pack(padx=10, pady=10)
                        
                tk.Label(frame2, text= "email:").pack()
                email2_entry = tk.Entry(frame2, textvariable=sv4, width=35)
                email2_entry.pack(padx=10, pady=10)
                
                tk.Label(frame2, text= "phone:").pack()
                phone2_entry = tk.Entry(frame2, textvariable=iv2, width=35)
                phone2_entry.pack(padx=10, pady=10)

                # Display all
                def display_all():                                       
                    global df_working  
                    global row_number
                    # This finds the row and column and replaces the text there 
                    df_working.loc[row_number, 'id'] = id2
                    df_working.loc[row_number, 'surname'] = surname2
                    df_working.loc[row_number, 'name'] = name2
                    df_working.loc[row_number, 'suffix'] = suffix2
                    df_working.loc[row_number, 'email'] = email2
                    df_working.loc[row_number, 'phone'] = phone2
                    # The dataframe df_working remains, only some text has changed in it
                    # Use the working dataframe with .loc edited values    
                    # Then show the new values in a table       
                    class AfterEditing:
                        def __init__(self, frame1):
                            self.frame = tk.Frame(frame1)
                            self.frame.pack(padx=10, pady=10)
                            self.table = Table(self.frame, dataframe=df_working, height = 140, width = 680)
                            self.table.show()
                    clear_frame1()
                    a = tk.Label (frame1, text = "Dataframe viewer", fg='white', bg='gray23', font=("Helvetica", 16))
                    a.pack(padx=10, pady=10)
                    tk.Label(frame1, text= "Table with edited data: ").pack()
                    AfterEditing(frame1)
                                   
                def validate_all():
                    # Get the user-input data from the Entry objects
                    # Then examine the data
                    global id2, surname2, name2, suffix2, email2, phone2
                    id2 = id2_entry.get()
                    surname2=surname2_entry.get() 
                    name2=name2_entry.get()  
                    suffix2=suffix2_entry.get()
                    email2=email2_entry.get()
                    phone2=phone2_entry.get()
                    if len(id2)<1 or len(surname2)<1 or len(name2)< 1 or len(suffix2) <1 or len(email2)<1 or len(phone2)<1: 
                        tk.messagebox.showwarning(title="Attention", message="All fields must be filled in!")
                        get_person_value()
                    else:
                        display_all()                                                     
                
                # A button to save the new employee values 
                # It displays the changes in an updated table
                save_button = tk.Button(frame2, text= "Save changes", command = validate_all, fg='white', bg='gray23', font=("Helvetica", 12))
                save_button.pack(padx=10, pady=10)            
                               
            # A button to confirm selection of one person   
            xxx = tk.Button(frame2, text= "Edit", command = get_person_value, fg='white', bg='gray23', font=("Helvetica", 11))
            xxx.pack(padx=10, pady=10)  
        
        # SEARCH
        
        def searching_validation():
            try: 
                df_working != None 
            except:
                tk.messagebox.showwarning(title="Attention", message="Open a file first.")
            else: 
                searching()
        
        def searching():
            # Unhide Frame2 if necessary         
            frame1.pack(side="left", padx=10, pady=10)
            frame2.pack(side="right", padx=10, pady=10)
            # Create a table with the working data
            class WorkingData:
                def __init__(self, frame1):
                    self.frame = tk.Frame(frame1) 
                    self.frame.pack(padx=10, pady=10)
                    self.table = Table(self.frame, dataframe=df_working, height = 140, width = 680)
                    self.table.show()
            # Display the table tk.Label(frame1, text= "These default data cannot be overwritten. ").pack()
            clear_frame1()
            clear_frame2()
            a = tk.Label (frame1, text = "Dataframe viewer", fg='white', bg='gray23', font=("Helvetica", 16))
            a.pack(padx=10, pady=10)
            tk.Label(frame1, text= "Working data").pack()
            WorkingData(frame1)        
                                    
            # Ask the user to write a surname
            vv = tk.IntVar()
            l = tk.Label(frame2, text= "Write surname of the person to display:").pack(padx=10, pady=10)
            e = tk.Entry(frame2, textvariable=vv, width=35)
            e.pack(padx=10, pady=10)

            # Define what happens after the Confirm button is pushed
            # We need to make sure the input data is OK
            def validating():
                if df_working['surname'].eq(e.get()).any() == False:
                    tk.messagebox.showwarning(title="Attention", message="Select a surname!")
                else:
                    display_one() 

            # Define what happens after pushing the confirmation button
            # Data about a single employee will be shown
            def display_one():
                class TableFind:
                    # Get a user-input value from the Enter object
                    e_text=e.get()
                    # Use the .loc method to identify a specific row containing something
                    global df_find
                    df_find = df_working.loc[df_working["surname"] == e_text]
                    # In a new window show a mini table with only one person 
                    def __init__(self, frame1):
                        self.frame = tk.Frame(frame1)
                        self.frame.pack(padx=10, pady=10)
                        self.table = Table(self.frame, dataframe=df_find, height = 140, width = 680)
                        self.table.show()        
                clear_frame1()
                a = tk.Label (frame1, text = "Dataframe viewer", fg='white', bg='gray23', font=("Helvetica", 16))
                a.pack(padx=10, pady=10)
                tk.Label(frame1, text= "Selected person:").pack(padx=10, pady=10)
                TableFind(frame1)                     

            # A button to display the selected person 
            w = tk.Button(frame2, text= "Confirm", command = validating, fg='white', bg='gray23', font=("Helvetica", 11))
            w.pack(padx=10, pady=10)  

        # CREATE A MENU FOR THE ROOT WINDOW
        menubar = Menu(root) 
        filemenu = Menu(menubar, tearoff=0, background='cyan')         
        filemenu.add_command(label="Open", command=open)
        filemenu.add_command(label="Save", command=export_validation)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quitting)
        menubar.add_cascade(label="File", menu=filemenu)
        editmenu = Menu(menubar, tearoff=0, background='cyan')
        editmenu.add_separator()
        editmenu.add_command(label="Sort", command=sorting_validation)
        editmenu.add_command(label="Add", command=adding_validation)
        editmenu.add_command(label="Delete", command=deletion_validation)
        editmenu.add_command(label="Edit", command=editing_validation)
        editmenu.add_command(label="Search", command=searching_validation)
        menubar.add_cascade(label="Manage", menu=editmenu)
        root.config(menu=menubar)

        root.mainloop()
               
# Define the login process                      
def login():  
    sv1 = StringVar
    iv1 = IntVar   

    tk.Label(login_frame, text= "User name").pack(pady=12,padx=10)
    global user_entry
    user_entry = tk.Entry(login_frame, textvariable= sv1, width=35)
    user_entry.pack(pady=12,padx=10)
    user_entry.get()
    
    tk.Label(login_frame, text="Password").pack(pady=12,padx=10)
    global user_pass
    user_pass = tk.Entry (login_frame, textvariable= iv1, width=35)
    user_pass.pack(pady=12,padx=10) 
    user_pass.get()

    butt = tk.Button(login_frame, text= "Log in", command=start_program, fg='white', bg='gray23', font=("Helvetica", 12))
    butt.pack(pady=12,padx=10)

    def hint():
        tk.messagebox.showinfo(title="Hint", message= "User name: User. Password: 12345")
        
    hnt = tk.Button(login_frame, text= "Hint", command=hint)
    hnt.pack(pady=12,padx=10)

# Start the login process      
login()

logapp.mainloop() 