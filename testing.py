"""Module containing logic to test the blockchain."""
import json
from argparse import ArgumentParser, Namespace
from hashlib import sha256
from random import choice, randint
from typing import List

from blockchain import Blockchain


def get_random_wallets(total: int = 1) -> List[str]:
    """Generate a random list of wallet addresses."""

    wallet_addresses = []
    for _ in range(total):
        wallet_address = sha256(bytes(randint(10000, 99999))).hexdigest()
        wallet_addresses.append(wallet_address)

    return wallet_addresses


def main(args: Namespace) -> None:
    """Execute the main process."""

    blockchain = Blockchain(verbose=args.verbose)

    wallets = get_random_wallets(30)

    for _ in range(randint(5, 10)):  # blocks
        for _ in range(randint(5, 15)):  # transactions
            amount = randint(1, 100000) / randint(20, 800)
            sender = choice(wallets)

            recipient = sender
            while sender == recipient:
                recipient = choice(wallets)

            blockchain.add_transaction(sender=sender,
                                       recipient=recipient,
                                       amount=amount)

        proof = blockchain.proof_of_work()
        blockchain.mine_block(proof=proof)

    print(json.dumps(blockchain.chain))


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("-v",
                        "--verbose",
                        action="store_true",
                        help="specify verbose flag to increase "
                             "logging verbosity")

    args = parser.parse_args()

    main(args)
