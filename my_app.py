from flask import Flask,redirect, url_for, render_template,request,jsonify,make_response, session,flash
import urllib.request,json
import requests
import json
import message
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


# -------------------------------------------------------------#
        # DOMAIN NAME CONTROL
# -------------------------------------------------------------#
@app.route('/')
def display_index_page():
    return redirect(url_for('login'))


# domail_name = "http://reachlovenheal.com:"
domail_name = "http://185.199.53.169:"
port_name = "8080"
base_url = f'{domail_name}{port_name}'

# -------------------------------------------------------------#
        # THIS ROUTE FOR DISPLAY LOGIN PAGE
# -------------------------------------------------------------#
@app.route('/login')
def login():
    session.clear()
    return render_template('UserAuth/login.html')


# -------------------------------------------------------------#
        # THIS FUNCTION FOR POST LOGIN FORM
# -------------------------------------------------------------#
@app.route('/login',methods=['POST'])
def authenticate():
    # GET DATA FROM REQUEST / FORM DATA
    mobile_no = request.form.get('username')
    country_code = request.form.get('country_code')
    username = f'+{country_code}{mobile_no}'
    password = request.form.get('password')
    response = userAuthenticate(username,password)
    data = response.json()

    if response.status_code == 200:
        
        json_str = json.dumps(data) # Convert JSON object to string
        
        # set cookie
        resp = make_response(redirect(url_for('dashboard')))
        resp.set_cookie('user_data',json_str)
        return resp
    else:
        message = data.get('message')
        
        # If user account allready created but user not confirm his mobile no
        # resend otp to verify 
        if message == "User is not Confirmed":
            if resend_otp(username):
                username = session['username']
                return redirect(url_for('otp'))
        
        password_error_message = None
        username_error_message = None
        if message == "Unauthorized":
            password_error_message = "Invalid password"
        else:
            username_error_message = "Invalid username"
        return render_template('UserAuth/login.html',password_error_message = password_error_message,mobile_no=mobile_no,username_error_message=username_error_message)
        
        
         
    
# -------------------------------------------------------------#
        # THIS ROUTE FOR SIGNUP GET AND POST
# -------------------------------------------------------------#
@app.route('/sign-up')
def displaySignUpPage():
    session.clear()
    return render_template('UserAuth/sign-up.html')

@app.route('/sign-up',methods=['POST'])
def signUp():
    # GET DATA FROM REQUEST / FORM DATA
    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')
    
    if request.form.get('gender'):
        gender = request.form.get('gender').upper()
    else:
        gender = None
    if request.form.get('email'):
        email = request.form.get('email')
    else:
        email = None

    mobile_no = request.form.get('username')
    country_code = request.form.get('country_code')
    username = f'+{country_code}{mobile_no}'
    password = request.form.get('signUpPassword')
    confirmPassword = request.form.get('signUpConfirmPassword')

    # IF PASSWORD AND CONFIRM PASSWORD NOT MATCH
    if password != confirmPassword:
        message = "Password and Confirm password not match"
        return render_template('UserAuth/sign-up.html',error_message=message)


    response = createUser(firstName,lastName,gender,email,username,password)
    data = response.json()

    if response.status_code == 200:
        
        session['username'] = username
        return redirect('/otp-verification')
    else:
        message = "A user already exists with this username"
        return render_template('UserAuth/sign-up.html',error_message=message)


     
# -------------------------------------------------------------#
        # THIS ROUTE SIGN-UP OTP VERIFICATION
# -------------------------------------------------------------#
@app.route('/otp-verification')
def otp():

    if 'username' in session:
        # If 'user_data' exists, retrieve it
        username = session['username']
    else:
        return redirect(url_for('login'))
    
    return render_template("UserAuth/sign-up-user-otp-verification.html")

