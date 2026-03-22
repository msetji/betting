import streamlit as st

from boost import arb_profit_boost
from freeplay import arb_freeplay
from protected import arb_no_sweat
from sizing import arb_rebate_mix

st.set_page_config(page_title="Arbitrage Calculator", layout="wide", page_icon="📈")

def to_decimal(odds):
    """Converts American odds to decimal, returns passed in decimal odds otherwise."""
    if odds >= 100:
        return (odds / 100.0) + 1.0
    elif odds <= -100:
        return (100.0 / abs(odds)) + 1.0
    return odds

st.title("💰 Sports Betting Arbitrage Calculators")

st.sidebar.header("Settings")
calc_type = st.sidebar.radio(
    "Select Calculator",
    [
        "Profit Boost Arbitrage",
        "Freeplay Maximization",
        "Protected Pick Arbitrage",
        "Maximize Standard"
    ]
)

odds_format = st.sidebar.radio(
    "Odds Format",
    ["American", "Decimal"]
)

st.write("---")

def odds_input(label, default_am, default_dec, key_suffix=""):
    if odds_format == "American":
        val = st.number_input(f"{label} (American)", value=default_am, step=5, format="%d", key=f"am_{key_suffix}")
    else:
        val = st.number_input(f"{label} (Decimal)", value=default_dec, step=0.01, format="%.2f", key=f"dec_{key_suffix}")
    return to_decimal(val)

def display_results(promo_stake, hedge_stake, profit, result_dict, conversion_rate=None):
    st.write("---")
    
    if conversion_rate is not None:
        res_col1, res_col2, res_col3, res_col4 = st.columns(4)
        with res_col1:
            st.metric("Promo/FreePlay Stake", f"${promo_stake:,.2f}")
        with res_col2:
            st.metric("Hedge Stake", f"${hedge_stake:,.2f}")
        with res_col3:
            st.metric("Guaranteed Profit", f"${profit:,.2f}")
        with res_col4:
            st.metric("Conversion Rate", f"{conversion_rate * 100:.2f}%")
    else:
        res_col1, res_col2, res_col3 = st.columns(3)
        with res_col1:
            st.metric("Promo/Boost Stake", f"${promo_stake:,.2f}")
        with res_col2:
            st.metric("Hedge Stake", f"${hedge_stake:,.2f}")
        with res_col3:
            st.metric("Guaranteed Profit", f"${profit:,.2f}")
            
    if profit > 0:
        st.success(f"Profitable Arb! Lock in a guaranteed profit of ${profit:,.2f}.")
    elif profit == 0:
        st.warning("Breakeven Arb. You will not lose or make money.")
    else:
        st.error(f"Negative Arb. You will take a guaranteed loss of ${abs(profit):,.2f}.")
        
    with st.expander("View Detailed Calculations"):
        st.json(result_dict)

if calc_type == "Profit Boost Arbitrage":
    st.header("🚀 Profit Boost Arbitrage")
    st.markdown("Calculate the optimal hedge for a 'Profit Boost' token.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Boosted Bet")
        stake_boost = st.number_input("Promo Stake ($)", value=50.0, step=10.0, format="%.2f")
        dec_boost = odds_input("Base Odds (Pre-Boost)", +100, 2.00, "base_bst")
        
    with col2:
        st.subheader("Hedge Bet")
        dec_hedge = odds_input("Hedge Odds", -105, 1.95, "h_bst")
        
    with col3:
        st.subheader("Promo Details")
        boost_percentage = st.number_input("Boost Percentage (%)", value=50.0, step=5.0, format="%.1f") / 100.0

    if st.button("Calculate Hedge", type="primary"):
        result = arb_profit_boost(
            base_odds_boost_side=dec_boost,
            decimal_hedge=dec_hedge,
            stake_boost_side=stake_boost,
            boost_percentage=boost_percentage
        )
        display_results(
            promo_stake=result["stake_boost_side"], 
            hedge_stake=result["stake_hedge_side"], 
            profit=result["guaranteed_profit"], 
            result_dict=result
        )

