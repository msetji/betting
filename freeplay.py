def arb_freeplay(
    decimal_normal: float,   # decimal odds for the cash hedge book
    decimal_freeplay: float, # decimal odds where the FP is used
    stake_freeplay: float    # free-play stake (stake not returned)
):
    """
    Computes the optimal hedge to fully convert a free-play (FP) wager into cash.

    - The FP stake is not returned on a win.
    - The cash hedge returns both stake and profit.
    - The result ensures equal profit regardless of outcome.

    Parameters:
        decimal_normal: Decimal odds for the normal (cash) book, e.g., 1.16
        decimal_freeplay: Decimal odds for the free-play bet, e.g., 5.75
        stake_freeplay: The FP stake amount (e.g., 59)

    Returns:
        Dictionary with hedge stake, payouts, profits, and conversion rate.
    """

    dN = decimal_normal
    dFP = decimal_freeplay
    F = stake_freeplay

    # Optimal hedge amount (cash)
    stake_normal = F * (dFP - 1) / dN

    # --- Profits ---
    profit_if_fp_wins = F * (dFP - 1) - stake_normal
    profit_if_normal_wins = stake_normal * (dN - 1)

    # --- Payouts (total return, not net profit) ---
    payout_if_fp_wins = F * (dFP - 1)                     # FP side wins (stake not returned)
    payout_if_normal_wins = stake_normal * dN              # cash side wins (stake + profit)

    # --- Guaranteed profit (both sides should match closely) ---
    guaranteed_profit = min(profit_if_fp_wins, profit_if_normal_wins)
    conversion_rate = guaranteed_profit / F  # per $1 FP

    return {
        "stake_freeplay": round(F, 2),
        "stake_normal_cash": round(stake_normal, 2),
        "total_cash_used": round(stake_normal, 2),  # FP doesn't consume cash

        "payout_if_fp_wins": round(payout_if_fp_wins, 2),
        "payout_if_normal_wins": round(payout_if_normal_wins, 2),

        "profit_if_fp_wins": round(profit_if_fp_wins, 2),
        "profit_if_normal_wins": round(profit_if_normal_wins, 2),

        "guaranteed_profit": round(guaranteed_profit, 2),
        "conversion_rate": round(conversion_rate, 4),
        "decimal_odds": {"normal": dN, "freeplay": dFP}
    }


def print_verbose(result: dict):
    for k, v in result.items():
        print(f"{k}: {v}\n")


# --- Example usage ---
if __name__ == "__main__":
    result = arb_freeplay(
        decimal_normal=1.14,   # hedge side
        decimal_freeplay=6.5, # free-play side
        stake_freeplay=201.3
    )
    print_verbose(result)

    
#                                 python3 fpbetsizing.py