@app.route('/otp-verification',methods=["POST"])
def verifyOTP():
    
    if 'username' in session:
        # If 'user_data' exists, retrieve it
        username = session['username']
    else:
        message = "Username not found or not set."
        return render_template('UserAuth/login.html',error_message = message)
    
    f1 = request.form.get('f1')
    f2 = request.form.get('f2')
    f3 = request.form.get('f3')
    f4 = request.form.get('f4')
    f5 = request.form.get('f5')
    f6 = request.form.get('f6')

    otpcode = f1+f2+f3+f4+f5+f6
    if len(otpcode) != 6:
        message = "Please enter valid otp. Otp should be 6 digits."
        return render_template('UserAuth/sign-up-user-otp-verification.html',error_message = message)
    
    response = verifyUser(username,otpcode)
    

    if response.status_code == 200:
        if 'username' in session:
            # If 'user_data' exists, delete
            session.pop('username')
        message = "OTP code verified successfully. Please Login with your username and password."
        return render_template('UserAuth/sign-up-user-otp-verification.html',success_message = message)
    else:
        message = "OTP is invalid. Please enter correct OTP."
        return render_template('UserAuth/sign-up-user-otp-verification.html',error_message=message)
        




# -------------------------------------------------------------#
        # THIS ROUTE FOR DASHBOARD
# -------------------------------------------------------------#
@app.route('/dashboard')
def dashboard():
    user = access_user_data_from_coocki()
    if user:
        first_name = user.get('firstName')
    else:
        return redirect(url_for('login'))
    
    return render_template('Auth-user/dashboard.html',first_name=first_name)





# -------------------------------------------------------------#
        # THIS ROUTE FOR CHANGE USER PASSWORD 
        # Display the Username / Mobile number
# -------------------------------------------------------------#
@app.route('/user-change-password')
def dislay_user_detail():
    user = access_user_data_from_coocki()
    if user:
        user_phone_number = user.get('username')
    else:
        return redirect(url_for('login'))
    
    phone = display_last_four_digits(user_phone_number)
    return render_template('Auth-user/user-change-password-one.html',phone=phone)

# Change Password - post
@app.route('/user-change-password',methods=['POST'])
def sent_top_to_user_phone():

    user = access_user_data_from_coocki()
    username = user.get('username')
    response = reset_user_password(username) 
    data = response.json()


    if response.status_code == 200:

        # This message var cantain responce message after sendind otp
        # message = data.get('otpCode') 
        # return render_template('Auth-user/user-change-password-one.html',success_message= message)
        return redirect(url_for('display_otp_verification_page'))
        
    else:
        message = data.get('errors').get('message')
        user = access_user_data_from_coocki()
        user_phone_number = user.get('username')
        phone = display_last_four_digits(user_phone_number)
        return render_template('Auth-user/user-change-password-one.html',phone=phone,error_message= message)
    

# -------------------------------------------------------------#
        # THIS ROUTE FOR CHANGE USER PASSWORD 
        # Verify OTP PAGE / VERIFY OTP
# -------------------------------------------------------------#
@app.route('/user-verify-otp')
def display_otp_verification_page():
    return render_template('Auth-user/user-change-password-two.html')

# CHANGE USER PASSWORD - POST - VERIFY OTP
@app.route('/user-verify-otp',methods=['POST'])
def user_verify_otp():
    # access username from coocki
    user = access_user_data_from_coocki()
    username = user.get('username')

    f1 = request.form.get('f1')
    f2 = request.form.get('f2')
    f3 = request.form.get('f3')
    f4 = request.form.get('f4')
    f5 = request.form.get('f5')
    f6 = request.form.get('f6')

    otpCode = f1+f2+f3+f4+f5+f6
    if len(otpCode)!= 6:
        message = "OTP length should be 6 digit."
        return render_template('Auth-user/user-change-password-two.html',error_message=message)
    
    response = verify_user_otp(username,otpCode)
    
    if response.status_code == 200:
        session['otpCode'] = otpCode
        return redirect(url_for('display_user_update_password_page'))
    else:
        message = "OTP is invalid. Please enter correct OTP."
        return render_template('Auth-user/user-change-password-two.html',error_message=message)
        
    
