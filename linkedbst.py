"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log
from random import randint, sample
import time


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node is not None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    def find_no_rec(self, item):
        if self._root is None:
            return None
        if self._root.data == item:
            return self._root.data
        else:
            parent = self._root
            while True:
                if item < parent.data:
                    if parent.left is None:
                        return None
                    parent = parent.left
                elif item > parent.data:
                    if parent.right is None:
                        return None
                    parent = parent.right
                elif item == parent.data:
                    return parent.data

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right is None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def insert(self, item):
        if self._root is None:
            self._root = BSTNode(item)
            self._size += 1
        else:
            parent = self._root
            while True:
                if item < parent.data:
                    if parent.left is None:
                        parent.left = BSTNode(item)
                        self._size += 1
                        break
                    else:
                        parent = parent.left
                else:
                    if parent.right is None:
                        parent.right = BSTNode(item)
                        self._size += 1
                        break
                    else:
                        parent = parent.right
                    

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right is None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node is None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed is None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left is None \
                and not current_node.right is None:
            liftMaxInLeftSubtreeToTop(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left is None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top : BSTNode):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top.left is None and top.right is None:
                return 0
            if top.left and top.right:
                return 1 + max(height1(top.left), height1(top.right))
            elif top.left:
                return 1 + height1(top.left)
            else:
                return 1 + height1(top.right)
        if self._root is None:
            return 0
        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        def count_node(top):
            assert isinstance(top, BSTNode)
            if top.left is None and top.right is None:
                return 0
            return 1 + count_node(top.left) + count_node(top.right)

        if self.height() < 2 * log(len(self) + 1) - 1:
            return True
        return False

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        graph_list = self.inorder()
        res = []
        for node in graph_list:
            if low <= node and node <= high:
                res.append(node)
        return res


    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        iter_list = list(self.inorder())
        res_list = []

        self.clear()

        def help(add_list):
            '''
            help function
            '''
            if len(add_list) > 1:
                res_list.append(add_list[len(add_list) // 2])
                help(add_list[:len(add_list)//2])
                if len(add_list) > 2:
                    help(add_list[len(add_list)//2+1:])
            else:
                res_list.append(add_list[0])

        help(iter_list)
        for element in res_list:
            self.add(element)


    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        graph_list = self.inorder()
        for elem in graph_list:
            if elem > item:
                return elem
        return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        graph_list = list(self.inorder())
        for elem in reversed(graph_list):
            if elem < item:
                return elem
        return None

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()[:20000]
        list_to_find = []
        while len(list_to_find) < 1000:
            word_index = randint(0, len(lines))
            if lines[word_index] not in list_to_find:
                list_to_find.append(lines[word_index])

        start_time = time.perf_counter()
        for word in list_to_find:
            _ = lines.index(word)
        end_time = time.perf_counter()
        print(f"Linear time : {end_time - start_time} seconds")

        self.clear()
        for word in lines:
            self.insert(word)

        start_time = time.perf_counter()
        for word in list_to_find:
            _ = self.find_no_rec(word)
        end_time = time.perf_counter()
        print(f"Binary time (sorted by alphabet): {end_time - start_time} seconds")

        self.clear()
        random_list = sample(lines, len(lines))
        for word in random_list:
            self.insert(word)

        start_time = time.perf_counter()
        for word in list_to_find:
            _ = self.find_no_rec(word)
        end_time = time.perf_counter()
        print(f"Binary time (unsorted): {end_time - start_time} seconds")

        self.rebalance()
        for word in list_to_find:
            _ = self.find_no_rec(word)
        end_time = time.perf_counter()
        print(f"Binary time (balanced): {end_time - start_time} seconds")
        

linked = LinkedBST()
linked.demo_bst('Trees\words.txt')