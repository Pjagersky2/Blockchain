"""Module containing the core logic for the blockchain."""
import json
import logging
import logging.config
from copy import deepcopy
from datetime import datetime
from hashlib import sha256
from typing import Dict, List, Union

from config import logger_config

logging.config.dictConfig(logger_config)
logger = logging.getLogger("blockchain")


class Blockchain:
    """The blueprint to the blockchain."""

    __transaction = Dict[str, Union[str, float]]
    __transactions = List[__transaction]
    __block = Dict[str, Union[str, int, float, __transactions]]

    def __init__(self) -> None:
        """Initialize a new instance."""

        self.chain = []
        self.transactions = []

        self.mine_block(proof=1, previous_hash="1")

    @property
    def last_block(self) -> __block:
        """The last block in the chain."""

        return self.chain[-1]

    def mine_block(self, proof: int, previous_hash: str = "") -> None:
        """Mine a new block into the chain."""

        index = len(self.chain) + 1

        timestamp = datetime.utcnow().timestamp()

        current_transactions = deepcopy(self.transactions)

        if not previous_hash:
            previous_hash = self.hash_block(self.last_block)

        block = {
            "index": index,
            "timestamp": timestamp,
            "transactions": current_transactions,
            "proof": proof,
            "previous_hash": previous_hash
        }

        self.chain.append(block)
        self.transactions.clear()

        logger.info(f"Mined a new block into the chain with index: {index}")

    def hash_block(self, block: __block) -> str:
        """Generates the SHA256 checksum of a block."""

        block_string = json.dumps(block, sort_keys=True)
        block_bytes = block_string.encode("utf8")
        block_hash = sha256(block_bytes).hexdigest()

        return block_hash


def main() -> None:
    """Execute the main process."""

    blockchain = Blockchain()

    blockchain.mine_block(4365)

    print(json.dumps(blockchain.chain))


if __name__ == "__main__":
    main()
