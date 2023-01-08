import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(word):
    """search up a word"""

    # Find the API
    try:
        api_key = os.environ.get("API_KEY")
        app_id = '3f687ae1'
        url = 'https://api.dictionaryapi.dev/api/v2/entries/en/'+word.lower()
        response = requests.get(url, headers = {"content-type": "application/json", "app_id": app_id, "api_key": api_key})
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Convert the user response into JSON
    try:
        r = response.json()
        definition = r[0]['meanings'][0]['definitions']
        return {
            "definition": definition[0]["definition"],
        }
    except Exception as e:
        print(e)
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"
