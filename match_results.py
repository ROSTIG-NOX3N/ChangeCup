import streamlit as st
import pandas as pd

def display_results():
    # CSV에서 경기 결과 불러오기
    try:
        results_df = pd.read_csv("Book(Result).csv")
    except FileNotFoundError:
        st.error("경기 결과 파일(Book(Result).csv)을 찾을 수 없습니다.")
        return

    st.subheader("📋 전체 경기 결과")

    # 조별로 그룹핑하여 보여주기
    for idx, row in results_df.iterrows():
        경기번호 = row.get("경기 번호", idx + 1)
        팀1 = row["팀1"]
        팀2 = row["팀2"]
        점수 = row["점수"]
        결과 = row["결과"]

        st.write(f"경기 {경기번호}: {팀1} vs {팀2} → {점수} ({결과})")
