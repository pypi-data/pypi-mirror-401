import calendar as py_calendar
from datetime import date, timedelta
from typing import Callable, Iterator


class BusinessCalendar(py_calendar.Calendar):
    """A calendar that defines business days by excluding weekends and specified holidays.

    Args:
        days_off: List of callable functions that return holiday dates for a given year.
    """

    def __init__(self, days_off: list[Callable[[int], date | None]]):
        super().__init__()
        self._days_off: list[Callable[[int], date | None]] = days_off

    def days(self, year: int) -> Iterator[date]:
        """Iterate over all days in the year."""
        day = date(year, 1, 1)
        while day.year == year:
            yield day
            day += timedelta(days=1)

    def week_days(self, year: int) -> Iterator[date]:
        """Iterate over weekdays (Monday-Friday) in the year."""
        return filter(self.is_week_day, self.days(year))

    def days_off(self, year: int) -> Iterator[date]:
        """Iterate over all holidays in the year."""
        return iter(
            sorted(
                filter(
                    lambda day: day is not None,
                    (day_off(year) for day_off in self._days_off),
                )
            )
        )

    def business_days(self, year: int) -> Iterator[date]:
        """Iterate over business days (weekdays minus holidays) in the year."""
        days_off_it = self.days_off(year)
        days_it = self.week_days(year)
        return filter(lambda d: d not in days_off_it, days_it)

    def is_week_day(self, dt: date) -> bool:
        """Check if a date is a weekday (Monday-Friday)."""
        return dt.weekday() < 5

    def next_week_day(self, dt: date, included: bool = True) -> date:
        """Find the next weekday from the given date.

        Args:
            dt: Starting date
            included: If True, return dt if it's already a weekday

        Returns:
            Next weekday date
        """
        next_day = dt if included else dt + timedelta(days=1)
        return (
            next_day
            if self.is_week_day(next_day)
            else next_day + timedelta(days=7 - next_day.weekday())
        )

    def previous_week_day(self, dt: date, included: bool = True) -> date:
        """Find the previous weekday from the given date.

        Args:
            dt: Starting date
            included: If True, return dt if it's already a weekday

        Returns:
            Previous weekday date
        """
        prev_day = dt if included else dt - timedelta(days=1)
        return (
            prev_day
            if self.is_week_day(prev_day)
            else prev_day - timedelta(days=prev_day.weekday() - 4)
        )

    def is_business_day(self, dt: date) -> bool:
        """Check if a date is a business day (weekday and not a holiday).

        Args:
            dt: Date to check

        Returns:
            True if the date is a business day
        """
        if not self.is_week_day(dt):
            return False
        return all(day != dt for day in self.days_off(dt.year))

    def is_day_off(self, dt: date) -> bool:
        """Check if a date is a day off (weekend or holiday).

        Args:
            dt: Date to check

        Returns:
            True if the date is a day off
        """
        return not self.is_business_day(dt)

    def next_business_day(self, dt: date, included: bool = True) -> date:
        """Find the next business day from the given date.

        Args:
            dt: Starting date
            included: If True, return dt if it's already a business day

        Returns:
            Next business day date
        """
        next_day = self.next_week_day(dt=dt, included=included)
        this_year = next_day.year
        this_year_days_off = filter(
            lambda day: day >= next_day, self.days_off(this_year)
        )
        next_day_off = next(this_year_days_off, None)
        if next_day_off is None or next_day < next_day_off:
            return next_day
        else:
            return self.next_business_day(next_day, included=False)

    def previous_business_day(self, dt: date, included: bool = True) -> date:
        """Find the previous business day from the given date.

        Args:
            dt: Starting date
            included: If True, return dt if it's already a business day

        Returns:
            Previous business day date
        """
        prev_day = self.previous_week_day(dt=dt, included=included)
        this_year = prev_day.year
        this_year_days_off = filter(
            lambda day: day <= prev_day, self.days_off(this_year)
        )
        prev_day_off = next(reversed(list(this_year_days_off)), None)
        if prev_day_off is None or prev_day > prev_day_off:
            return prev_day
        else:
            return self.previous_business_day(prev_day, included=False)


# Predefined Calendars
class Target(BusinessCalendar):
    def __init__(self):
        super().__init__(
            days_off=[
                fixed_day(1, 1),
                easter_sunday_delta(delta=-2),  # Good Friday
                easter_sunday_delta(delta=1),  # Easter Monday
                fixed_day(5, 1),
                fixed_day(12, 25),
                fixed_day(12, 26),
            ]
        )


class USGovt(BusinessCalendar):
    def __init__(self):
        super().__init__(
            days_off=[
                us_dayoff_adjust(fixed_day(1, 1)),  # New Year's Day
                _mlk_day,
                _presidents_day,
                memorial_day,
                us_dayoff_adjust(_juneteenth),
                us_dayoff_adjust(fixed_day(7, 4)),
                _us_labor_day,
                _columbus_day,
                us_dayoff_adjust(fixed_day(11, 11)),  # Veterans Day
                _thanksgiving_day,
                us_dayoff_adjust(fixed_day(12, 25)),  # Christmas Day
            ]
        )


