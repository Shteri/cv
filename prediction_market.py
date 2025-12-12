"""Refactored Prediction Market AMM (CPMM) into two conceptual parts:

1) State Manager (Simulated Redis):
   - A global dictionary `MARKET_STATE` holds the persistent market state.
   - `get_market_state()` reads it.
   - `update_market_state(new_yes, new_no)` writes it.

2) Trade Processor (Core logic):
   - `calculate_price_from_state()` computes prices from the current state.
   - `execute_trade(outcome, amount)` performs a CPMM trade and persists updates
     through `update_market_state(...)`.

CPMM invariant:
    x * y = k
where:
    x = YES_Shares in the pool
    y = NO_Shares in the pool
    k = constant product invariant

Trade interpretation (educational):
When a trader buys outcome shares, they remove that outcome from the pool.
To preserve x*y=k, the opposite side must increase; we interpret that increase
as the trader's cost in currency units.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# 1) State Manager (simulated Redis)
# ---------------------------------------------------------------------------

MARKET_STATE: dict[str, float] = {
    "YES_Shares": 1000.0,
    "NO_Shares": 1000.0,
    "k_invariant": 1000.0 * 1000.0,
}


def get_market_state() -> dict[str, float]:
    """Return the current market state (a copy, like reading from Redis)."""
    return dict(MARKET_STATE)


def update_market_state(new_yes: float, new_no: float) -> None:
    """Update the share balances in the global state (like writing to Redis)."""
    if new_yes <= 0 or new_no <= 0:
        raise ValueError("new_yes and new_no must remain positive")
    MARKET_STATE["YES_Shares"] = float(new_yes)
    MARKET_STATE["NO_Shares"] = float(new_no)


# ---------------------------------------------------------------------------
# 2) Trade Processor (core CPMM logic)
# ---------------------------------------------------------------------------

def calculate_price_from_state() -> dict[str, float]:
    """Compute current prices for YES/NO from the persisted state.

    We use a simple normalized pricing rule to obtain complementary prices:
        p(YES) = y / (x + y)
        p(NO)  = x / (x + y)

    This guarantees:
    - each price is in [0, 1]
    - p(YES) + p(NO) = 1
    """
    state = get_market_state()
    x = state["YES_Shares"]
    y = state["NO_Shares"]
    denom = x + y
    if denom <= 0:
        raise RuntimeError("invalid pool state: YES_Shares + NO_Shares must be positive")
    return {"YES": y / denom, "NO": x / denom}


def execute_trade(outcome: str, amount: float) -> dict[str, float | str]:
    """Execute a CPMM trade and persist results via `update_market_state`.

    Core CPMM math (x*y = k):
    - Let x be the pool balance of the outcome being purchased.
    - Let y be the pool balance of the opposite outcome.

    Buying `amount` shares removes them from that side of the pool:
        x_new = x - amount

    To keep the invariant:
        x_new * y_new = k  =>  y_new = k / x_new

    The pool's opposite-side balance increases by:
        cost = y_new - y

    We interpret `cost` as the currency paid by the trader.
    """
    outcome = outcome.upper()
    if outcome not in ("YES", "NO"):
        raise ValueError("outcome must be 'YES' or 'NO'")
    if amount <= 0:
        raise ValueError("amount must be positive")

    state = get_market_state()
    yes = state["YES_Shares"]
    no = state["NO_Shares"]
    k = state["k_invariant"]

    if outcome == "YES":
        x = yes
        y = no
        if amount >= x:
            raise ValueError("amount too large: would exhaust YES liquidity")

        x_new = x - amount
        y_new = k / x_new
        cost = y_new - y

        # Persist (simulate Redis write).
        update_market_state(new_yes=x_new, new_no=y_new)
    else:
        x = no
        y = yes
        if amount >= x:
            raise ValueError("amount too large: would exhaust NO liquidity")

        x_new = x - amount
        y_new = k / x_new
        cost = y_new - y

        # Persist (simulate Redis write).
        update_market_state(new_yes=y_new, new_no=x_new)

    prices = calculate_price_from_state()
    return {
        "Outcome": outcome,
        "Shares Purchased": float(amount),
        "Cost": float(cost),
        "New Price": float(prices[outcome]),
    }


# ---------------------------------------------------------------------------
# 3) Demonstration
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Initial MARKET_STATE:", get_market_state())
    print("Initial prices:", {k: round(v, 6) for k, v in calculate_price_from_state().items()})
    print()

    result_1 = execute_trade("YES", 100)
    print("Trade 1 result:", {k: (round(v, 6) if isinstance(v, float) else v) for k, v in result_1.items()})
    print("State after trade 1:", get_market_state())
    print("Prices after trade 1:", {k: round(v, 6) for k, v in calculate_price_from_state().items()})
    print()

    result_2 = execute_trade("NO", 50)
    print("Trade 2 result:", {k: (round(v, 6) if isinstance(v, float) else v) for k, v in result_2.items()})
    print("State after trade 2:", get_market_state())
    print("Prices after trade 2:", {k: round(v, 6) for k, v in calculate_price_from_state().items()})
