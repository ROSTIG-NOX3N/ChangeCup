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
     ("메인 메뉴","경기 결과","득점자","반별 통계"))


if option == "경기 결과":
    st.subheader("📋 전체 경기 결과")
    st.dataframe(results_df)

elif option == "득점자":
    st.subheader("🥅 득점자 순위")
    sorted_scorers = scorers_df.sort_values(by="득점", ascending=False).reset_index(drop=True)

    for idx, row in sorted_scorers.iterrows():
        st.markdown(f"""
        <div style="border: 1px solid #ccc; border-radius: 10px; padding: 10px; margin-bottom: 10px; background-color: #f9f9f9;">
            <h4 style="margin: 0;">🏅 {idx+1}위 - {row['이름']} ({row['소속']})</h4>
            <p style="margin: 0;">⚽ 득점 수: <strong>{row['득점']}</strong></p>
        </div>
        """, unsafe_allow_html=True)

elif option == "반별 통계":
    st.subheader("📊 반별 승/무/패 통계")
    st.dataframe(class_stats_df)

