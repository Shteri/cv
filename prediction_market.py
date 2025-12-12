from __future__ import annotations


class PredictionMarket:
    """A simple Constant Product Market Maker (CPMM) for a binary market: 'YES'/'NO'.

    We maintain the invariant:
        x * y = k
    where:
        x = shares['YES']  (pool reserve of YES shares)
        y = shares['NO']   (pool reserve of NO shares)
        k is constant (ignoring fees).

    Intuition:
    - If traders buy YES, they remove YES from the pool (x decreases).
      To keep x*y=k, the pool's NO reserve must increase (y increases),
      and that increase is the trade "cost" (paid into the pool).
    - Symmetrically for buying NO.
    """

    def __init__(self, initial_liquidity: float = 1000.0):
        if initial_liquidity <= 0:
            raise ValueError("initial_liquidity must be > 0")

        x = float(initial_liquidity)
        y = float(initial_liquidity)

        self.shares = {"YES": x, "NO": y}
        # Constant product invariant: k = x * y
        self.k = x * y

    def calculate_price(self, outcome: str) -> float:
        """Return a normalized price (probability-like) between 0 and 1.

        We use a common CPMM-style normalization:
            price(YES) = y / (x + y)
            price(NO)  = x / (x + y)

        This ensures:
        - prices are in [0, 1]
        - price(YES) + price(NO) = 1
        - when x == y, both prices are 0.5
        """

        if outcome not in ("YES", "NO"):
            raise ValueError("outcome must be 'YES' or 'NO'")

        x = self.shares["YES"]
        y = self.shares["NO"]
        total = x + y
        if total <= 0:
            raise RuntimeError("invalid pool state: x+y must be > 0")

        if outcome == "YES":
            return y / total
        return x / total

    def buy_shares(self, outcome: str, amount: float) -> tuple[float, float]:
        """Buy `amount` shares of `outcome` from the pool.

        CPMM math (no fees):
        Let outcome reserve be r_out, other reserve be r_other.
        Buying `amount` outcome shares removes them from the pool:
            r_out_new = r_out - amount

        To keep the invariant r_out_new * r_other_new = k:
            r_other_new = k / r_out_new

        The trader must pay the increase in the other reserve into the pool:
            cost = r_other_new - r_other

        Returns:
            (cost, new_price_of_outcome)
        """

        if outcome not in ("YES", "NO"):
            raise ValueError("outcome must be 'YES' or 'NO'")
        if amount <= 0:
            raise ValueError("amount must be > 0")

        other = "NO" if outcome == "YES" else "YES"

        r_out = self.shares[outcome]
        r_other = self.shares[other]

        # You cannot buy more shares than exist in the pool reserve.
        if amount >= r_out:
            raise ValueError(
                f"amount too large: pool has {r_out:.6f} {outcome} shares"
            )

        # Remove `amount` of outcome from the pool.
        r_out_new = r_out - amount

        # Enforce constant product: r_out_new * r_other_new = k
        r_other_new = self.k / r_out_new

        # The required payment is the increase in the other reserve.
        cost = r_other_new - r_other
        if cost < 0:
            # In a correct CPMM buy, cost should be positive.
            raise RuntimeError("computed negative cost; invalid trade")

        # Update pool reserves.
        self.shares[outcome] = r_out_new
        self.shares[other] = r_other_new

        return cost, self.calculate_price(outcome)


if __name__ == "__main__":
    market = PredictionMarket(initial_liquidity=1000)

    print("Initial pool shares:", market.shares)
    print(f"Initial price YES: {market.calculate_price('YES'):.6f}")
    print(f"Initial price NO : {market.calculate_price('NO'):.6f}")
    print("-")

    trades = [("YES", 100), ("NO", 50), ("YES", 200)]

    for outcome, amount in trades:
        cost, new_price = market.buy_shares(outcome, amount)
        print(f"Buy {amount} {outcome} shares")
        print(f"  Cost paid (in opposite reserve units): {cost:.6f}")
        print(f"  New price {outcome}: {new_price:.6f}")
        print(f"  Pool shares now: {market.shares}")
        print("-")
