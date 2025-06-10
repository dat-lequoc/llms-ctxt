# GitHub OAuth in your Python Flask app

This guide explains how to build an OAuth 2.0 integration into a Flask app using `Supabase-py`, allowing users to log in with their GitHub account.

## Prerequisites

This guide assumes you are familiar with creating a Flask application and have a basic understanding of Supabase Authentication.

You will need the following tools:
- [Flask](https://flask.palletsprojects.com/en/3.0.x/) (version 2.3.3 was used for the original article)
- A Supabase account ([create one here](https://database.new/))

## Getting started

First, install the `supabase` library in your Flask application's terminal:

```bash
pip install supabase
```

## Session storage

Create a file named `flask_storage.py` to handle session storage for the JSON Web Token (JWT). This class tells the Supabase authentication library (`gotrue`) how to manage the session.

```python
from gotrue import SyncSupportedStorage
from flask import session

class FlaskSessionStorage(SyncSupportedStorage):
    def __init__(self):
        self.storage = session

    def get_item(self, key: str) -> str | None:
        if key in self.storage:
            return self.storage[key]

    def set_item(self, key: str, value: str) -> None:
        self.storage[key] = value

    def remove_item(self, key: str) -> None:
        if key in self.storage:
            self.storage.pop(key, None)
```

## Initiate the client

Create another file, `supabase_client.py`, to initialize the Supabase client.

```python
import os
from flask import g
from werkzeug.local import LocalProxy
from supabase.client import Client, ClientOptions
from flask_storage import FlaskSessionStorage

url = os.environ.get("SUPABASE_URL", "")
key = os.environ.get("SUPABASE_KEY", "")

def get_supabase() -> Client:
    if "supabase" not in g:
        g.supabase = Client(
            url,
            key,
            options=ClientOptions(
                storage=FlaskSessionStorage(),
                flow_type="pkce"
            ),
        )
    return g.supabase

supabase: Client = LocalProxy(get_supabase)
```
This code creates a Supabase client instance, using the `FlaskSessionStorage` class for session management and setting `flow_type="pkce"` to handle the OAuth flow on the server side.

## Sign in with GitHub

For detailed instructions on setting up GitHub as an OAuth provider, refer to the [official Supabase documentation](https://supabase.com/docs/guides/auth/social-login/auth-github).

## Create sign-in route

In your main application file (`app.py`), create a route to trigger the GitHub sign-in process.

```python
@app.route("/signin/github")
def signin_with_github():
    res = supabase.auth.sign_in_with_oauth(
        {
            "provider": "github",
            "options": {
                "redirect_to": f"{request.host_url}callback"
            },
        }
    )
    return redirect(res.url)
```
This route generates a URL that redirects the user to the GitHub OAuth consent screen. The `redirect_to` parameter specifies the callback URL for after authentication.

## Create callback route

Add the callback route to your `app.py` to handle the response from GitHub.

```python
@app.route("/callback")
def callback():
    code = request.args.get("code")
    next = request.args.get("next", "/")
    if code:
        res = supabase.auth.exchange_code_for_session({"auth_code": code})
    return redirect(next)
```
This route receives an authorization `code` from GitHub, which is then exchanged for a user session. The `supabase` library handles storing the session JWT in a cookie and signing the user in.

## Conclusion

This guide covered setting up a Flask session storage to work with the Supabase Python library, using the PKCE flow, and creating sign-in and callback routes to handle user authentication via GitHub OAuth.

## More Resources

- [supabase-py reference docs](https://supabase.com/docs/reference/python/installing)
- [supabase-py GitHub repo](https://github.com/supabase-community/supabase-py)
- [Deep Dive series on auth concepts in Supabase](https://supabase.com/docs/learn/auth-deep-dive/auth-deep-dive-jwts)
