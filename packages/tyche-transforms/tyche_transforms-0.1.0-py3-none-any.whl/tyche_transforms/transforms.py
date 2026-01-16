from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Callable

import numpy as np
import pandas as pd

SeriesLike = pd.Series | Sequence[pd.Series]

DEGREE_DAY_BASE_C = 18.0


def _apply_series(series: SeriesLike, func: Callable[[pd.Series], pd.Series]) -> SeriesLike:
    """Apply a transform to a single series or a list of series.

    Parameters:
        series: A pandas Series or a sequence of Series to transform.
        func: Function that accepts a Series and returns a transformed Series.

    Returns:
        The transformed Series if the input is a Series, otherwise a list of transformed Series.
    """
    if isinstance(series, pd.Series):
        return func(series)
    return [func(item) for item in series]


def _require_datetime_index(series: pd.Series) -> pd.DatetimeIndex:
    """Validate that a series uses a DatetimeIndex.

    Parameters:
        series: Series expected to be indexed by datetime.

    Returns:
        The DatetimeIndex for the series.

    Raises:
        ValueError: If the series index is not a DatetimeIndex.
    """
    if not isinstance(series.index, pd.DatetimeIndex):
        raise ValueError("series must have a DatetimeIndex")
    return series.index


def convert_m_to_mm(series: SeriesLike) -> SeriesLike:
    """Convert a length series from meters to millimeters.

    Parameters:
        series: Series (or list of series) containing values in meters. If a series
            has a ``units`` attribute, it must be ``\"m\"``.

    Returns:
        The converted series in millimeters with ``units`` set to ``\"mm\"``.

    Raises:
        ValueError: If a series has a ``units`` attribute that is not ``\"m\"``.
    """

    def _convert(item: pd.Series) -> pd.Series:
        units = item.attrs.get("units")
        if units not in (None, "m"):
            raise ValueError("series units must be 'm' to convert to 'mm'")
        converted = item * 1000.0
        converted.attrs = dict(item.attrs)
        converted.attrs["units"] = "mm"
        return converted

    return _apply_series(series, _convert)


def cumulative_to_increment(series: SeriesLike) -> SeriesLike:
    """Convert a cumulative series to daily increments.

    Parameters:
        series: Series (or list of series) containing cumulative totals with a
            DatetimeIndex.

    Returns:
        A daily series of increments computed from the last value each day. If a
        daily difference is negative (reset), the daily last value is used instead.

    Raises:
        ValueError: If a series is not indexed by datetime.
    """

    def _convert(item: pd.Series) -> pd.Series:
        _require_datetime_index(item)
        daily_last = item.resample("1D").last()
        daily_diff = daily_last.diff()
        mask = (daily_diff >= 0) | daily_diff.isna()
        daily_diff = daily_diff.where(mask, daily_last)
        daily_diff.attrs = dict(item.attrs)
        return daily_diff

    return _apply_series(series, _convert)


def daily_average(series: SeriesLike) -> SeriesLike:
    """Resample a series to daily mean values.

    Parameters:
        series: Series (or list of series) indexed by datetime.

    Returns:
        Daily mean series with one value per day.

    Raises:
        ValueError: If a series is not indexed by datetime.
    """

    def _convert(item: pd.Series) -> pd.Series:
        _require_datetime_index(item)
        return item.resample("1D").mean()

    return _apply_series(series, _convert)


def daily_sum(series: SeriesLike) -> SeriesLike:
    """Resample a series to daily sum values.

    Parameters:
        series: Series (or list of series) indexed by datetime.

    Returns:
        Daily sum series with one value per day.

    Raises:
        ValueError: If a series is not indexed by datetime.
    """

    def _convert(item: pd.Series) -> pd.Series:
        _require_datetime_index(item)
        return item.resample("1D").sum()

    return _apply_series(series, _convert)


def daily_max(series: SeriesLike) -> SeriesLike:
    """Resample a series to daily maximum values.

    Parameters:
        series: Series (or list of series) indexed by datetime.

    Returns:
        Daily maximum series with one value per day.

    Raises:
        ValueError: If a series is not indexed by datetime.
    """

    def _convert(item: pd.Series) -> pd.Series:
        _require_datetime_index(item)
        return item.resample("1D").max()

    return _apply_series(series, _convert)


def hdd(series: pd.Series) -> pd.Series:
    """Compute heating degree days using a base of 18 C.

    Parameters:
        series: Daily average temperature series in Celsius.

    Returns:
        Series of heating degree days where values below 18 C contribute positively.
    """
    return (DEGREE_DAY_BASE_C - series).clip(lower=0)


