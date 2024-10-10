# Device Authentication Grant Workflow Sample

This Python script is a Flask app using OAuth with Webex APIs via the device authorization grant flow, covering key web development and OAuth concepts, including:

- Secure credentials
- Token polling
- QR code generation

The app uses libraries such as `Flask`, `requests`, and `qrcode`, starts with a secret key and base64 encoded credentials, and includes functions for generating QR codes, polling and refreshing tokens, and fetching user info from Webex. Flask routes manage the authorization flow, token readiness, and user data display.

## Prerequisites for Running the Sample Application

Before continuing, make sure you meet the following prerequisites:

### Install Python Modules

Install the following Python modules using pip:

```bash
pip install flask
pip install requests
pip install qrcode[pil]
```

- The **flask** module is a web framework for Python, which provides functionalities for building web applications.
- The **requests** module is used for making HTTP requests in Python. It abstracts the complexities of making requests behind a beautiful, simple API so that you can focus on interacting with services and consuming data in your application.
- The **qrcode[pil]** module is used to generate QR codes. The `[pil]` part is an extra requirement which means that it will also install the Pillow library, a fork of PIL (Python Imaging Library). It adds some user-friendly features.

### Create an Integration and Retrieve Integration Authorization Information

You’ll need to create a Webex integration and retrieve its **Client ID** and **Client Secret** for use in the sample script.

To create a new Webex integration:

1. Navigate to the Webex Developer Portal at [https://developer.webex.com](https://developer.webex.com).
1. Select **Log in** at the top right corner and log in with your Webex account credentials. If you don't have an account, create one.
1. After logging in, select **Start building apps** in the body of the landing page.
1. In the Integrations card, choose **Create an Integration**.
1. Enter the following details for your new integration:
    - **Will this integration use a mobile SDK?** Select **No**.
    - **Integration name**: Enter an alpha-numeric name for your integration.
    - **Icon**: Choose one of the default icons.
    - **App Hub Description**: Enter a brief description, for instance, `OAuth testing integration.`
    - **Redirect URI(s)**: Enter the following URLs:
        - <https://oauth-helper-a.wbx2.com/helperservice/v1/actions/device/callback>
        - <https://oauth-helper-k.wbx2.com/helperservice/v1/actions/device/callback>
        - <https://oauth-helper-r.wbx2.com/helperservice/v1/actions/device/callback>
    - **Scopes**: Select the following scopes for your integration:
        - `meeting:recordings_read`
        - `spark:all`
        - `spark:kms`
1. Select **Add Integration** at the bottom of the page to save your integration.
1. After saving, you will be provided with a **Client ID** and **Client Secret**. Store these securely. You’ll use them in the sample code.

## Run the Sample

To run the sample app:

1. Update the following variables in oauth.py:
    - `clientID`: <**Client ID** from the integration you created above>
    - `clientSecret`: <**Client Secret** from the integration you created above>
1. Open a terminal or command prompt.
1. Navigate to the directory where `oauth.py` is located.
1. Run the Python script using the following command:

    ```bash
    python oauth.py
    ```
