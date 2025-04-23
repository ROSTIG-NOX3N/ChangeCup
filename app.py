import streamlit as st
from ui_display import display_groups

# 각 조별 팀 목록
groups = {
    "A": ["1-2", "1-1", "1-4"],
    "B": ["2-6", "2-7", "3-7"],
    "C": ["2-2", "1-7", "2-5"],
    "D": ["2-3", "3-2", "3-6"],
    "E": ["3-4", "1-6", "1-3"],
    "F": ["3-3", "3-5", "3-1"],
    "G": ["1-5", "2-1", "2-4"],
}

# 제목 및 페이지 설정
st.set_page_config(page_title="아침체인지컵 2025 - 조별 팀 구성", layout="wide")
st.title("2025 아침체인지컵 조별리그")

# 그룹 표시
display_groups(groups)
