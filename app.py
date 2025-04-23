import streamlit as st
import pandas as pd

st.set_page_config(page_title="아침체인지컵 2025", layout="wide")
st.title("🏆 아침체인지컵 2025")
st.markdown("**반대항 축구대회 | 1, 2, 3학년 연합전**")

# 데이터 불러오기
df = pd.read_csv("group_data.csv")

# 조 선택
group = st.selectbox("조를 선택하세요", sorted(df["조"].unique()))
group_df = df[df["조"] == group]

# 결과 출력
st.subheader(f"📋 {group}조 팀 구성")
st.table(group_df.reset_index(drop=True))
