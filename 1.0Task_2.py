def isPolinom(x):
    s = str(x)
    for i in range(len(s)//2+1):
        c = s[i]!=s[-1 - i]
        if s[i]!=s[-1 - i]:
            return False
    return True

def longestCommonPrefix(strs):
    s = ""
    strs.sort(key=len, reverse=True)
    for i in range(len(strs[0])):
        s = s + strs[0][i]
        for word in strs:
            if i >= len(word) or word[i] != s[-1]:
                s = s[:-1]
                return s
    return s


def removeDuplicates(nums):
    k = 1
    for i in range(1, len(nums)):
        if nums[i] != nums[k - 1]:
            nums[k] = nums[i]
            k += 1
    return k


def twoSum(nums, target):
    nums.sort()
    for i in range(len(nums)):
        for k in range(i+1, len(nums)):

            if nums[i] + nums[k] == target:
                return [i,k]

def addBinary( a, b):
    result = bin((int(a, 2))+ (int(b, 2)))
    return result [2:]


#print(isPolinom(121))                                          #true
#print(isPolinom(-121))                                         #false
#print(isPolinom(10))                                           #fase

#print(longestCommonPrefix(["flower","flow","flight"]))         #fl
#print(longestCommonPrefix(["dog","racecar","car"]))            #""
#print(longestCommonPrefix(["dog","racecar","car"]))            #""
#print(longestCommonPrefix(["","d"]))            #""

#removeDuplicates([1,1,2])                      #2, nums = [1,2,_]

#print( twoSum([2,7,11,15], 9))                                 #[0,1]
#print( twoSum([3,2,4], 6))                                     #[1,2]
#print( twoSum([3,3], 6))                                       #[0,1]

#print(addBinary("11", "1"))                                    #100
#print(addBinary("1010", "1011"))                               #10101
