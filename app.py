import streamlit as st

st.set_page_config(page_title="아침체인지컵 조별 구성", layout="wide")
st.title("⚽ 아침체인지컵 2025 - 조별 팀 구성")

# 각 조별 팀 목록
groups = {
    "A조": ["1-2", "1-1", "1-4"],
    "B조": ["2-6", "2-7", "3-7"],
    "C조": ["2-2", "1-7", "2-5"],
    "D조": ["2-3", "3-2", "3-6"],
    "E조": ["3-4", "1-6", "1-3"],
    "F조": ["3-3", "3-5", "3-1"],
    "G조": ["1-5", "2-1", "2-4"],
}

# 컬럼 7개 생성
cols = st.columns(7)

# 각 조별로 열에 표시
for idx, (group, teams) in enumerate(groups.items()):
    with cols[idx]:
        st.markdown(f"### {group}")
        for i, team in enumerate(teams, start=1):
            st.markdown(f"**{i}️⃣** {team}")
