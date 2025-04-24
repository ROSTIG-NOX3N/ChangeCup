import streamlit as st
import pandas as pd

results_df = pd.read_csv("Book(Result).csv")
st.write("컬럼명 확인:", results_df.columns.tolist())

st.title("📋 아침체인지컵 경기 결과")

# 한 경기씩 출력
for idx, match in results_df.iterrows():
    st.markdown(f"<h4>⚽ {match['경기']}: {match['1팀']} vs {match['2팀']}</h4>", unsafe_allow_html=True)
    st.markdown("---")
