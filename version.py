import json
import difflib

class TrieNode:
    def __init__(self):
        self.children = {}
        self.end_of_version = False

class VersionControlSystem:
    def __init__(self):
        self.root = TrieNode()
        self.base_version = ""
        self.deltas = []

    def add_version(self, new_version):
        if not self.base_version:
            
            self.base_version = new_version
            self._insert_version(new_version, 1)
        else:
            
            last_version = self.get_version(len(self.deltas) + 1)
            delta = self.compute_delta(last_version, new_version)
            self.deltas.append(delta)
            self._insert_version(new_version, len(self.deltas) + 1)

    def get_version(self, version_number):
        version = []
        node = self.root
        version_count = 0

        def dfs(current_node, current_version):
            nonlocal version_count
            if version_count == version_number:
                return
            if current_node.end_of_version:
                version_count += 1
                if version_count == version_number:
                    version.extend(current_version)
                    return

            for char, child in current_node.children.items():
                dfs(child, current_version + [char])
                if version_count == version_number:
                    return

        dfs(node, [])
        return ''.join(version)

    def compute_delta(self, old_version, new_version):
        diff = difflib.ndiff(old_version, new_version)
        delta = ''.join(diff)
        return delta

    def _insert_version(self, version, version_number):
        node = self.root
        for char in version:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.end_of_version = True

    def save_to_file(self, filename):
        data = {
            "base_version": self.base_version,
            "deltas": self.deltas
        }
        with open(filename, 'w') as file:
            json.dump(data, file)

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        self.base_version = data["base_version"]
        self.deltas = data["deltas"]
        self._insert_version(self.base_version, 1)
        for i, delta in enumerate(self.deltas):
            version = self.apply_delta(self.get_version(i + 1), delta)
            self._insert_version(version, i + 2)

    def apply_delta(self, version, delta):
        version = list(version)
        index = 0
        for change in delta:
            if change.startswith('-'):
                if index < len(version):
                    version.pop(index)
            elif change.startswith('+'):
                if len(change) > 2:
                    version.insert(index, change[2])
                    index += 1
            elif change.startswith(' '):
                index += 1
        return ''.join(version)


if __name__ == "__main__":
    vcs = VersionControlSystem()
    vcs.add_version("Hello World")
    vcs.add_version("Hello World!")
    vcs.add_version("Hello, World!")
    vcs.add_version("Hello, World!!!")

    print(vcs.get_version(1))  
    print(vcs.get_version(2))  
    print(vcs.get_version(3))  
    print(vcs.get_version(4))  

    # Save to file
    vcs.save_to_file('versions.json')

    # Load from file
    vcs2 = VersionControlSystem()
    vcs2.load_from_file('versions.json')
    print(vcs2.get_version(4))  