# -------------------------------------------------------------#
        # THIS ROUTE FOR CHANGE USER PASSWORD 
        # UPDATE USER PASSWORD , display page
        # upadte user passwod - post method
# -------------------------------------------------------------#
@app.route('/user-update-password')
def display_user_update_password_page():
    return render_template('Auth-user/user-change-password-three.html')

# CHANGE USER PASSWORD -3 POST
@app.route('/user-update-password',methods=['POST'])
def user_update_password():
    # access username from coocki
    user = access_user_data_from_coocki()
    username = user.get('username')

    # Check otpCode found or not from session.
    if 'otpCode' in session:
        otpCode = session['otpCode']
    else:
        return redirect(url_for('dashboard'))
    
    # check new password and confirm password same or not.
    if request.form.get('new_password') != request.form.get('Confirm_new_password'):
        message = "New password and confirm password not match"
        return render_template('Auth-user/user-change-password-three.html',error_message=message)
    
    new_password = request.form.get('new_password')

    response = change_user_password(username,otpCode,new_password)
    if response.status_code == 200:
        data = response.json()
        message = "Your password is updated successfully. Please login again with your new password."
        # Delete the username and otp code after the change password
        session.pop('otpCode', None)

        # Create a response object
        resp = make_response(render_template('Auth-user/user-change-password-three.html',success_message=message))
    
        # Set the cookie with an expiration date in the past/ delete cookie
        resp.set_cookie('user_data', expires=0)
        return resp
    

    else:
        data = response.json()
        message = data.get('errors').get('message')
        return render_template('Auth-user/user-change-password-three.html',error_message=message)
    






    

# -------------------------------------------------------------#
        # THIS ROUTE FOR FORGET-PASSWORD
# -------------------------------------------------------------#
@app.route('/forgot-password')
def displayForgotPasswordPage():
    return render_template('UserAuth/forgot-password-step-one.html')

# -------------------------------------------------------------#
    # THIS ROUTE FOR FORGET-PASSWORD
    # call reset passwordapi it will genrate otp
# -------------------------------------------------------------#
@app.route('/forgot-password',methods=['POST'])
def send_otp_for_reset_password():
    # Call user reset password function 
    mobile_no = request.form.get('username')
    country_code = request.form.get('country_code')
    username = f'+{country_code}{mobile_no}'
    
    # Check the phone number length
    if len(username) != 13:
        message = "Phone number should be 10 digits for Country code india."
        return render_template('UserAuth/forgot-password-step-one.html',error_message= message)
    
    response = reset_user_password(username) 
    data = response.json()
    if response.status_code == 200:
        session['username'] = username
        message = data.get('otpCode')
        # return render_template('UserAuth/forgot-password-step-one.html',success_message= message)
        return redirect(url_for('display_forgot_password_verify_otp'))
    else:
        message = data.get('errors').get('message')
        return render_template('UserAuth/forgot-password-step-one.html',error_message= message)


# -------------------------------------------------------------#
    # THIS ROUTE FOR FORGET-PASSWORD
    # Display forgot-password-verify-otp-step-2 page otp , 
    # otp genrate by reset password
# -------------------------------------------------------------#
@app.route('/verify-user-otp')
def display_forgot_password_verify_otp():
    return render_template('UserAuth/forgot-password-verify-otp-step-2.html')

# -------------------------------------------------------------#
    # THIS ROUTE FOR FORGET-PASSWORD
    # Verify user otp , otp genrate by reset password
