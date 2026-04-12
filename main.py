def task_01() :
    x = input(int)
    x_str=str(x)
    print (x_str[len(x_str)-1])

def task_02():
    x = input(int)
    print (len(x))

def task_03():
    s = input(str)
    if(len(s)>1):
        print(s[len(s)-2])

def task_04():
    for i in range(2,101,2):
        print (i)

def task_05():
    summ = 0
    my_list = input("list== ").split()
    for i in my_list:
        if 0 < int(i):
            summ +=int(i)
    print(summ)

def task_06():
    s1 = str(input("s1 =="))
    s2 = str(input("s2 =="))
    if(s2.find(s1)==-1):
        print("FASLE")
    else:
        print("TRUE")       #TRUE в случае если find нашёл s1 в s2

def task_07():
    my_list =["123444", "https://web.telegram.org/", "qwerty", "https://www.youtube.com/watch?v=REQfiT1qvGQ", "https://habr.com/"]
    for s in my_list :
        if s.find("https://") != 0 :
            my_list.remove(s)
    print(my_list)

def task_08():
    s=str(input("s == "))
    print("ind == ",s.find('0')+1)

def task_09_1():
    my_list = [1, 2, 3, 4, 5, -3, 3, -2, 13, -234, -234324, -234, "1234", "qwerqt", "pupupu", -148]
    ans = 0

    for num in my_list:
        try:
            if (int(num) < 0):
                ans += 1
        except:
            continue
    print(ans)

def task_09_2():
    my_list = [1, 2, 3, 4, 5, -3, 3, -2, 13, -234, -234324, -234, "1234", "qwerqt", "pupupu", -148]
    ans = 0

    for num in my_list:
        if str(num)[0]=='-' and str(num)[1:].isdigit():
            ans+=1
    print(ans)

def task_10():
    my_list1 = [1, 2, 3, 4, 5, -3, 3, -2, 13, -234, -234324, -234, "1234", "qwerqt", "pupupu", -148]
    my_list2 = [1, "qwert", 148, "titi", 'q', "90", -3, 48, -234]
    for s1 in my_list1:
        for s2 in my_list2:
            if s1 == s2:
                print(s1)

menu = [task_01, task_02, task_03, task_04, task_05, task_06, task_07, task_08, task_09_1, task_09_2, task_10]
while(True):
    task_num = int (input ("task==")) -1
    menu[task_num]()
