import streamlit as st

def display_groups(groups):
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

    # 최대 7개의 열을 나누기
    cols = st.columns(min(7, len(groups)))  # 그룹 수가 7개보다 많을 경우 7개로 고정

    # 각 조별로 표시
    for idx, (group, teams) in enumerate(groups.items()):
        col_idx = idx % 7  # 7개의 열로 순차적으로 배분
        with cols[col_idx]:
            # 각 그룹마다 박스 스타일 적용
            st.markdown(f"""
            <div style="background-color:{group_colors[group]}; padding:20px; border-radius:15px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); margin-bottom:15px; text-align:center;">
                <div style="font-size:32px; font-weight:bold; margin-bottom:10px; color:white;">{group}조</div>
                <div style="font-size:24px; color:black;">
                    {"<br>".join([f"<strong>{i}️⃣</strong> {team}" for i, team in enumerate(teams, start=1)])}
                </div>
            </div>
            """, unsafe_allow_html=True)
