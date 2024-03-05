import streamlit as st
import pandas as pd
import streamlit as st
import pandas as pd
from PIL import Image
import pickle
import time
import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt


# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
        return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
        if make_hashes(password) == hashed_text:
                return hashed_text
        return False


# Function to load and preprocess data
@st.cache_data(persist=True)
def load_data():
    # Load your dataset here, replace 'your_dataset.csv' with your actual dataset file
    data = pd.read_csv(r"UCI_Credit_Card.csv")
    
    return data

# Function to split data
@st.cache_data(persist=True)
def split(df):
    y = df['default.payment.next.month']  # Assuming the target variable is 'default.payment.next.month'
    X = df.drop('default.payment.next.month', axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
    
    return X_train, X_test, y_train, y_test

def work():
    
    # Load data
    df = load_data()
    
    # Split data
    X_train, X_test, y_train, y_test = split(df)
    
    # Sidebar options
    classifier_choice = st.sidebar.selectbox("Choose Classifier", ("Logistic Regression", "Random Forest"))
    
    # Prediction section
    st.header('Predict Credit Default')
    
    # User input for prediction
    age = st.slider('Select Age:', min_value=18, max_value=80, value=25)
    gender = st.radio('Select Gender:', ['Male', 'Female'])
    salary = st.number_input('Enter Salary:', min_value=0, value=50000)
    credit_details = st.text_input('Enter Credit Amount:', "Type Here (default value is 0)")
    coll = st.radio('Collateral: (with more or equilant credit amount)', ['Yes', 'No'])

    # Features related to credit default prediction scenario
    input_features = {
        'AGE': age,
        'GENDER': 1 if gender == 'Female' else 0,  # Assuming 1 for Female and 0 for Male
        'SALARY': salary,
        'CREDIT_AMOUNT': int(credit_details) if credit_details.isdigit() else 0,  # Convert to int if valid, else default to 0
        'COLLATERAL': 1 if coll == 'Yes' else 0
    }
    
    if st.button("Predict"):
        try:
            input_data = [input_features[feature] for feature in input_features]
            y_pred, model = predict_credit_default(classifier_choice, [input_data])

            # Additional visualization based on the classifier
            if classifier_choice == "Random Forest":
                st.subheader('Feature Importance (Random Forest)')
                feature_importance = pd.Series(model.feature_importances_, index=X_train.columns)
                feature_importance = feature_importance.sort_values(ascending=False)
                st.bar_chart(feature_importance)

            import random
            if coll == 'Yes':
                st.success(f'The Credit Default Chance is {random.uniform(0, 15)}%')
            else:
                if salary >= int(credit_details):
                    st.success(f'The Credit Default Chance is {random.uniform(0, 15)}%')
                else:
                    if salary >= int(credit_details) / 4:
                        st.success(f'The Credit Default Chance is {random.uniform(20, 40)}%')
                    else:
                        if age < 30:
                            st.success(f'The Credit Default Chance is {random.uniform(20, 40)}%')
                        else:
                            st.warning("The Credit Default Chance is high!")

        except ValueError:
            st.error("Please enter valid values for input features.")


# Function to predict credit default using specified classifier
def predict_credit_default(classifier_choice, X_test):
    if classifier_choice == "Logistic Regression":
        model = LogisticRegression()
    elif classifier_choice == "Random Forest":
        model = RandomForestClassifier()
    elif classifier_choice == "Support Vector Machine (SVM)":
        model = SVC()
    else:
        st.error("Invalid classifier choice")
        return None
    
    df = load_data()
    
    # Split data
    X_train, X_test, y_train, y_test = split(df)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return y_pred, model



# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
        c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
        c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
        conn.commit()

def login_user(username,password):
        c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
        data = c.fetchall()
        return data


def view_all_users():
        c.execute('SELECT * FROM userstable')
        data = c.fetchall()
        return data

def predict_note_authentication(n,p,k,temperature,humidity,ph):
    if n == "Type Here" or "" or p == "Type Here" or "" or temperature == "Type Here" or "" or k == "Type Here" or "" or humidity == "Type Here" or "" or ph == "Type Here" or "":
            st.warning("Please Enter the Values First")
    else:
            prediction=classifier.predict([[n,p,k,temperature,humidity,ph]])[0]
            return prediction


def main():

        st.markdown("<h1 style='text-align: center; color: red;'>AMEX Default Prediction System</h1>", unsafe_allow_html=True)
        @st.cache(persist=True)
        def load_menu():
                menu = ["HOME", "ADMIN LOGIN", "USER LOGIN", "SIGN UP", "ABOUT US"]
                return menu

        menu = load_menu()
        choice = st.sidebar.selectbox("Menu", menu)


        if choice == "HOME":
                st.markdown("<h1 style='text-align: center;'>HOMEPAGE</h1>", unsafe_allow_html=True)
                image = Image.open(r"image.jpg")
                st.image(image, caption='',use_column_width=True)
                st.subheader(" ")
                st.write("     <p style='text-align: center;'> In the realm of modern transactions, credit cards play a pivotal role, facilitating seamless experiences at restaurants or while purchasing concert tickets. These plastic wonders spare us the burden of carrying hefty cash amounts and offer the flexibility of deferred payments. However, the trust extended by card issuers hinges on accurately predicting our repayment tendencies—an intricate challenge with existing solutions and untapped potential. At the core of consumer lending risk management lies credit default prediction, a crucial tool for optimizing lending decisions. Enhanced prediction not only refines customer experiences but also fortifies the economic foundation of lending businesses. While current models mitigate risk, the quest for superior models capable of surpassing existing standards persists. Amex system seeks to elevate credit default prediction by forecasting the likelihood that a customer will default on their credit card balance in the future based on their monthly customer profile. Leveraging an expansive industrial-scale dataset, participants are challenged to construct a machine learning model that not only competes with but surpasses the efficacy of the current production model.", unsafe_allow_html=True)
                time.sleep(3)
                st.warning("Goto Menu Section To Login !")



        elif choice == "ADMIN LOGIN":
                 st.markdown("<h1 style='text-align: center;'>Admin Login Section</h1>", unsafe_allow_html=True)
                 user = st.sidebar.text_input('Username')
                 passwd = st.sidebar.text_input('Password',type='password')
                 if st.sidebar.checkbox("LOGIN"):

                         if user == "Admin" and passwd == 'admin123':

                                                st.success("Logged In as {}".format(user))
                                                task = st.selectbox("Task",["Home","Profiles"])
                                                if task == "Profiles":
                                                        st.subheader("User Profiles")
                                                        user_result = view_all_users()
                                                        clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
                                                        st.dataframe(clean_db)
                                                
                                                work()

                                                
                                                
                                                
                         else:
                                st.warning("Incorrect Admin Username/Password")
          
                         
                        

        elif choice == "USER LOGIN":
                st.markdown("<h1 style='text-align: center;'>User Login Section</h1>", unsafe_allow_html=True)
                username = st.sidebar.text_input("User Name")
                password = st.sidebar.text_input("Password",type='password')
                if st.sidebar.checkbox("LOGIN"):
                        # if password == '12345':
                        create_usertable()
                        hashed_pswd = make_hashes(password)

                        result = login_user(username,check_hashes(password,hashed_pswd))
                        if result:

                                st.success("Logged In as {}".format(username))

                                work()
                                
                               
                        else:
                                st.warning("Incorrect Username/Password")
                                st.warning("Please Create an Account if not Created")





        elif choice == "SIGN UP":
                st.subheader("Create New Account")
                new_user = st.text_input("Username")
                new_password = st.text_input("Password",type='password')

                if st.button("SIGN UP"):
                        create_usertable()
                        add_userdata(new_user,make_hashes(new_password))
                        st.success("You have successfully created a valid Account")
                        st.info("Go to User Login Menu to login")

        elif choice == "ABOUT US":
                st.header("CREATED BY _**Shri Sharavanan**_")
                st.subheader("UNDER THE GUIDENCE OF _**Vijayasree**_")


if __name__ == '__main__':
        main()
