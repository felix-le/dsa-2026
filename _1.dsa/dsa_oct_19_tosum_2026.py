#you are given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

# You may assume that each input would have exactly one solution, and you may not use the same element twice.

# You can return the answer in any order.

# Example 1:

# Input: nums = [2,7,11,15], target = 9
# Output: [0,1]
# Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
# Example 2:

# Input: nums = [3,2,4], target = 6
# Output: [1,2]
# Example 3:

# Input: nums = [3,3], target = 6
# Output: [0,1]

# Constraints:

# 2 <= nums.length <= 104
# -109 <= nums[i] <= 109
# -109 <= target <= 109
# Only one valid answer exists.

# Follow-up: Can you come up with an algorithm that is less than O(n2) time complexity?

#Pseudocode:
#function twoSum(arr, target):
  #seen = empty map              # a notebook: value -> index where we saw it

  # for each position i, value x in arr:
    #  need = target - x         # the partner number x is looking for

    # if need is in seen:
    #    return [seen[need], i] # found it — return both positions

    # seen[x] = i               # not found yet — write x into the notebook

from typing import List # List type like TS number[]

class Solution:
    # self, python requires it explicitly
    # nums: List[int] like nums: number[] (type hint, optional)
    # -> List[int] return type
  def twoSum(self, nums: List[int], target: int) -> List[int]: #function in JS
    # create an object JS to store the position and value ~ in Python it is a dict

    seen = {} #dict
    for i, x in enumerate(nums):
      # enumerate(nums) yields each (index i, value x) pair
      # ~ JS: for (let i = 0; i < nums.length; i++) { const x = nums[i]; ... }
      need = target - x # the partner x needs to reach target (complement)
      if need in seen:
        # need in seen  ~  JS: (need in seen)
        # direct lookup "is need in the notebook?", O(1), no scanning
        return [seen[need], i]
      seen[x] = i