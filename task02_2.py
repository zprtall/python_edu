def isPolinom(x):
    s = str(x)
    for i in range(len(s)//2+1):
        if s[i]!=s[-1 -i]:

            return False
    return True

def longestCommonPrefix(strs):
    s = ""
    strs.sort(key=len, reverse=True)
    for i in range(len(strs[0])):
        s = s + strs[0][i]
        for word in strs:
           if word[i]!=s[-1]:
               s = s[:-1]
               return s
    return s

def removeDuplicates(nums):
    digit=-101
    new_nums =[]
    size = len(nums)
    for i in range(len(nums)):

        if digit != nums[i]:
            digit = nums[i]
            new_nums.append(digit)
        else:
            size -= 1
            nums[i] = '_'
    new_nums.extend('_' * (len(nums) - size))
    return size, new_nums


def twoSum(nums, target):
    for i in range(len(nums)):
        for k in range(i+1, len(nums)):

            if nums[i] + nums[k] == target:
                return [i,k]

def addBinary( a, b):
    rezult = bin((int(a, 2))+ (int(b, 2)))
    return rezult [2:]


#print(isPolinom(121))                                          #true
#print(isPolinom(-121))                                         #false
#print(isPolinom(10))                                           #fase

#print(longestCommonPrefix(["flower","flow","flight"]))         #fl
#print(longestCommonPrefix(["dog","racecar","car"]))            #""

#size, my_list = removeDuplicates([1,1,2])                      #2, nums = [1,2,_]
#size, my_list = removeDuplicates([0,0,1,1,1,2,2,3,3,4])        #5, nums = [0,1,2,3,4,_,_,_,_,_]
#print(size, "nums = ", my_list)

#print( twoSum([2,7,11,15], 9))                                 #[0,1]
#print( twoSum([3,2,4], 6))                                     #[1,2]
#print( twoSum([3,3], 6))                                       #[0,1]

#print(addBinary("11", "1"))                                    #100
#print(addBinary("1010", "1011"))                               #10101