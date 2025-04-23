import streamlit as st
from team_data import load_team_data
from ui_display import display_dashboard

# 페이지 설정
st.set_page_config(page_title="아침체인지컵 2025 - 대시보드", layout="wide")

# 팀 데이터 파일 경로
file_path = 'group_data.csv'

# 팀 데이터 불러오기
groups = load_team_data(file_path)

# 대시보드 표시
display_dashboard(groups)
