from calfi import fin_cal as fc
from datetime import date, timedelta


def test_business_calendar():
    bc = fc.BusinessCalendar(days_off=[fc.fixed_day(1, 1), fc.fixed_day(12, 25)])
    assert len(list(bc.days(2023))) == 365
    assert len(list(bc.days(2024))) == 366  # Leap year
    assert len(list(bc.days_off(2023))) == 2
    # Weekdays
    assert bc.is_week_day(date(2023, 3, 15))  # Wednesday
    assert not bc.is_week_day(date(2023, 3, 18))  # Saturday
    assert not bc.is_week_day(date(2023, 3, 19))  # Sunday
    assert bc.is_week_day(date(2025, 1, 1))  # New Year's Day
    # Business days
    assert bc.is_business_day(date(2023, 3, 15))  # Wednesday
    assert not bc.is_business_day(date(2023, 3, 18))  # Saturday
    assert not bc.is_business_day(date(2023, 3, 19))  # Sunday
    assert not bc.is_business_day(date(2023, 1, 1))  # New Year's Day
    assert not bc.is_business_day(date(2023, 12, 25))  # Christmas
    # Next/Previous weekdays
    assert bc.next_week_day(date(2023, 3, 17), True) == date(2023, 3, 17)  # Friday
    assert bc.next_week_day(date(2023, 3, 18), True) == date(2023, 3, 20)  # Saturday
    assert bc.next_week_day(date(2023, 3, 17), False) == date(2023, 3, 20)  # Monday
    assert bc.previous_week_day(date(2023, 3, 19)) == date(2023, 3, 17)  # Friday
    assert bc.previous_week_day(date(2023, 3, 20)) == date(2023, 3, 20)  # Monday
    assert bc.next_business_day(date(2023, 12, 23), False) == date(
        2023, 12, 26
    )  # Skip Christmas
    assert bc.next_business_day(date(2023, 12, 22)) == date(
        2023, 12, 22
    )  # Skip Christmas
    assert bc.previous_business_day(date(2023, 1, 2), False) == date(
        2022, 12, 30
    )  # Skip New Year's Day
    assert bc.previous_business_day(date(2023, 1, 2)) == date(
        2023, 1, 2
    )  # Skip New Year's Day


def test_target_calendar():
    target = fc.Target()
    # Known holidays
    assert not target.is_business_day(date(2023, 4, 7))  # Good Friday
    assert not target.is_business_day(date(2023, 4, 10))  # Easter Monday
    assert not target.is_business_day(date(2023, 1, 1))  # New Year's Day
    assert not target.is_business_day(date(2023, 5, 1))  # Labor Day
    assert not target.is_business_day(date(2023, 12, 25))  # Christmas
    assert not target.is_business_day(date(2023, 12, 26))  # St. Stephen's Day
    # Business days
    assert target.is_business_day(date(2023, 4, 6))  # Thursday before Good Friday
    assert target.is_business_day(date(2023, 4, 11))  # Tuesday after Easter Monday
    assert target.is_business_day(date(2023, 5, 2))  # Day after Labor Day


def test_us_calendar():
    us = fc.USGovt()
    # Known holidays
    assert not us.is_business_day(date(2023, 1, 2))  # New Year's Day observed
    assert not us.is_business_day(date(2023, 1, 16))  # Martin Luther King Jr. Day
    assert not us.is_business_day(date(2023, 2, 20))  # Presidents' Day
    assert not us.is_business_day(date(2023, 5, 29))  # Memorial Day
    assert not us.is_business_day(date(2023, 6, 19))  # Juneteenth
    assert not us.is_business_day(date(2023, 7, 4))  # Independence Day
    assert not us.is_business_day(date(2023, 9, 4))  # Labor Day
    assert not us.is_business_day(date(2023, 10, 9))  # Columbus Day
    assert not us.is_business_day(date(2023, 11, 10))  # Veterans Day observed
    assert not us.is_business_day(date(2023, 11, 23))  # Thanksgiving Day
    assert not us.is_business_day(date(2023, 12, 25))  # Christmas
    # Business days


def test_fixed_day():
    d = fc.fixed_day(12, 25)(2023)
    assert d == date(2023, 12, 25)
    d = fc.fixed_day(1, 1)(2024)
    assert d == date(2024, 1, 1)
    d = fc.fixed_day(7, 4)(2025)
    assert d == date(2025, 7, 4)


def test_good_friday():
    # Known Easter Sunday date
    for year, expected in _known_easter_dates().items():
        assert fc.easter_sunday_delta(delta=-2)(year) == (expected - timedelta(days=2))


def test_easter_monday():
    # Known Easter Sunday date
    for year, expected in _known_easter_dates().items():
        assert fc.easter_sunday_delta(delta=1)(year) == (expected + timedelta(days=1))


def _known_easter_dates() -> dict[int, date]:
    return {
        2008: date(2008, 3, 23),
        2009: date(2009, 4, 12),
        2010: date(2010, 4, 4),
        2011: date(2011, 4, 24),
        2012: date(2012, 4, 8),
        2013: date(2013, 3, 31),
        2014: date(2014, 4, 20),
        2015: date(2015, 4, 5),
        2016: date(2016, 3, 27),
        2017: date(2017, 4, 16),
        2018: date(2018, 4, 1),
        2019: date(2019, 4, 21),
        2020: date(2020, 4, 12),
        2021: date(2021, 4, 4),
        2022: date(2022, 4, 17),
        2023: date(2023, 4, 9),
        2024: date(2024, 3, 31),
        2025: date(2025, 4, 20),
        2026: date(2026, 4, 5),
        2027: date(2027, 3, 28),
        2028: date(2028, 4, 16),
        2029: date(2029, 4, 1),
        2030: date(2030, 4, 21),
        2031: date(2031, 4, 13),
        2032: date(2032, 3, 28),
        2033: date(2033, 4, 17),
        2034: date(2034, 4, 9),
        2035: date(2035, 3, 25),
        2036: date(2036, 4, 13),
        2037: date(2037, 4, 5),
        2038: date(2038, 4, 25),
        2039: date(2039, 4, 10),
        2040: date(2040, 4, 1),
    }
