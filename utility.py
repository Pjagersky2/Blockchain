"""Module containing helper methods for the project."""
from hashlib import sha256
from random import choice, randint
from typing import Dict, List, Union
from uuid import uuid4

from blockchain import Blockchain

__transaction = Dict[str, Union[str, float]]
__transactions = List[__transaction]
__block = Dict[str, Union[str, int, float, __transactions]]


def generate_node_id() -> str:
    """Get a new unique node identifier."""

    return str(uuid4()).replace("-", "")


def get_random_wallets(total: int = 1) -> List[str]:
    """Generate a random list of wallet addresses."""

    wallet_addresses = []
    for _ in range(total):
        wallet_address = sha256(bytes(randint(10000, 99999))).hexdigest()
        wallet_addresses.append(wallet_address)

    return wallet_addresses


def mine_block(blockchain: Blockchain, node_id: str) -> __block:
    """Perform the mine block algorithm."""

    proof = blockchain.proof_of_work()

    blockchain.add_transaction(sender="0",
                               recipient=node_id,
                               amount=1.0)

    block = blockchain.mine_block(proof=proof)

    return block


def get_simulated_blockchain(verbose: bool = True,
                             randomize: bool = False,
                             node_id: str = ""
                             ) -> None:
    """Get a blockchain instance with simulated data."""

    blockchain = Blockchain(verbose=verbose)

    node_id = node_id if node_id else generate_node_id()

    default_max_wallets = 30
    default_max_blocks = 2
    default_max_transactions = 5

    max_blocks = default_max_blocks
    max_transactions = default_max_transactions
    if randomize:
        max_blocks = randint(5, 10)
        max_transactions = randint(5, 15)

    wallets = get_random_wallets(default_max_wallets)

    for _ in range(max_blocks):  # blocks
        for _ in range(max_transactions):  # transactions
            amount = randint(1, 100000) / randint(20, 800)
            sender = choice(wallets)

            recipient = sender
            while sender == recipient:
                recipient = choice(wallets)

            blockchain.add_transaction(sender=sender,
                                       recipient=recipient,
                                       amount=amount)

        mine_block(blockchain, node_id)

    return blockchain
