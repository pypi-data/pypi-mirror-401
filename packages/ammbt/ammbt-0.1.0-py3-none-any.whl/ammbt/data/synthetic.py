"""
Synthetic swap data generation for testing and development.

Generates realistic swap sequences with:
- Price movements (GBM, jump diffusion)
- Volume patterns
- Time-of-day effects
"""

import numpy as np
import pandas as pd
from typing import Optional, Literal


def generate_price_path(
    n_steps: int,
    initial_price: float = 1.0,
    volatility: float = 0.02,
    drift: float = 0.0,
    dt: float = 1.0,
    model: Literal['gbm', 'jump'] = 'gbm',
    jump_intensity: float = 0.1,
    jump_size: float = 0.05,
    seed: Optional[int] = None,
) -> np.ndarray:
    """
    Generate synthetic price path.

    Parameters
    ----------
    n_steps : int
        Number of time steps
    initial_price : float
        Starting price
    volatility : float
        Annualized volatility (e.g., 0.02 = 2%)
    drift : float
        Annualized drift/trend
    dt : float
        Time step size (1.0 = 1 day)
    model : {'gbm', 'jump'}
        Price model type
        - 'gbm': Geometric Brownian Motion
        - 'jump': Jump diffusion (adds sudden price jumps)
    jump_intensity : float
        Average number of jumps per time unit (for jump model)
    jump_size : float
        Average jump size as fraction of price
    seed : int, optional
        Random seed for reproducibility

    Returns
    -------
    np.ndarray
        Price path (n_steps,)

    Examples
    --------
    >>> prices = generate_price_path(1000, volatility=0.03, drift=0.001)
    >>> len(prices)
    1000
    """
    if seed is not None:
        np.random.seed(seed)

    prices = np.zeros(n_steps)
    prices[0] = initial_price

    if model == 'gbm':
        # Geometric Brownian Motion: dS = μS dt + σS dW
        for i in range(1, n_steps):
            dW = np.random.normal(0, np.sqrt(dt))
            drift_component = drift * dt
            diffusion_component = volatility * dW
            prices[i] = prices[i-1] * np.exp(drift_component + diffusion_component)

    elif model == 'jump':
        # Jump diffusion: adds Poisson jumps to GBM
        for i in range(1, n_steps):
            # GBM component
            dW = np.random.normal(0, np.sqrt(dt))
            drift_component = drift * dt
            diffusion_component = volatility * dW

            # Jump component
            jump_occurs = np.random.poisson(jump_intensity * dt) > 0
            jump_component = 0.0
            if jump_occurs:
                jump_direction = np.random.choice([-1, 1])
                jump_magnitude = np.random.exponential(jump_size)
                jump_component = jump_direction * jump_magnitude

            prices[i] = prices[i-1] * np.exp(
                drift_component + diffusion_component + jump_component
            )

    else:
        raise ValueError(f"Unknown model: {model}")

    return prices


