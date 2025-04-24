import streamlit as st
import pandas as pd

# 데이터 불러오기
results_df = pd.read_csv('Book(Result).csv')
scorers_df = pd.read_csv('Book(Scorer).csv')
class_stats_df = pd.read_csv('Book(Class_Stat).csv')

# 페이지 제목
st.title("⚽ 2025 아침체인지컵 ")

option = st.sidebar.selectbox(
    'Menu',
     ("메인 메뉴", "경기 결과", "득점자", "반별 통계"))

# 득점자 순위를 위한 정렬
sorted_scorers = scorers_df.sort_values(by='득점', ascending=False)

# CSS 영역
def scorer_card(name, team, goals):
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
        <h4 style="margin: 0;">🏅 {name} ({team})</h4>
        <p style="margin: 0;">⚽ 득점 수: <strong>{goals}골</strong></p>
    </div>
    """
    return card_html

if option == "경기 결과":
    st.subheader("📋 전체 경기 결과")
    st.dataframe(results_df)

elif option == "득점자":
    st.subheader("득점 순위")
    top_scorers = sorted_scorers[sorted_scorers['득점'] >= 2].head(10)

    for idx, row in top_scorers.iterrows():
        st.markdown(scorer_card(row['이름'], row['소속'], row['득점']), unsafe_allow_html=True)

elif option == "반별 통계":
    st.subheader("📊 반별 승/무/패 통계")
    st.dataframe(class_stats_df)
