November 2 2026
#Linked List

1. What is the linked list?
   A linked list is a linear data structure where elements are stored in nodes, and each node contains a reference (or link) to the next node in the sequence.

1.1 what is a node?

- Unit of data, holds two things: a value (val for short) and link (next) to the next node.

1 | _ -> 2| _ -> 3| \_ -> None
1 points to 2, 2 points to 3, and 3 points to None (end of the list).

The very beginning of node is called head and the last one is called tail. If the linked list has only 1 node, then the head and tail are the same.

2. How differs from an array?

An array has indices. write a[2] -> get the element at position 2 -> instant access.
In linked list, you must traverse step by step using the link from the head. You keep a reference (a pointer) to the current node then move to the next node with current = current.next.

3. ListNode in LeetCode (python)

```python
class ListNode:
    def __init__(self, val=0, next=None): # constructor
        self.val = val # value of the node
        self.next = next # link to the next node = None


# empty linked list

class LinkedList:
    def __init__(self):
        self.head = None # head of the linked list
        self.tail = None # tail of the linked list
```

4. Linking node (splicing)

Node are joined by reassigning the link.

`a.next = b`
a is [1] and b is [2], now a points to b.
a. next = b means the chain is now [1] -> [2] -> None

5. Take away:

1. node = one value (val) + one link (next)
1. No indices, must traverse from head to tail with .next
1. An empty list is None, a list it its head
1. Splicing nodes = reassigning the link to the next node and the values don't change
