"""
Count Occurrences of a Substring
Given two strings haystack and needle, return the number of times needle occurs 

in haystack as a substring. Overlapping occurrences count separately. If needle does not occur in haystack, return 0.
Example 1:
Input: haystack = "ababab", needle = "ab"
Output: 3
Explanation: "ab" occurs at index 0, 2, and 4.
Example 2:
Input: haystack = "aaaa", needle = "aa"
Output: 3
Explanation: "aa" occurs at index 0, 1, and 2. 
Overlapping occurrences count separately.
Example 3:
Input: haystack = "leetcode", needle = "leeto"
Output: 0
Explanation: "leeto" does not occur in "leetcode".
Constraints:
1 <= haystack.length, needle.length <= 10^4
haystack and needle consist of only lowercase English letters.
"""

def countOccurs(self, haystack, needle):
    if len(needle) > len(haystack):
        return 0

    countRepeatTime = 0
    
    for start in range((len(haystack)) - len(needle) + 1):
        match = True

        for j in range(len(needle)):
            if haystack[start + j] != needle[j]:
                match = False
                break
        if match:
            countRepeatTime += 1
    return countRepeatTime