import time


def func_information(func):
    def wrapper(*args, **kwargs):
        print("\n--- Функция ---")
        print(f"Функция {func.__name__} Входные данные: {args, kwargs}")
        print("-" * 30)

        start_time = time.perf_counter()
        data = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"Результат работы: {data} \nработала: {end_time - start_time:} сек.")



    return wrapper



@func_information
def task_01(data) :
    data_str=str(data)
    return (data_str[len(data_str)-1])

@func_information
def task_02(data):
    x = data
    return (len(str(x)))

@func_information
def task_03(data):
    s = data
    if(len(s)>1):
        return (s[len(s)-2])

@func_information
def task_04(a, b, c):
    my_list = list()
    for i in range(a, b, c):
        my_list.append(i)
    return my_list

@func_information
def task_05(data):
    summ = 0
    my_list = data
    for i in my_list:
        if 0 < int(i):
            summ +=int(i)
    return summ

@func_information
def task_06(s1, s2):
    ans = s2.find(s1) == -1
    return ans

@func_information
def task_07(data):
    new_list = [s for s in data if s.find("https://") == 0]
    return new_list

@func_information
def task_08(data):
    s = data
    return "ind == ",s.find('0')

@func_information
def task_09_1(data):
    ans = 0

    for num in data:
        try:
            if (int(num) < 0):
                ans += 1
        except:
            continue
    return ans

@func_information
def task_09_2(data):
    my_list = data
    ans = 0

    for num in my_list:
        if str(num)[0]=='-' and str(num)[1:].isdigit():
            ans+=1
    return ans

@func_information
def task_10(list1, list2):
    ans_list = []
    for s1 in list1:
        for s2 in list2:
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

# первый способ
# data = [
#     100000005,
#     1092384345,
#     "qwezf124r2344 wer990rt",
#     (2, 101, 2),
#     [1, 2, 3, 4, -5, 0, 23, -123],
#     ("12", "qwertysdga434asd21wer12sdfsa"),
#     ["123444", "https://web.telegram.org/", "qwerty", "https://www.youtube.com/watch?v=REQfiT1qvGQ",
#      "https://habr.com/"],
#     "qwertysdga430asd21wer12sdfsa",
#     [1, 2, 3, 4, 5, -3, 3, -2, 13, -234, -234324, -234, "1234", "qwerqt", "pupupu", -148],
#     [1, 2, 3, 4, 5, -3, 3, -2, 13, -234, -234324, -234, "1234", "qwerqt", "pupupu", -148],
#     ([1, 2, 3, 4, 5, -3, 3, -2, 13, -234, -234324, -234, "1234", "qwerqt", "pupupu", -148],
#      [1, "qwert", 148, "titi", 'q', "90", -3, 48, -234])
# ]
#
#
# for i in range(len(menu)):
#     print("\n", task_list[i])
#     data_item = data[i]
#
#
#     if isinstance(data_item, tuple):
#         menu[i](*data_item)
#     else:
#         menu[i](data_item)


# 2 вариант
# tasks = [
#     (task_01, 100000005, 0),
#     (task_02, 1092384345, 1),
#     (task_03, "qwezf124r2344 wer990rt", 2),
#     (task_04, (2, 101, 2), 3),
#     (task_05, [1, 2, 3, 4, -5, 0, 23, -123], 4),
#     (task_06, ("12", "qwertysdga434asd21wer12sdfsa"), 5),
#     (task_07, ["123444", "https://web.telegram.org/", "qwerty", "https://www.youtube.com/watch?v=REQfiT1qvGQ", "https://habr.com/"], 6),
#     (task_08, "qwertysdga430asd21wer12sdfsa", 7),
#     (task_09_1, [1, 2, 3, 4, 5, -3, 3, -2, 13, -234, -234324, -234, "1234", "qwerqt", "pupupu", -148], 8),
#     (task_09_2, [1, 2, 3, 4, 5, -3, 3, -2, 13, -234, -234324, -234, "1234", "qwerqt", "pupupu", -148], 9),
#     (task_10, ([1, 2, 3, 4, 5, -3, 3, -2, 13, -234, -234324, -234, "1234", "qwerqt", "pupupu", -148],
#                [1, "qwert", 148, "titi", 'q', "90", -3, 48, -234]), 10)
# ]
#
# for func, args, idx in tasks:
#     print("\n", task_list[idx])
#     if isinstance(args, tuple):
#         func(*args)
#     else:
#         func(args)

tasks_config = {
    0: (task_01, (100000005,)),
    1: (task_02, (1092384345,)),
    2: (task_03, ("qwezf124r2344 wer990rt",)),
    3: (task_04, (2, 101, 2)),
    4: (task_05, ([1, 2, 3, 4, -5, 0, 23, -123],)),
    5: (task_06, ("12", "qwertysdga434asd21wer12sdfsa",)),
    6: (task_07, (["123444", "https://web.telegram.org/", "qwerty", "https://www.youtube.com/watch?v=REQfiT1qvGQ", "https://habr.com/"],)),
    7: (task_08, ("qwertysdga430asd21wer12sdfsa",)),
    8: (task_09_1, ([1, 2, 3, 4, 5, -3, 3, -2, 13, -234, -234324, -234, "1234", "qwerqt", "pupupu", -148],)),
    9: (task_09_2, ([1, 2, 3, 4, 5, -3, 3, -2, 13, -234, -234324, -234, "1234", "qwerqt", "pupupu", -148],)),
    10: (task_10, ([1, 2, 3, 4, 5, -3, 3, -2, 13, -234, -234324, -234, "1234", "qwerqt", "pupupu", -148],
                   [1, "qwert", 148, "titi", 'q', "90", -3, 48, -234]))
}

for idx, (func, args) in tasks_config.items():
    print("\n", task_list[idx])
    func(*args)

    # if isinstance(args, tuple):
    #     func(*args)
    # else:
    #     func(args)
