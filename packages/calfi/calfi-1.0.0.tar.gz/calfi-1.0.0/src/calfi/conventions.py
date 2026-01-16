from enum import Enum, IntEnum
from datetime import date, timedelta
from calfi.fin_cal import BusinessCalendar


class DayCountConvention(Enum):
    """Enumeration of day count conventions used in financial calculations."""

    ACT_360 = "ACT/360"
    ACT_365 = "ACT/365"
    ACT_ACT = "ACT/ACT"
    THIRTY_360 = "30/360"

    def days(self, start_date: date, end_date: date) -> int:
        """Calculate the number of days between two dates according to this convention.

        Args:
            start_date: Start date (inclusive)
            end_date: End date (inclusive)

        Returns:
            Number of days according to the convention
        """
        delta = (end_date - start_date).days
        match self:
            case DayCountConvention.ACT_360:
                return delta
            case DayCountConvention.ACT_365:
                return delta
            case DayCountConvention.ACT_ACT:
                return delta
            case DayCountConvention.THIRTY_360:
                d1 = start_date.replace(day=min(start_date.day, 30))
                d2 = end_date.replace(day=min(end_date.day, 30))
                if (d1 + timedelta(days=1)).month != start_date.month:
                    d1 = 30
                else:
                    d1 = d1.day
                if (d2 + timedelta(days=1)).month != end_date.month:
                    d2 = 30
                else:
                    d2 = d2.day
                return (
                    (end_date.year - start_date.year) * 360
                    + (end_date.month - start_date.month) * 30
                    + (d2 - d1)
                )
            case _:
                raise ValueError(f"Unsupported day count convention: {self}")

    def denominator(self, year: int | None = None) -> int:
        """Get the denominator used for year fraction calculations.

        Args:
            year: Year for ACT/ACT calculations (optional)

        Returns:
            Denominator for the convention
        """
        match self:
            case DayCountConvention.ACT_360:
                return 360
            case DayCountConvention.ACT_365:
                return 365
            case DayCountConvention.ACT_ACT:
                if year is not None:
                    return self.days(date(year, 1, 1), date(year + 1, 1, 1))
                else:
                    return 365  # Simplified; actual ACT/ACT may vary
            case DayCountConvention.THIRTY_360:
                return 360
            case _:
                raise ValueError(f"Unsupported day count convention: {self}")


class BusinessDayConvention(Enum):
    """Enumeration of business day conventions for adjusting dates to business days."""

    FOLLOWING = "Following"
    MODIFIED_FOLLOWING = "Modified Following"
    PRECEDING = "Preceding"
    MODIFIED_PRECEDING = "Modified Preceding"
    EOM = "End of Month"

    def adjust_date(self, dt: date, calendar: BusinessCalendar) -> date:
        """Adjust a date according to this business day convention.

        Args:
            dt: Date to adjust
            calendar: Business calendar to use for business day determination

        Returns:
            Adjusted date that falls on a business day
        """
        match self:
            case BusinessDayConvention.FOLLOWING:
                return calendar.next_business_day(dt, included=True)
            case BusinessDayConvention.PRECEDING:
                return calendar.previous_business_day(dt, included=True)
            case BusinessDayConvention.MODIFIED_FOLLOWING:
                following = calendar.next_business_day(dt, included=True)
                if following.month != dt.month:
                    return calendar.previous_business_day(dt, included=False)
                return following
            case BusinessDayConvention.MODIFIED_PRECEDING:
                preceding = calendar.previous_business_day(dt, included=True)
                if preceding.month != dt.month:
                    return calendar.next_business_day(dt, included=False)
                return preceding
            case BusinessDayConvention.EOM:
                raise NotImplementedError("EOM adjustment not implemented yet")
                # return dt.replace(day=dt.monthrange(dt.year, dt.month)[1])


class Frequency(IntEnum):
    """Enumeration of payment frequencies for financial instruments."""

    ANNUAL = 1
    SEMI_ANNUAL = 2
    QUARTERLY = 4
    MONTHLY = 12
    WEEKLY = 52
    DAILY = 365

    def next_date(self, base_date: date) -> date:
        """Calculate the next payment date based on this frequency.

        Args:
            base_date: Base date for calculation

        Returns:
            Next date according to the frequency
        """
        match self:
            case Frequency.ANNUAL:
                day = min(
                    base_date.day,
                    (
                        date(base_date.year + 1, base_date.month + 1, 1)
                        - timedelta(days=1)
                    ).day,
                )
                return date(base_date.year + 1, base_date.month, day)
            case Frequency.SEMI_ANNUAL:
                month = base_date.month + 6
                year = base_date.year + (month - 1) // 12
                month = (month - 1) % 12 + 1
                day = min(
                    base_date.day, (date(year, month + 1, 1) - timedelta(days=1)).day
                )
                return date(year, month, day)
            case Frequency.QUARTERLY:
                month = base_date.month + 3
                year = base_date.year + (month - 1) // 12
                month = (month - 1) % 12 + 1
                day = min(
                    base_date.day, (date(year, month + 1, 1) - timedelta(days=1)).day
                )
                return date(year, month, day)
            case Frequency.MONTHLY:
                month = base_date.month + 1
                year = base_date.year + (month - 1) // 12
                month = (month - 1) % 12 + 1
                day = min(
                    base_date.day, (date(year, month + 1, 1) - timedelta(days=1)).day
                )
                return date(year, month, day)
            case Frequency.WEEKLY:
                return base_date + timedelta(weeks=1)
            case Frequency.DAILY:
                return base_date + timedelta(days=1)
            case _:
                raise ValueError(f"Unsupported frequency: {self}")
