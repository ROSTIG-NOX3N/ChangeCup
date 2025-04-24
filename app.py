import streamlit as st
import pandas as pd

# 데이터 불러오기
results_df = pd.read_csv('Book(Result).csv')
scorers_df = pd.read_csv('Book(Scorer).csv')
class_stats_df = pd.read_csv('Book(Class_Stat).csv')

# 페이지 제목
st.title("⚽ 2025 아침체인지컵 ")
sorted_scorers = scorers_df.sort_values(by='득점', ascending=False)

option = st.sidebar.selectbox(
    'Menu',
     ("메인 메뉴","경기 결과","득점자","반별 통계"))

#css 영역
def scorer_card(name, team, goals, rank_label):
    card_html = f"""
    <style>
    .scorer-card {{
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 10px;
        background-color: #f5f5f5;
        color: #000;
        transition: all 0.3s ease;
    }}

    @media (prefers-color-scheme: dark) {{
        .scorer-card {{
            background-color: #222;
            color: #fff;
            border: 1px solid #555;
        }}
    }}
    </style>

    <div class="scorer-card">
        <h4 style="margin: 0;">🏅 {rank_label} - {name} ({team})</h4>
        <p style="margin: 0;">⚽ 득점 수: <strong>{goals}</strong></p>
    </div>
    """
    return card_html
    
if option == "경기 결과":
    st.subheader("📋 전체 경기 결과")
    st.dataframe(results_df)

elif option == "득점자":
    st.subheader("🥅 득점자 순위")
    prev_goals = None
    rank = 0
    display_rank = 0
    
    for idx, row in sorted_scorers.iterrows():
        goals = row['득점']
        
        if goals != prev_goals:
            rank = display_rank + 1
            rank_label = f"{rank}위"
        else:
            rank_label = f"공동 {rank}위"
        
        st.markdown(scorer_card(row['이름'], row['소속'], goals, rank_label), unsafe_allow_html=True)
        
        prev_goals = goals
        display_rank += 1



elif option == "반별 통계":
    st.subheader("📊 반별 승/무/패 통계")
    st.dataframe(class_stats_df)

