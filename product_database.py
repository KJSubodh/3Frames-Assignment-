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
        return self._collect_all_ids(node)

    def _collect_all_ids(self, node):
        ids = set(node.product_ids)
        for child in node.children.values():
            ids.update(self._collect_all_ids(child))
        return ids

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
        # Index product attributes in lowercase
        self._index_substrings(name.lower(), product_id)
        self._index_substrings(category.lower(), product_id)
        self._index_substrings(description.lower(), product_id)

    def _index_substrings(self, text, product_id):
        length = len(text)
        for i in range(length):
            for j in range(i + 1, length + 1):
                self.trie.insert(text[i:j], product_id)

    def search(self, query):
        query = query.lower()  
        product_ids = self.trie.search(query)
        results = [self.products[pid] for pid in product_ids]
        return results

def main():
    db = ProductDatabase()
    
    while True:
        print("\n1. Add Product")
        print("2. Search Products")
        print("3. Exit")
        choice = input("Enter your choice 1/2/3: ").strip()

        if choice == '1':
            try:
                product_id = int(input("Enter product ID: ").strip())
                name = input("Enter product name: ").strip()
                category = input("Enter product category: ").strip()
                description = input("Enter product description: ").strip()
                price = float(input("Enter product price: ").strip())
                
                if price < 0:
                    print("Price cannot be negative.")
                    continue
                
                db.add_product(product_id, name, category, description, price)
                print(f"Product {product_id} added successfully.")
            except ValueError as e:
                print(f"Invalid input: {e}. Please enter the correct data type.")

        elif choice == '2':
            query = input("Enter search query: ").strip()
            if not query:
                print("Search query cannot be empty.")
                continue
            
            results = db.search(query)
            if results:
                print("\nSearch results:")
                for product in results:
                    print(json.dumps(product, indent=2))
            else:
                print("No products found.")

        elif choice == '3':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()
