import hashlib
import time
import random
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

class Block:
    def __init__(self, index, previous_hash, voter_id, vote, timestamp, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.voter_id = voter_id
        self.vote = vote
        self.timestamp = timestamp
        self.nonce = nonce
        self.hash = self.compute_hash()
    
    def compute_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.voter_id}{self.vote}{self.timestamp}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def __repr__(self):
        return f"Block(index={self.index}, vote={self.vote}, hash={self.hash[:6]}...)"

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        genesis_block = Block(0, "0", "GENESIS", "None", time.time())
        self.chain.append(genesis_block)
    
    def add_block(self, voter_id, vote):
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), previous_block.hash, voter_id, vote, time.time())
        self.chain.append(new_block)

    def is_valid_chain(self):
        for i in range(1, len(self.chain)):
            if self.chain[i].previous_hash != self.chain[i-1].hash:
                return False
        return True

# Voter Simulation
blockchain = Blockchain()
voters = {f"Voter_{i}": random.choice(["Candidate_A", "Candidate_B", "Candidate_C"]) for i in range(1, 6)}

for voter_id, vote in voters.items():
    blockchain.add_block(voter_id, vote)
    time.sleep(1)

# Visualizing the Blockchain
def visualize_blockchain(blockchain):
    G = nx.DiGraph()
    labels = {}
    positions = {}
    
    for i, block in enumerate(blockchain.chain):
        G.add_node(i)
        labels[i] = f"Block {i}\n{block.vote}\n{block.hash[:6]}..."
        positions[i] = (i * 2, 0)
        if i > 0:
            G.add_edge(i - 1, i)
    
    plt.figure(figsize=(10, 4))
    nx.draw(G, pos=positions, with_labels=True, labels=labels, node_color='lightblue', node_size=3000, edge_color='gray')
    plt.title("Blockchain Voting Simulation")
    plt.show()

visualize_blockchain(blockchain)

# Display Election Results
results = {}
for block in blockchain.chain[1:]:
    results[block.vote] = results.get(block.vote, 0) + 1

print("Election Results:")
for candidate, votes in results.items():
    print(f"{candidate}: {votes} votes")
