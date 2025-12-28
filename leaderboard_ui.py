import streamlit as st
import auth

def show_leaderboard_section():
    """Renders a visually appealing Hall of Fame with high-end cards."""
    st.markdown("<h3 style='color: #00ffcc; text-shadow: 0 0 10px #00ffcc; text-align: center;'>🏆 HALL OF FAME</h3>", unsafe_allow_html=True)
    st.divider()
    
    top_players = auth.get_top_players()
    
    if not top_players.empty:
        for i, row in top_players.iterrows():
            if i == 0:
                color, medal, bg = "#FFD700", "🥇", "rgba(255, 215, 0, 0.1)"
            elif i == 1:
                color, medal, bg = "#C0C0C0", "🥈", "rgba(192, 192, 192, 0.05)"
            elif i == 2:
                color, medal, bg = "#CD7F32", "🥉", "rgba(205, 127, 50, 0.05)"
            else:
                color, medal, bg = "#FFFFFF", "👤", "transparent"

            st.markdown(f"""
                <div style='border: 1px solid {color}; background-color: {bg}; padding: 12px; border-radius: 12px; margin-bottom: 8px; display: flex; justify-content: space-between;'>
                    <span style='font-weight: bold; color: {color};'>{medal} {row['username']}</span>
                    <span style='font-family: monospace; color: #00FF00;'>${row['high_score']:,.2f}</span>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.write("No legends yet...")