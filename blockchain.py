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

    target_proof_string = "B00B"

    __transaction = Dict[str, Union[str, float]]
    __transactions = List[__transaction]
    __block = Dict[str, Union[str, int, float, __transactions]]

    def __init__(self, verbose: bool = True) -> None:
        """Initialize a new instance."""

        self.verbose = verbose

        self.chain = []
        self.transactions = []

        self.mine_block(proof=1, previous_hash="1")

    def __len__(self):
        """The length of the blockchain."""

        return len(self.chain)

    @property
    def last_block(self) -> __block:
        """The last block in the chain."""

        return self.chain[-1]

    def mine_block(self, proof: int, previous_hash: str = "") -> __block:
        """Mine a new block into the chain."""

        index = len(self)

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

        if self.verbose:
            logger.info(f"Mined new block into the chain with index: {index}")

        return block

    def add_transaction(self,
                        sender: str,
                        recipient: str,
                        amount: float
                        ) -> None:
        """Add a transaction to the pending blockchain transactions."""

        transaction = {
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        }

        self.transactions.append(transaction)

        if self.verbose:
            logger.info(f"Added a new transaction with amount {amount} "
                        f"from {sender} to {recipient}.")

    def proof_of_work(self) -> int:
        """Calculate the proof of work for a mining operation."""

        previous_proof = self.last_block["proof"]
        previous_hash = self.hash_block(self.last_block)

        proof = 0
        while not self.check_proof(previous_proof, previous_hash, proof):
            proof += 1

        return proof

    def check_proof(self,
                    previous_proof: int,
                    previous_hash: str,
                    proof: int
                    ) -> bool:
        """Check to see if the proof is valid."""

        proof_string = f"{previous_proof}{previous_hash}{proof}"
        proof_hash = sha256(proof_string.encode("utf8")).hexdigest()

        is_valid = False
        proof_prefix = proof_hash[:len(self.target_proof_string)]
        if proof_prefix.upper() == self.target_proof_string:
            if self.verbose:
                logger.info(f"Proof of work solved with "
                            f"previous proof {previous_proof}, "
                            f"previous hash {previous_hash}, and "
                            f"proof {proof}")

            is_valid = True

        return is_valid

    @staticmethod
    def hash_block(block: __block) -> str:
        """Generates the SHA256 checksum of a block."""

        block_string = json.dumps(block, sort_keys=True)
        block_bytes = block_string.encode("utf8")
        block_hash = sha256(block_bytes).hexdigest()

        return block_hash
