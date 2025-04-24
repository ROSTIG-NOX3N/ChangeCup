import pandas as pd
import streamlit as st

# CSV 파일 읽기
df = pd.read_csv('Book(Class_Stat).csv')

# 데이터 확인
st.write(df)

# 승점 계산 함수
def calculate_points(row):
    points = 0
    if row['승'] == 1:
        points += 3
    elif row['무'] == 1:
        points += 1
    return points

# 각 학반의 승점을 계산하고 결과를 저장
df['승점'] = df.apply(calculate_points, axis=1)

# 골득실 차이 계산 함수
def calculate_goal_difference(row):
    return row['득점'] - row['실점']

# 골득실 차이를 추가
df['골득실'] = df.apply(calculate_goal_difference, axis=1)

# 다득점 계산 함수
def calculate_total_goals(row):
    return row['득점']

# 각 팀의 다득점 계산
df['다득점'] = df.apply(calculate_total_goals, axis=1)

# 최소실점 계산 함수
def calculate_minimum_conceded(row):
    return row['실점']

# 각 팀의 최소실점 계산
df['최소실점'] = df.apply(calculate_minimum_conceded, axis=1)

# 승부차기 값은 데이터에 없다면 0으로 초기화
df['승부차기'] = 0

# 각 조별로 승점, 골득실, 다득점, 최소실점, 승부차기 순으로 정렬
grouped = df.groupby('조').apply(
    lambda x: x.sort_values(
        by=['승점', '골득실', '다득점', '최소실점', '승부차기'], 
        ascending=[False, False, False, True, False]
    )
)

# 각 조별 1위팀 추출
top_teams = {}
for group, group_data in grouped.groupby('조'):
    top_teams[group] = group_data.head(1)  # 상위 1팀

# 조별 1위팀 출력
st.subheader("조별 1위팀")
for group, team in top_teams.items():
    st.write(f"{group}: {team['학반'].values[0]}")

# 1위팀으로 8강 대진표 만들기
quarterfinals = list(top_teams['A']['학반']) + list(top_teams['B']['학반']) + list(top_teams['C']['학반']) + list(top_teams['D']['학반'])

st.subheader("8강 대진표")
for i in range(0, len(quarterfinals), 2):
    st.write(f"경기 {i//2 + 1}: {quarterfinals[i]} vs {quarterfinals[i + 1]}")
