"""Module containing the logic to host the blockchain interface."""
from flask import Flask, jsonify, render_template, request

import utility

app = Flask(__name__)

node_id = utility.generate_node_id()

blockchain = utility.get_simulated_blockchain(node_id=node_id)


@app.route("/")
def home():
    """The home route for the '/' web server path."""

    return render_template("home.html")


@app.route("/chain")
def chain():
    """Get the full chain for the blockchain."""

    response = {
        "chain": blockchain.chain,
        "length": len(blockchain)
    }

    return jsonify(response), 200


@app.route("/mine")
def mine():
    """Mine a new block into the blockchain."""

    block = utility.mine_block(blockchain, node_id)

    response = {
        "block": block,
        "status": "New block forged."
    }

    return jsonify(response), 201


@app.route("/transactions/new", methods=["POST"])
def new_transaction():
    """Add a new transaction to next block forged in the blockchain."""

    try:
        transaction = {
            "sender": request.form["sender"],
            "recipient": request.form["recipient"],
            "amount": float(request.form["amount"])
        }
    except (KeyError, ValueError):
        response = {
            "status": "Failed to add transaction!"
        }
    else:
        blockchain.add_transaction(**transaction)
        response = {
            "status": "Added new transaction.",
            "transaction": transaction
        }

    return jsonify(response), 302


def main():
    """Execute the main process."""

    app.run(host="localhost", port=5000, debug=True)


if __name__ == "__main__":
    main()
