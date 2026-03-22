def arb_no_sweat(
    decimal_no_sweat: float,    # Odds at the book with the promo
    decimal_hedge: float,       # Odds at the hedge book
    stake_no_sweat: float,      # Your actual cash stake on the promo
    bonus_refund_rate: float = 1.0,  # Usually 1.0 (100% back)
    bonus_conversion: float = 0.70   # What you turn bonus bets into (e.g., 0.70)
):
    """
    Calculates the hedge for a 'No Sweat Bet' where a loss triggers a bonus bet.
    
    Logic: 
    If No Sweat Wins: Profit = Stake * (Odds - 1) - Hedge
    If No Sweat Loses: Profit = (Stake * Refund * Conversion) + Hedge * (Odds - 1) - Stake
    """
    
    dS = decimal_no_sweat
    dH = decimal_hedge
    S = stake_no_sweat
    
    # The 'Value' of the refund if the bet fails
    refund_value = S * bonus_refund_rate * bonus_conversion
    
    # Formula to equalize profit on both sides:
    # Hedge = (S * dS - refund_value) / dH
    stake_hedge = (S * dS - refund_value) / dH
    
    # Calculations
    profit_if_ns_wins = (S * (dS - 1)) - stake_hedge
    # If it loses, you lose S, but gain (Hedge Profit) + Refund Value
    profit_if_hedge_wins = (stake_hedge * (dH - 1)) - S + refund_value
    
    total_outlay = S + stake_hedge
    guaranteed_profit = min(profit_if_ns_wins, profit_if_hedge_wins)

    return {
        "stake_no_sweat_cash": round(S, 2),
        "stake_hedge_cash": round(stake_hedge, 2),
        "total_cash_risk": round(total_outlay, 2),
        
        "if_no_sweat_wins": {
            "payout": round(S * dS, 2),
            "net_profit": round(profit_if_ns_wins, 2)
        },
        "if_hedge_wins": {
            "payout_cash": round(stake_hedge * dH, 2),
            "bonus_earned": round(S * bonus_refund_rate, 2),
            "net_profit_inc_bonus": round(profit_if_hedge_wins, 2)
        },
        
        "guaranteed_profit": round(guaranteed_profit, 2),
        "profit_margin": round(guaranteed_profit / S, 4)
    }

def print_verbose(result: dict):
    for k, v in result.items():
        if isinstance(v, dict):
            print(f"--- {k} ---")
            for sub_k, sub_v in v.items():
                print(f"  {sub_k}: {sub_v}")
        else:
            print(f"{k}: {v}")
    print("\n")

# Example: $100 No Sweat Bet at 3.50 odds, Hedged at 1.45 odds
if __name__ == "__main__":
    result = arb_no_sweat(
        decimal_no_sweat=3.5, 
        decimal_hedge=1.32, 
        stake_no_sweat=1000.0,
        bonus_refund_rate=1.0,
        bonus_conversion=0.67
    )
    print_verbose(result)