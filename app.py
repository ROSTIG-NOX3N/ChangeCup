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
        # 경기 번호 4부터 10까지 선택할 수 있는 Selectbox
        경기선택 = st.selectbox(
            "경기를 선택하세요",
            options=[f"{경기}경기 영상보기" for 경기 in range(4, 11)]  # 4경기부터 10경기까지 선택 옵션 생성
        )

        # 선택한 경기 번호 (문자열에서 숫자만 추출)
        경기번호 = int(경기선택.split()[0].replace("경기", ""))

        # 선택된 경기 영상 제목 출력
        st.title(f"{경기번호}경기 영상")
        
        # 영상 링크 찾기
        영상링크 = video_links.get(경기번호, "영상없음")
        
        # 영상이 존재하면 표시
        if 영상링크 != "영상없음":
            st.video(영상링크)
        else:
            st.write("이 경기는 영상이 아직 업로드되지 않았습니다.")

    # 조별결과 탭
    elif tab_option == "조별결과":
        st.subheader("📊 조별 승/무/패 통계")
    
        # 조 선택을 위한 selectbox (오름차순으로 정렬)
        조선택 = st.selectbox(
            "조를 선택하세요",
            options=sorted(class_stats_df['조'].unique())  # 조 이름을 오름차순으로 정렬
        )
    
        # 선택된 조의 데이터 필터링
        selected_group = class_stats_df[class_stats_df['조'] == 조선택]
    
        # 승률 계산: 승 / (승 + 무 + 패) 후 백분율로 변환
        selected_group['승률'] = (selected_group['승'] / (selected_group['승'] + selected_group['무'] + selected_group['패'])) * 100
    
        # 득실 계산: 득점 - 실점
        selected_group['득실'] = selected_group['득점'] - selected_group['실점']
    
        # 선택된 조별 성적 출력
        st.dataframe(selected_group)

        # C조 확정 팀을 제외하고 나머지 조별 본선 진출팀 계산
        if 조선택 != "C":
            # C조는 이미 확정된 팀 (2학년 2반) 제외
            exclude_groups = ['선생님팀', 'C조']  # 선생님팀과 C조를 제외
        else:
            exclude_groups = ['선생님팀', 'C조']

        filtered_class_stats_df = class_stats_df[~class_stats_df['조'].isin(exclude_groups)]

        # 승률과 골득실을 기반으로 확률 계산
        def calculate_probability(row):
            # 승률 계산: 승/전체 경기수
            total_games = row['승'] + row['무'] + row['패']
            win_rate = row['승'] / total_games if total_games > 0 else 0

            # 골득실 계산: 득점 - 실점
            goal_difference = row['득점'] - row['실점']

            # 승률과 골득실을 결합하여 확률 계산
            # 기본 확률 = 승률의 50%, 골득실의 50%
            probability = (win_rate * 0.5) + ((goal_difference / total_games) * 0.5 if total_games > 0 else 0)
            
            # 확률을 0~1로 정규화
            probability = np.clip(probability, 0, 1)
            return probability

        # 각 팀의 확률을 계산하여 새로운 컬럼에 추가
        filtered_class_stats_df['확률'] = filtered_class_stats_df.apply(calculate_probability, axis=1)

        # 결과 출력
        st.write("각 조별 본선 진출 가능성 계산 결과:")
        st.write(filtered_class_stats_df[['학반', '승', '무', '패', '득점', '실점', '조', '확률']])

        # 각 조에서 한 팀만 본선 진출 가능 표시 (C조는 이미 확정된 팀 제외)
        if 조선택 != "C":
            st.write(f"**{조선택} 조에서 본선 진출 가능성이 높은 팀은**:")
            best_team = filtered_class_stats_df.loc[filtered_class_stats_df['확률'].idxmax()]
            st.write(f"{best_team['학반']} (확률: {best_team['확률']*100:.2f}%)")

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
