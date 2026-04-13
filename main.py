import time


def func_inf(func):
    def wrapper(data):


        print("\n--- Функция ---")
        print(f"Входные данные: {data}")
        print("-" * 30)

        start_time = time.perf_counter()

        print(f"Результат работы: {func(data)}"2)

        end_time = time.perf_counter()
        print(f"Функция {func.__name__} работала: {end_time - start_time:} сек.")

    return wrapper



@func_inf
def task_01(data) :
    x = data
    x_str=str(x)
    return (x_str[len(x_str)-1])

@func_inf
def task_02(data):
    x = data
    return (len(str(x)))

@func_inf
def task_03(data):
    s = data
    if(len(s)>1):
        return (s[len(s)-2])

@func_inf
def task_04(data):
    a = int(data[0])
    b = int(data[1])
    c = int(data[2])
    my_list = list()
    for i in range(a,b,c):
        my_list.append(i)
    return my_list

@func_inf
def task_05(data):
    summ = 0
    my_list = data
    for i in my_list:
        if 0 < int(i):
            summ +=int(i)
    return summ

@func_inf
def task_06(data):
    s1 = data[0]
    s2 = data[1]
    if(s2.find(s1)==-1):
        return "FASLE"
    else:
        return "TRUE"       #TRUE в случае если find нашёл s1 в s2

@func_inf
def task_07(data):
    my_list = data
    for s in my_list :
        if s.find("https://") != 0 :
            my_list.remove(s)
    return my_list

@func_inf
def task_08(data):
    s = data
    return "ind == ",s.find('0')+1

@func_inf
def task_09_1(data):
    my_list = data
    ans = 0

    for num in my_list:
        try:
            if (int(num) < 0):
                ans += 1
        except:
            continue
    return ans

@func_inf
def task_09_2(data):
    my_list = data
    ans = 0

    for num in my_list:
        if str(num)[0]=='-' and str(num)[1:].isdigit():
            ans+=1
    return ans

@func_inf
def task_10(data):
    my_list1 = data[0]
    my_list2 = data[1]
    ans_list = []
    for s1 in my_list1:
        for s2 in my_list2:
            if s1 == s2:
                ans_list.append(s1)
    return ans_list

menu = [task_01, task_02, task_03, task_04, task_05, task_06, task_07, task_08, task_09_1, task_09_2, task_10]
task_list = ["1. Дано число. Выведите в консоль последнюю цифру этого числа.",
        "2. Дано число. Выведите количество цифр в этом числе.",
        "3. Дана строка. Если в этой строке более одного символа, выведите в консоль предпоследний символ этой строки.",
        "4. Выведите в консоль все четные числа из промежутка от 1 до 100",
        "5. Найдите сумму положительных элементов этого списка.",
        "6. Дано 2 строки. Понять, является ли строка 1 подстрокой строки 2",
        "7. Дан список со строками. Оставьте в этом списке только те строки, которые начинаются на http://",
        "8. Дана некоторая строка. Найдите позицию первого нуля в строке.",
        "9. Дан список с числами. Подсчитайте количество отрицательных чисел в этом списке.",
        "10. Дан список с числами. Подсчитайте количество отрицательных чисел в этом списке. второй способ",
        "11. Дано 2 списка. Найдите все элементы, которые есть в обоих списках"]

data = [100000005, 1092384345, "qwezf124r2344 wer990rt", [2, 101, 2], [1, 2, 3, 4, -5, 0, 23, -123], ["12", "qwertysdga434asd21wer12sdfsa"],
        ["123444", "https://web.telegram.org/", "qwerty", "https://www.youtube.com/watch?v=REQfiT1qvGQ", "https://habr.com/"], "qwertysdga430asd21wer12sdfsa",
        [1, 2, 3, 4, 5, -3, 3, -2, 13, -234, -234324, -234, "1234", "qwerqt", "pupupu", -148], [1, 2, 3, 4, 5, -3, 3, -2, 13, -234, -234324, -234, "1234", "qwerqt", "pupupu", -148],
        [[1, 2, 3, 4, 5, -3, 3, -2, 13, -234, -234324, -234, "1234", "qwerqt", "pupupu", -148], [1, "qwert", 148, "titi", 'q', "90", -3, 48, -234]]]


for i in range(len(data)):

    print("\n",task_list[i])

    data_cont = data[i]

    menu[i](data_cont)