# Helper functions for common holidays patterns
def fixed_day(month: int, day: int) -> Callable[[int], date | None]:
    """Create a holiday that occurs on a fixed date every year.

    Args:
        month: Month number (1-12)
        day: Day of the month (1-31)

    Returns:
        A callable that takes a year and returns the holiday date, or None if invalid.

    Example:
        new_years = fixed_day(1, 1)  # January 1st every year
    """
    return lambda year: date(year, month, day)


def nth_weekday_of_month(
    month: int, weekday: int, n: int
) -> Callable[[int], date | None]:
    """Create a holiday that occurs on the nth weekday of a month.

    Args:
        month: Month number (1-12)
        weekday: Weekday number (0=Monday, 6=Sunday)
        n: Which occurrence (1=first, 2=second, etc.)

    Returns:
        A callable that takes a year and returns the holiday date.

    Example:
        mlk_day = nth_weekday_of_month(1, 0, 3)  # Third Monday in January
    """
    return lambda year: _nth_weekday_of_month(year, month, weekday, n)


def last_weekday_of_month(month: int, weekday: int) -> Callable[[int], date | None]:
    """Create a holiday that occurs on the last weekday of a month.

    Args:
        month: Month number (1-12)
        weekday: Weekday number (0=Monday, 6=Sunday)

    Returns:
        A callable that takes a year and returns the holiday date.

    Example:
        memorial_day = last_weekday_of_month(5, 0)  # Last Monday in May
    """
    return lambda year: _last_weekday_of_month(year, month, weekday)


def easter_sunday_delta(delta: int) -> Callable[[int], date | None]:
    """Create a holiday relative to Easter Sunday.

    Args:
        delta: Days offset from Easter Sunday (negative = before, positive = after)

    Returns:
        A callable that takes a year and returns the holiday date.

    Example:
        good_friday = easter_sunday_delta(-2)  # 2 days before Easter
        easter_monday = easter_sunday_delta(1)  # 1 day after Easter
    """
    return lambda year: _easter(year) + timedelta(days=delta)


def us_dayoff_adjust(day: Callable[[int], date | None]) -> Callable[[int], date | None]:
    """Adjust a holiday to the nearest weekday (US federal holiday rule).

    If the holiday falls on Saturday, moves it to Friday.
    If the holiday falls on Sunday, moves it to Monday.

    Args:
        day: A holiday function that returns a date or None

    Returns:
        A callable that takes a year and returns the adjusted holiday date.

    Example:
        adjusted_christmas = us_dayoff_adjust(fixed_day(12, 25))
    """
    return lambda year: _us_dayoff_adjust(day(year))


# Helpers for calculating specific holidays
def _easter(y: int) -> date:
    """Copied from dateutil but i did not want to be dependant of the whole library"""
    c = y // 100
    g = y % 19
    h = (c - c // 4 - (8 * c + 13) // 25 + 19 * g + 15) % 30
    i = h - (h // 28) * (1 - (h // 28) * (29 // (h + 1)) * ((21 - g) // 11))
    j = (y + y // 4 + i + 2 - c + c // 4) % 7
    p = i - j
    d = 1 + (p + 27 + (p + 6) // 40) % 31
    m = 3 + (p + 26) // 30
    return date(int(y), int(m), int(d))


def _last_weekday_of_month(year: int, month: int, weekday: int) -> date:
    last_day = date(
        year if month < 12 else year + 1, month + 1 if month < 12 else 1, 1
    ) - timedelta(days=1)
    last_weekday = last_day - timedelta(days=(last_day.weekday() - weekday + 7) % 7)
    return last_weekday


def _nth_weekday_of_month(year: int, month: int, weekday: int, n: int) -> date:
    first_day = date(year, month, 1)
    first_weekday = first_day + timedelta(days=(weekday - first_day.weekday() + 7) % 7)
    return first_weekday + timedelta(weeks=n - 1)


def _us_dayoff_adjust(unadjusted_day: date | None) -> date | None:
    if unadjusted_day is None:
        return None
    weekday = unadjusted_day.weekday()
    adjust = (weekday // 5) * (2 * (weekday // 6) - 1)
    return unadjusted_day + timedelta(days=adjust)


# Others
def _mlk_day(year: int) -> date | None:
    # MLK Day is the third Monday in January
    if year < 1986:
        return None
    return _nth_weekday_of_month(year, 1, 0, 3)


def _presidents_day(year: int) -> date | None:
    # Presidents' Day is the third Monday in February
    if year < 1879:
        return None
    return _nth_weekday_of_month(year, 2, 0, 3)


def _thanksgiving_day(year: int) -> date | None:
    # Thanksgiving Day is the fourth Thursday in November
    if year < 1863:
        return None
    return _nth_weekday_of_month(year, 11, 3, 4)


def _us_labor_day(year: int) -> date | None:
    # Labor Day is the first Monday in September
    return _nth_weekday_of_month(year, 9, 0, 1)


def _columbus_day(year: int) -> date | None:
    # Columbus Day is the second Monday in October
    return _nth_weekday_of_month(year, 10, 0, 2)


def memorial_day(year: int) -> date | None:
    # Memorial Day is the last Monday in May
    if year < 1971:
        return None
    return _last_weekday_of_month(year, 5, 0)


def _juneteenth(year: int) -> date | None:
    if year <= 2021:
        return None
    return date(year, 6, 19)
