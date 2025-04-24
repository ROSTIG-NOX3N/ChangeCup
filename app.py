import streamlit as st
import pandas as pd

# 데이터 불러오기
try:
    results_df = pd.read_csv('Book(Result).csv')
except FileNotFoundError as e:
    st.error(f"파일을 찾을 수 없습니다: {e}")
except Exception as e:
    st.error(f"파일 로드 중 오류가 발생했습니다: {e}")

# 데이터프레임 컬럼 확인
st.write("데이터프레임 컬럼:", results_df.columns)

# 페이지 제목
st.title("⚽ 2025 아침체인지컵 ")

option = st.sidebar.selectbox(
    'Menu',
    ("메인 메뉴", "경기 결과", "득점자", "반별 통계"))

# '메인 메뉴'일 때 최근 경기 및 주변 경기 출력
if option == "메인 메뉴":
    st.subheader("📋 최근 경기 및 그 주변 경기 결과")

    # 데이터프레임 컬럼 확인
    st.write("현재 사용 중인 컬럼:", results_df.columns)

    # 예외 처리: 결과가 비어있을 경우 처리
    if results_df.empty:
        st.error("경기 결과 데이터가 없습니다.")
    else:
        # '경기' 열을 숫자형으로 변환하여 처리
        try:
            results_df['경기'] = pd.to_numeric(results_df['경기'], errors='coerce')
        except Exception as e:
            st.error(f"데이터 변환 중 오류가 발생했습니다: {e}")

        # 예정된 경기: 득점이 NaN인 경기 (예: 1팀득점 또는 2팀득점)
        try:
            scheduled_matches = results_df[results_df['1팀득점'].isna() | results_df['2팀득점'].isna()]
        except KeyError as e:
            st.error(f"컬럼 오류: {e}")
            scheduled_matches = pd.DataFrame()  # 빈 데이터프레임으로 처리
        
        scheduled_matches = scheduled_matches.sort_values(by='경기', ascending=True)

        # 이미 치러진 경기: 득점이 모두 있는 경기
        try:
            completed_matches = results_df[results_df['1팀득점'].notna() & results_df['2팀득점'].notna()]
        except KeyError as e:
            st.error(f"컬럼 오류: {e}")
            completed_matches = pd.DataFrame()  # 빈 데이터프레임으로 처리

        completed_matches = completed_matches.sort_values(by='경기', ascending=False)

        # 예정된 경기 중 가장 작은 3개
        if not scheduled_matches.empty:
            st.markdown("### 📅 예정된 경기 (경기번호 가장 작은 3개)")
            scheduled_matches_display = scheduled_matches.head(3)
            for idx, match in scheduled_matches_display.iterrows():
                경기번호 = match['경기']
                팀1 = match['1팀']
                팀2 = match['2팀']
                st.markdown(f"**{경기번호}** | **{팀1}** vs **{팀2}** | ⏳ 경기 예정")
                st.markdown("---")
        else:
            st.markdown("예정된 경기가 없습니다.")

        # 이미 치러진 경기 중 가장 큰 3개
        if not completed_matches.empty:
            st.markdown("### ✅ 이미 치러진 경기 (경기번호 가장 큰 3개)")
            completed_matches_display = completed_matches.head(3)
            for idx, match in completed_matches_display.iterrows():
                경기번호 = match['경기']
                팀1 = match['1팀']
                팀2 = match['2팀']
                팀1득점 = match['1팀득점']
                팀2득점 = match['2팀득점']
                결과 = match['결과']
                st.markdown(f"**{경기번호}** | **{팀1}** {팀1득점} : {팀2득점} **{팀2}** | 📌 {결과}")
                st.markdown("---")
        else:
            st.markdown("치러진 경기가 없습니다.")
