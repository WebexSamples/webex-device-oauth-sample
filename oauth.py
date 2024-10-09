from flask import Flask, render_template, jsonify
from threading import Thread
import requests
import time
import os
import qrcode
import secrets

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.secret_key = os.urandom(16)

# Global storage for the access token
session = {}

# Define your clientID and client secret
clientID = ''
clientSecret = ''
credentials = ''  #base64 ecnode the clientid and client secret with a colon in the middle


def qr_cde_generation(url):
    img = qrcode.make(url)
    img.save('./static/qr_code.png')


def poll_for_access_token(device_code, poll_interval, secure_prefix):
    """Poll the token endpoint for an access token."""
    token_url = "https://webexapis.com/v1/device/token"
    headers = {'Authorization': f'Basic {credentials}'}
    body = {
        'client_id': f'{clientID}',
        'device_code': f'{device_code}',
        'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'
    }

    # Polling in seconds based on the poll_interval value
    while True:
        time.sleep(poll_interval)
        token_request = requests.post(url=token_url, data=body, headers=headers)
        if token_request.status_code == 200:
            # Store the access token in session or another secure place
            session[secure_prefix]['access_token'] = token_request.json()['access_token']
            session[secure_prefix]['refresh_token'] = token_request.json()['refresh_token']
            session[secure_prefix]['token_ready'] = True
            print(token_request.json())
            break
        else:
            # Handle other errors (e.g., 'slow_down', 'expired_token')
            print("Response Code:", token_request.status_code,
                  token_request.json()['errors'][0]['description'])


def device_refresh_token():
    refresh_token_url = "https://webexapis.com/v1/access_token"
    refresh_headers = {'Content-type': 'application/x-www-form-urlencoded'}

    refresh_body = {
        'grant_type': 'refresh_token',
        'client_id': f'{clientID}',
        'client_secret': f'{clientSecret}',
        'refresh_token': f'{session["refresh_token"]}',
    }

    token_refresh_reqeust = requests.post(url=refresh_token_url, data=refresh_body, headers=refresh_headers)
    session['access_token'] = token_refresh_reqeust.json()['access_token']
    session['refresh_token'] = token_refresh_reqeust.json()['refresh_token']


def whoami_lookup(secure_prefix):
    people_api_url = "https://webexapis.com/v1/people/me?callingData=true"
    headers = {'Authorization': f"Bearer {session[secure_prefix]['access_token']}"}
    people_api = requests.get(url=people_api_url, headers=headers)
    return people_api


@app.route("/")
def main_page():
    return render_template("index.html")


@app.route("/sign-in")
def sign_in():
    """Main Grant page"""
    scopes = "meeting:recordings_read spark:all spark:kms"
    params = {'client_id': clientID, 'scope': scopes}
    device_auth_url = "https://webexapis.com/v1/device/authorize"
    device_auth_request = requests.post(url=device_auth_url, data=params)
    device_auth_response = device_auth_request.json()
    print(device_auth_response)

    # Generate a secure random alphanumeric string to be used as part of the session key
    secure_prefix = secrets.token_hex(8)  # Generates a secure random string

    # Create a nested dictionary with the desired structure
    nested_dict = {
        'access_token': None,
        'refresh_token': None,
        'token_ready': False,
        'device_code': device_auth_response['device_code'],
        'poll_interval': device_auth_response['interval']
    }

    # Store the nested dictionary in the session using secure_prefix as the key
    session[secure_prefix] = nested_dict

    # Store the device code using the unique session key
    session[secure_prefix]['device_code'] = device_auth_response['device_code']
    session[secure_prefix]['poll_interval'] = device_auth_response['interval']

    qrcode_url = device_auth_response['verification_uri_complete']
    verification_uri = device_auth_response['verification_uri']
    user_code = device_auth_response['user_code']

    # Generate QR Code image
    qr_cde_generation(qrcode_url)

    # Start polling in a separate thread
    thread = Thread(target=poll_for_access_token, args=(session[secure_prefix]['device_code'], session[secure_prefix]['poll_interval'], secure_prefix))
    thread.start()

    # Render the template and pass verification url, and user code for manual user authorization
    return render_template("sign-in.html", verification_url=verification_uri, user_code=user_code, secure_prefix=secure_prefix)


@app.route("/granted/<secure_prefix>")
def granted(secure_prefix):
    # Check if the access token is ready and render the granted.html template
    if session[secure_prefix]['token_ready']:
        return render_template("granted.html", secure_prefix=secure_prefix)
    else:
        # If the token isn't ready, you might want to inform the user or redirect
        return "Access token not ready yet. Please try again later."


@app.route("/whoami/<secure_prefix>")
def whoami(secure_prefix):
    # Using the device access token, use /people API to display user information.
    user_info = whoami_lookup(secure_prefix)

    if user_info.status_code == 401:
        device_refresh_token()
        user_info = whoami_lookup(secure_prefix)
    else:
        user_info = user_info.json()

    return render_template("whoami.html", me=user_info)


@app.route("/access_token_ready/<secure_prefix>")
def access_token_ready(secure_prefix):
    return jsonify({'token_ready': session[secure_prefix]['token_ready']})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=10060)
