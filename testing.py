"""Module containing logic to test the blockchain."""
import json
from argparse import ArgumentParser, Namespace

from utility import get_simulated_blockchain


def main(args: Namespace) -> None:
    """Execute the main process."""

    blockchain = get_simulated_blockchain(verbose=args.verbose)

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
