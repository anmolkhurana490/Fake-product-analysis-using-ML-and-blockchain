import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, current_hash=None):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.current_hash = current_hash or self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256(
            f"{self.index}{self.previous_hash}{self.timestamp}{self.data}".encode()
        ).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        index = len(self.chain)
        previous_block = self.get_latest_block()
        previous_hash = previous_block.current_hash
        timestamp = time.time()
        new_block = Block(index, previous_hash, timestamp, data)
        self.chain.append(new_block)

def print_blockchain(blockchain):
    for block in blockchain.chain:
        print(f"Index: {block.index}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Timestamp: {block.timestamp}")
        print(f"Data: {block.data}")
        print(f"Current Hash: {block.current_hash}")
        print("\n")

# Example Usage:
if __name__ == "__main__":
    blockchain = Blockchain()
    blockchain.add_block("Transaction 1")
    blockchain.add_block("Transaction 2")
    blockchain.add_block("Transaction 3")

    print_blockchain(blockchain)