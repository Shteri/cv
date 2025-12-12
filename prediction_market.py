class PredictionMarket:
    """Constant Product Market Maker (CPMM) for a binary market: 'YES'/'NO'.

    The pool holds reserves (shares) for both outcomes:
      x = shares['YES']
      y = shares['NO']

    The invariant is constant product:
      x * y = k

    A trader who buys `amount` shares of an outcome removes that many shares
    from the pool (decreasing that reserve). To keep x*y constant, the other
    reserve must increase accordingly; the trader pays exactly that increase.
    """

    def __init__(self, initial_liquidity: float):
        if initial_liquidity <= 0:
            raise ValueError("initial_liquidity must be > 0")

        x = float(initial_liquidity)
        y = float(initial_liquidity)

        self.shares = {"YES": x, "NO": y}
        self.k = x * y

    def calculate_price(self, outcome: str) -> float:
        """Return the current probability-like price for 'YES' or 'NO'.

        We normalize prices to [0, 1] and to sum to 1:
          p(YES) = y / (x + y)
          p(NO)  = x / (x + y)

        This matches the CPMM intuition that when YES reserve gets smaller
        (YES is being bought), p(YES) increases.
        """

        if outcome not in self.shares:
            raise ValueError("outcome must be 'YES' or 'NO'")

        x = self.shares["YES"]
        y = self.shares["NO"]
        total = x + y
        if total <= 0:
            raise RuntimeError("invalid pool state: total shares must be > 0")

        if outcome == "YES":
            return y / total
        return x / total

    def buy_shares(self, outcome: str, amount: float):
        """Buy `amount` shares of `outcome` from the pool.

        CPMM math (x * y = k):

        If buying YES:
          - Pool gives the trader Δx = amount YES shares
          - New YES reserve: x' = x - Δx
          - To keep invariant: x' * y' = k  =>  y' = k / x'
          - Trader must add Δy = y' - y of the OTHER side into the pool
            (interpreted here as the currency cost).

        If buying NO, the roles of x and y swap.

        Returns:
          (cost, new_price_for_outcome)
        """

        if outcome not in self.shares:
            raise ValueError("outcome must be 'YES' or 'NO'")
        if amount <= 0:
            raise ValueError("amount must be > 0")

        yes = self.shares["YES"]
        no = self.shares["NO"]

        if outcome == "YES":
            if amount >= yes:
                raise ValueError("amount too large: cannot buy all (or more) YES liquidity")

            # x' = x - Δx
            x_new = yes - amount
            # Maintain x'*y' = k => y' = k / x'
            y_new = self.k / x_new
            # Cost is the required increase in the opposite reserve: Δy = y' - y
            cost = y_new - no

            self.shares["YES"] = x_new
            self.shares["NO"] = y_new

        else:  # outcome == 'NO'
            if amount >= no:
                raise ValueError("amount too large: cannot buy all (or more) NO liquidity")

            # y' = y - Δy
            y_new = no - amount
            # Maintain x'*y' = k => x' = k / y'
            x_new = self.k / y_new
            # Cost is the required increase in the opposite reserve: Δx = x' - x
            cost = x_new - yes

            self.shares["YES"] = x_new
            self.shares["NO"] = y_new

        new_price = self.calculate_price(outcome)
        return cost, new_price


if __name__ == "__main__":
    market = PredictionMarket(initial_liquidity=1000)

    print("Initial reserves:", market.shares)
    print(
        "Initial prices:",
        {"YES": market.calculate_price("YES"), "NO": market.calculate_price("NO")},
    )
    print()

    trades = [("YES", 100), ("NO", 50), ("YES", 200)]

    for outcome, amount in trades:
        cost, new_price = market.buy_shares(outcome, amount)
        print(f"Trade: buy {amount} {outcome}")
        print(f"  Cost paid (other reserve increase): {cost:.6f}")
        print("  New reserves:", {k: round(v, 6) for k, v in market.shares.items()})
        print(
            "  New prices:",
            {
                "YES": round(market.calculate_price("YES"), 6),
                "NO": round(market.calculate_price("NO"), 6),
            },
        )
        print(f"  New {outcome} price: {new_price:.6f}")
        print()
