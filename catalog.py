import json

class TrieNode:
    def __init__(self):
        self.children = {}
        self.product_ids = set()

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, key, product_id):
        node = self.root
        for char in key:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.product_ids.add(product_id)

    def search(self, key):
        node = self.root
        for char in key:
            if char not in node.children:
                return set()
            node = node.children[char]
        return node.product_ids

class ProductDatabase:
    def __init__(self):
        self.trie = Trie()
        self.products = {}

    def add_product(self, product_id, name, category, description, price):
        product_data = {
            "name": name,
            "category": category,
            "description": description,
            "price": price
        }
        self.products[product_id] = product_data
        self.trie.insert(name, product_id)
        self.trie.insert(category, product_id)
        # Additional attributes can be indexed similarly

    def search(self, query):
        product_ids = self.trie.search(query)
        results = [self.products[pid] for pid in product_ids]
        return results

# Example usage
if __name__ == "__main__":
    db = ProductDatabase()
    db.add_product(1, "Smartphone", "Electronics", "Latest model smartphone with high resolution", 699)
    db.add_product(2, "Laptop", "Electronics", "High performance laptop with 16GB RAM", 1200)
    db.add_product(3, "Coffee Maker", "Home Appliances", "Automatic coffee maker with programmable settings", 85)

    print("Search results for 'Electronics':")
    for product in db.search("Electronics"):
        print(json.dumps(product, indent=2))
    
    print("Search results for 'Smartphone':")
    for product in db.search("Smartphone"):
        print(json.dumps(product, indent=2))
