import streamlit as st
from match_results import display_results
from goal_statistics import display_goal_statistics
from highlights import display_highlights

def display_groups(groups):
    # 각 조별로 열 생성
    cols = st.columns(7)

    # 각 조별로 표시, 배경색 추가
    group_colors = {
        "A": "#FFEBEE",  # 연한 빨강
        "B": "#FFEB3B",  # 노랑
        "C": "#4CAF50",  # 초록
        "D": "#2196F3",  # 파랑
        "E": "#9C27B0",  # 보라
        "F": "#FF5722",  # 주황
        "G": "#607D8B",  # 회색
    }

    # 각 조별로 표시
    for idx, (group, teams) in enumerate(groups.items()):
        with cols[idx]:
            st.markdown(f"<div style='background-color:{group_colors[group]}; padding:10px; border-radius:8px;'>", unsafe_allow_html=True)
            st.markdown(f"### {group}조")
            for i, team in enumerate(teams, start=1):
                st.markdown(f"**{i}️⃣** {team}")
            st.markdown("</div>", unsafe_allow_html=True)

def display_dashboard(groups):
    st.title("⚽ 아침체인지컵 2025 - 대회 대시보드")
    st.header("조별 팀 구성")
    display_groups(groups)
    display_results()
    display_goal_statistics()
    display_highlights()
