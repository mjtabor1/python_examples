

# hash map, dictionary, object -> { key: value, key: value, key: value }

# TWO SUM 
'''
Given an array of integers nums and an integer target, return the indices i and j such that nums[i] + nums[j] == target and i != j.

You may assume that every input has exactly one pair of indices i and j that satisfy the condition.

Return the answer with the smaller index first.

Input: 
nums = [3,4,5,6], target = 7

Output: [0,1]
'''

def two_sum_brute_force(nums: List[int], target: int) -> List[int]:
  for i in range(len(nums)):
    for j in range(i + 1, len(nums)):
      if nums[i] + nums[j] == target:
        return [i, j]
  return []


def two_sum_hash_map(nums: List[int], target: int) -> List[int]:
  hash_map = {}

  for i, num in enumerate(nums): # i=1, num=4
    difference = target - num  # 3
    if difference in hash_map:
      return [hash_map[difference], i] # -> [0, 1]

    hash_map[num] = i # { 3: 0 }

  return []
