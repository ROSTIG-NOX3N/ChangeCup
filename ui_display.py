import streamlit as st

def display_groups(groups):
    # CSS 스타일을 Streamlit에 적용 (폰트 크기, 구분선 등)
    st.markdown("""
        <style>
            .group-container {
                padding: 15px;
                border-radius: 8px;
                font-size: 24px;  /* 폰트 크기 설정 */
            }
            .group-title {
                font-size: 28px;  /* 그룹 제목 폰트 크기 설정 */
                font-weight: bold;
            }
            .divider {
                border: 1px solid #ccc;
                margin-top: 10px;
            }
        </style>
    """, unsafe_allow_html=True)
    
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
            # 각 그룹마다 고유 스타일 적용
            st.markdown(f"<div class='group-container' style='background-color:{group_colors[group]};'>", unsafe_allow_html=True)
            st.markdown(f"<div class='group-title'>{group}조</div>", unsafe_allow_html=True)
            for i, team in enumerate(teams, start=1):
                st.markdown(f"**{i}️⃣** {team}", unsafe_allow_html=True)
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)  # 구분선 추가
            st.markdown("</div>", unsafe_allow_html=True)
