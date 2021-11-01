from os import name
from numpy import e
import streamlit as st
import pandas as pd
import hashlib
import sqlite3 

class User:
    # Security
    #passlib,hashlib,bcrypt,scrypt
    def __init__(self):     
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()
        self.create_usertable()

    def make_hashes(self,password):
        return hashlib.sha256(str.encode(password)).hexdigest()

    def check_hashes(self,password,hashed_text):
        if self.make_hashes(password) == hashed_text:
            return hashed_text
        return False
   
    def create_usertable(self):
        self.c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


    def add_userdata(self,username,password):
        self.c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,self.make_hashes(password)))
        self.conn.commit()

    def login_user(self,username,password):
        if username == 'admin' and password == 'test':
            user_role = 'admin'
            data = ('admin','*****')
        else:
            user_role = 'user'
            self.c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,self.make_hashes(password)))
            data = self.c.fetchall()
        return user_role,data

    def view_all_users(self):
        self.c.execute('SELECT * FROM userstable')
        data = self.c.fetchall()
        return data


class Role:

    def __init__(self):
        pass




def main():
    """Simple Login App"""

    user = User()

    user.create_usertable()

    
    st.title("Simple Login App")
    basic_menu = ["Home","Login","SignUp"]
    user_menu = ["Home","Secured Page 1","Logout"]
    admin_menu = ["Home","Secured Page 1","Admin Settings","Logout"]

    if 'login' in st.session_state and st.session_state.login == True:
        print("login: True")
        menu = user_menu
    else:
        menu = basic_menu
    
    if 'is_admin' in st.session_state and st.session_state.is_admin == True:
        print("is_admin: True")
        menu = admin_menu
    
    #choice = st.sidebar.selectbox("Menu",menu)

    sidebar_choises = st.sidebar.empty()
    choice = sidebar_choises.radio("Menu",menu,key="sidebar_radios")

    if choice == "Home":
        st.subheader("Home")

    elif choice == "Login":
        st.subheader("Login Section")

        username = st.text_input("Username",key="login_username")
        password = st.text_input("Password",type='password',key="login_password")
        
        
        if st.button("Login"):
        
            role,result = user.login_user(username,password)
            if(role == 'admin'):
        
                choice = sidebar_choises.radio("Menu",admin_menu,key="sidebar_radios")
                st.session_state.is_admin = True
            else:
                
                choice = sidebar_choises.radio("Menu",user_menu,key="sidebar_radios")
                st.session_state.is_admin = False

            if result:
                st.session_state.login = True
                st.success("Logged In as {}".format(username))
                    
            else:
                st.session_state.login = False
                st.warning("Incorrect Username/Password")


    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username",key="key1")
        new_password = st.text_input("Password",type='password')

        if st.button("Signup"):            
            user.add_userdata(new_user,new_password)
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")
   
    elif choice == "Admin Settings":       
        st.subheader("User Profiles")
        task = st.selectbox("Task",["Profiles"])
        if task == "Profiles":
            user_result = user.view_all_users()
            clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
            st.dataframe(clean_db)

    elif choice == "Logout":
        choice = sidebar_choises.radio("Menu",basic_menu,key="sidebar_radios")
        st.subheader("Logout")
        st.session_state.login = False
        st.session_state.is_admin = False


if __name__ == '__main__':
    main()
