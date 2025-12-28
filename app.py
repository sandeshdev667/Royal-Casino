import streamlit as st
import engine
import auth
import leaderboard_ui
import time
import random

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def show_login():
    st.markdown("<h1 style='text-align: center; color: #FFD700;'>🎰 ROYAL CASINO</h1>", unsafe_allow_html=True)
    with st.expander("📖 View Game Rules"):
        st.write("Match 3: 10x | Match 2: 2x | Data saves to your name.")
    
    with st.form("login_form"):
        user = st.text_input("Username").strip()
        submit = st.form_submit_button("Enter Casino")
        if submit and user:
            data = auth.get_user(user)
            st.session_state.user = user
            st.session_state.balance = float(data['balance']) if data else 1000.0
            st.session_state.high_score = float(data['high_score']) if data else 1000.0
            st.session_state.logged_in = True
            st.rerun()






def show_slots():
    if 'total_relief' not in st.session_state:
        st.session_state.total_relief = 0.0

    # --- CALCULATIONS ---
    starting_balance = 1000.0
    total_diff = st.session_state.balance - starting_balance - st.session_state.total_relief

    # --- SIDEBAR UI ---
    # We use unique keys for every button to prevent the DuplicateElementId error
    
    st.sidebar.markdown(f"## 👤 {st.session_state.user}")
    st.sidebar.divider()
    
    # Metrics Section
    st.sidebar.metric("Bankroll", f"${st.session_state.balance:,.2f}")
    st.sidebar.metric("Personal Best", f"${st.session_state.high_score:,.2f}")
    
    # Profit/Loss Metric with color coding
    st.sidebar.metric(
        label="Total Profit/Loss", 
        value=f"${abs(total_diff):,.2f}", 
        delta=f"{'+' if total_diff >= 0 else '-'}${abs(total_diff):,.2f}",
        delta_color="normal"
    )
    
    st.sidebar.divider()
    
    # Relief Fund Button - added a unique key
    # Relief Fund Button in Sidebar
    if st.session_state.balance < 1:
        if st.sidebar.button("💸 Relief Fund", key="sidebar_relief_btn"):
            st.session_state.balance += 500.0
            st.session_state.total_relief += 500.0 # Track the debt
            auth.save_user(st.session_state.user, st.session_state.balance, st.session_state.high_score)
            st.rerun()
    
    # Logout Button - added a unique key
    if st.sidebar.button("LOGOUT", key="sidebar_logout_btn"):
        auth.save_user(st.session_state.user, st.session_state.balance, st.session_state.high_score)
        st.session_state.logged_in = False
        st.rerun()

    # --- UPDATED GOLD UI STYLING ---

    st.markdown("""
    <style>
    .stButton>button:active {
        transform: scale(0.95);
        box-shadow: inset 0 0 10px #000;
        background: linear-gradient(180deg, #8A6E2F, #B38728);
    }
                /* Increase the size of the slot symbols */
        .reel-text {
            font-size: 5rem !important; /* Scaled up from standard size */
            font-weight: bold;
            text-align: center;
            letter-spacing: 20px;
            margin: 10px 0;
        }

        /* Make the reel container larger and centered */
        .reel-container {
            background: linear-gradient(145deg, #050505, #111111);
            border: 3px solid #FFD700; 
            border-radius: 30px; 
            padding: 50px 20px; /* More padding for a 'bigger' feel */
            box-shadow: 0 0 40px rgba(255, 215, 0, 0.3); 
            margin: 20px auto;
            max-width: 600px;
        }

        /* Scale the Pull Lever button */
        .stButton>button {
            height: 60px;
            font-size: 1.5rem !important;
            border-radius: 15px;
        .reel-container {
            background: linear-gradient(145deg, #050505, #111111);
            border: 3px solid #FFD700; 
            border-radius: 30px; 
            padding: 50px 20px;
            text-align: center;
        }
        .reel-text { font-size: 5rem !important; }
    </style>
""", unsafe_allow_html=True)
    

    col_game, col_spacer, col_lead = st.columns([2, 1, 1])
   
        
    with col_spacer:
        # This column stays empty to create the 'gap'
        st.write("") 




    with col_game:
        # Step=5.0 and key="bet_val" keep the bet locked
        st.markdown("<h1 style='text-align: center; color: #FFD700;'>🎰 ROYAL SLOTS</h1>", unsafe_allow_html=True)
        bet = st.number_input("Wager Amount", 1.0, 1000000.0, step=5.0, key="bet_val")
        
        reel_box = st.empty()
        reel_box.markdown('<div class="reel-container"><h1 style="text-align: center;">🍒 | 🍋 | 💎</h1></div>', unsafe_allow_html=True)

        if st.button("🎰 PULL LEVER"):
            if st.session_state.balance >= bet:
                st.session_state.balance -= bet
                
                # Animation frames
                for _ in range(12):
                    temp = [random.choice(engine.SYMBOLS) for _ in range(3)]
                    reel_box.markdown(f'<div class="reel-container"><h1 style="text-align: center;">{temp[0]} | {temp[1]} | {temp[2]}</h1></div>', unsafe_allow_html=True)
                    time.sleep(0.08)
                
                final_reels, res_type = engine.get_balanced_spin()
                
                # Jackpot Effect
                if res_type == "JACKPOT":
                    st.balloons()
                    for color in ["#FFD700", "#111", "#FFD700"]:
                        reel_box.markdown(f'<div class="reel-container" style="background-color:{color};"><h1 style="text-align: center;">{final_reels[0]} | {final_reels[1]} | {final_reels[2]}</h1></div>', unsafe_allow_html=True)
                        time.sleep(0.1)
                
                reel_box.markdown(f'<div class="reel-container"><h1 style="text-align: center;">{final_reels[0]} | {final_reels[1]} | {final_reels[2]}</h1></div>', unsafe_allow_html=True)
                
                payout = engine.get_payout(bet, res_type)
                st.session_state.balance += payout
                
                # Update High Score
                if st.session_state.balance > st.session_state.high_score:
                    st.session_state.high_score = st.session_state.balance
                
                # Save Data
                auth.save_user(st.session_state.user, st.session_state.balance, st.session_state.high_score)
                
                if res_type == "JACKPOT": st.success(f"💰 JACKPOT! +${payout:,.2f}")
                elif res_type == "MATCH_TWO": st.info(f"✨ 2 Matches! +${payout:,.2f}")
                else: st.error("Loss")

                # --- REFRESH FIX ---
                # Brief pause so the user can see the win message, then refresh to update leaderboard
                time.sleep(1.2)
                st.rerun()
            else:
                st.warning("Insufficient funds!")

    with col_lead:
        # Modular leaderboard section

        leaderboard_ui.show_leaderboard_section()

if __name__ == "__main__":
    if not st.session_state.logged_in:
        show_login()
    else:
        show_slots()