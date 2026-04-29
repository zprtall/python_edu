import re

# опять насрал говна с сеттером, исправить что бы не вызывал сам себя через _surname и тд
class Person:
    RETIREMENT_AGE = 65
    CURRENT_YEAR = 2026

    def __init__(self, surname, name, birth_date, gender, city):
        self.surname = surname
        self.name = name
        self.birth_date = birth_date
        self.gender = gender
        self.city = city

    @property           # проверить работает ли вообще
    def age(self, ):
        return int(self.CURRENT_YEAR[range(6, 9)]) - self.birth_date[2]

    @property
    def surname(self):
        return self.surname

    @property
    def name(self):
        return self.surname

    @property
    def birth_date(self):
        return self.birth_date

    @property
    def gender(self):
        return self.gender

    @property
    def city(self):
        return self.city

    @surname.setter
    def surname(self, surname):
        if isinstance(self.surname) and len(self.surname) < 2:
            raise "Неверный формат фамилии"
        else:
            self.surname = surname

    @name.setter
    def name(self, name):
        if isinstance(self.name) and len(self.name) < 2:
            raise "Неверный формат имени"
        else:
            self.name = name

    @birth_date.setter
    def birth_date(self,birth_date):
        pattern = r"^(0[1-9]|[12][0-9]|3[01]):(0[1-9]|1[0-2]):\d{4}$"
        if not re.match(pattern, birth_date):
            raise "Неверный формат даты (dd:mm:yyyy)"
        else:
            self.birth_date = birth_date

    @gender.setter
    def gender(self, gender):
        if gender != ("m" or "w"):
            raise "Неверный формат пола (m/w)"
        else:
            self.gender = gender

    @city.setter
    def city(self,city):
        if not isinstance(city, str):
            raise "Неверный формат города"
        else:
            self.city = city

class Candidate(Person):
    def __init__(self, surname, name, birth_date, gender, city, id, job_title, comments, status = "Новый"):
        super().__init__(surname, name, birth_date, gender, city)
        self.id = id
        self.job_title = job_title
        self.status = status
        self.comments = comments

    def __str__(self):      # красивый вывод инфы по условию
        pass

    def to_dict(self):      # перевод в словарь для сохранений в json
        pass

class Candidate_System:
    def __init__(self,candidates,storage_file):
        self.candidates = candidates        #списки для хранения кандидатов
        self.storage_file = storage_file    # назв json файла

    def add_candidate(self):        # добавить кандидата
        pass

    def remove_candidate(self):     # удалить кандидата из списка
        pass


    def save_data(self):            # сохранили в json файлик
        pass

    def load_data(self):            # загрузили из json файлика
        pass

class App:
    def main_loop(self):        # выборка пункта меню в while'e
        pass
