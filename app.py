import streamlit as st
import pandas as pd

# 데이터 불러오기
results_df = pd.read_csv('Book(Result).csv')
scorers_df = pd.read_csv('Book(Scorer).csv')
class_stats_df = pd.read_csv('Book(Class_Stat).csv')
video_links_df = pd.read_csv('video_links.csv', sep="\t")

# 컬럼 공백 제거
video_links_df.columns = video_links_df.columns.str.strip()
video_links_df['경기번호'] = video_links_df['경기번호'].astype(int)
video_links_df['영상링크'] = video_links_df['영상링크'].astype(str).str.strip()

# 페이지 제목
st.title("⚽ 2025 아침체인지컵 ")

# 메뉴
option = st.sidebar.selectbox(
    'Menu',
    ("메인 메뉴", "경기 결과", "득점자", "반별 통계", "경기 영상")
)

# 득점자 정렬
sorted_scorers = scorers_df.sort_values(by='득점', ascending=False)

# CSS 포함된 카드 함수
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

# 영상링크 불러오기
video_links_df = pd.read_csv('video_links.csv')

# 컬럼명 공백 제거
video_links_df.columns = video_links_df.columns.str.strip().str.replace(" ", "")

# 확인용 출력
st.write("video_links_df 컬럼:", video_links_df.columns.tolist())

# 타입 변환
video_links_df['경기번호'] = video_links_df['경기번호'].astype(int)
video_links_df['영상링크'] = video_links_df['영상링크'].astype(str).str.strip()

# 메뉴별 화면 구성
if option == "메인 메뉴":
    st.subheader("메인 페이지")
    st.write("왼쪽 메뉴에서 항목을 선택하세요.")

elif option == "경기 결과":
    st.subheader("📋 경기 결과")
    st.dataframe(results_df)

elif option == "득점자":
    st.subheader("🥅 득점 순위")
    for idx, row in sorted_scorers.iterrows():
        medal = ''
        if row['득점'] == sorted_scorers.iloc[0]['득점']:
            medal = 'gold'
        elif row['득점'] == sorted_scorers.iloc[1]['득점']:
            medal = 'silver'
        elif row['득점'] == sorted_scorers.iloc[2]['득점']:
            medal = 'bronze'
        st.markdown(scorer_card(row['이름'], row['학반'], row['득점'], medal), unsafe_allow_html=True)

elif option == "반별 통계":
    st.subheader("📊 반별 통계")

    # 득실과 승률 계산
    class_stats_df['득실'] = class_stats_df['득점'] - class_stats_df['실점']
    total_games = class_stats_df['승'] + class_stats_df['무'] + class_stats_df['패']
    class_stats_df['승률(%)'] = (class_stats_df['승'] / total_games * 100).fillna(0).round(1)

    st.dataframe(class_stats_df)

elif option == "경기 영상":
    st.subheader("🎥 경기 영상")
    경기 = st.number_input("경기 번호를 입력하세요", min_value=1, max_value=video_links_df['경기번호'].max(), step=1)

    영상링크 = video_links_df.loc[video_links_df['경기번호'] == 경기, '영상링크'].values
    if 영상링크.size > 0 and 영상링크[0] != "영상없음":
        st.video(영상링크[0])
    else:
        st.warning("❗ 해당 경기의 영상이 없습니다.")
