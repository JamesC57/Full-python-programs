import sqlite3 as sql
from customtkinter import *
import bcrypt
from PIL import Image
import pathlib as Path

def remove_frames(s):
    for widget in s.window.winfo_children():  # Iterate over all child widgets
        if isinstance(widget, CTkFrame):  # Check if widget is a frame
            widget.destroy()  # Destroy the frame

#am I effectively using colours
class menus:
    def __init__(s,window):
        s.window = window
    def open_option(s,var):
        print(var,"pressed")
    def top_bar(s):
        s.menu_frame = CTkFrame(s.window, height=50)
        my_image = CTkImage(Image.open(Path.Path(__file__).parent / 'icon.ico'),
                                  size=(50,50))
        #int(s.window.winfo_width),int(s.window.winfo_height))
        image = CTkLabel(s.menu_frame, image=my_image,text="")
        image.grid(row=0,column=0)
        s.menu_dropdown = CTkOptionMenu(s.menu_frame,values=["option 1","option 2","option 3"],command=s.open_option)
        s.menu_dropdown.grid(row=0,column=1)
        s.menu_frame.pack(fill=X)
      

class logins:
    def __init__(s,window):
        s.window = window
                    
    def remove_label(s):
        try:
            s.valid_label.destroy()
        except Exception:
            pass
        
    def signup_valid_details(s):
        valid = True
        if s.email_input.get() in s.email_list:
            valid = "An account with that email exists" 
        elif "@" not in s.email_input.get():
            valid = "Email is invalid" 
        elif len(s.email_input.get()) < 8:
            valid = "Email is too short"
        elif len(s.password_input.get()) < 5:
            valid = "Passwords need to be longer than 5 characters"
        elif s.password_input.get().isalpha==False and s.password_input.get().isalnum:
            valid = "Password should contain numbers and letters"
        return valid
    
    def signup_submit_function(s):
        s.remove_label()
        db = sql.connect("database.db")
        cursor = db.execute("select email from ACCOUNTS ;")
        s.email_list = []
        for email in cursor:
            s.email_list.append(email[0])
            
        if s.signup_valid_details() == True:
            password = s.password_input.get().encode('utf-8')
            hashed = bcrypt.hashpw(password, bcrypt.gensalt(rounds = 12))
            db.execute("INSERT INTO ACCOUNTS (email, password) VALUES (?, ?);", (s.email_input.get(), hashed))
            db.commit()
            s.valid_label = CTkLabel(s.signup_frame,text="Account Created")
        else:
            s.valid_label = CTkLabel(s.signup_frame,text=s.signup_valid_details())
        s.valid_label.pack()
            
    def sign_up(s):
        remove_frames(s)
        s.signup_frame = CTkFrame(s.window,fg_color = "transparent")
        s.email_input = CTkEntry(s.signup_frame,placeholder_text="Enter your email",width=300,height=50)
        s.password_input = CTkEntry(s.signup_frame,placeholder_text="Enter your password",width=300,height=50)
        s.password_input.configure(show="*")

        page_title = CTkLabel(s.signup_frame,text="Sign up to Rosla",font=("Adobe Gothic Std B",24,"bold"),pady=10,padx=10)

        top_divider = CTkButton(s.signup_frame,command="",text="",border_spacing=15,state="disabled",width=1000,height=50,corner_radius=0) 
        bottom_divider = CTkButton(s.signup_frame,command="",text="",border_spacing=15,state="disabled",width=1000,height=50,corner_radius=0) 


        submit_button = CTkButton(s.signup_frame,text = "submit",command=s.signup_submit_function,border_spacing=15) 
        
        s.create_account_button = CTkButton(s.signup_frame,text = "Already have an account? sign in",
                                          command=s.login_existing,
                                          fg_color="transparent",) 

        top_divider.pack(pady=20,padx=20,expand=True,anchor=CENTER)
        page_title.pack(pady=10,padx=20,expand=True,anchor=CENTER)
        s.email_input.pack(pady=10,padx=20,expand=True,anchor=CENTER)
        s.password_input.pack(pady=10,padx=20,expand=True,anchor=CENTER)
        s.create_account_button.pack(pady=10,padx=20,expand=True,anchor=CENTER)
        submit_button.pack(pady=10,padx=20,expand=True,anchor=CENTER)
        bottom_divider.pack(pady=10,padx=20,expand=True,anchor=CENTER)

        s.signup_frame.pack(expand=True,anchor=CENTER)



    def login_submit_function(s):
        s.remove_label()
        email_input = s.email_input.get()
        password_input = s.password_input.get()
        db = sql.connect("database.db")
        cursor = db.execute("select email,password from ACCOUNTS ;")
        correct_email=False
        for details in cursor:
            if email_input == details[0] and bcrypt.checkpw(password_input.encode('utf-8'), details[1]):
                s.valid_label = CTkLabel(s.login_frame,text="Login Sucessful")
                correct_email=True
                break
            elif email_input == details[0] and bcrypt.checkpw(password_input.encode('utf-8'), details[1])==False:
                s.valid_label = CTkLabel(s.login_frame,text="Incorrect Password")
                correct_email=True
                break
        if correct_email == False:
            s.valid_label = CTkLabel(s.login_frame,text="No account ascociated with that email")
        s.valid_label.pack()
    
    def login_existing(s):
        remove_frames(s)
        s.login_frame = CTkFrame(s.window,fg_color = "transparent")
        s.email_input = CTkEntry(s.login_frame,placeholder_text="Enter your email",width=300,height=50)
        s.password_input = CTkEntry(s.login_frame,placeholder_text="Enter your password",width=300,height=50)
        s.password_input.configure(show="*")

        
        page_title = CTkLabel(s.login_frame,text="Login to your account",font=("Adobe Gothic Std B",24,"bold"),pady=10,padx=10)
        page_title.pack(pady=10,padx=20,expand=True,anchor=CENTER)

        submit_button = CTkButton(s.login_frame,text = "submit",command=s.login_submit_function,border_spacing=15) 
        
        s.create_account_button = CTkButton(s.login_frame,text = "Dont have an account? sign up",
                                          command=s.sign_up,
                                          fg_color="transparent",) 
        s.email_input.pack(pady=10,padx=20,expand=True,anchor=CENTER)
        s.password_input.pack(pady=10,padx=20,expand=True,anchor=CENTER)
        s.create_account_button.pack(pady=10,padx=20,expand=True,anchor=CENTER)
        submit_button.pack(pady=10,padx=20,expand=True,anchor=CENTER)
        s.login_frame.pack(expand=True,anchor=CENTER)
    
    
    def sign_up_login(s):        
        s.choice_frame = CTkFrame(s.window,corner_radius=15)
        signup_button = CTkButton(s.choice_frame,text = "Sign up",fg_color="#e27e7e",command=s.sign_up,hover_color="#8a2020") 
        login_button = CTkButton(s.choice_frame,text = "Login",command=s.login_existing) 
        signup_button.pack(pady=10,padx=20)
        login_button.pack(pady=10,padx=20)
        s.choice_frame.pack(expand=True,anchor=CENTER)
    

     
