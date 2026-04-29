class Time:
    MAX_HOURS = 24
    MAX_MINUTES = 60
    MAX_SECONDS = 60

    def __init__(self, hours, minutes, seconds):
        self.hours = None
        self.minutes = None
        self.seconds = None

        self.hours_set = hours
        self.minutes_set = minutes
        self.seconds_set = seconds

    @property
    def hours_set(self):
        return self.hours

    @hours_set.setter
    def hours_set(self, value):
        if value < 0 or value > 23 :
            raise ValueError(f"Значение {value} не входит в диапазон от 0 до 23")
        else:
            self.hours = value

    @property
    def minutes_set(self):
        return self.minutes

    @minutes_set.setter
    def minutes_set(self, value):
        if value < 0 or value > 59 :
            raise ValueError(f"Значение {value} не входит в диапазон от 0 до 59")
        else:
            self.minutes = value

    @property
    def seconds_set(self):
        return self.seconds

    @seconds_set.setter
    def seconds_set(self, value):
        if value < 0 or value > 59:
            raise ValueError(f"Значение {value} не входит в диапазон от 0 до 59")
        else:
            self.seconds = value



    def __str__(self):
        return f"time = {self.hours}:{self.minutes}:{self.seconds}"

    # сравнение
    def __eq__ (self,other):        # ==
        return self.hours == other.hours and self.minutes == other.minutes and self.seconds == other.seconds

    def __lt__(self, other):        # <
        if self.hours != other.hours:
            return self.hours < other.hours
        elif self.minutes != other.minutes:
            return self.minutes < other.minutes
        else:
            return self.seconds < other.seconds

    def __gt__(self, other):        # >
        if self.hours != other.hours:
            return self.hours > other.hours
        elif self.minutes != other.minutes:
            return self.minutes > other.minutes
        else:
            return self.seconds > other.seconds

    # арифм операторы
    def __add__(self, other):       # +
        h = self.hours - other.hours
        m = self.minutes - other.minutes
        s = self.seconds - other.seconds

        if s > 59:
            s -= 60
            m += 1

        if m > 59:
            m -= 60
            h += 1

        if h > 23:
            h -= 24

        return Time(h, m, s)

    def __sub__(self, other):
        h = self.hours - other.hours
        m = self.minutes - other.minutes
        s = self.seconds - other.seconds

        if s < 0:
            s += 60
            m -= 1

        if m < 0:
            m += 60
            h -= 1

        if h < 0:
            h += 24

        return Time(h, m, s)

    def __mul__(self, other):
        h = self.hours * other.hours
        m = self.minutes * other.minutes
        s = self.seconds * other.seconds

        if s >= 60:
            m += s // 60
            s = s % 60

        if m >= 60:
            h += m // 60
            m = m % 60

        if h >= 24:
            h = h % 24

        return Time(h, m, s)

    def __floordiv__(self, other):       # /
        result = Time(
            self.hours // (other.hours or 1),
            self.minutes // (other.minutes or 1),
            self.seconds // (other.seconds or 1)
        )
        return result

#тесты для вычитания
time1 = Time(15, 10, 15)
time2 = Time(12, 45, 50)
print (time1 - time2)
# ожидается time3 = 2:24:25

time1 = Time(10, 45, 30)
time2 = Time(5, 20, 10)
print (time1 - time2)
# ожидается time3 = 05:25:20

#тесты для умножения
time1 = Time(12, 30, 30)
time2 = Time(2, 2, 2)
print (time1 * time2)
# ожидается time3 = 1:1:0

time1 = Time(0, 0, 30)
time2 = Time(0, 0, 2)
print (time1 * time2)
# ожидается time3 = 0:1:0

# time1 = Time(-1, 5, 6)
# time2 = Time(3, 2, 3)
#
# time3 = time1 // time2
# print(time3)
