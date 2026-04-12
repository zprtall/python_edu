import time


def decorator(func):
    def wrapper(task_text):


        print("\n--- Задание ---")
        print(task_text)
        print("-" * 30)

        start_time = time.perf_counter()

        func(task_text)

        end_time = time.perf_counter()
        print(f"Функция {func.__name__} работала: {end_time - start_time:} сек.")
        print()
    return wrapper



@decorator
def task_01(task_num) :
    x = input(int)
    x_str=str(x)
    print (x_str[len(x_str)-1])

@decorator
def task_02(task_text):
    x = input(int)
    print (len(x))

@decorator
def task_03(task_text):
    s = input(str)
    if(len(s)>1):
        print(s[len(s)-2])

@decorator
def task_04(task_text):
    for i in range(2,101,2):
        print (i)

@decorator
def task_05(task_text):
    summ = 0
    my_list = input("list== ").split()
    for i in my_list:
        if 0 < int(i):
            summ +=int(i)
    print(summ)

@decorator
def task_06(task_text):
    s1 = str(input("s1 =="))
    s2 = str(input("s2 =="))
    if(s2.find(s1)==-1):
        print("FASLE")
    else:
        print("TRUE")       #TRUE в случае если find нашёл s1 в s2

@decorator
def task_07(task_text):
    my_list =["123444", "https://web.telegram.org/", "qwerty", "https://www.youtube.com/watch?v=REQfiT1qvGQ", "https://habr.com/"]
    for s in my_list :
        if s.find("https://") != 0 :
            my_list.remove(s)
    print(my_list)

@decorator
def task_08(task_text):
    s=str(input("s == "))
    print("ind == ",s.find('0')+1)

@decorator
def task_09_1(task_text):
    my_list = [1, 2, 3, 4, 5, -3, 3, -2, 13, -234, -234324, -234, "1234", "qwerqt", "pupupu", -148]
    ans = 0

    for num in my_list:
        try:
            if (int(num) < 0):
                ans += 1
        except:
            continue
    print(ans)

@decorator
def task_09_2(task_text):
    my_list = [1, 2, 3, 4, 5, -3, 3, -2, 13, -234, -234324, -234, "1234", "qwerqt", "pupupu", -148]
    ans = 0

    for num in my_list:
        if str(num)[0]=='-' and str(num)[1:].isdigit():
            ans+=1
    print(ans)

@decorator
def task_10(task_text):
    my_list1 = [1, 2, 3, 4, 5, -3, 3, -2, 13, -234, -234324, -234, "1234", "qwerqt", "pupupu", -148]
    my_list2 = [1, "qwert", 148, "titi", 'q', "90", -3, 48, -234]
    for s1 in my_list1:
        for s2 in my_list2:
            if s1 == s2:
                print(s1)

menu = [task_01, task_02, task_03, task_04, task_05, task_06, task_07, task_08, task_09_1, task_09_2, task_10]
task = ["1. Дано число. Выведите в консоль последнюю цифру этого числа.",
        "2. Дано число. Выведите количество цифр в этом числе.",
        "3. Дана строка. Если в этой строке более одного символа, выведите в консоль предпоследний символ этой строки.",
        "4. Выведите в консоль все четные числа из промежутка от 1 до 100",
        "5. Найдите сумму положительных элементов этого списка.",
        "6. Дано 2 строки. Понять, является ли строка 1 подстрокой строки 2",
        "7. Дан список со строками. Оставьте в этом списке только те строки, которые начинаются на http://",
        "8. Дана некоторая строка. Найдите позицию первого нуля в строке.",
        "9. Дан список с числами. Подсчитайте количество отрицательных чисел в этом списке.",
        "10. Дан список с числами. Подсчитайте количество отрицательных чисел в этом списке. второй способ",
        "11. Дано 2 списка. Найдите все элементы, которые есть в обоих списках]"]


while(True):
    task_num = int (input ("task==")) -1
    menu[task_num](task[task_num])