class Time:
    MAX_HOURS = 24
    MAX_MINUTES = 60
    MAX_SECONDS = 60

    def __init__(self, hours, minutes, seconds):
        self._hours = None
        self._minutes = None
        self._seconds = None

        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    @property
    def hours(self):
        return self._hours

    @hours.setter
    def hours(self, value):
        if 0 <= value < 24 :
            self._hours = value
        else:
            raise ValueError(f"Значение {value} не входит в диапазон от 0 до 23")

    @property
    def minutes(self):
        return self._minutes

    @minutes.setter
    def minutes(self, value):
        if 0 <= value < 60 :
            self._minutes = value
        else:
            raise ValueError(f"Значение {value} не входит в диапазон от 0 до 59")

    @property
    def seconds(self):
        return self._seconds

    @seconds.setter
    def seconds(self, value):
        if 0 <= value < 60 :
            self._seconds = value
        else:
            raise ValueError(f"Значение {value} не входит в диапазон от 0 до 59")



    def __str__(self):
        return f"time = {self._hours}:{self._minutes}:{self._seconds}"

    # сравнение
    def __eq__ (self,other):        # ==
        return self._hours == other._hours and self._minutes == other._minutes and self._seconds == other._seconds

    def __lt__(self, other):        # <
        if self._hours != other._hours:
            return self._hours < other._hours
        elif self._minutes != other._minutes:
            return self._minutes < other._minutes
        else:
            return self._seconds < other._seconds

    def __gt__(self, other):        # >
        if self._hours != other._hours:
            return self._hours > other._hours
        elif self._minutes != other._minutes:
            return self._minutes > other._minutes
        else:
            return self._seconds > other._seconds

    # арифм операторы
    def __add__(self, other):       # +
        h = self._hours - other._hours
        m = self._minutes - other._minutes
        s = self._seconds - other._seconds

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
        h = self._hours - other._hours
        m = self._minutes - other._minutes
        s = self._seconds - other._seconds

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
        h = self._hours * other._hours
        m = self._minutes * other._minutes
        s = self._seconds * other._seconds

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
        if other._hours == 0:
            other._hours = 1
        if other._minutes == 0:
            other._minutes = 1
        if other._seconds == 0:
            other._seconds = 1

        result = Time(
            self._hours // other._hours,
            self._minutes // other._minutes,
            self._seconds // other._seconds
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
