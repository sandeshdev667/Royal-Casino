import random

# HIDDEN HOUSE SETTINGS
PROB_JACKPOT = 0.10  # 10% chance for 3-of-a-kind
PROB_MATCH_TWO = 0.25  # 25% chance for 2-of-a-kind
SYMBOLS = ["🍒", "🍋", "🔔", "💎", "7️⃣"]

def get_balanced_spin():
    """Determines result based on hidden terminal-level probabilities."""
    rand_val = random.random()
    
    if rand_val < PROB_JACKPOT:
        sym = random.choice(SYMBOLS)
        return [sym, sym, sym], "JACKPOT"
    
    elif rand_val < (PROB_JACKPOT + PROB_MATCH_TWO):
        sym1 = random.choice(SYMBOLS)
        remaining_syms = [s for s in SYMBOLS if s != sym1]
        sym2 = random.choice(remaining_syms)
        results = [sym1, sym1, sym2]
        random.shuffle(results)
        return results, "MATCH_TWO"
    
    else:
        results = random.sample(SYMBOLS, k=3)
        return results, "LOSS"

def get_payout(bet, result_type):
    """Tiered payout logic."""
    if result_type == "JACKPOT":
        return bet * 10 
    elif result_type == "MATCH_TWO":
        return bet * 2   
    return 0