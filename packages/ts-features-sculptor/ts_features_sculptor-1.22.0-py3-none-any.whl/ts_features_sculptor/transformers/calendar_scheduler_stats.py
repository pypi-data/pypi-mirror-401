from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class CalendarSchedulerStats(BaseEstimator, TransformerMixin):
    """
    Трансформер для оценки вероятности назначения воздействия,
    рассчитанной по внешнему (независимому от индивидуального временного
    ряда) глобальному профилю политики назначения:
      q_hat(t) = P(T(t)=1 | keys(t)).
    Используется в задачах оценки причинного эффекта воздействия.

    Пользователь выбирает календарные ключи (year, dow, month, days),
    и ключи компоненты смеси для хранения политик назначения
    воздействия. Трансформер нужен чтобы хранить политики и
    интерполировать вероятность назначения воздейсвия.

    Ключи должны содержаться в обрабатываемых данных X.

    Профиль (base_profile_df):
      - содержит ключевые колонки keys
      - и либо готовую вероятность q_hat_col
      - либо сырые счётчики push_cnt_col / days_cnt_col для проведения
        вычислений
          q = (push + alpha) / (days + alpha + beta)

    Если для строки X нет выборки по ключам в профиле:
      - fillna="mean": подставляем среднее q по профилю
      - fillna="const": подставляем fillna_value
      - fillna=None: оставляем NaN (редко нужно)

    Parameters
    ----------
    base_profile_df : pd.DataFrame
    keys : tuple[str, ...]
        Ключи, например ("year","dow0","hour_bucket")
    q_hat_col : str | None
        Вероятность назначения воздействия.
    push_cnt_col, days_cnt_col : str
        Сырые счётчики назначения воздействия.
    alpha, beta : float
        Коэффициенты сглаживания.
    fillna : str | None
        "mean" | "const" | None
    fillna_value : float
    out_q_hat_col : str
    eps : float
        Ограницения на  q_hat в [eps, 1-eps].

    Examples
    --------
    12-часовые бакеты: hour_bucket in {0, 12}
      - 0  означает [00:00..11:59]
      - 12 означает [12:00..23:59]

    >>> import pandas as pd
    >>> base_profile_df = pd.DataFrame({
    ...   "year":        [2021, 2021, 2021, 2021],
    ...   "dow0":        [0,    1,    0,    1],      # 0=Пн, 1=Вт
    ...   "hour_bucket": [0,    0,    12,   12],
    ...   "hist_push_cnt": [2,  12,   10,   4],
    ...   "hist_days":     [52, 52,   52,   52],
    ... })
    >>>
    >>> X = pd.DataFrame({
    ...   "time": pd.to_datetime([
    ...     "2021-01-04",  # Пн
    ...     "2021-01-05",  # Вт
    ...     "2021-01-06",  # Ср работает fillna
    ...   ]),
    ...   "year": [2021, 2021, 2021],
    ...   "dow0": [0, 1, 2],
    ...   "hour_bucket": [0, 0, 0],
    ... })
    >>>
    >>> tr = CalendarSchedulerStats(
    ...   base_profile_df=base_profile_df,
    ...   keys=("year","dow0","hour_bucket"),
    ...   push_cnt_col="hist_push_cnt",
    ...   days_cnt_col="hist_days",
    ...   alpha=1.0,
    ...   beta=1.0,
    ...   fillna="mean",
    ...   out_q_hat_col="q_hat",
    ... )
    >>> result_df = tr.fit_transform(X)
    >>> print(result_df.round(2).to_string(index=False))
          time  year  dow0  hour_bucket  q_hat
    2021-01-04  2021     0            0   0.06
    2021-01-05  2021     1            0   0.24
    2021-01-06  2021     2            0   0.15
    """

    def __init__(
        self,
        base_profile_df: pd.DataFrame,
        keys: tuple[str, ...],
        q_hat_col: str | None = None,
        push_cnt_col: str = "hist_push_cnt",
        days_cnt_col: str = "hist_days",
        alpha: float = 1.0,
        beta: float = 1.0,
        fillna: str | None = "mean",
        fillna_value: float = 0.0,
        out_q_hat_col: str = "q_hat",
        eps: float = 1e-4,
    ):
        self.base_profile_df = base_profile_df
        self.keys = tuple(keys)
        self.q_hat_col = q_hat_col
        self.push_cnt_col = push_cnt_col
        self.days_cnt_col = days_cnt_col
        self.alpha = float(alpha)
        self.beta = float(beta)
        self.fillna = fillna
        self.fillna_value = float(fillna_value)
        self.out_q_hat_col = out_q_hat_col
        self.eps = float(eps)

    def fit(self, X: pd.DataFrame, y=None):
        prof = self.base_profile_df

        if self.q_hat_col is not None:
            q = pd.to_numeric(prof[self.q_hat_col], errors="coerce").astype(float)
        else:
            push = pd.to_numeric(
                prof[self.push_cnt_col], errors="coerce").astype(float)
            days = pd.to_numeric(
                prof[self.days_cnt_col], errors="coerce").astype(float)
            q = (push + self.alpha) / (days + self.alpha + self.beta)

        idx = pd.MultiIndex.from_frame(prof[list(self.keys)])
        self._q = pd.Series(q.to_numpy(), index=idx)
        self._q_mean = float(np.nanmean(q.to_numpy()))
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        df = X.copy()

        idx = pd.MultiIndex.from_frame(df[list(self.keys)])
        q_hat = self._q.reindex(idx).to_numpy(dtype=float)

        if self.fillna == "mean":
            miss = np.isnan(q_hat)
            if miss.any():
                q_hat[miss] = self._q_mean
        elif self.fillna == "const":
            miss = np.isnan(q_hat)
            if miss.any():
                q_hat[miss] = self.fillna_value

        q_hat = np.clip(q_hat, self.eps, 1.0 - self.eps)
        df[self.out_q_hat_col] = q_hat
        return df
