"""Basic Constant Product Market Maker (CPMM) for a binary prediction market.

We model a pool that holds two outcome share reserves:
- x = shares['YES']
- y = shares['NO']

The CPMM invariant is:
    x * y = k

A trade that buys YES removes YES shares from the pool (x decreases).
To preserve the invariant, the NO reserve must increase to y' = k / x'.
We interpret the increase in the opposite reserve (Δy) as the trader's cost.

This is a simplified educational model.
"""


class PredictionMarket:
    def __init__(self, initial_liquidity: float):
        """Initialize a symmetric binary CPMM pool.

        Args:
            initial_liquidity: starting shares on BOTH sides (x=y=initial_liquidity)
        """
        if initial_liquidity <= 0:
            raise ValueError("initial_liquidity must be > 0")

        x = float(initial_liquidity)
        y = float(initial_liquidity)

        self.shares = {"YES": x, "NO": y}
        self.k = x * y  # constant product invariant

    def calculate_price(self, outcome: str) -> float:
        """Return the current price (interpreted probability) for 'YES' or 'NO'.

        We use a common CPMM-style normalized quote that stays in [0, 1] and sums to 1:
            p_yes = y / (x + y)
            p_no  = x / (x + y)

        Intuition: if NO reserve y is large relative to YES reserve x, YES is expensive (high p_yes).
        """
        outcome = outcome.upper()
        if outcome not in ("YES", "NO"):
            raise ValueError("outcome must be 'YES' or 'NO'")

        x = self.shares["YES"]
        y = self.shares["NO"]
        total = x + y
        if total <= 0:
            raise RuntimeError("Invalid pool state: x + y must be > 0")

        if outcome == "YES":
            return y / total
        return x / total

    def buy_shares(self, outcome: str, amount: float):
        """Buy `amount` of outcome shares from the pool.

        CPMM math:

        Let reserves be (x, y) with invariant x*y = k.

        - Buying YES means the pool gives the trader Δx=amount YES shares:
              x' = x - Δx
          To keep x'*y' = k, the new NO reserve must be:
              y' = k / x'
          The trader must provide the increase in NO reserve:
              cost = Δy = y' - y

        - Buying NO is symmetric:
              y' = y - Δy
              x' = k / y'
              cost = Δx = x' - x

        Args:
            outcome: 'YES' or 'NO'
            amount: number of shares to buy (>0)

        Returns:
            (cost, new_price_for_outcome)
        """
        outcome = outcome.upper()
        if outcome not in ("YES", "NO"):
            raise ValueError("outcome must be 'YES' or 'NO'")
        if amount <= 0:
            raise ValueError("amount must be > 0")

        x = self.shares["YES"]
        y = self.shares["NO"]

        if outcome == "YES":
            if amount >= x:
                raise ValueError("Not enough YES shares in the pool to buy that amount")

            # Remove YES from the pool.
            x_new = x - float(amount)

            # Maintain x_new * y_new = k  =>  y_new = k / x_new
            y_new = self.k / x_new

            # Cost is how much NO reserve must increase.
            cost = y_new - y

        else:  # outcome == "NO"
            if amount >= y:
                raise ValueError("Not enough NO shares in the pool to buy that amount")

            # Remove NO from the pool.
            y_new = y - float(amount)

            # Maintain x_new * y_new = k  =>  x_new = k / y_new
            x_new = self.k / y_new

            # Cost is how much YES reserve must increase.
            cost = x_new - x

        # Update pool state.
        self.shares["YES"] = x_new
        self.shares["NO"] = y_new

        new_price = self.calculate_price(outcome)
        return cost, new_price


if __name__ == "__main__":
    market = PredictionMarket(initial_liquidity=1000)

    print("Starting reserves:", market.shares)
    print("Starting prices:")
    print("  YES:", round(market.calculate_price("YES"), 6))
    print("  NO :", round(market.calculate_price("NO"), 6))

    trades = [("YES", 100), ("NO", 50), ("YES", 200)]

    for outcome, amount in trades:
        cost, new_price = market.buy_shares(outcome, amount)
        print("\nTrade: buy", amount, outcome)
        print("  Cost (in opposite reserve units):", round(cost, 6))
        print("  New reserves:", {k: round(v, 6) for k, v in market.shares.items()})
        print("  New price", outcome + ":", round(new_price, 6))
        print("  Prices now: YES=", round(market.calculate_price("YES"), 6), ", NO=", round(market.calculate_price("NO"), 6))