# -------------------------------------------------------------#
@app.route('/verify-user-otp',methods=['POST'])
def forgot_password_verify_otp():
    if 'username' in session:
        # If 'user_data' exists, retrieve it
        username = session['username']
    else:
        return redirect('url_for(login)')
    
    f1 = request.form.get('f1')
    f2 = request.form.get('f2')
    f3 = request.form.get('f3')
    f4 = request.form.get('f4')
    f5 = request.form.get('f5')
    f6 = request.form.get('f6')

    otpCode = f1+f2+f3+f4+f5+f6
    if len(otpCode)!= 6:
        message = "OTP length should be 6 digit."
        return render_template('UserAuth/forgot-password-verify-otp-step-2.html',error_message=message)
    
    response = verify_user_otp(username,otpCode)
    
    if response.status_code == 200:
        session['otpCode'] = otpCode
        return redirect(url_for('display_change_password'))
    else:
        message = "OTP is invalid. Please enter correct OTP."
        return render_template('UserAuth/forgot-password-verify-otp-step-2.html',error_message=message)
        


# -------------------------------------------------------------#
    # THIS ROUTE FOR FORGET-PASSWORD
    # Display Change password
# -------------------------------------------------------------#
@app.route('/change-user-password')
def display_change_password():
    return render_template('UserAuth/forgot-password-change-password.html')


# -------------------------------------------------------------#
    # THIS ROUTE FOR FORGET-PASSWORD
    # Update new password
# -------------------------------------------------------------#
@app.route('/change-user-password',methods=['POST'])
def update_user_password():

    # Check username found or not from session.
    if 'username' in session:
        username = session['username']
    else:
        return redirect('url_for(displayForgotPasswordPage)')
    
    # Check otpCode found or not from session.
    if 'otpCode' in session:
        otpCode = session['otpCode']
    else:
        return redirect(url_for(displayForgotPasswordPage))
    
    # check new password and confirm password same or not.
    if request.form.get('new_password') != request.form.get('Confirm_new_password'):
        message = "New password and confirm password not match"
        return render_template('UserAuth/forgot-password-change-password.html',error_message=message)
    
    new_password = request.form.get('new_password')

    response = change_user_password(username,otpCode,new_password)
    if response.status_code == 200:
        data = response.json()
        message = "Your password has been change successfully. Please Login with your new password"

        # Delete the username and otp code after the change password
        session.pop('username', None) 
        session.pop('otpCode', None)

        return render_template('UserAuth/forgot-password-change-password.html',success_message=message)
    else:
        data = response.json()
        message = data.get('errors').get('message')
        return render_template('UserAuth/forgot-password-change-password.html',error_message=message)
    



# -------------------------------------------------------------#
            # ROUTE FOR LOG-OUT
# -------------------------------------------------------------#
@app.route('/logout')
def logout():
    response = user_logout()
    if response.status_code == 200:
        message = response.text

        # Delete the username and otp code after the change password
        session.pop('otpCode', None)
        session.clear()

        # Create a response object COOKI DELETED
        resp = make_response(render_template('Auth-user/dashboard.html',success_message=message))
        resp.set_cookie('user_data', expires=0)
        return resp
    else:
        message = "Unauthorized"
        return render_template('Auth-user/dashboard.html',error_message=message)
        

# -------------------------------------------------------------#
            # API RE-SEND OTP
# -------------------------------------------------------------#
@app.route('/re-send-otp')
def otp_resend():
    username = None
    if 'username' in session:
        username = session['username']

    user = access_user_data_from_coocki()
    if user:
        username = user.get('username')

    if username == None:
        return "User Not found"
    
    if resend_otp(username):
        session['otp_message'] = "OTP sent successfully"
        return redirect(request.referrer)
    else:
        session['otp_message'] = "OTP Not sent"
        return redirect(request.referrer)
    

# -------------------------------------------------------------#
            # API CALLING FUNCTIONS
# -------------------------------------------------------------#

def userAuthenticate(username,password):
    # THIS IS API RUL
    # url = 'http://185.199.53.169:8080/core/auth/public/login'
    url = f'{base_url}/core/auth/public/login'
    
    # HEADERS
    headers = {
        'accept': '',
        'Content-Type': 'application/json'
    }
    
    # DATA SENT BY POST REQUEST
    body = {
        'username': username,
        'password': password,
    }

    # POST request to the API and stored result in responce veriable
    response = requests.post(url, headers=headers, json=body)
    return response

