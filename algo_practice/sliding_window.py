"""
Longest Substring Without Repeating Characters
Given a string s, find the length of the longest substring without duplicate characters.

A substring is a contiguous sequence of characters within a string.


Input: s = "abcabcbb"
Output: 3
"""

# Sliding Window Approach
def length_of_longest_substring(s: str) -> int:
  """
  Keep one window that always has unique characters. We expand the window by moving the right pointer. 
  If we ecounter a duplicate character, we shrink the window from the left until we remove the duplicate.
  """
  char_set = set() # empty set to store unique characters
  left = 0 # left edge of the window

  result = 0

  for right in range(len(s)): # right = right edge that moves through the string
    while s[right] in char_set:
      char_set.remove(s[left])
      left += 1
    char_set.add(s[right])
    result = max(result, right - left + 1)
  return result