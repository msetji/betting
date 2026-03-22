def arb_profit_boost(
    base_odds_boost_side: float,   # e.g. 2.0 (+100)
    decimal_hedge: float,          # e.g. 1.95 (-105)
    stake_boost_side: float,       # e.g. 50.0
    boost_percentage: float = 0.50 # e.g. 0.50 for 50%
):
    """
    Calculates the hedge for a Profit Boosted bet.
    The boost only applies to the PROFIT, not the stake.
    """
    
    # 1. Calculate the 'Boosted' Decimal Odds
    # New Odds = 1 + (Original Profit * (1 + Boost))
    boosted_odds = 1 + (base_odds_boost_side - 1) * (1 + boost_percentage)
    
    # 2. Standard Arb Hedge Calculation
    # Stake_H = (Stake_B * Boosted_Odds) / Hedge_Odds
    stake_hedge = (stake_boost_side * boosted_odds) / decimal_hedge
    
    # 3. Profit Calculations
    payout_boost_side = stake_boost_side * boosted_odds
    payout_hedge_side = stake_hedge * decimal_hedge
    
    total_stake = stake_boost_side + stake_hedge
    guaranteed_profit = payout_boost_side - total_stake

    return {
        "original_odds": round(base_odds_boost_side, 3),
        "boosted_odds": round(boosted_odds, 3),
        "stake_boost_side": round(stake_boost_side, 2),
        "stake_hedge_side": round(stake_hedge, 2),
        "total_outlay": round(total_stake, 2),
        
        "payout_if_boost_wins": round(payout_boost_side, 2),
        "payout_if_hedge_wins": round(payout_hedge_side, 2),
        
        "guaranteed_profit": round(guaranteed_profit, 2),
        "roi_percent": round((guaranteed_profit / total_stake) * 100, 2)
    }

def print_verbose(result: dict):
    for k, v in result.items():
        print(f"{k}: {v}")
    print("-" * 30)

# Example: $50 bet at 2.0 odds boosted by 50%, hedged at 2.80
if __name__ == "__main__":
    result = arb_profit_boost(
        base_odds_boost_side=2.5, 
        decimal_hedge=1.61, 
        stake_boost_side=100.0,
        boost_percentage=0.25
    )
    print_verbose(result)