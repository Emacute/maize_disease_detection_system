import streamlit as st
import sqlite3
import hashlib
from streamlit_option_menu import option_menu
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
from skimage.io import imread
from skimage.transform import resize



def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False


conn = sqlite3.connect('data.db')
c = conn.cursor()


def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username, password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)', (username, password))
    conn.commit()


def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    return data


import numpy as np


def main():
    
    ## Home page
    choice = option_menu(
        menu_title=None,
        options=['Home', 'Login', 'Signup'],
        icons=['house', 'book', 'envelope'],
        menu_icon='cast',  # optional
        default_index=0,
        orientation='horizontal'

    )
    if choice == 'Home':

        st.subheader('Home')
    elif choice == 'Login':
        st.sidebar.subheader('Login section')
        user = st.sidebar.text_input('User Name')
        passwd = st.sidebar.text_input('Password', type='password')
        if st.sidebar.checkbox('Login'):
            # if password == '1234':
            create_usertable()
            hashed_pswd = make_hashes(passwd)
            result = login_user(user, check_hashes(passwd, hashed_pswd))
            if result:

                st.success('Logged In as {}'.format(user))
                with st.sidebar:
                    task = option_menu(
                        menu_title=None,
                        options=['Prediction', 'view profile', 'Edit profile'],
                        icons=['house', 'book', 'envolope'],
                        menu_icon='cast',  # optional
                        default_index=0,

                    )

                if task == 'Prediction':
                    st.subheader('You can upload your image for prediction')
                    st.text('Upload image')
                    MODEL = tf.keras.models.load_model("models/1")
                    upload_file = st.file_uploader('Choose an image...', type='jpg')
                    if upload_file is not None:
                        img = Image.open(upload_file)
                        st.image(img, caption='uploaded Image')

                        if st.button('PREDICT'):
                            CLASS_NAMES = ['Blight', 'Common_Rust', 'Gray_Leaf_Spot', 'Healthy']
                            st.write('Result...')
                            img_batch = np.expand_dims(img, 0)
                            predictions = MODEL.predict(img_batch)
                            predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
                            st.title(f'PREDICTED OUTPUT: {predicted_class}')
                            confidence = np.max(predictions[0])
                            st.write(confidence)
                elif task == 'analytic':
                    st.subheader('analyze')
                elif task == 'check profile':
                    st.subheader('my profile')
            else:
                st.warning('Incorrect username/password please enter corect informations')
    elif choice == 'Signup':
        st.subheader('create new account')
        new_user = st.text_input('Username')
        new_passwd = st.text_input('Password', type='password')
        if st.button('signup'):
            create_usertable()
            add_userdata(new_user, make_hashes(new_passwd))
            st.success('You have successfully created an account')
            st.info('You can go to login menu')


if __name__ == '__main__':
    main()
