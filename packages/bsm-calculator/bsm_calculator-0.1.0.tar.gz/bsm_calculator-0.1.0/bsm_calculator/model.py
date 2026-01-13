import numpy as np
from scipy.special import ndtr  # Fastest Vectorized Normal CDF
# Standard Normal PDF formula is simple enough to write in numpy

class BSM:
    """
    Vectorized BSM Model. 
    Accepts scalar floats OR lists/arrays/pandas Series.
    """

    def __init__(self, spot, strike, time_days, rate, vol, div=0.0):
        """
        Initialize with arrays or scalars.
        """
        # Convert inputs to numpy arrays for vectorization
        self.S = np.array(spot, dtype=float)
        self.K = np.array(strike, dtype=float)
        self.T = np.array(time_days, dtype=float) / 365.0
        self.r = np.array(rate, dtype=float)
        self.sigma = np.array(vol, dtype=float)
        self.q = np.array(div, dtype=float)

        # Handle potential broadcasting if single values passed with arrays
        # (e.g., Spot is array, but Rate is just 0.10)
        # This is handled automatically by numpy operations below.

    # --- INTERNAL HELPER PROPERTIES ---
    
    @property
    def _d1(self):
        """Calculates d1 (Vectorized). Handles T=0 gracefully."""
        # Use simple mask to avoid division by zero warnings
        with np.errstate(divide='ignore', invalid='ignore'):
            d1 = (np.log(self.S / self.K) + (self.r - self.q + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
        
        # Where T is 0, d1 is undefined (NaN). We can replace NaNs with 0 to prevent crashes
        return np.where(self.T > 0, d1, 0.0)

    @property
    def _d2(self):
        """Calculates d2 (Vectorized)."""
        return np.where(self.T > 0, self._d1 - self.sigma * np.sqrt(self.T), 0.0)

    def _pdf(self, x):
        """Standard Normal PDF (Vectorized)."""
        return (1.0 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * x ** 2)

    def _cdf(self, x):
        """Standard Normal CDF (Vectorized)."""
        return ndtr(x)

    # --- PRICING METHODS ---

    def call_price(self, sigma_override=None):
        """Vectorized Call Price."""
        vol = self.sigma if sigma_override is None else sigma_override
        
        # Re-calc d1/d2 if vol is overridden (used for IV calculation)
        if sigma_override is not None:
            with np.errstate(divide='ignore', invalid='ignore'):
                temp_d1 = (np.log(self.S / self.K) + (self.r - self.q + 0.5 * vol ** 2) * self.T) / (vol * np.sqrt(self.T))
                temp_d1 = np.where(self.T > 0, temp_d1, 0.0)
                temp_d2 = np.where(self.T > 0, temp_d1 - vol * np.sqrt(self.T), 0.0)
        else:
            temp_d1, temp_d2 = self._d1, self._d2

        return np.exp(-self.q * self.T) * self.S * self._cdf(temp_d1) - \
               self.K * np.exp(-self.r * self.T) * self._cdf(temp_d2)

    def put_price(self, sigma_override=None):
        """Vectorized Put Price."""
        vol = self.sigma if sigma_override is None else sigma_override
        
        if sigma_override is not None:
            with np.errstate(divide='ignore', invalid='ignore'):
                temp_d1 = (np.log(self.S / self.K) + (self.r - self.q + 0.5 * vol ** 2) * self.T) / (vol * np.sqrt(self.T))
                temp_d1 = np.where(self.T > 0, temp_d1, 0.0)
                temp_d2 = np.where(self.T > 0, temp_d1 - vol * np.sqrt(self.T), 0.0)
        else:
            temp_d1, temp_d2 = self._d1, self._d2

        return self.K * np.exp(-self.r * self.T) * self._cdf(-temp_d2) - \
               np.exp(-self.q * self.T) * self.S * self._cdf(-temp_d1)

    # --- GREEKS ---

    def delta(self, option_type="call"):
        # We use np.where to handle 'call' vs 'put' string logic for arrays
        # But usually 'option_type' is passed as a single string. 
        # If option_type is 'call', return call delta, else put delta.
        
        call_delta = np.exp(-self.q * self.T) * self._cdf(self._d1)
        
        if option_type.lower() == "call":
            return call_delta
        else:
            return call_delta - np.exp(-self.q * self.T)

    def gamma(self):
        """Gamma (Same for Call and Put)."""
        # Avoid division by zero
        denom = self.S * self.sigma * np.sqrt(self.T)
        return np.where(denom > 0, (np.exp(-self.q * self.T) * self._pdf(self._d1)) / denom, 0.0)

    def vega(self):
        """Vega."""
        return np.where(self.T > 0, 0.01 * self.S * np.exp(-self.q * self.T) * np.sqrt(self.T) * self._pdf(self._d1), 0.0)

    def theta(self, option_type="call"):
        """Theta (Daily)."""
        term1 = -(self.S * self.sigma * np.exp(-self.q * self.T) * self._pdf(self._d1)) / (2 * np.sqrt(self.T))
        
        # These calculations are vectorized
        call_term2 = -self.r * self.K * np.exp(-self.r * self.T) * self._cdf(self._d2)
        call_term3 = self.q * self.S * np.exp(-self.q * self.T) * self._cdf(self._d1)
        
        put_term2 = self.r * self.K * np.exp(-self.r * self.T) * self._cdf(-self._d2)
        put_term3 = -self.q * self.S * np.exp(-self.q * self.T) * self._cdf(-self._d1)

        if option_type.lower() == "call":
            return np.where(self.T > 0, (term1 + call_term2 + call_term3) / 365.0, 0.0)
        else:
            return np.where(self.T > 0, (term1 + put_term2 + put_term3) / 365.0, 0.0)

    def rho(self, option_type="call"):
        """Rho."""
        if option_type.lower() == "call":
            return 0.01 * self.K * self.T * np.exp(-self.r * self.T) * self._cdf(self._d2)
        else:
            return -0.01 * self.K * self.T * np.exp(-self.r * self.T) * self._cdf(-self._d2)

    # --- VECTORIZED IMPLIED VOLATILITY ---

    def implied_vol(self, target_price, option_type="call"):
        """
        Vectorized Binary Search for IV.
        Can process millions of rows simultaneously.
        """
        targets = np.array(target_price, dtype=float)
        
        # 1. Initialize High/Low arrays
        high = np.ones_like(targets) * 5.0  # 500% vol max
        low = np.zeros_like(targets)
        
        # 2. Iterate fixed times (20 iterations gives precision ~0.0001)
        # This is faster than a while loop for vectors
        for _ in range(20):
            mid = (high + low) / 2
            
            if option_type == "call":
                mid_price = self.call_price(sigma_override=mid)
            else:
                mid_price = self.put_price(sigma_override=mid)

            # Vectorized update: 
            # If ModelPrice > Target, we need Lower Vol (High = Mid)
            # If ModelPrice < Target, we need Higher Vol (Low = Mid)
            high = np.where(mid_price > targets, mid, high)
            low = np.where(mid_price <= targets, mid, low)

        return (high + low) / 2