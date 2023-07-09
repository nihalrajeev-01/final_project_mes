import streamlit_authenticator as stauth

import postgreData as db

usernames = ["john", "john2","john3","john4" ]
names = ["John 1", "John 2", "John 3", "John 4"]
passwords = ["1234", "1234", "1234", "1234"]
hashed_passwords = stauth.Hasher(passwords).generate()


for (username, name, hash_password) in zip(usernames, names, hashed_passwords):
    db.insert_user(username, name, hash_password)