def create_db():
    data = sql.connect("database.db")#creates the database
    try:
        data.execute("""create table ACCOUNTS 
                    (ACCOUNT_ID integer primary key,
                    email text char(254),
                    password text,
                    first_name text
                    last_name text,
                    address text,
                    phone_number text,
                    admin boolean);""")
        
        data.execute("""create table USER_DATA 
                    (ACCOUNT_ID integer primary key references ACCOUNTS(ACCOUNT_ID),
                    visual_preference text,
                    carbon_footprint text,
                    energy_used int,
                    peak_time text,
                    measurement_range text);""")
        
        data.execute("""create table BOOKINGS 
                    (BOOKING_ID integer primary key,
                    datetime text,
                    customer_id integer references ACCOUNTS(ACCOUNT_ID),
                    staff_id integer references ACCOUNTS(ACCOUNT_ID),
                    booking details text,
                    type text,
                    completed boolean);""")
             
        data.commit()
    except Exception:
        print("database already exists")
    data.close()    
       
       
def create_window():
    #set_default_color_theme(Path.Path(__file__).parent / 'Theme.json')  # Themes: "blue" (standard), "green", "dark-blue"
    set_default_color_theme(Path.Path(__file__).parent / 'HC_theme.json')  # Themes: "blue" (standard), "green", "dark-blue"
    
    window = CTk()
    window.configure()  # Use your theme's bg color
    window.minsize(400,400)
    window.title("Rosla technologies")
    window.attributes('-topmost')
    #window.iconbitmap("icon.ico")
    return window       
    
def main():
    create_db()

    window = create_window()
    menu_frame = menus(window)
    menu_frame.top_bar()
    login_frames=logins(window)
    login_frames.sign_up_login()

    window.mainloop()
    
main()