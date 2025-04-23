import streamlit as st

def display_groups(groups):
    # 최대 7개의 열을 나누기
    cols = st.columns(min(7, len(groups)))  # 그룹 수가 7개보다 많을 경우 7개로 고정

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
        col_idx = idx % 7  # 7개의 열로 순차적으로 배분
        with cols[col_idx]:
            st.markdown(f"<div style='background-color:{group_colors[group]}; padding:15px; border-radius:8px; font-size:20px;'>", unsafe_allow_html=True)
            st.markdown(f"### {group}조")
            for i, team in enumerate(teams, start=1):
                st.markdown(f"**{i}️⃣** {team}", unsafe_allow_html=True)
            st.markdown("<hr style='border:1px solid #ccc;'>", unsafe_allow_html=True)  # 구분선 추가
            st.markdown("</div>", unsafe_allow_html=True)
