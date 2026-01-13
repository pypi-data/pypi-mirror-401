"""Unit tests for display utilities."""

from datetime import datetime, timedelta

from rich.style import Style

from taskng.cli.display import (
    format_description,
    format_due,
    format_priority,
    format_size,
    format_urgency,
    get_due_style,
    get_priority_style,
    get_urgency_style,
    is_color_enabled,
)
from taskng.core.models import Task


class TestGetDueStyle:
    """Tests for get_due_style function."""

    def test_overdue_returns_red_bold(self) -> None:
        due = datetime.now() - timedelta(days=1)
        style = get_due_style(due)
        assert style.color.name == "red"
        assert style.bold is True

    def test_due_today_returns_yellow_bold(self) -> None:
        due = datetime.now() + timedelta(hours=1)
        style = get_due_style(due)
        assert style.color.name == "yellow"
        assert style.bold is True

    def test_due_this_week_returns_cyan(self) -> None:
        due = datetime.now() + timedelta(days=3)
        style = get_due_style(due)
        assert style.color.name == "cyan"

    def test_future_due_returns_green(self) -> None:
        due = datetime.now() + timedelta(days=14)
        style = get_due_style(due)
        assert style.color.name == "green"

    def test_none_returns_empty_style(self) -> None:
        style = get_due_style(None)
        assert style == Style()


class TestGetPriorityStyle:
    """Tests for get_priority_style function."""

    def test_high_priority_returns_red_bold(self) -> None:
        style = get_priority_style("H")
        assert style.color.name == "red"
        assert style.bold is True

    def test_medium_priority_returns_yellow(self) -> None:
        style = get_priority_style("M")
        assert style.color.name == "yellow"

    def test_low_priority_returns_blue(self) -> None:
        style = get_priority_style("L")
        assert style.color.name == "blue"

    def test_none_returns_empty_style(self) -> None:
        style = get_priority_style(None)
        assert style == Style()


class TestGetUrgencyStyle:
    """Tests for get_urgency_style function."""

    def test_high_urgency_returns_red_bold(self) -> None:
        style = get_urgency_style(12.5)
        assert style.color.name == "red"
        assert style.bold is True

    def test_medium_urgency_returns_yellow(self) -> None:
        style = get_urgency_style(7.0)
        assert style.color.name == "yellow"

    def test_low_urgency_returns_default(self) -> None:
        style = get_urgency_style(2.0)
        assert style == Style()


class TestFormatDue:
    """Tests for format_due function."""

    def test_overdue_shows_days_ago(self) -> None:
        due = datetime.now() - timedelta(hours=72)  # 3 days ago
        text = format_due(due)
        assert "d ago" in text.plain

    def test_due_today_shows_today(self) -> None:
        due = datetime.now() + timedelta(hours=1)
        text = format_due(due)
        assert text.plain == "today"

    def test_due_tomorrow_shows_tomorrow(self) -> None:
        due = datetime.now() + timedelta(hours=30)  # ~1.25 days
        text = format_due(due)
        assert text.plain == "tomorrow"

    def test_due_this_week_shows_days(self) -> None:
        due = datetime.now() + timedelta(hours=72)  # 3 days
        text = format_due(due)
        assert "in" in text.plain and "d" in text.plain

    def test_future_shows_date(self) -> None:
        due = datetime.now() + timedelta(days=30)
        text = format_due(due)
        assert "-" in text.plain  # Date format

    def test_none_returns_empty(self) -> None:
        text = format_due(None)
        assert text.plain == ""


class TestFormatPriority:
    """Tests for format_priority function."""

    def test_high_priority_formats(self) -> None:
        text = format_priority("H")
        assert text.plain == "H"

    def test_medium_priority_formats(self) -> None:
        text = format_priority("M")
        assert text.plain == "M"

    def test_low_priority_formats(self) -> None:
        text = format_priority("L")
        assert text.plain == "L"

    def test_none_returns_empty(self) -> None:
        text = format_priority(None)
        assert text.plain == ""


