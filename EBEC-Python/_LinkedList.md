# Python Programming
* ### [Menu](./README.md)
* ### Data Structures - Linked List
    * Append / Prepend / Insert / Delete / Length
    * Swap Data / Swap Nodes
    * Reverse
    * Remove n-th Last Node
    * Merge Two Linked Lists
    * Remove Duplicates
    * Rotate
* ### LeetCode Problems
    * [0002. Add Two Numbers (Medium)](https://leetcode.com/problems/add-two-numbers/)
    * [0009. Palindrome Number (Easy)](https://leetcode.com/problems/palindrome-number/)
    * [0019. Remove Nth Node From End of List (Medium)](https://leetcode.com/problems/remove-nth-node-from-end-of-list/)
    * [0021. Merge Two Sorted Lists (Easy)](https://leetcode.com/problems/merge-two-sorted-lists/)
    * [0061. Rotate List (Medium)](https://leetcode.com/problems/rotate-list/)
    * [0083. Remove Duplicates from Sorted List (Easy)](https://leetcode.com/problems/remove-duplicates-from-sorted-list/)
    * [0206. Reverse Linked List (Easy)](https://leetcode.com/problems/reverse-linked-list/)
    * [0234. Palindrome Linked List (Easy)](https://leetcode.com/problems/palindrome-linked-list/)
    * [0445. Add Two Numbers II (Medium)](https://leetcode.com/problems/add-two-numbers-ii/)

<br />

## Linked List          <a name="p17"></a>
```python
from __future__ import print_function

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        """
        Add new node to the tail of the linked list
        """
        new = Node(data)
        if not self.head: self.head = new
        else: 
            cur = self.head
            while cur.next: cur = cur.next
            cur.next = new

    def prepend(self, data):
        """
        Add new node to the head of the linked list
        """
        new = Node(data)
        new.next = self.head
        self.head = new

    def insert_after(self, node, data):
        """
        Add new node after the specific node
        """
        new = Node(data)
        new.next = node.next
        node.next = new

    def delete(self, key):
        """
        Delete node by searching key as node's data
        """
        cur = self.head

        # Node to be deleted is head
        if cur.data == key:
            self.head = cur.next
            cur = None

        # Search for the node to be deleted
        else:
            while cur.next and cur.next.data != key: cur = cur.next
            if cur.next: cur.next = cur.next.next

    def delete_pos(self, pos):
        """
        Delete node by its position
        """
        # Node to be deleted is head
        if pos == 0 and self.head:
            self.head = self.head.next
        
        else:
            cur, prev, index = self.head, None, 0
            while cur and index != pos:
                cur, prev, index = cur.next, cur, index+1
            if cur: prev.next, cur = cur.next, None

    def swap_data(self, key1, key2):
        """
        Swap two nodes' data by searching key as node's data
        """
        # Iterate the list to find two target nodes
        cur, node1, node2 = self.head, None, None
        while cur:
            if cur.data == key1: node1 = cur
            if cur.data == key2: node2 = cur
            cur = cur.next

        if node1 and node2: node1.data, node2.data = node2.data, node1.data

    def swap_node(self, key1, key2):
        """
        Swap two nodes by searching key as node's data
        """
        cur, prev = self.head, None
        prev1, node1, pre2v, node2 = None, None, None, None

        # # Iterate the list to find two target nodes and their previous nodes
        while cur:
            if   cur.data == key1: node1, prev1 = cur, prev
            elif cur.data == key2: node2, prev2 = cur, prev
            
            cur, prev = cur.next, cur

        # Return: Both nodes non-exist / Two nodes are the same
        if not (node1 and node2) or (node1 == node2): return

        # Node1's previous node exists, assign next pointer to node2
        if prev1: prev1.next = node2
        # Otherwise, assign node2 to head
        else: self.head = node2

        # Node1's previous node exists, assign next pointer to node2
        if prev2: prev2.next = node1
        # Otherwise, assign node2 to head
        else: self.head = node1

        # Swap node1 and node2's next pointers
        node1.next, node2.next = node2.next, node1.next

    def reverse_iterative(self):
        """
        Reverse the linked list by iterative method
        """
        cur, prev = self.head, None
        while cur:
            cur.next, prev, cur = prev, cur, cur.next
        self.head = prev

    def reverse_recursive(self):
        """
        Reverse the linked list by recursive method
        """
        def helper(cur):
            # No node in the list / Only 1 node in the list
            if not cur or not cur.next: return cur
            
            # Keep recursion until the tail node, which is returned
            node = helper(cur.next)

            '''
                    (cur)  (node)
            A -> B -> C -> D    None
                        <-

                    (cur)  (node)
            A -> B -> C <- D    None
                      |-> None

               (cur)       (node)
            A -> B -> C <- D    None
                   <-

               (cur)       (node)
            A -> B <- C <- D    None
                 |-> None

            (cur)            (node)
            A -> B -> C <- D    None
              <-

            (cur)            (node=HEAD)
            A <- B <- C <- D    None
            |-> None
            '''
            cur.next.next = cur
            cur.next = None

            return node
        
        node = helper(self.head)
        self.head = node

    def remove_nthToLast(self, n):
        """
        Get the nth node from the tail of the linked list
        """
        fastP, slowP = self.head, self.head

        '''
        n = 3
        (slowP)          (fastP)
        1 -> 2 -> '3' -> 4 -> 5
        '''
        for _ in range(n): fastP = fastP.next

        if not fastP: self.head = self.head.next

        '''
        n = 3
             (slowP)          (fastP)
        1 -> 2 -> '3' -> 4 -> 5
        '''
        while fastP.next: fastP, slowP = fastP.next, slowP.next

        slowP.next = slowP.next.next

    def get_node(self, key):
        """
        Retrieve node by key (data)
        """
        cur = self.head
        while cur: 
            if cur.data == key: return cur
            cur = cur.next

    def get_len_iterative(self):
        """
        Get the length of the linked list (iterative)
        """
        cur, count = self.head, 0
        while cur: cur, count = cur.next, count+1
        return count

    def get_len_recursive(self, node):
        """
        Get the length of the linked list (recursive)
        """
        if not node: return 0
        return 1 + self.get_len_recursive(node.next)

    def print_list(self):
        """
        Print the linked list from HEAD to the TAIL node
        """
        cur = self.head
        while cur:
            print(cur.data, end='')
            cur = cur.next
        print('')

def mergeTwoLists_iterative(l1, l2):
    ret = cur = Node(0)

    while l1 and l2:
        if l1.data < l2.data:
            cur.next = l1
            cur, l1 = cur.next, l1.next
        else:
            cur.next = l2
            cur, l2 = cur.next, l2.next
    
    cur.next = l1 or l2
    return ret.next

def mergeTwoLists_recursive(l1, l2):
    if not l1: return l2
    if not l2: return l1

    if l1.data > l2.data: l1, l2 = l2, l1
    l1.next = mergeTwoLists_recursive(l1.next, l2)

    return l1

def removeDuplicate_set(node):
    record = set()
    prev, cur = None, node

    while cur:
        if cur.data in record:
            prev.next = cur.next
        else:
            record.add(cur.data)
            prev = cur
        
        cur = cur.next

def removeDuplicate_ifSorted(node):
    cur = node
    while cur:
        while cur.next and cur.data == cur.next.data:
            cur.next = cur.next.next

        cur = cur.next

def rotate(node, n, dir='right'):
    """
    FIND NEW and ORI TAIL NODE
    ================================================================
    A -> B -> C -> D -> E (n = 2, length = 5)
    Rotate to the right = C is new tail node = 5 - 2 - 1 gaps from A
                          D is new head node

    Rotate to the left  = B is new tail node = 2 - 1     gaps from A
                          C is new head node
    ================================================================
    """
    tail, length = node, 1
    while tail.next: tail, length = tail.next, length + 1

    n %= length
    if n == 0: return node

    if   dir == 'right': rotation = length - n - 1
    elif dir == 'left':  rotation = n - 1

    new_tail = node    
    for _ in range(rotation): new_tail = new_tail.next

    head = new_tail.next
    tail.next, new_tail.next = node, None

    return head

if __name__ == '__main__':
    l1 = LinkedList()
    l1.append('B')                              # B
    l1.prepend('A')                             # AB
    l1.insert_after(l1.get_node('B'), 'C')      # ABC
    l1.insert_after(l1.get_node('C'), 'D')      # ABCD
    length = l1.get_len_iterative()             # 4

    l1.delete("B")                              # ACD
    l1.delete("E")                              # ACD

    l1.insert_after(l1.get_node('A'), 'B')      # ABCD
    l1.delete_pos(2)                            # ABD

    length = l1.get_len_iterative()             # 3
    length = l1.get_len_recursive(l1.head)      # 3

    l1.insert_after(l1.get_node('B'), 'C')      # ABCD
    length = l1.get_len_iterative()             # 4

    l1.swap_data('A', 'C')                      # CBAD
    l1.swap_data('C', 'A')                      # ABCD

    l1.swap_node('A', 'D')                      # DBCA
    l1.swap_node('C', 'B')                      # DCBA

    l1.reverse_iterative()                      # ABCD
    l1.reverse_recursive()                      # DCBA

    l2 = LinkedList()
    l2.append('E')
    l2.append('F')
    l2.append('G')
    l2.append('H')                              # EFGH

    print('l1: ', end=''); l1.print_list()      # DCBA
    print('l2: ', end=''); l2.print_list()      # EFGH
    l3 = mergeTwoLists_recursive(l1.head, l2.head)
    l4 = LinkedList()
    while l3:
        l4.append(l3.data)
        l3 = l3.next
    print('Merge: ', end=''); l4.print_list()   # DCBAEFGH
    print()

    l1 = LinkedList()
    l1.append('A')
    l1.append('B')
    l1.append('G')
    l1.append('H')

    print('l1: ', end=''); l1.print_list()      # ABGH
    print('l2: ', end=''); l2.print_list()      # EFGH
    l3 = mergeTwoLists_iterative(l1.head, l2.head)
    l4 = LinkedList()
    while l3:
        l4.append(l3.data)
        l3 = l3.next
    print('Merge:      ', end=''); l4.print_list()   # ABEFGGHH

    removeDuplicate_set(l4.head)
    print('Remove Dup: ', end='')
    l4.print_list()                             # ABEFGH
    print()

    l4.insert_after(l4.get_node('A'), 'A')
    l4.insert_after(l4.get_node('A'), 'A')
    l4.insert_after(l4.get_node('G'), 'G')
    l4.insert_after(l4.get_node('H'), 'H')      # AAABEFGGHH

    print('l4:         ', end='')
    l4.print_list()                             # AAABEFGGHH
    removeDuplicate_ifSorted(l4.head)
    print('Remove Dup: ', end='')
    l4.print_list()                             # ABEFGH

    print('Remove 3th last node: ', end='')
    l4.remove_nthToLast(3)                      # ABE_GH
    l4.print_list()
    print()

    print('l4:             ', end='')
    l4.print_list()                             # ABEGH
    node = rotate(l4.head, 2, dir='right')
    l3 = LinkedList()
    while node:
        l3.append(node.data)
        node = node.next
    print('Rotate right 2: ', end='')
    l3.print_list()                             # GHABE

    node = rotate(l3.head, 2, dir='left')
    l3 = LinkedList()
    while node:
        l3.append(node.data)
        node = node.next
    print('Rotate left  2: ', end='')
    l3.print_list()                             # ABEGH
```