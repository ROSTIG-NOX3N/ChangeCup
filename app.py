import streamlit as st
import pandas as pd
from video_links import video_links
import numpy as np

# 데이터 불러오기
results_df = pd.read_csv('Book(Result).csv')
scorers_df = pd.read_csv('Book(Scorer).csv')
class_stats_df = pd.read_csv('Book(Class_Stat).csv')

# 페이지 제목
st.title("⚽ 2025 아침체인지컵 ")

# 사이드 메뉴
option = st.sidebar.selectbox(
    'Menu',
    ("메인 메뉴", "경기 일정", "득점자", "반별 통계")
)

# 메인 메뉴 탭 기능
if option == "메인 메뉴":
    # 탭 3개: 공지사항, 경기영상, 조별결과
    tab_option = st.radio(
        "메인 메뉴 선택",
        ("공지사항", "경기영상", "조별결과")
    )

    # 공지사항 탭
    if tab_option == "공지사항":
        st.subheader("공지사항")
        st.write("여기에 공지사항을 입력하세요.")

    # 경기영상 탭
    elif tab_option == "경기영상":
        경기선택 = st.selectbox(
            "경기를 선택하세요",
            options=[f"{경기}경기 영상보기" for 경기 in range(4, 11)]
        )
        경기번호 = int(경기선택.split()[0].replace("경기", ""))
        st.title(f"{경기번호}경기 영상")
        영상링크 = video_links.get(경기번호, "영상없음")
        if 영상링크 != "영상없음":
            st.video(영상링크)
        else:
            st.write("이 경기는 영상이 아직 업로드되지 않았습니다.")

    # 조별결과 탭
    elif tab_option == "조별결과":
        st.subheader("📊 조별 승/무/패 통계")

        # 진출확정 팀 제외
        제외팀 = ["C조", "선생님팀"]

        # 승률 계산
        class_stats_df['경기수'] = class_stats_df['승'] + class_stats_df['무'] + class_stats_df['패']
        class_stats_df['승률'] = class_stats_df['승'] / class_stats_df['경기수']

        # 득실차 계산
        class_stats_df['득실차'] = class_stats_df['득점'] - class_stats_df['실점']

        # 확률 점수 계산 (승률 70%, 득실차 30%)
        후보팀 = class_stats_df[~class_stats_df['조'].isin(제외팀)].copy()
        후보팀['점수'] = 후보팀['승률'] * 0.7 + (후보팀['득실차'] - 후보팀['득실차'].min()) / (후보팀['득실차'].max() - 후보팀['득실차'].min()) * 0.3

        # 확률 백분율로 변환
        후보팀['진출확률(%)'] = (후보팀['점수'] / 후보팀['점수'].sum()) * 100

        st.markdown("### 🔮 8강 진출 확률 (C조, 선생님팀 제외)")
        st.dataframe(후보팀[['조', '진출확률(%)']].sort_values(by='진출확률(%)', ascending=False).round(1).reset_index(drop=True))

# 경기 결과 탭
elif option == "경기 일정":
    st.subheader("📋 전체 경기 일정")
    st.dataframe(results_df)

# 득점자 탭
elif option == "득점자":
    st.subheader("다득점자")
    sorted_scorers = scorers_df.sort_values(by='득점', ascending=False)
    max_goals = sorted_scorers['득점'].max()

    for idx, row in sorted_scorers.iterrows():
        # 메달 색상 설정
        if row['득점'] == max_goals:
            medal_color = 'gold'  # 금메달
        elif row['득점'] == max_goals - 1:
            medal_color = 'silver'  # 은메달
        elif row['득점'] == max_goals - 2:
            medal_color = 'bronze'  # 동메달
        else:
            medal_color = ''  # 메달 없음

        st.markdown(scorer_card(row['이름'], row['소속'], row['득점'], medal_color), unsafe_allow_html=True)

# 반별 통계 탭
elif option == "반별 통계":
    st.subheader("📊 반별 승/무/패 통계")

    # 승률 계산: 승 / (승 + 무 + 패) 후 백분율로 변환
    class_stats_df['승률'] = (class_stats_df['승'] / (class_stats_df['승'] + class_stats_df['무'] + class_stats_df['패'])) * 100

    # 득실 계산: 득점 - 실점
    class_stats_df['득실'] = class_stats_df['득점'] - class_stats_df['실점']

    # 반별로 성적을 보기 좋게 정렬
    class_stats_df = class_stats_df.sort_values(by='득점', ascending=False)  # 득점 기준으로 정렬

    # 반별 통계 출력 (색상 변경 없이)
    st.dataframe(class_stats_df)