def cdd(series: pd.Series) -> pd.Series:
    """Compute cooling degree days using a base of 18 C.

    Parameters:
        series: Daily average temperature series in Celsius.

    Returns:
        Series of cooling degree days where values above 18 C contribute positively.
    """
    return (series - DEGREE_DAY_BASE_C).clip(lower=0)


def sum_value(series: pd.Series) -> float:
    """Sum a series and return a scalar.

    Parameters:
        series: Series of numeric values.

    Returns:
        Sum of all values as a float.
    """
    return float(series.sum())


def avg(series: pd.Series) -> float:
    """Average a series and return a scalar.

    Parameters:
        series: Series of numeric values.

    Returns:
        Mean of the series as a float.
    """
    return float(series.mean())


def max_value(series: pd.Series) -> float:
    """Maximum value of a series as a scalar.

    Parameters:
        series: Series of numeric values.

    Returns:
        Maximum value as a float.
    """
    return float(series.max())


def min_value(series: pd.Series) -> float:
    """Minimum value of a series as a scalar.

    Parameters:
        series: Series of numeric values.

    Returns:
        Minimum value as a float.
    """
    return float(series.min())


def date_max(series: pd.Series) -> pd.Timestamp:
    """Return the timestamp of the maximum value in a series.

    Parameters:
        series: Series of numeric values indexed by datetime.

    Returns:
        Timestamp corresponding to the maximum value.

    Raises:
        ValueError: If the series is empty or not indexed by datetime.
    """
    _require_datetime_index(series)
    if series.empty:
        raise ValueError("series must not be empty")
    return series.idxmax()


def date_first(series: pd.Series, threshold: float) -> pd.Timestamp:
    """Return the timestamp of the first value above a threshold.

    Parameters:
        series: Series of numeric values indexed by datetime.
        threshold: Threshold to exceed.

    Returns:
        Timestamp of the first value greater than the threshold.

    Raises:
        ValueError: If no values exceed the threshold or the index is invalid.
    """
    _require_datetime_index(series)
    matches = series[series > threshold]
    if matches.empty:
        raise ValueError("no values exceed the threshold")
    return matches.index[0]


def runlen_lt(series: pd.Series, threshold: float) -> int:
    """Length of the longest run where values are below a threshold.

    Parameters:
        series: Series of numeric values.
        threshold: Threshold that values must stay below.

    Returns:
        The length of the longest consecutive run below the threshold.
    """
    mask = (series < threshold).fillna(False).to_numpy()
    max_run = 0
    current = 0
    for value in mask:
        if value:
            current += 1
            max_run = max(max_run, current)
        else:
            current = 0
    return int(max_run)


def abs_scalar(value: float) -> float:
    """Absolute value of a scalar.

    Parameters:
        value: Numeric scalar.

    Returns:
        Absolute value as a float.
    """
    return float(abs(value))


def subtract_v(value: float, threshold: float) -> float:
    """Subtract a fixed threshold from a scalar.

    Parameters:
        value: Numeric scalar.
        threshold: Threshold to subtract.

    Returns:
        The difference ``value - threshold`` as a float.
    """
    return float(value - threshold)


def subtract(values: Iterable[float]) -> float:
    """Subtract the first scalar from the second (loc1 - loc0).

    Parameters:
        values: Iterable containing exactly two numeric values.

    Returns:
        The difference between the second and first value.

    Raises:
        ValueError: If the iterable does not contain exactly two values.
    """
    values = list(values)
    if len(values) != 2:
        raise ValueError("subtract expects exactly two values")
    return float(values[1] - values[0])


TRANSFORM_REGISTRY: dict[str, Callable[..., object]] = {
    "CONVERT_M_TO_MM": convert_m_to_mm,
    "CUMULATIVE_TO_INCREMENT": cumulative_to_increment,
    "DAILY_AVERAGE": daily_average,
    "DAILY_SUM": daily_sum,
    "DAILY_MAX": daily_max,
    "HDD": hdd,
    "CDD": cdd,
    "SUM": sum_value,
    "AVG": avg,
    "MAX": max_value,
    "MIN": min_value,
    "DATE_MAX": date_max,
    "DATE_FIRST": date_first,
    "RUNLEN_LT": runlen_lt,
    "ABS": abs_scalar,
    "SUBTRACT_V": subtract_v,
    "SUBTRACT": subtract,
}
