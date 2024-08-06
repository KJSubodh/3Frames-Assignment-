import argparse
import sys
from collections import defaultdict
import math

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.count = 0

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.count += 1

    def get_words(self, node=None, prefix=''):
        if node is None:
            node = self.root
        words = []
        if node.is_end_of_word:
            words.append((prefix, node.count))
        for char, next_node in node.children.items():
            words.extend(self.get_words(next_node, prefix + char))
        return words

def read_file_in_chunks(file_path, chunk_size=1024*1024):  # 1 MB chunk size
    with open(file_path, 'r') as file:
        while True:
            data = file.read(chunk_size)
            if not data:
                break
            yield data

def process_file(file_path, trie):
    word_buffer = ''
    for chunk in read_file_in_chunks(file_path):
        words = (word_buffer + chunk).split()
        word_buffer = words.pop() if chunk[-1].isalpha() else ''
        for word in words:
            trie.insert(word.lower())
    if word_buffer:
        trie.insert(word_buffer.lower())

def output_sorted_words(trie):
    words_with_counts = trie.get_words()
    sorted_words = sorted(words_with_counts, key=lambda x: x[0])
    for word, count in sorted_words:
        print(f"{word}: {count}")

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def fuzzy_search(trie, word, max_distance=1):
    matches = []
    def search(node, current_word):
        if node.is_end_of_word and levenshtein_distance(word, current_word) <= max_distance:
            matches.append((current_word, node.count))
        for char, next_node in node.children.items():
            search(next_node, current_word + char)
    search(trie.root, '')
    return matches

def main():
    parser = argparse.ArgumentParser(description='Process a large text file to count word frequencies and perform fuzzy search.')
    parser.add_argument('file_path', type=str, help='Path to the large text file.')
    parser.add_argument('search_word', type=str, help='Word to search for using fuzzy search.')
    args = parser.parse_args()

    trie = Trie()
    process_file(args.file_path, trie)
    output_sorted_words(trie)

    fuzzy_matches = fuzzy_search(trie, args.search_word)
    for match, count in fuzzy_matches:
        print(f"Fuzzy match: {match} with count {count}")

if __name__ == '__main__':
    main()
