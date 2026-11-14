# LeetCode #9 — Palindrome Number (Easy)
#
# Requirement:
# Given an integer x, return True if x is a palindrome and False otherwise.
#
# Example 1:
# Input: x = 121
# Output: True
# Explanation: 121 reads as 121 from left to right and from right to left.
#
# Example 2:
# Input: x = -121
# Output: False
# Explanation: From left to right, it reads -121. From right to left, it
# becomes 121-. Therefore, it is not a palindrome.
#
# Example 3:
# Input: x = 10
# Output: False
# Explanation: It reads 01 from right to left. Therefore, it is not a
# palindrome.
#
# Constraints:
# - -2^31 <= x <= 2^31 - 1
#
# Follow-up:
# Solve it without converting the integer to a string.

class Solution:
  def isPalindrome(self, x: int)->bool:
    s = str(x)
    i = 0
    j = len(s) - 1
    while i < j:
      if s[i] != s[j]:
        return False

      i += 1
      j -= 1
    return True
      