elif calc_type == "Freeplay Maximization":
    st.header("💸 Freeplay Maximization")
    st.markdown("Convert a Free Play / Bonus Bet into maximum cash (where stake is not returned on a win).")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Free Play Bet")
        stake_freeplay = st.number_input("Free Play Stake ($)", value=50.0, step=10.0, format="%.2f")
        dec_freeplay = odds_input("Free Play Odds", +475, 5.75, "fp")
        
    with col2:
        st.subheader("Hedge Bet (Cash)")
        dec_normal = odds_input("Hedge Odds", -600, 1.16, "h_fp")
        
    if st.button("Calculate Hedge", type="primary"):
        result = arb_freeplay(
            decimal_normal=dec_normal,
            decimal_freeplay=dec_freeplay,
            stake_freeplay=stake_freeplay
        )
        display_results(
            promo_stake=result["stake_freeplay"], 
            hedge_stake=result["stake_normal_cash"], 
            profit=result["guaranteed_profit"], 
            result_dict=result,
            conversion_rate=result["conversion_rate"]
        )

elif calc_type == "Protected Pick Arbitrage":
    st.header("🛡️ Protected Pick Arbitrage")
    st.markdown("Calculate the optimal hedge for a 'No Sweat Bet' where a loss triggers a bonus bet refund.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Promo Bet")
        stake_no_sweat = st.number_input("Promo Stake ($)", value=100.0, step=10.0, format="%.2f")
        dec_no_sweat = odds_input("Promo Odds", 250, 3.50, "ns")
        
    with col2:
        st.subheader("Hedge Bet")
        dec_hedge = odds_input("Hedge Odds", -300, 1.33, "h_ns")
        
    with col3:
        st.subheader("Bonus Details")
        refund_rate = st.number_input("Refund Rate (%)", value=100.0, step=5.0, format="%.1f") / 100.0
        conversion = st.number_input("Bonus Conversion (%)", value=70.0, step=5.0, format="%.1f") / 100.0
        
    if st.button("Calculate Hedge", type="primary"):
        result = arb_no_sweat(
            decimal_no_sweat=dec_no_sweat,
            decimal_hedge=dec_hedge,
            stake_no_sweat=stake_no_sweat,
            bonus_refund_rate=refund_rate,
            bonus_conversion=conversion
        )
        display_results(
            promo_stake=result["stake_no_sweat_cash"], 
            hedge_stake=result["stake_hedge_cash"], 
            profit=result["guaranteed_profit"], 
            result_dict=result
        )

elif calc_type == "Maximize Standard":
    st.header("🔄 Maximize Standard (Rebate Mix)")
    st.markdown("Calculate the optimal hedge when one side receives a percentage rebate on a loss, or bias standard bets.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Promo (Rebate) Bet")
        stake_rebate = st.number_input("Rebate Stake ($)", value=100.0, step=10.0, format="%.2f")
        dec_rebate = odds_input("Rebate Odds", -115, 1.86, "reb")
        
    with col2:
        st.subheader("Standard (Hedge) Bet")
        dec_normal = odds_input("Standard Odds", +105, 2.05, "n_reb")
        
    with col3:
        st.subheader("Rebate Details")
        rebate_rate = st.number_input("Rebate Rate (%)", value=40.0, step=5.0, format="%.1f") / 100.0
        fp_val = st.number_input("Free Play Value (%)", value=50.0, step=5.0, format="%.1f") / 100.0
        profit_ratio = st.number_input("Profit Bias Setting", value=1.0, min_value=0.01, step=0.1, help=">1 biases profit to rebate side")

    if st.button("Calculate Hedge", type="primary"):
        try:
            result = arb_rebate_mix(
                decimal_normal=dec_normal,
                decimal_rebate=dec_rebate,
                stake_rebate=stake_rebate,
                rebate_rate=rebate_rate,
                freeplay_value=fp_val,
                profit_ratio_rebate_over_normal=profit_ratio
            )
            display_results(
                promo_stake=result["stake_rebate"], 
                hedge_stake=result["stake_normal"], 
                profit=result["guaranteed_profit"], 
                result_dict=result
            )
        except Exception as e:
            st.error(f"Error calculating hedge: {e}")
