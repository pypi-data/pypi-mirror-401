from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "analysis3054" / "tx_refineries.py"
spec = importlib.util.spec_from_file_location("tx_refineries", MODULE_PATH)
tx_refineries = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = tx_refineries
spec.loader.exec_module(tx_refineries)


def test_build_statement_url():
    url = tx_refineries._build_statement_url(2025, 2)
    assert (
        url
        == "https://www.rrc.texas.gov/oil-and-gas/research-and-statistics/refinery-statements/"
        "refineries-statements-2025/refinery-statements-2-2025/"
    )


def test_iter_statement_months():
    months = list(tx_refineries._iter_statement_months(2024, 2025, 2))
    assert months[0] == (2024, 1)
    assert months[-1] == (2025, 2)
    assert (2024, 12) in months
    assert (2025, 1) in months


def test_iter_statement_months_start_month():
    months = list(tx_refineries._iter_statement_months(2025, 2025, 10, start_month=4))
    assert months[0] == (2025, 4)
    assert months[-1] == (2025, 10)


def test_parse_statement_period_from_name():
    parsed = tx_refineries._parse_statement_period_from_name(
        "https://www.rrc.texas.gov/media/wlskqq0o/2025-january-08-2869.pdf"
    )
    assert parsed == (2025, 1)


def test_normalize_facility_number():
    assert tx_refineries._normalize_facility_number("4-161") == "04-0161"
    assert tx_refineries._normalize_facility_number("10-0026") == "10-0026"


def test_parse_report_month_year():
    assert tx_refineries._parse_report_month("Sep") == 9
    assert tx_refineries._parse_report_month("09") == 9
    assert tx_refineries._parse_report_year("25") == 2025
    assert tx_refineries._parse_report_year("2024") == 2024


def test_coerce_number():
    assert tx_refineries._coerce_number("1,234") == 1234.0
    assert tx_refineries._coerce_number("(1,234)") == -1234.0
    assert tx_refineries._coerce_number("-") == 0.0
