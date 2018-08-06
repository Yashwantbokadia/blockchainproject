import datetime
import json
from hashlib import sha256
import requests
from flask import render_template, redirect, request

from app import app


# The node with which our application interacts, there can be multiple
# such nodes as well.
CONNECTED_NODE_ADDRESS = "http://0.0.0.0:8000"

posts = []


def fetch_posts():
    """
    Function to fetch the chain from a blockchain node, parse the
    data and store it locally.
    """
    get_chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            print(block)
            tx = {"index": block["index"], "senderHash":block["senderHash"], "reciver":block["reciver"], "amount":block["amount"], "hash":block["previous_hash"], "timestamp":block["timestamp"]}
            content.append(tx)


        global posts
        """posts = sorted(content, key=lambda k: k['timestamp'],
                       reverse=True)"""
        posts = content


@app.route('/signin')#SignIn Page
def signinPage():
   return render_template('signin.html')


@app.route('/')#SignIn Page
def root():
    fetch_posts()
    return render_template('index.html',
                        title='BLocky',
                        posts=posts,
                        senderHash = senderHash,
                        node_address=CONNECTED_NODE_ADDRESS,
                        readable_time=timestamp_to_string)

@app.route('/index', methods=['POST'])#Index(Main) Page
def index():
    name = request.form["name"]
    password = request.form["pasd"]

    global senderHash
    senderHash = sha256((name+password).encode()).hexdigest()

    fetch_posts()
    return render_template('index.html',
                        title='BLocky',
                        posts=posts,
                        senderHash = senderHash,
                        node_address=CONNECTED_NODE_ADDRESS,
                        readable_time=timestamp_to_string)

@app.route('/submit', methods=['POST'])#When hit submit in Index page
def submit_textarea():
    """
    Endpoint to create a new transaction via our application.
    """
    print(request.form["amount"])
    amount = request.form["amount"]
    reciver = request.form["reciver"]
    
    post_object = {
        'amount': amount,
        'senderHash': senderHash,
        'reciver': reciver
    }
    print(post_object)
    # Submit a transaction
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)

    requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})
    return redirect('/')


def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')
