def arb_rebate_mix(
    decimal_normal: float,            # e.g. 1.97
    decimal_rebate: float,            # e.g. 1.91
    stake_rebate: float,              # stake on rebate book
    rebate_rate: float = 0.40,        # percent returned as FP on loss
    freeplay_value: float = 0.50,     # FP cash conversion rate
    profit_ratio_rebate_over_normal: float = 2.0  # bias profit to rebate side
):
    """
    decimal_normal: decimal odds at the normal book (e.g., 1.97)
    decimal_rebate: decimal odds at rebate book (e.g., 1.91)
    stake_rebate: stake placed on rebate sportsbook
    rebate_rate: rebate % when rebate wager loses (e.g., 0.40 = 40%)
    freeplay_value: cash conversion value of rebate/freeplay (0.48 -> worth 48%)
    profit_ratio_rebate_over_normal: r > 1 biases profit to rebate (normal ~ breakeven)
    """

    dN = decimal_normal
    dR = decimal_rebate

    # effective FP credit fraction
    rf = rebate_rate * freeplay_value
    r = float(profit_ratio_rebate_over_normal)

    # target: profit_rebate = r * profit_normal
    denom = (dN - 1) + r
    if denom <= 0:
        raise ValueError("Invalid configuration: adjust r or odds.")

    # stake on normal to satisfy ratio
    stake_normal = stake_rebate * ((dR - 1) + r * (1 - rf)) / denom

    # profits
    profit_if_normal_wins = stake_normal * (dN - 1) - stake_rebate + rf * stake_rebate
    profit_if_rebate_wins = stake_rebate * (dR - 1) - stake_normal

    # payouts (including stake return + rebate if losing rebate side)
    payout_if_normal_wins = stake_normal * dN
    payout_if_normal_wins_plus_stake = stake_normal * dN + rf * stake_rebate
    payout_if_rebate_wins = stake_rebate * dR

    return {
        "stake_normal": round(stake_normal, 2),
        "stake_rebate": round(stake_rebate, 2),
        "total_stake": round(stake_normal + stake_rebate, 2),


        "payout_if_normal_wins": round(payout_if_normal_wins, 2),

        "payout_if_normal_wins_plus_stake": round(payout_if_normal_wins_plus_stake, 2),
        "payout_if_rebate_wins": round(payout_if_rebate_wins, 2),

        "profit_if_normal_wins": round(profit_if_normal_wins, 2),
        "profit_if_rebate_wins": round(profit_if_rebate_wins, 2),

        "guaranteed_profit": round(min(profit_if_normal_wins, profit_if_rebate_wins), 2),
        "profit_bias_ratio_rebate_over_normal": r,
        "total_edge": round(min(profit_if_normal_wins, profit_if_rebate_wins) / (stake_normal + stake_rebate), 4),
        "decimal_odds": {"normal": round(dN, 3), "rebate": round(dR, 3)},
    }


def print_verbose(result: dict):
    for k, v in result.items():
        print(f"{k}: {v}\n")


# Example usage
if __name__ == "__main__":
    result = arb_rebate_mix(        #decimal odds are payout per $1 stake
        decimal_normal=2.07,     # normal book decimal odds
        decimal_rebate=1.86,      # rebate book decimal odds
        stake_rebate=100.00,
        rebate_rate=0,
        freeplay_value=0.67,
        profit_ratio_rebate_over_normal=1.0
    )
    print_verbose(result)


#              python3 betsizing.py

