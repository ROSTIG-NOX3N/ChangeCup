import streamlit as st
import pandas as pd

# 데이터 불러오기
results_df = pd.read_csv('Book(Result).csv')
scorers_df = pd.read_csv('Book(Scorer).csv')
class_stats_df = pd.read_csv('Book(Class_Stat).csv')

# 페이지 제목
st.title("⚽ 2025 아침체인지컵 ")

# 섹션 선택
section = st.radio("메뉴를 선택하세요", ["경기 결과", "득점자", "반별 통계"])

# CSV 불러오기
results_df = pd.read_csv("Book(Result).csv")

# 테이블 보기
st.dataframe(results_df)

if section == "경기 결과":
    st.subheader("📋 전체 경기 결과")
    st.dataframe(results_df)

elif section == "득점자":
    st.subheader("🥅 득점자 순위")
    sorted_scorers = scorers_df.sort_values(by="골 수", ascending=False)
    st.dataframe(sorted_scorers)

elif section == "반별 통계":
    st.subheader("📊 반별 승/무/패 통계")
    st.dataframe(class_stats_df)
