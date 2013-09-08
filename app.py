import json, requests
from BeautifulSoup import BeautifulSoup
from flask import Flask, request


app = Flask(__name__)

@app.route('/')
def homepage():
    return open('templates/homepage.html').read()

@app.route('/api/')
def api():

    # grab the name they're searching for
    name = request.args.get('name')
    name = str(name)

    prefixes = request.args.get('prefixes').split(",")
    suffixes = request.args.get('suffixes').split(",")

    data = []
    name_options = build_name_options(name, prefixes, suffixes)
    http_session = requests.Session()

    for name_option in name_options:
        option_data = lookup_info(name_option, http_session)
        option_data["option"] = name_option
        data.append(option_data)

    response = json.dumps(data, indent=1)
    resp_headers = {"Content-Type:": "application/json"}
    return (response, 200, resp_headers)


def build_name_options(name, prefixes, suffixes):
    """takes a single name and returns common variations on it"""
    
    if "" not in prefixes:
        prefixes.insert(0, "")
    if "" not in suffixes:
        suffixes.insert(0, "")

    perms = []
    for p in prefixes:
        for s in suffixes:
            perms.append(p + name + s)

    return perms


def lookup_info(option, session):
    """takes a potential naming option and looks up info about it"""

    """
    other sources to search:
    - USPTO
    """

    domainr_response = session.get("https://domai.nr/api/json/search?q=" + option).json()
    other_domains,  com_is_available, com_register = [], None, ""
    for result in domainr_response.get("results", []):
        if result.get("path") != "":
            continue  # no one uses those path hacks...

        if result.get("domain", "").endswith(".com"):
            com_is_available = result.get("availability") == "available"
            if com_is_available:
                com_register = result.get("register_url")
        elif result.get("availability") == "available":
            other_domains.append({
                "domain": result.get("domain"),
                "register": result.get("register_url")
                })

    data = {
        "com_is_available": com_is_available,
        "com_register": com_register,
        "other_domains": other_domains,
    }
    data["twitter_is_available"] = session.get("http://twitter.com/" + option.replace(" ", "")).status_code == 404
    data["facebook_is_available"] = session.get("http://www.facebook.com/" + option.replace(" ", "")).status_code == 404

    return data


if __name__ == '__main__':
    app.run()
