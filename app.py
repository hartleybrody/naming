import json, requests
from flask import Flask, request, render_template


app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/api')
def api():

    # grab the name they're searching for
    name = request.args.get('name')
    name = str(name)

    data = {}
    options = build_name_options(name)
    for option in options:
        data[option] = lookup_info(option)


    response = json.dumps(data, indent=1)
    resp_headers = {"Content-Type:": "application/json"}
    return (response, 200, resp_headers)

def build_name_options(name):
    """takes a single name and returns common variations on it"""

    prefixes = ["", "get", "try"]
    suffixes = ["", "app", "co"]

    perms = []
    for p in prefixes:
        for s in suffixes:
            perms.append(p + name + s)

    return perms

def lookup_info(option):
    """takes a name option and looks up info about it"""

    # domainr_response = requests.get("https://domai.nr/api/json/search?q=" + option).json()
    #twitter
    #google search results
    #USPTO trademark

    return []


if __name__ == '__main__':
    app.debug = True
    app.run()