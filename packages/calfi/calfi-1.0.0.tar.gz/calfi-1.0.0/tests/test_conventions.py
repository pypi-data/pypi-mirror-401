from calfi import conventions as conv
from calfi.fin_cal import USGovt
from datetime import date


def test_next_date():
    d = conv.Frequency.ANNUAL.next_date(date(2023, 3, 15))
    assert d == date(2024, 3, 15)

    d = conv.Frequency.ANNUAL.next_date(date(2024, 2, 29))
    assert d == date(2025, 2, 28)

    d = conv.Frequency.SEMI_ANNUAL.next_date(date(2023, 3, 15))
    assert d == date(2023, 9, 15)

    d = conv.Frequency.SEMI_ANNUAL.next_date(date(2023, 9, 15))
    assert d == date(2024, 3, 15)

    d = conv.Frequency.SEMI_ANNUAL.next_date(date(2024, 2, 29))
    assert d == date(2024, 8, 29)

    d = conv.Frequency.SEMI_ANNUAL.next_date(date(2023, 8, 29))
    assert d == date(2024, 2, 29)

    d = conv.Frequency.SEMI_ANNUAL.next_date(date(2023, 8, 30))
    assert d == date(2024, 2, 29)

    d = conv.Frequency.SEMI_ANNUAL.next_date(date(2023, 8, 31))
    assert d == date(2024, 2, 29)

    d = conv.Frequency.SEMI_ANNUAL.next_date(date(2024, 8, 31))
    assert d == date(2025, 2, 28)

    d = conv.Frequency.QUARTERLY.next_date(date(2023, 3, 15))
    assert d == date(2023, 6, 15)

    d = conv.Frequency.MONTHLY.next_date(date(2023, 3, 15))
    assert d == date(2023, 4, 15)

    d = conv.Frequency.WEEKLY.next_date(date(2023, 3, 15))
    assert d == date(2023, 3, 22)

    d = conv.Frequency.DAILY.next_date(date(2023, 3, 15))
    assert d == date(2023, 3, 16)


def test_business_day_convention():
    us = USGovt()
    dt = date(2023, 12, 23)  # Saturday
    adjusted = conv.BusinessDayConvention.FOLLOWING.adjust_date(dt, us)
    assert adjusted == date(2023, 12, 26)  # Tuesday (25th is Christmas)

    dt = date(2023, 12, 23)  # Saturday
    adjusted = conv.BusinessDayConvention.PRECEDING.adjust_date(dt, us)
    assert adjusted == date(2023, 12, 22)  # Friday

    dt = date(2023, 12, 30)  # Saturday
    adjusted = conv.BusinessDayConvention.MODIFIED_FOLLOWING.adjust_date(dt, us)
    assert adjusted == date(2023, 12, 29)  # Friday (next business day is in next month)

    dt = date(2023, 1, 1)  # Sunday
    adjusted = conv.BusinessDayConvention.MODIFIED_PRECEDING.adjust_date(dt, us)
    assert (
        adjusted == date(2023, 1, 3)
    )  # Monday (previous business day is in previous month) and 2nd is observed holiday in the US in 2023


def test_day_count_convention():
    d = conv.DayCountConvention.ACT_360.days(date(2023, 1, 1), date(2023, 1, 15))
    assert d == 14
    d = conv.DayCountConvention.ACT_365.days(date(2023, 1, 1), date(2023, 1, 15))
    assert d == 14
    d = conv.DayCountConvention.THIRTY_360.days(date(2023, 1, 1), date(2023, 1, 15))
    assert d == 14
    d = conv.DayCountConvention.THIRTY_360.days(date(2023, 1, 31), date(2023, 2, 28))
    assert d == 30
    d = conv.DayCountConvention.THIRTY_360.days(date(2023, 1, 30), date(2023, 2, 28))
    assert d == 30
    d = conv.DayCountConvention.THIRTY_360.days(date(2024, 1, 31), date(2024, 2, 28))
    assert d == 28
    d = conv.DayCountConvention.THIRTY_360.days(date(2024, 1, 30), date(2024, 2, 29))
    assert d == 30
    d = conv.DayCountConvention.THIRTY_360.days(date(2024, 1, 31), date(2024, 2, 29))
    assert d == 30
    d = conv.DayCountConvention.THIRTY_360.days(date(2023, 1, 15), date(2024, 1, 15))
    assert d == 360
    d = conv.DayCountConvention.THIRTY_360.days(date(2023, 1, 31), date(2024, 1, 31))
    assert d == 360
    d = conv.DayCountConvention.THIRTY_360.days(date(2024, 2, 29), date(2025, 2, 28))
    assert d == 360
    d = conv.DayCountConvention.THIRTY_360.days(date(2024, 2, 27), date(2024, 2, 28))
    assert d == 1
    d = conv.DayCountConvention.THIRTY_360.days(date(2024, 2, 28), date(2024, 2, 29))
    assert d == 2

    d = conv.DayCountConvention.ACT_360.days(date(2022, 3, 1), date(2023, 3, 1))
    assert d == 365
    d = conv.DayCountConvention.ACT_360.days(date(2023, 3, 1), date(2024, 3, 1))
    assert d == 366
    d = conv.DayCountConvention.ACT_365.days(date(2023, 3, 1), date(2024, 3, 1))
    assert d == 366
    d = conv.DayCountConvention.ACT_ACT.days(date(2023, 3, 1), date(2024, 3, 1))
    assert d == 366
