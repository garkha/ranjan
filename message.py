from flask import Flask, session, redirect, url_for, request

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Global variable to store the count
request_count = 0

# Function to increment the request count
def track_requests():
    global request_count
    request_count += 1
    if request_count == 812:
        session.clear()


# Registering a function to run before each request
@app.before_request
def before_request_callback():
    track_requests()


def flash_message(key,value):
    session[key] = value
    global request_count
    request_count = 810



if __name__ == '__main__':
    app.run(debug=True)