class TestFormatUrgency:
    """Tests for format_urgency function.

    Urgency values are formatted with one decimal place for readability.
    Python's default rounding (round-half-to-even/banker's rounding) is used.
    """

    def test_formats_with_one_decimal_using_standard_rounding(self) -> None:
        """Should format urgency to one decimal using round-half-to-even.

        6.25 rounds to 6.2 (banker's rounding rounds to nearest even).
        This provides consistent, unbiased rounding for display purposes.
        """
        text = format_urgency(6.25)
        assert text.plain == "6.2"

    def test_formats_high_urgency(self) -> None:
        """High urgency (>=10) should display exact value."""
        text = format_urgency(12.5)
        assert "12.5" in text.plain

    def test_formats_low_urgency(self) -> None:
        """Low urgency should display with one decimal."""
        text = format_urgency(1.0)
        assert "1.0" in text.plain


class TestFormatDescription:
    """Tests for format_description function."""

    def test_short_description_not_truncated(self) -> None:
        task = Task(description="Short task")
        text = format_description(task)
        assert text.plain == "Short task"

    def test_long_description_truncated(self) -> None:
        task = Task(description="A" * 100)
        text = format_description(task, max_length=50)
        assert len(text.plain) <= 50
        assert "..." in text.plain

    def test_blocked_task_shows_indicator(self) -> None:
        task1 = Task(description="Blocker", uuid="blocker-uuid")
        task2 = Task(description="Blocked task", depends=["blocker-uuid"])
        all_tasks = [task1, task2]

        text = format_description(task2, all_tasks)
        assert "[B]" in text.plain

    def test_unblocked_task_no_indicator(self) -> None:
        task = Task(description="Normal task")
        text = format_description(task, [task])
        assert "[B]" not in text.plain

    def test_annotated_task_shows_count(self) -> None:
        task = Task(description="Annotated task")
        task.add_annotation("Note 1")
        task.add_annotation("Note 2")

        text = format_description(task)
        assert "[2]" in text.plain

    def test_no_annotations_no_indicator(self) -> None:
        task = Task(description="Normal task")
        text = format_description(task)
        assert "[" not in text.plain or "[B]" in text.plain


class TestIsColorEnabled:
    """Tests for is_color_enabled function."""

    def test_returns_bool(self) -> None:
        result = is_color_enabled()
        assert isinstance(result, bool)


class TestFormatSize:
    """Tests for format_size function."""

    def test_zero_bytes(self) -> None:
        """Should format 0 bytes as '0 B'."""
        assert format_size(0) == "0 B"

    def test_bytes_less_than_1024(self) -> None:
        """Should format bytes without decimal point."""
        assert format_size(100) == "100 B"
        assert format_size(1023) == "1023 B"

    def test_exactly_1024_bytes(self) -> None:
        """Should format exactly 1KB as '1.0 KB'."""
        assert format_size(1024) == "1.0 KB"

    def test_kilobytes(self) -> None:
        """Should format kilobytes with one decimal place."""
        assert format_size(1536) == "1.5 KB"  # 1.5 KB
        assert format_size(2048) == "2.0 KB"  # 2.0 KB
        assert format_size(10240) == "10.0 KB"  # 10.0 KB

    def test_megabytes(self) -> None:
        """Should format megabytes with one decimal place."""
        assert format_size(1048576) == "1.0 MB"  # 1 MB
        assert format_size(1572864) == "1.5 MB"  # 1.5 MB
        assert format_size(10485760) == "10.0 MB"  # 10 MB

    def test_gigabytes(self) -> None:
        """Should format gigabytes with one decimal place."""
        assert format_size(1073741824) == "1.0 GB"  # 1 GB
        assert format_size(5368709120) == "5.0 GB"  # 5 GB

    def test_terabytes(self) -> None:
        """Should format terabytes with one decimal place."""
        assert format_size(1099511627776) == "1.0 TB"  # 1 TB
        assert format_size(2199023255552) == "2.0 TB"  # 2 TB

    def test_petabytes(self) -> None:
        """Should format petabytes with one decimal place."""
        # Beyond TB, should use PB
        assert format_size(1125899906842624) == "1.0 PB"  # 1 PB

    def test_very_large_size(self) -> None:
        """Should handle very large sizes in PB."""
        assert format_size(1125899906842624 * 10) == "10.0 PB"  # 10 PB

    def test_decimal_precision(self) -> None:
        """Should round to one decimal place."""
        # 1.25 KB (1280 bytes)
        result = format_size(1280)
        assert result == "1.2 KB" or result == "1.3 KB"  # Depends on rounding

        # 2.75 MB (2883584 bytes)
        result = format_size(2883584)
        assert result == "2.8 MB" or result == "2.7 MB"  # Depends on rounding
