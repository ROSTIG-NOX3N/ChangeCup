import streamlit as st
import pandas as pd

# CSV 파일 불러오기
results_df = pd.read_csv("Book(Result).csv")

# 앱 제목
st.title("📋 아침체인지컵 경기 결과")

# 한 경기씩 출력
for idx, match in results_df.iterrows():
    경기번호 = match['경기']
    팀1 = match['1팀']
    팀2 = match['2팀']
    팀1득점 = match['1팀득점']
    팀2득점 = match['2팀득점']
    결과 = match['결과']
    조 = match['조']
    경기일자 = match['경기일자']

    st.markdown(f"### ⚽ {경기번호} | {조}조")
    if str(팀1득점).isdigit() and str(팀2득점).isdigit():
        st.markdown(f"**{팀1}** {팀1득점} : {팀2득점} **{팀2}**")
        st.markdown(f"📌 결과: {결과}")
    else:
        st.markdown(f"**{팀1}** vs **{팀2}**")
        st.markdown("⏳ 경기 예정")

    st.markdown(f"📅 경기일자: {경기일자}")
    st.markdown("---")
