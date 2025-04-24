import streamlit as st
import pandas as pd

st.title("📋 아침체인지컵 경기 결과")

# CSV 불러오기
results_df = pd.read_csv("Book(Result).csv")

# 테이블 보기
st.dataframe(results_df)

# 한 경기씩 출력
for idx, match in results_df.iterrows():
    st.markdown(f"<h4>⚽ {match['경기']}경기: {match['팀1']} vs {match['팀2']}</h4>", unsafe_allow_html=True)
    st.markdown("---")
