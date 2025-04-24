import streamlit as st
import pandas as pd

results_df = pd.read_csv("Book(Result).csv")

st.title("📋 아침체인지컵 경기 결과")

for idx, match in results_df.iterrows():
    경기번호 = match['경기']
    팀1 = match['1팀']
    팀2 = match['2팀']
    팀1득점 = match['1팀득점']
    팀2득점 = match['2팀득점']
    결과 = match['결과']

    st.markdown(f"# ⚽ {경기번호}")
    st.markdown(f"##{팀1} {팀1득점} - {팀2득점} {팀2}")
    st.write(f"####결과: {결과}")
    st.markdown("---")
