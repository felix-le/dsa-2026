# Write a function to find the longest common prefix string amongst an array of strings.

# If there is no common prefix, return an empty string "".

# Example 1:

# Input: strs = ["flower","flow","flight"]
#Output: "fl"
#Example 2:

#Input: strs = ["dog","racecar","car"]
#Output: ""
#Explanation: There is no common prefix among the input strings.
#Constraints:

#1 <= strs.length <= 200
#0 <= strs[i].length <= 200
#strs[i] consists of only lowercase English letters if it is non-empty.

"""
From the requirements:
- Prefix is starting from the beginning.
- separate for each pair
- compare strs[0] with strs[1] => common characters
- keep only the result, do not repeat this step for the next element of strs
- use the prefix to compare the next element:

if it is the same -> move the next element
if it has only 2 out of 5 common letter -> keep only 2
Notice: the prefix only reduces!!!

- if prefix = "" -> return ""
- repeat all step until end of the array.

pseudocode:

declare prefix = strs[0] - the first element of strs

create a loop to check each element from the second element of strs 

for word in strs[1:]
i= 0
while i < len(prefix) and i < len(word) and prefix[i] == word[i]
i+=1
prefix = prefix[:i]
if prefix ==""
return ""
return prefix

Good luck!

"""




class Solution(object):
  def longestCommonPrefix(self, strs):
    if not strs:
      return ""
    prefix = strs[0]

    for word in strs[1:]:
      i = 0
      while i <len(prefix) and i < len(word) and prefix[i]== word[i]:
        i +=1
      prefix = prefix[:i]
      if prefix == "":
        return ""
    return prefix