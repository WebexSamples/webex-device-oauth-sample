# Webex Device Authentication Grant Sample

A comprehensive Flask application demonstrating the OAuth 2.0 Device Authorization Grant flow with Webex APIs. This sample showcases secure authentication for devices without keyboards or browsers, including QR code generation, token polling, and user profile retrieval.

## 🎯 Features

This sample shows how to implement the OAuth 2.0 Device Authorization Grant flow with Webex APIs:

* **Device Authorization Grant** - OAuth flow for input-constrained devices
* **QR Code Generation** - Visual authentication for mobile devices
* **Token Polling** - Secure background token retrieval
* **Automatic Token Refresh** - Handle expired tokens seamlessly
* **User Profile Retrieval** - Fetch authenticated user information
* **Real-time Updates** - jQuery-powered status polling
* **Secure Session Management** - Safe credential storage

## 📚 Prerequisites

### Software Requirements

- **Python 3.6 or higher**
- **Flask** web framework
- **Requests** library for HTTP operations
- **QRCode** library with PIL support

### Webex Developer Account

- **[Webex Developer Account](https://developer.webex.com/)** - Sign up for free
- **Webex Integration** with device authorization capabilities

## 🚀 Quick Start

### Install Python Dependencies

Install the required Python modules using pip:

```bash
pip install flask
pip install requests
pip install qrcode[pil]
```

**Module Details:**
- **Flask**: Web framework for Python applications
- **Requests**: Simplified HTTP library for API calls  
- **QRCode[PIL]**: QR code generation with image support (includes Pillow)

### Create Webex Integration

1. **Navigate** to [Webex Developer Portal](https://developer.webex.com)
2. **Log in** with your Webex account credentials
3. **Select** "Start building apps" on the landing page
4. **Choose** "Create an Integration" in the Integrations card
5. **Configure** your integration:

   | Field | Value |
   |-------|-------|
   | **Mobile SDK** | No |
   | **Integration Name** | Your app name (alphanumeric) |
   | **Icon** | Choose from default icons |
   | **Description** | e.g., "OAuth testing integration" |
   | **Redirect URIs** | Use the helper service URLs below |
   | **Scopes** | `spark:all` |

   **Required Redirect URIs:**
   ```
   https://oauth-helper-a.wbx2.com/helperservice/v1/actions/device/callback
   https://oauth-helper-k.wbx2.com/helperservice/v1/actions/device/callback
   https://oauth-helper-r.wbx2.com/helperservice/v1/actions/device/callback
   ```

6. **Save** your integration and securely store the **Client ID** and **Client Secret**

### Setup and Run

1. **Update environment variables** in the `.env` file:
   ```env
   CLIENT_ID=your_client_id_here
   CLIENT_SECRET=your_client_secret_here
   ```

2. **Start the application**:
   ```bash
   python oauth.py
   ```

3. **Access the application** at the generated URL:
   ```
   Running on http://10.26.164.77:10060
   ```

4. **Authenticate** by scanning the QR code or entering the URL and code manually

5. **View profile** information after successful authentication

## 📁 Project Structure

```
webex-device-oauth-sample/
├── oauth.py                 # Main Flask application
├── .env                     # Environment variables (not tracked)
├── static/css/             # CSS styling files
├── templates/              # HTML templates
│   ├── index.html          # Landing page
│   ├── sign-in.html        # Authentication page with QR code
│   ├── granted.html        # Post-authentication page
│   ├── whoami.html         # User profile display
│   └── temp.html           # Base template
├── package.json            # Development tools configuration
└── README.md               # This file
```

## 🔧 Functionality Overview

### OAuth 2.0 Device Authorization Grant Flow

| Step | Description | Implementation |
|------|-------------|----------------|
| **1. Device Authorization** | Request device and user codes | `/sign-in` endpoint |
| **2. User Authentication** | User authorizes via QR code or URL | External Webex authorization |
| **3. Token Polling** | Background polling for access token | `poll_for_access_token()` |
| **4. Token Retrieval** | Receive access and refresh tokens | Background thread processing |
| **5. API Access** | Use tokens for authenticated API calls | `/whoami` endpoint |

### Key Components

#### Device Authorization Request
```python
def sign_in():
    scopes = "meeting:recordings_read spark:all spark:kms"
    params = {'client_id': clientID, 'scope': scopes}
    device_auth_url = "https://webexapis.com/v1/device/authorize"
    device_auth_request = requests.post(url=device_auth_url, data=params)
```

#### QR Code Generation
```python
def qr_cde_generation(url):
    img = qrcode.make(url)
    img.save('./static/qr_code.png')
```

#### Token Polling
```python
def poll_for_access_token(device_code, poll_interval, secure_prefix):
    token_url = "https://webexapis.com/v1/device/token"
    while True:
        time.sleep(poll_interval)
        token_request = requests.post(url=token_url, data=body, headers=headers)
        if token_request.status_code == 200:
            # Store tokens and mark as ready
            break
```

## 🔐 Authentication Flow

### Step-by-Step Process

1. **User Clicks Sign-In**: Initiates the device authorization flow
2. **Device Authorization**: App requests device and user codes from Webex
3. **QR Code Display**: Visual representation of the verification URL
4. **User Authentication**: User scans QR code or visits URL to authorize
5. **Token Polling**: App polls Webex for authorization completion
6. **Token Storage**: Access and refresh tokens stored securely
7. **Profile Access**: User can view their Webex profile information

### Security Features

- **Secure Session Management**: Random alphanumeric session prefixes
- **Base64 Credential Encoding**: Client credentials properly encoded
- **Automatic Token Refresh**: Handles expired tokens transparently
- **Thread-Safe Polling**: Background token retrieval without blocking UI

## 📡 API Integration

### Core Endpoints

#### Device Authorization
```python
POST https://webexapis.com/v1/device/authorize
Content-Type: application/x-www-form-urlencoded

client_id=YOUR_CLIENT_ID&scope=spark:all
```

#### Token Exchange
```python
POST https://webexapis.com/v1/device/token
Authorization: Basic {base64_encoded_credentials}

client_id=YOUR_CLIENT_ID&device_code=DEVICE_CODE&grant_type=urn:ietf:params:oauth:grant-type:device_code
```

#### User Profile
```python
GET https://webexapis.com/v1/people/me?callingData=true
Authorization: Bearer ACCESS_TOKEN
```

### Error Handling

The application includes comprehensive error handling:

```python
def poll_for_access_token(device_code, poll_interval, secure_prefix):
    while True:
        token_request = requests.post(url=token_url, data=body, headers=headers)
        if token_request.status_code == 200:
            # Success - store tokens
            break
        else:
            # Handle errors like 'slow_down', 'expired_token'
            print("Response Code:", token_request.status_code,
                  token_request.json()['errors'][0]['description'])
```

## 🎨 User Interface

### Frontend Technologies

- **Flask Templates** with Jinja2 templating
- **jQuery** for asynchronous token status checking
- **CSS Styling** for professional appearance
- **QR Code Display** for mobile-friendly authentication

### Real-time Token Polling

The sign-in page uses jQuery to poll for token readiness:

```javascript
function checkAccessToken() {
    $.ajax({
        url: '/access_token_ready/{{ secure_prefix }}',
        type: 'GET',
        success: function (response) {
            if (response.token_ready) {
                window.location.href = '/granted/{{ secure_prefix }}';
            } else {
                setTimeout(checkAccessToken, 2000); // Poll every 2 seconds
            }
        }
    });
}
```

### User Experience Flow

1. **Landing Page**: Simple interface with "Sign-In" button
2. **Authentication Page**: QR code and manual entry options
3. **Waiting State**: Automatic polling with user feedback
4. **Success Page**: Confirmation and profile access
5. **Profile Display**: Formatted JSON user information

## 🔧 Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `CLIENT_ID` | Webex Integration Client ID | `C1234567890abcdef...` |
| `CLIENT_SECRET` | Webex Integration Client Secret | `secret123...` |

### Application Settings

```python
# Flask configuration
app.secret_key = os.urandom(16)  # Secure session key
app.run(debug=True, host='0.0.0.0', port=10060)  # Development settings
```

### Scope Configuration

```python
# OAuth scopes requested
scopes = "meeting:recordings_read spark:all spark:kms"
```

## 🌐 Production Considerations

### Security Best Practices

1. **Environment Variables**: Never hardcode credentials
   ```python
   clientID = os.getenv('CLIENT_ID')
   clientSecret = os.getenv('CLIENT_SECRET')
   ```

2. **HTTPS**: Use HTTPS in production
3. **Session Security**: Implement proper session management
4. **Token Storage**: Use secure storage for production tokens

### Deployment Recommendations

```python
# Production configuration
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10060))
    app.run(host='0.0.0.0', port=port, debug=False)
```

### Monitoring and Logging

```python
import logging

# Configure logging for production
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def poll_for_access_token(device_code, poll_interval, secure_prefix):
    logger.info(f"Starting token polling for session {secure_prefix}")
    # ... polling logic
```

## 🔧 Development

### Local Development Setup

1. **Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Debug Mode**:
   ```python
   app.run(debug=True, host='0.0.0.0', port=10060)
   ```

### Adding Features

Example: Adding token expiration checking:

```python
import jwt
from datetime import datetime

def is_token_expired(access_token):
    try:
        payload = jwt.decode(access_token, options={"verify_signature": False})
        exp_timestamp = payload.get('exp')
        return datetime.now().timestamp() > exp_timestamp
    except Exception:
        return True
```

### Testing the Flow

1. **Start the application**
2. **Navigate to the landing page**
3. **Click "Sign-In"** to initiate flow
4. **Scan QR code** or enter URL manually
5. **Authorize** in Webex
6. **View profile** information

## 🔗 Related Resources

- [Webex Developer Portal](https://developer.webex.com/)
- [OAuth 2.0 Device Authorization Grant](https://tools.ietf.org/html/rfc8628)
- [Webex API Documentation](https://developer.webex.com/docs/api/v1/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [QRCode Library Documentation](https://pypi.org/project/qrcode/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly with Webex integrations
5. Submit a pull request

## 📄 License

This project is licensed under the **Cisco Sample Code License**.

### License Summary

- ✅ **Permitted**: Copy, modify, and redistribute for use with Cisco products
- ❌ **Prohibited**: Use independent of Cisco products or to compete with Cisco
- ℹ️ **Warranty**: Provided "as is" without warranty
- ℹ️ **Support**: Not supported by Cisco TAC

See the [LICENSE](LICENSE) file for full license terms.

## 🆘 Support

- Create an issue in this repository
- Visit [Webex Developer Support](https://developer.webex.com/support)
- Join the [Webex Developer Community](https://developer.webex.com/community)

---

**Ready to implement device authentication with Webex!** 🚀📱
