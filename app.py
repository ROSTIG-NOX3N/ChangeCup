import streamlit as st
import pandas as pd

# 데이터 불러오기
results_df = pd.read_csv('Book(Result).csv')
scorers_df = pd.read_csv('Book(Scorer).csv')
class_stats_df = pd.read_csv('Book(Class_Stat).csv')

# 페이지 제목
st.title("⚽ 2025 아침체인지컵 ")

option = st.sidebar.selectbox(
    'Menu',
    ("메인 메뉴", "경기 결과", "득점자", "반별 통계"))

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

# '메인 메뉴'일 때 최근 경기 및 주변 경기 출력
if option == "메인 메뉴":
    st.subheader("📋 최근 경기 및 그 주변 경기 결과")

    # 경기 번호 기준으로 정렬 (최신 경기부터 표시)
    try:
        # '경기' 열을 숫자형으로 변환하여 처리
        results_df['경기'] = pd.to_numeric(results_df['경기'], errors='coerce')
    except Exception as e:
        st.error(f"데이터 변환 중 오류가 발생했습니다: {e}")

    # '경기' 열에 NaN 값이 있을 경우 처리
    results_df = results_df.dropna(subset=['경기'])

    # 경기 번호 기준으로 정렬
    results_df = results_df.sort_values(by='경기', ascending=False)

    # 가장 최근 경기 번호 찾기
    latest_match_number = results_df.iloc[0]['경기']

    # 최근 경기 번호 기준으로 n-2, n-1, n, n+1, n+2, n+3 경기를 가져오기
    matches_to_display = results_df[
        (results_df['경기'] >= latest_match_number - 2) &
        (results_df['경기'] <= latest_match_number + 3)
    ]

    # 한 경기씩 출력
    for idx, match in matches_to_display.iterrows():
        경기번호 = match['경기']
        팀1 = match['1팀']
        팀2 = match['2팀']
        팀1득점 = match['1팀득점']
        팀2득점 = match['2팀득점']
        결과 = match['결과']
        조 = match['조']
        경기일자 = match['경기일자']

        st.markdown(f"### ⚽ {경기번호} | {조}조")
        if str(팀1득점).isdigit() and str(팀2득점).isdigit():
            st.markdown(f"**{팀1}** {팀1득점} : {팀2득점} **{팀2}**")
            st.markdown(f"📌 결과: {결과}")
        else:
            st.markdown(f"**{팀1}** vs **{팀2}**")
            st.markdown("⏳ 경기 예정")

        st.markdown(f"📅 경기일자: {경기일자}")
        st.markdown("---")

# '경기 결과'일 때
elif option == "경기 결과":
    st.subheader("📋 전체 경기 결과")
    st.dataframe(results_df)

# '득점자'일 때
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

# '반별 통계'일 때
elif option == "반별 통계":
    st.subheader("📊 반별 승/무/패 통계")
    st.dataframe(class_stats_df)