def generate_swaps(
    n_swaps: int = 10000,
    initial_price: float = 1.0,
    volatility: float = 0.02,
    drift: float = 0.0,
    base_volume: float = 100000.0,
    volume_volatility: float = 0.5,
    dt: float = 1.0,
    model: Literal['gbm', 'jump'] = 'gbm',
    seed: Optional[int] = None,
) -> pd.DataFrame:
    """
    Generate synthetic swap data.

    Creates realistic swap sequences from price movements and volume patterns.

    Parameters
    ----------
    n_swaps : int
        Number of swaps to generate
    initial_price : float
        Starting price (token1/token0)
    volatility : float
        Price volatility
    drift : float
        Price drift/trend
    base_volume : float
        Average swap volume in token1 terms
    volume_volatility : float
        Volume randomness (0 = constant, 1 = very random)
    dt : float
        Time step between swaps
    model : {'gbm', 'jump'}
        Price model
    seed : int, optional
        Random seed

    Returns
    -------
    pd.DataFrame
        Swap data with columns:
        - timestamp: Swap timestamp
        - price: Price after swap
        - amount0: Token0 amount (negative = out)
        - amount1: Token1 amount (negative = out)
        - volume: Swap volume in USD terms

    Examples
    --------
    >>> swaps = generate_swaps(1000, volatility=0.03)
    >>> swaps.head()
    """
    if seed is not None:
        np.random.seed(seed)

    # Generate price path
    prices = generate_price_path(
        n_swaps,
        initial_price=initial_price,
        volatility=volatility,
        drift=drift,
        dt=dt,
        model=model,
        seed=seed,
    )

    # Generate swap volumes
    volumes = np.abs(np.random.lognormal(
        mean=np.log(base_volume),
        sigma=volume_volatility,
        size=n_swaps,
    ))

    # Determine swap direction based on price changes
    # Positive price change = more token0 bought = amount0 negative, amount1 positive
    amount0 = np.zeros(n_swaps)
    amount1 = np.zeros(n_swaps)

    for i in range(1, n_swaps):
        price_change = prices[i] - prices[i-1]
        volume = volumes[i]

        if price_change > 0:
            # Price increased: someone bought token0 with token1
            # amount0 is negative (out), amount1 is positive (in)
            amount0[i] = -volume / prices[i]  # Negative
            amount1[i] = volume  # Positive
        else:
            # Price decreased: someone bought token1 with token0
            # amount0 is positive (in), amount1 is negative (out)
            amount0[i] = volume / prices[i]  # Positive
            amount1[i] = -volume  # Negative

    # First swap: initialize pool
    amount0[0] = volumes[0] / prices[0]
    amount1[0] = volumes[0]

    # Create timestamps
    timestamps = pd.date_range(
        start='2024-01-01',
        periods=n_swaps,
        freq=f'{int(dt * 24 * 60)}min',
    )

    # Assemble DataFrame
    swaps = pd.DataFrame({
        'timestamp': timestamps,
        'price': prices,
        'amount0': amount0,
        'amount1': amount1,
        'volume': volumes,
    })

    return swaps


def generate_swaps_from_ohlcv(
    ohlcv: pd.DataFrame,
    swaps_per_candle: int = 100,
    volume_distribution: Literal['uniform', 'normal', 'exponential'] = 'exponential',
    seed: Optional[int] = None,
) -> pd.DataFrame:
    """
    Generate synthetic swaps from OHLCV data.

    Useful for backtesting with real price data but synthetic swap granularity.

    Parameters
    ----------
    ohlcv : pd.DataFrame
        OHLCV data with columns: open, high, low, close, volume
    swaps_per_candle : int
        Number of swaps to generate per candle
    volume_distribution : str
        How to distribute volume across swaps
    seed : int, optional
        Random seed

    Returns
    -------
    pd.DataFrame
        Synthetic swaps matching OHLCV price movements
    """
    if seed is not None:
        np.random.seed(seed)

    all_swaps = []

    for idx, row in ohlcv.iterrows():
        # Generate intra-candle price path
        # Simple approach: random walk from open to close hitting high/low
        prices = np.zeros(swaps_per_candle)
        prices[0] = row['open']
        prices[-1] = row['close']

        # Fill intermediate prices
        for i in range(1, swaps_per_candle - 1):
            # Random walk between open and close
            progress = i / (swaps_per_candle - 1)
            target = row['open'] + progress * (row['close'] - row['open'])
            noise = np.random.normal(0, (row['high'] - row['low']) / 10)
            prices[i] = target + noise
            # Clip to high/low
            prices[i] = np.clip(prices[i], row['low'], row['high'])

        # Distribute volume across swaps
        total_volume = row['volume']
        if volume_distribution == 'uniform':
            volumes = np.full(swaps_per_candle, total_volume / swaps_per_candle)
        elif volume_distribution == 'normal':
            volumes = np.abs(np.random.normal(
                total_volume / swaps_per_candle,
                total_volume / swaps_per_candle / 3,
                swaps_per_candle
            ))
            volumes = volumes * (total_volume / volumes.sum())  # Normalize
        elif volume_distribution == 'exponential':
            volumes = np.random.exponential(
                total_volume / swaps_per_candle,
                swaps_per_candle
            )
            volumes = volumes * (total_volume / volumes.sum())
        else:
            raise ValueError(f"Unknown distribution: {volume_distribution}")

        # Create swaps
        for i in range(swaps_per_candle):
            price = prices[i]
            volume = volumes[i]

            # Determine direction
            if i > 0:
                price_change = prices[i] - prices[i-1]
            else:
                price_change = 0

            if price_change > 0:
                amount0 = -volume / price
                amount1 = volume
            else:
                amount0 = volume / price
                amount1 = -volume

            all_swaps.append({
                'timestamp': idx,  # Use candle timestamp
                'price': price,
                'amount0': amount0,
                'amount1': amount1,
                'volume': volume,
            })

    return pd.DataFrame(all_swaps)
