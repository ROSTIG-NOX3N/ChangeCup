import streamlit as st
import pandas as pd
from video_links import video_links

# 데이터 불러오기
results_df = pd.read_csv('Book(Result).csv')
scorers_df = pd.read_csv('Book(Scorer).csv')
class_stats_df = pd.read_csv('Book(Class_Stat).csv')

# 페이지 제목
st.title("⚽ 2025 아침체인지컵 ")
st.subheader("본선 진출 현황")

#본선 진출 현황
st.markdown("### A조 : 미정 ")
st.markdown("### B조 : 미정 ")
st.markdown("# C조 : 2학년 2반 ")
st.markdown("### D조 : 미정 ")
st.markdown("### E조 : 미정 ")
st.markdown("### F조 : 미정 ")
st.markdown("### G조 : 미정 ")

# 사이드 메뉴
option = st.sidebar.selectbox(
    'Menu',
    ("메인 메뉴", "경기 일정", "득점자", "반별 통계")
)

# 메인 메뉴 탭 기능
if option == "메인 메뉴":
    # 탭 3개: 공지사항, 경기영상, 조별결과
    tab1, tab2, tab3 = st.tabs(["공지사항", "경기영상", "조별결과"])

    with tab1:
        st.subheader("공지사항")
        st.write("여기에 공지사항을 입력하세요.")

    with tab2:
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

    with tab3:
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

        # 스타일 함수 정의 (C조 2학년 2반만 초록색, 나머지는 기본 배경)
        def colorize(row):
            # 'C조'의 '2학년 2반'만 초록색 배경
            if row['조'] == 'C' and row['학반'] == '2학년 2반':
                return ['background-color: green; color: white'] * len(row)
            else:
                return [''] * len(row)  # 기본 배경

        # 스타일 적용
        styled_df = selected_group.style.apply(colorize, axis=1)

        # 선택된 조별 성적 출력
        st.dataframe(styled_df)

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

    # 스타일 함수 정의 (C조 2학년 2반만 초록색, 나머지는 기본 배경)
    def colorize(row):
        if row['조'] == 'C' and row['학반'] == '2학년 2반':
            return ['background-color: green; color: white'] * len(row)
        else:
            return [''] * len(row)  # 기본 배경

    # 스타일 적용
    styled_df = class_stats_df.style.apply(colorize, axis=1)

    # 반별 성적 출력
    st.dataframe(styled_df)
