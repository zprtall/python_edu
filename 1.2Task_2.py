class Time:
    MAX_HOURS = 24
    MAX_MINUTES = 60
    MAX_SECONDS = 60

    def __init__(self, hours, minutes, seconds):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    def __str__(self):
        return f"time = {self.hours}:{self.minutes}:{self.seconds}"

    # сравнение
    def __eq__ (self,other):        # ==
        return self.hours == other.hour and self.minutes == other.minutes and self.seconds == other.seconds

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
        result = Time(
            self.hours + other.hours,
            self.minutes + other.minutes,
            self.seconds + other.seconds
        )

        if result.seconds >= Time.MAX_SECONDS:
            result.minutes += result.seconds // Time.MAX_SECONDS
            result.seconds = result.seconds % Time.MAX_SECONDS

        if result.minutes >= Time.MAX_MINUTES:
            result.hours += result.minutes // Time.MAX_MINUTES
            result.minutes = result.minutes % Time.MAX_MINUTES

        if result.hours >= Time.MAX_HOURS:
            result.hours = result.hours % Time.MAX_HOURS

        return result

    def __sub__(self, other):       # -
        result = Time(
            self.hours - other.hours,
            self.minutes - other.minutes,
            self.seconds - other.seconds
        )

        if result.seconds < 0:
            result.minutes -= 1
            result.seconds = Time.MAX_SECONDS + result.seconds

        if result.minutes < 0:
            result.hours -= 1
            result.minutes = Time.MAX_MINUTES + result.minutes

        if result.hours < 0:
            result.hours = Time.MAX_HOURS + result.hours

        return result

    def __mul__(self, other):       # умножение но я не знаю как ты хочешь что бы я реализовал, как есть
        #или что бы переводилось в секунды а потом разбивалось
        result = Time(
            self.hours * other.hours,
            self.minutes * other.minutes,
            self.seconds * other.seconds
        )

        if result.seconds >= Time.MAX_SECONDS:
            result.minutes += result.seconds // Time.MAX_SECONDS
            result.seconds = result.seconds % Time.MAX_SECONDS

        if result.minutes >= Time.MAX_MINUTES:
            result.hours += result.minutes // Time.MAX_MINUTES
            result.minutes = result.minutes % Time.MAX_MINUTES

        if result.hours >= Time.MAX_HOURS:
            result.hours = result.hours % Time.MAX_HOURS

        return result

    def __floordiv__(self, other):       # /
        if other.hours == 0:
            other.hours = 1
        if other.minutes == 0:
            other.minutes = 1
        if other.seconds == 0:
            other.seconds = 1

        result = Time(
            self.hours // other.hours,
            self.minutes // other.minutes,
            self.seconds // other.seconds
        )
        return result


            

#тесты для вычитания
# time1 = Time(15, 10, 15)
# time2 = Time(12, 45, 50)
# ожидается time3 = 2:24:25

# time1 = Time(10, 45, 30)
# time2 = Time(5, 20, 10)
# ожидается time3 = 05:25:20

#тесты для умножения
# time1 = Time(12, 30, 30)
# time2 = Time(2, 2, 2)
# ожидается time3 = 1:1:0

# time1 = Time(0, 0, 30)
# time2 = Time(0, 0, 2)
# ожидается time3 = 0:1:0

time1 = Time(10, 5, 6)
time2 = Time(3, 2, 3)


time3 = time1 // time2
print(time3)

