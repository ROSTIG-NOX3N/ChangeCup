import streamlit as st
import pandas as pd

# 데이터 불러오기
results_df = pd.read_csv('Book(Result).csv')
scorers_df = pd.read_csv('Book(Scorer).csv')
class_stats_df = pd.read_csv('Book(Class_Stat).csv')
video_links_df = pd.read_csv('video_links.csv')

# 컬럼 정리 및 타입 변환
video_links_df.columns = video_links_df.columns.str.strip()
video_links_df['경기번호'] = video_links_df['경기번호'].astype(int)

# 페이지 제목
st.title("⚽ 2025 아침체인지컵 ")

option = st.sidebar.selectbox(
    'Menu',
    ("메인 메뉴", "경기 결과", "득점자", "반별 통계")
)

# 득점자 순위를 위한 정렬
sorted_scorers = scorers_df.sort_values(by='득점', ascending=False)
max_goals = sorted_scorers['득점'].max()

# CSS 카드 스타일 함수
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

# 🏆 메뉴별 기능 분기
if option == "경기 결과":
    st.subheader("📋 전체 경기 결과")
    st.dataframe(results_df)

    경기 = st.selectbox("🔍 영상 보기: 경기 선택", sorted(results_df['경기번호'].unique()))
    
    try:
        경기_int = int(경기)
        if 경기_int <= 3:
            st.warning("해당 경기는 영상이 제공되지 않습니다.")
        else:
            영상링크 = video_links_df.loc[video_links_df['경기번호'] == 경기_int, '영상링크'].values[0]
            if 영상링크 != "영상없음":
                st.video(영상링크)
            else:
                st.info("영상이 없습니다.")
    except Exception as e:
        st.error(f"오류 발생: {e}")

elif option == "득점자":
    st.subheader("⚽ 득점 순위")
    for i, row in sorted_scorers.iterrows():
        name = row['이름']
        team = row['반']
        goals = row['득점']
        if goals == max_goals:
            color = 'gold'
        elif goals == max_goals - 1:
            color = 'silver'
        elif goals == max_goals - 2:
            color = 'bronze'
        else:
            color = None

        if color:
            st.markdown(scorer_card(name, team, goals, color), unsafe_allow_html=True)

elif option == "반별 통계":
    st.subheader("📊 반별 경기 통계")
    st.dataframe(class_stats_df)

else:
    st.markdown("🏟️ **2025 아침체인지컵**에 오신 것을 환영합니다! 좌측 메뉴에서 항목을 선택해 주세요.")
