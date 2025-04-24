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

def sort_key(class_name):
    grade, ban = class_name.split('학년 ')
    grade = int(grade)
    ban = int(ban.replace('반', ''))
    return grade * 10 + ban

class_stats_df["sort_order"] = class_stats_df["학반"].apply(sort_key)

# 사이드 메뉴
option = st.sidebar.selectbox(
    'Menu',
    ("메인 메뉴", "경기 일정", "득점자", "반별 통계")
)

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

if option == "메인 메뉴":
    # 탭 4개: 공지사항, 경기영상, 조별결과, 전체결과
    tab1, tab2, tab3, tab4 = st.tabs(["공지사항", "경기영상", "조별결과", "전체 결과"])

    with tab1:
        st.markdown("""
            <style>
            .group-box {
                border-radius: 12px;
                padding: 15px;
                margin-bottom: 10px;
                background-color: #f0f2f6;
                border: 1px solid #ccc;
            }
    
            .group-box h4 {
                margin: 0;
            }
    
            .qualified {
                color: white;
                background-color: #28a745;
                padding: 4px 8px;
                border-radius: 6px;
                font-size: 0.9em;
            }
    
            .pending {
                color: #555;
                background-color: #eaeaea;
                padding: 4px 8px;
                border-radius: 6px;
                font-size: 0.9em;
            }
    
            @media (prefers-color-scheme: dark) {
                .group-box {
                    background-color: #2a2a2a;
                    border: 1px solid #444;
                }
    
                .pending {
                    background-color: #444;
                    color: #ccc;
                }
            }
            </style>
    
            <div class='group-box'><h4>A조 : <span class='pending'>미정</span></h4></div>
            <div class='group-box'><h4>B조 : <span class='pending'>미정</span></h4></div>
            <div class='group-box'><h4>C조 : <span class='qualified'>2학년 2반</span></h4></div>
            <div style="margin-bottom: 15px;">
                <video controls width="100%">
                    <source src="https://youtu.be/ZPLiaRIAfhg" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>
            <div class='group-box'><h4>D조 : <span class='pending'>미정</span></h4></div>
            <div class='group-box'><h4>E조 : <span class='pending'>미정</span></h4></div>
            <div class='group-box'><h4>F조 : <span class='pending'>미정</span></h4></div>
            <div class='group-box'><h4>G조 : <span class='pending'>미정</span></h4></div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("### 🎥 경기 영상")
        for title, link in video_links.items():
            st.markdown(f"- [{title}]({link})")

    with tab3:
        st.markdown("### 🏆 조별 결과")
    
        class_stats_df["승점"] = class_stats_df["승"] * 3 + class_stats_df["무"]
        class_stats_df["골득실"] = class_stats_df["득점"] - class_stats_df["실점"]
    
        grouped = class_stats_df.copy()
    
        def highlight_qualified(row):
            if row["학반"] == "2학년 2반":
                return ['background-color: lightgreen'] * len(row)
            return [''] * len(row)
    
        for group, group_data in grouped.groupby("조"):
            st.markdown(f"#### 조 {group}")
            sorted_group = group_data.sort_values(
                by=["승점", "골득실", "득점", "실점"],
                ascending=[False, False, False, True]
            )
            st.dataframe(
                sorted_group[["학반", "승", "무", "패", "득점", "실점", "승점", "골득실"]]
                .style.apply(highlight_qualified, axis=1)
            )

    with tab4:
        st.markdown("### 📊 전체 결과")
    
        class_stats_df_display = class_stats_df.copy()
        class_stats_df_display["승점"] = class_stats_df_display["승"] * 3 + class_stats_df_display["무"]
        class_stats_df_display["골득실"] = class_stats_df_display["득점"] - class_stats_df_display["실점"]
    
        sorted_all = class_stats_df_display.sort_values(by="sort_order")
    
        def highlight_qualified(row):
            if row["학반"] == "2학년 2반":
                return ['background-color: green'] * len(row)
            return [''] * len(row)
    
        st.dataframe(
            sorted_all[["학반", "승", "무", "패", "득점", "실점", "승점", "골득실"]]
            .style.apply(highlight_qualified, axis=1)
        )

# 경기 결과 탭
elif option == "경기 일정":
    st.subheader("📋 전체 경기 일정")
    st.dataframe(results_df)

# 득점자 탭
elif option == "득점자":
    st.subheader("다득점자")

    # 득점자 목록을 득점수로 내림차순 정렬
    sorted_scorers = scorers_df.sort_values(by='득점', ascending=False)
    max_goals = sorted_scorers['득점'].max()  # 최대 득점 계산

    # 득점자가 2골 이상인 경우만 카드 출력
    for idx, row in sorted_scorers.iterrows():
        if row['득점'] >= 2:  # 2골 이상인 경우만 출력
            # 메달 색상 설정
            if row['득점'] == max_goals:
                medal_color = 'gold'  # 금메달
            elif row['득점'] == max_goals - 1:
                medal_color = 'silver'  # 은메달
            elif row['득점'] == max_goals - 2:
                medal_color = 'bronze'  # 동메달
            else:
                medal_color = ''  # 메달 없음
    
            # 득점자 카드 출력
            st.markdown(scorer_card(row['이름'], row['소속'], row['득점'], medal_color), unsafe_allow_html=True)

# 반별 통계 탭
elif option == "반별 통계":
    st.markdown("### 📋 반별 경기 통계")

    # 학년/반 선택 위젯
    col1, col2 = st.columns(2)
    with col1:
        grade = st.selectbox("학년 선택", [1, 2, 3])
    with col2:
        classroom = st.selectbox("반 선택", [1, 2, 3, 4, 5, 6, 7])

    # 선택된 학반 문자열로 조합
    selected_class = f"{grade}학년 {classroom}반"

    # 해당 반의 데이터 필터링
    class_data = class_stats_df[class_stats_df["학반"] == selected_class]

    if not class_data.empty:
        st.markdown(f"#### 🔍 {selected_class} 통계")
        st.dataframe(class_data.reset_index(drop=True))

        # 통계 요약 출력
        wins = int(class_data['승'])
        draws = int(class_data['무'])
        losses = int(class_data['패'])
        goals = int(class_data['득점'])
        conceded = int(class_data['실점'])
        goal_diff = goals - conceded
        points = wins * 3 + draws

        st.markdown(f"""
        - ✅ 승리: {wins}승  
        - 🤝 무승부: {draws}무  
        - ❌ 패배: {losses}패  
        - ⚽ 득점: {goals}  
        - 🛡️ 실점: {conceded}  
        - 🧮 골득실: {goal_diff}  
        - 🏅 승점: {points}
        """)
    else:
        st.warning(f"{selected_class}에 대한 데이터가 없습니다.")


