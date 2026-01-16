import numpy as np
import pandas as pd
import pytest

from tyche_transforms.transforms import (
    abs_scalar,
    avg,
    cdd,
    convert_m_to_mm,
    cumulative_to_increment,
    daily_average,
    daily_max,
    daily_sum,
    date_first,
    date_max,
    hdd,
    max_value,
    min_value,
    runlen_lt,
    subtract,
    subtract_v,
    sum_value,
)


def test_convert_m_to_mm_series():
    series = pd.Series([0.0, 0.001])
    series.attrs["units"] = "m"

    result = convert_m_to_mm(series)

    np.testing.assert_allclose(result.values, [0.0, 1.0])
    assert result.attrs["units"] == "mm"


def test_convert_m_to_mm_rejects_units():
    series = pd.Series([1.0])
    series.attrs["units"] = "mm"

    with pytest.raises(ValueError, match="units"):
        convert_m_to_mm(series)


def test_convert_m_to_mm_list():
    series_a = pd.Series([0.0, 0.002])
    series_b = pd.Series([0.1, 0.0])

    result = convert_m_to_mm([series_a, series_b])

    assert isinstance(result, list)
    np.testing.assert_allclose(result[0].values, [0.0, 2.0])
    np.testing.assert_allclose(result[1].values, [100.0, 0.0])


def test_cumulative_to_increment_daily_with_reset():
    times = pd.date_range("2024-01-01", periods=30, freq="h")
    values = np.concatenate(
        [
            np.linspace(0.0, 5.0, 24),
            np.linspace(0.2, 1.2, 6),
        ]
    )
    series = pd.Series(values, index=times)

    result = cumulative_to_increment(series)

    values = result.dropna().values
    assert len(values) == 1
    assert values[0] == pytest.approx(1.2)


def test_cumulative_to_increment_requires_datetime_index():
    series = pd.Series([1.0, 2.0, 3.0])

    with pytest.raises(ValueError, match="DatetimeIndex"):
        cumulative_to_increment(series)


def test_cumulative_to_increment_list():
    times = pd.date_range("2024-01-01", periods=30, freq="h")
    series_a = pd.Series(np.linspace(0.0, 3.0, 30), index=times)
    series_b = pd.Series(np.linspace(0.0, 6.0, 30), index=times)

    result = cumulative_to_increment([series_a, series_b])

    assert isinstance(result, list)
    assert len(result) == 2


def test_daily_average_sum_max():
    times = pd.date_range("2024-01-01", periods=24, freq="h")
    series = pd.Series(np.arange(24), index=times)

    mean_result = daily_average(series)
    sum_result = daily_sum(series)
    max_result = daily_max(series)

    assert mean_result.iloc[0] == pytest.approx(11.5)
    assert sum_result.iloc[0] == pytest.approx(np.sum(np.arange(24)))
    assert max_result.iloc[0] == 23


def test_hdd_cdd():
    series = pd.Series([10.0, 18.0, 25.0])

    hdd_result = hdd(series)
    cdd_result = cdd(series)

    np.testing.assert_allclose(hdd_result.values, [8.0, 0.0, 0.0])
    np.testing.assert_allclose(cdd_result.values, [0.0, 0.0, 7.0])


def test_scalar_aggregations():
    series = pd.Series([1.0, 2.0, 3.0])

    assert sum_value(series) == 6.0
    assert avg(series) == 2.0
    assert max_value(series) == 3.0
    assert min_value(series) == 1.0


def test_date_max():
    times = pd.date_range("2024-01-01", periods=3, freq="D")
    series = pd.Series([1.0, 5.0, 5.0], index=times)

    assert date_max(series) == times[1]


def test_date_first():
    times = pd.date_range("2024-01-01", periods=3, freq="D")
    series = pd.Series([1.0, 5.0, 7.0], index=times)

    assert date_first(series, threshold=4.0) == times[1]


def test_date_first_raises_when_missing():
    times = pd.date_range("2024-01-01", periods=2, freq="D")
    series = pd.Series([1.0, 2.0], index=times)

    with pytest.raises(ValueError, match="threshold"):
        date_first(series, threshold=10.0)


def test_runlen_lt():
    series = pd.Series([0.0, 0.0, 1.0, 0.5, 0.4, 2.0])

    assert runlen_lt(series, threshold=1.0) == 2


def test_abs_subtracts():
    assert abs_scalar(-5.0) == 5.0
    assert subtract_v(10.0, 3.5) == 6.5
    assert subtract([2.0, 5.0]) == 3.0


def test_subtract_requires_two_values():
    with pytest.raises(ValueError, match="exactly two"):
        subtract([1.0])
