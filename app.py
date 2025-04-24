import streamlit as st
import pandas as pd

# 데이터 불러오기
results_df = pd.read_csv('Book(Result).csv')
scorers_df = pd.read_csv('Book(Scorer).csv')
class_stats_df = pd.read_csv('Book(Class_Stat).csv')
video_links_df = pd.read_csv('video_links.csv')

# 페이지 제목
st.title("⚽ 2025 아침체인지컵 ")

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

if option == "경기 결과":
    st.subheader("📋 전체 경기 결과")
    st.dataframe(results_df)

elif option == "메인 메뉴":
    st.subheader("⚽ 아침체인지컵 메인 메뉴")
    
    # 경기 번호 기준으로 정렬 (최신 경기부터 표시)
    results_df = results_df.sort_values(by='경기', ascending=False)
    
    # 경기 번호 4~10에 대한 유튜브 영상 링크 가져오기
    for idx, match in results_df.iterrows():
        경기 = match['경기']  # 여기에서 '경기번호' 대신 '경기' 사용
        
        # 영상 링크 가져오기
        영상링크 = video_links_df.loc[video_links_df['경기번호'] == 경기, '영상링크'].values  # '경기번호'로 수정
        
        if len(영상링크) > 0 and 영상링크[0] != "영상없음":
            영상상태 = f"업로드 완료: [영상 보기]({영상링크[0]})"
        else:
            영상상태 = "업로드 예정"
        
        st.markdown(f"### ⚽ 경기 {경기}")
        st.markdown(f"📅 경기일자: {match['경기일자']}")
        st.markdown(f"📝 영상 상태: {영상상태}")
        st.markdown("---")

elif option == "득점자":
    st.subheader("다득점자")
    top_scorers = sorted_scorers[sorted_scorers['득점'] >= 2].head(10)

    for idx, row in top_scorers.iterrows():
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

elif option == "반별 통계":
    st.subheader("📊 반별 승/무/패 통계")

    # 승률 계산: 승 / (승 + 무 + 패)
    class_stats_df['승률'] = class_stats_df['승'] / (class_stats_df['승'] + class_stats_df['무'] + class_stats_df['패'])

    # 득실 계산: 득점 - 실점
    class_stats_df['득실'] = class_stats_df['득점'] - class_stats_df['실점']

    # 반별로 성적을 보기 좋게 정렬
    class_stats_df = class_stats_df.sort_values(by='득점', ascending=False)  # 득점 기준으로 정렬

    # 반별 통계 출력 (색상 변경 없이)
    st.dataframe(class_stats_df)
