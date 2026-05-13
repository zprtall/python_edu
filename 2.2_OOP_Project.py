import re
import json

class Person:
    RETIREMENT_AGE = 65
    CURRENT_YEAR = 2026

    def __init__(self, surname, name, birth_date, gender, city):
        self.surname = surname
        self.name = name
        self.birth_date = birth_date
        self.gender = gender
        self.city = city

    # ---------------- AGE ----------------
    @property
    def age(self):
        year = int(self._birth_date.split(":")[2])
        return self.CURRENT_YEAR - year

    # ---------------- SURNAME ----------------
    @property
    def surname(self):
        return self._surname

    @surname.setter
    def surname(self, value):
        if not isinstance(value, str) or len(value) < 2:
            raise ValueError("Неверный формат фамилии")
        self._surname = value

    # ---------------- NAME ----------------
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value) < 2:
            raise ValueError("Неверный формат имени")
        self._name = value

    # ---------------- BIRTH DATE ----------------
    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value):
        pattern = r"^(0[1-9]|[12][0-9]|3[01]):(0[1-9]|1[0-2]):\d{4}$"
        if not isinstance(value, str) or not re.match(pattern, value):
            raise ValueError("Неверный формат даты (dd:mm:yyyy)")
        self._birth_date = value

    # ---------------- GENDER ----------------
    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, value):
        if value not in ("m", "w"):
            raise ValueError("Неверный формат пола (m/w)")
        self._gender = value

    # ---------------- CITY ----------------
    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Неверный формат города")
        self._city = value


class Candidate(Person):
    def __init__(self, surname, name, birth_date, gender, city,
                 id, job_title, comments, status="Новый"):
        super().__init__(surname, name, birth_date, gender, city)
        self.id = id
        self.job_title = job_title
        self.status = status
        self.comments = comments

    def __str__(self):
        return (
            f"ID: {self.id}\n"
            f"{self.surname} {self.name}\n"
            f"Возраст: {self.age}\n"
            f"Город: {self.city}\n"
            f"Должность: {self.job_title}\n"
            f"Статус: {self.status}\n"
            f"Комментарий: {self.comments}\n"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "surname": self.surname,
            "name": self.name,
            "birth_date": self.birth_date,
            "gender": self.gender,
            "city": self.city,
            "job_title": self.job_title,
            "status": self.status,
            "comments": self.comments
        }

class Candidate_System:
    def __init__(self, candidates=None):
        self.candidates = candidates or []

    def __str__(self):
        result = ""
        for c in self.candidates:
            result += str(c) + "\n" + "-" * 30 + "\n"
        return result

    def add_candidate(self, candidate):
        self.candidates.append(candidate)

    def remove_candidate(self, candidate_id):
        self.candidates = [
            c for c in self.candidates if c.id != candidate_id
        ]

    def save_data(self, filename="candidates.json"):
        data = [c.to_dict() for c in self.candidates]

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_data(self, filename="candidates.json"):
        import json

        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.candidates = [Candidate(**{
            "surname": c["surname"],
            "name": c["name"],
            "birth_date": c["birth_date"],
            "gender": c["gender"],
            "city": c["city"],
            "id": c["id"],
            "job_title": c["job_title"],
            "comments": c["comments"],
            "status": c["status"]
        }) for c in data]


class App:
    def __init__(self):
        self.system = Candidate_System()

    def main_loop(self):
        while True:
            print("\n===== MENU =====")
            print("1. Показать всех кандидатов")
            print("2. Добавить кандидата")
            print("3. Удалить кандидата")
            print("4. Сохранить в JSON")
            print("5. Загрузить из JSON")
            print("0. Выход")

            choice = input("Выбор: ")

            if choice == "1":
                print(self.system)

            elif choice == "2":
                self.add_candidate()

            elif choice == "3":
                cid = int(input("ID кандидата: "))
                self.system.remove_candidate(cid)

            elif choice == "4":
                self.system.save_data()
                print("Сохранено!")

            elif choice == "5":
                self.system.load_data()
                print("Загружено!")

            elif choice == "0":
                break

            else:
                print("Неверный выбор")

    def add_candidate(self):
        print("\n--- Новый кандидат ---")

        c = Candidate(
            surname=input("Фамилия: "),
            name=input("Имя: "),
            birth_date=input("Дата (dd:mm:yyyy): "),
            gender=input("Пол (m/w): "),
            city=input("Город: "),
            id=int(input("ID: ")),
            job_title=input("Должность: "),
            comments=input("Комментарий: "),
            status="Новый"
        )

        self.system.add_candidate(c)
        print("Добавлено!")


my_test = [
    Candidate(
        "Ivanov",
        "Ivan",
        "12:05:1998",
        "m",
        "Moscow",
        1,
        "Python Developer",
        "Junior candidate, knows Django",
        "Новый"
    ),
    Candidate(
        "Petrov",
        "Alexey",
        "03:11:1995",
        "m",
        "Saint Petersburg",
        2,
        "Data Analyst",
        "Knows SQL and Python, some experience in BI",
        "В процессе"
    ),
    Candidate(
        "Sidorova",
        "Anna",
        "27:06:2000",
        "w",
        "Kazan",
        3,
        "Frontend Developer",
        "React, HTML, CSS, beginner level",
        "Новый"
    ),
    Candidate(
        "Smirnov",
        "Dmitry",
        "15:09:1992",
        "m",
        "Novosibirsk",
        4,
        "DevOps Engineer",
        "Docker, Linux, CI/CD pipelines",
        "Принят"
    ),
    Candidate(
        "Kuznetsova",
        "Elena",
        "08:02:1997",
        "w",
        "Yekaterinburg",
        5,
        "UX/UI Designer",
        "Figma, user research, prototyping",
        "Отказ"
    )
]


app = App()
app.system.candidates = my_test   # загрузка тестовых данных
app.main_loop()
