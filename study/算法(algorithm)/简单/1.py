class Solution:
    def isPalindrome(self, s: str) -> bool:
        if not s:
            str1 = s.replace(' ', '').upper()
            str2 = str1[::-1]
            return str1 == str2