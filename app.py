import streamlit as st
import pandas as pd

# 데이터 불러오기
results_df = pd.read_csv('Book(Result).csv')
scorers_df = pd.read_csv('Book(Scorer).csv')
class_stats_df = pd.read_csv('Book(Class_Stat).csv')
video_links_df = pd.read_csv('video_links.csv')

# 페이지 제목
st.title("⚽ 2025 아침체인지컵 ")

# 사이드바 메뉴
option = st.sidebar.selectbox(
    'Menu',
    ("메인 메뉴", "경기 결과", "득점자", "반별 통계")
)

# 득점자 순위를 위한 정렬
sorted_scorers = scorers_df.sort_values(by='득점', ascending=False)

# 최댓값 득점자 수
max_goals = sorted_scorers['득점'].max()

# CSS 영역
def scorer_card(name, team, goals, medal_color):
    medal_html = ""
    if medal_color == 'gold':
        medal_html = "<span style='color: gold;'>🥇</span>"
    elif medal_color == 'silver':
        medal_html = "<span style='color: silver;'>🥈</span>"
    elif medal_color == 'bronze':
        medal_html = "<span style='color: #cd7f32;'>🥉</span>"

    card_html = f"""
    <style>
    .scorer-card {{
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 10px;
        background-color: #f5f5f5;
        color: #000;
        transition: all 0.3s ease;
    }}

    @media (prefers-color-scheme: dark) {{
        .scorer-card {{
            background-color: #222;
            color: #fff;
            border: 1px solid #555;
        }}
    }}
    </style>

    <div class="scorer-card">
        <h4 style="margin: 0;">{medal_html} {name} ({team})</h4>
        <p style="margin: 0;">⚽ 득점 수: <strong>{goals}골</strong></p>
    </div>
    """
    return card_html

# 득점자 출력
if option == "득점자":
    st.subheader("⚽ 득점자 순위")
    
    # 첫 번째, 두 번째, 세 번째 득점자
    for idx, row in sorted_scorers.iterrows():
        name = row['이름']
        team = row['팀']
        goals = row['득점']

        # 메달 색상 설정
        if goals == max_goals:
            medal_color = 'gold'
        elif goals == max_goals - 1:
            medal_color = 'silver'
        elif goals == max_goals - 2:
            medal_color = 'bronze'
        else:
            medal_color = 'none'

        # 득점자 카드 HTML 표시
        card_html = scorer_card(name, team, goals, medal_color)
        st.markdown(card_html, unsafe_allow_html=True)

# 경기 결과
elif option == "경기 결과":
    st.subheader("📋 전체 경기 결과")
    st.dataframe(results_df)

# 반별 통계
elif option == "반별 통계":
    st.subheader("📊 반별 승/무/패 통계")

    # 승률 계산: 승 / (승 + 무 + 패) 후 백분율로 변환
    class_stats_df['승률'] = (class_stats_df['승'] / (class_stats_df['승'] + class_stats_df['무'] + class_stats_df['패'])) * 100

    # 득실 계산: 득점 - 실점
    class_stats_df['득실'] = class_stats_df['득점'] - class_stats_df['실점']

    # 반별로 성적을 보기 좋게 정렬
    class_stats_df = class_stats_df.sort_values(by='득점', ascending=False)  # 득점 기준으로 정렬

    # 반별 통계 출력
    st.dataframe(class_stats_df)
