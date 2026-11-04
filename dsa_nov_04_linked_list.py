class ListNode:
  def __init__(self, val=0, next=None):
    self.val = val
    self.next = next


class Solution:
  def mergeTwoLists(self, list1, list2):
    dummy = ListNode()
    dummy.next = list1
    prev, c1, c2 = dummy, list1, list2
    while c1 and c2:
      if c2.val < c1.val:
        nxt = c2.next
        prev.next = c2
        c2.next = c1
        prev = c2
        c2 = nxt
      else:
        prev = c1
        c1 = c1.next
    if c2:
      prev.next = c2
    return dummy.next
    