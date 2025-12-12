"""Prediction Market AMM (CPMM) for a binary event.

We model a Constant Product Market Maker with two outcome share pools:
- x = pool inventory of 'YES' shares
- y = pool inventory of 'NO' shares

The invariant is:
    x * y = k

A trader who buys shares of one outcome *removes* those shares from the pool.
To preserve x*y=k, the pool must gain shares on the other side; we interpret
that required increase as the trade's *cost in currency units*.

This is a simplified educational model.
"""

from __future__ import annotations


class PredictionMarket:
    """A CPMM-based binary prediction market ('YES'/'NO')."""

    def __init__(self, initial_liquidity: float):
        """Initialize the pool with symmetric liquidity on both sides.

        Args:
            initial_liquidity: starting shares for each side (x=y=initial_liquidity)
        """
        if initial_liquidity <= 0:
            raise ValueError("initial_liquidity must be positive")

        x = float(initial_liquidity)
        y = float(initial_liquidity)
        self.shares = {"YES": x, "NO": y}
        self.k = x * y

    def calculate_price(self, outcome: str) -> float:
        """Return a probability-like price in [0, 1] for the given outcome.

        We normalize the pool balances to get complementary prices:
            p(YES) = y / (x + y)
            p(NO)  = x / (x + y)

        This stays within [0,1] and ensures p(YES)+p(NO)=1.
        """
        outcome = outcome.upper()
        if outcome not in self.shares:
            raise ValueError("outcome must be 'YES' or 'NO'")

        x = self.shares["YES"]
        y = self.shares["NO"]
        denom = x + y
        if denom <= 0:
            raise RuntimeError("invalid pool state: x + y must be positive")

        if outcome == "YES":
            return y / denom
        return x / denom

    def buy_shares(self, outcome: str, amount: float) -> tuple[float, float]:
        """Buy `amount` shares of `outcome`, returning (cost, new_price).

        Trade math (CPMM invariant x*y=k):

        Suppose buying 'YES' shares:
        - Pool's YES inventory decreases: x_new = x - amount
        - To keep x_new * y_new = k, we solve:
              y_new = k / x_new
        - The pool must *gain* (y_new - y) units of NO-side inventory.

        We interpret this required increase in the opposite side as the
        currency cost paid by the trader:
              cost = y_new - y

        The same logic applies symmetrically for buying 'NO'.

        Notes:
        - This model treats the opposite-side increase as "cost in currency".
        - amount must be smaller than the pool's current inventory of that outcome.
        """
        outcome = outcome.upper()
        if outcome not in self.shares:
            raise ValueError("outcome must be 'YES' or 'NO'")
        if amount <= 0:
            raise ValueError("amount must be positive")

        yes = self.shares["YES"]
        no = self.shares["NO"]

        if outcome == "YES":
            x = yes
            y = no
            if amount >= x:
                raise ValueError("amount too large: would exhaust YES liquidity")

            # Remove YES from pool.
            x_new = x - amount
            # Keep invariant: x_new * y_new = k  =>  y_new = k / x_new
            y_new = self.k / x_new
            # Trader must add the difference on the other side.
            cost = y_new - y

            self.shares["YES"] = x_new
            self.shares["NO"] = y_new

        else:  # outcome == "NO"
            x = no
            y = yes
            if amount >= x:
                raise ValueError("amount too large: would exhaust NO liquidity")

            x_new = x - amount
            y_new = self.k / x_new
            cost = y_new - y

            self.shares["NO"] = x_new
            self.shares["YES"] = y_new

        new_price = self.calculate_price(outcome)
        return cost, new_price


if __name__ == "__main__":
    market = PredictionMarket(initial_liquidity=1000)

    print("Initial pool shares:", market.shares)
    print("Initial prices:")
    print("  YES:", round(market.calculate_price("YES"), 6))
    print("  NO :", round(market.calculate_price("NO"), 6))
    print()

    trades = [("YES", 100), ("NO", 50), ("YES", 200)]

    for i, (outcome, amount) in enumerate(trades, start=1):
        cost, new_price = market.buy_shares(outcome, amount)
        print(f"Trade {i}: buy {amount} {outcome}")
        print("  Cost (currency units):", round(cost, 6))
        print("  New pool shares:", {k: round(v, 6) for k, v in market.shares.items()})
        print(f"  New price({outcome}):", round(new_price, 6))
        print("  Prices now: YES=", round(market.calculate_price("YES"), 6), ", NO=", round(market.calculate_price("NO"), 6))
        print()