def createUser(first_name,last_name,gender,email,username,password):
    # THIS IS END POINT FOR API RUL
    url = f'{base_url}/core/auth/public/signup'
    
    # HEADERS
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    # DATA SENT BY POST REQUEST
    body = {
        'first_name':first_name,
        'last_name': last_name,
        'gender': gender,
        'email': email,
        'userType': "test user",
        'username': username,
        'password': password,
    }

    # POST request to the API and stored result in responce veriable
    response = requests.post(url, headers=headers, json=body)
    return response


def verifyUser(username,otpcode):
    # THIS IS END POINT FOR API RUL
    url = f'{base_url}/core/auth/public/confirmOtp'
    
    # HEADERS
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    # DATA SENT BY POST REQUEST
    body = {
        'otpCode' : otpcode,
        'username' : username,
    }

    # POST request to the API and stored result in responce veriable
    response = requests.post(url, headers=headers, json=body)
    return response

def reset_user_password(username):

    # api url for reset password 
    # if the user exist send to otp to their registerd mobile no.
    url = f'{base_url}/core/auth/public/resetpassword'
    
    # HEADERS
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    # DATA SENT BY POST REQUEST
    body = {
        'username' : username,
    }

    # POST request to the API and stored result in responce veriable
    response = requests.post(url, headers=headers, json=body)
    return response


def verify_user_otp(username,otpCode):
    # api url for verify otp 
    # if the otp is valid then it will not return status code 200.
    url = f'{base_url}/core/auth/public/confirmOtp'
    
    # HEADERS
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    # DATA SENT BY POST REQUEST
    body = {
        'username' : username,
        "otpCode": otpCode,
    }

    # POST request to the API and stored result in responce veriable
    response = requests.post(url, headers=headers, json=body)
    return response

def change_user_password(username,otpCode,new_password):
    # api url for change password 
    # if the otp is valid then it will not return status code 200.
    url = f'{base_url}/core/auth/public/changepassword'
    
    # HEADERS
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    # DATA SENT BY POST REQUEST
    body = {
        'username' : username,
        "otpCode": otpCode,
        "newPassword": new_password,
    }

    # POST request to the API and stored result in responce veriable
    response = requests.post(url, headers=headers, json=body)
    return response


def user_logout():
    session.clear()
    url = f'{base_url}/core/auth/logout'
    # access username from coocki
    user = access_user_data_from_coocki()
    accessToken = user.get('accessToken')

    headers = {
        'Authorization': 'Bearer ' + accessToken,
        'Accept': 'application/json'
    }

    response = requests.post(url, headers=headers)
    return response

    
def resend_otp(username):
    # url for resend otp
    url = f'{base_url}/core/auth/public/resendOtp'
    
    # HEADERS
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    # DATA SENT BY POST REQUEST
    body = {
        'username' : username,
    }

    # POST request to the API and stored result in responce veriable
    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        return True
    else:
        return False


def access_user_data_from_coocki():
    # ACCESS COOKIE
    user = request.cookies.get('user_data')
    if user:
        user_data = json.loads(user)
        return user_data
    else:
        return False



# THIS FUNCTION IS FOR SHO LAST 4 DIGITS OF MOBILE NUMBER
def display_last_four_digits(mobile_number):
    # Check if the mobile number is valid (at least 4 digits)
    if len(mobile_number) >= 4:
        # Extract the last four digits
        last_four_digits = mobile_number[-4:]
        # Create a string with asterisks (*) for the digits preceding the last four digits
        masked_number = "* " * (len(mobile_number) - 7) + last_four_digits
        # Add +91 to the starting of the mobile number
        masked_number_with_country_code = "+91 " + masked_number
        return masked_number_with_country_code
    else:
        # If the mobile number is less than 4 digits, return it as it is
        return mobile_number

# -------------------------------------------------------------#
            # API CALLING FUNCTIONS END
# -------------------------------------------------------------#




if __name__ == '__main__':
    app.run(debug=True)