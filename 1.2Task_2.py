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


            


time1 = Time(12, 45, 22)
time2 = Time(12, 11, 28)
time3 = time1 + time2
print(time3)
print(time1)
