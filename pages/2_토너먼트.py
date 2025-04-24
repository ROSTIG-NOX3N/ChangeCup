import pandas as pd

# CSV 파일 경로
file_path = 'Book(Class_Stat).csv'  # 실제 경로에 맞게 수정 필요

# CSV 파일 읽기
df = pd.read_csv(file_path)

# 승점 계산
df['승점'] = df['승'] * 3 + df['무']  # 승점 = 승 * 3 + 무 * 1

# 골득실차 계산
df['골득실차'] = df['득점'] - df['실점']

# 다득점 계산
# 이미 '득점' 컬럼이 있기 때문에 따로 다득점 기준으로 정렬이 가능합니다.

# 각 조별 1위 추출
grouped = df.groupby('조')

# 각 조에서 승점, 골득실차, 다득점, 최소 실점 기준으로 1위 추출
def get_group_winner(group):
    # 순위를 매기기 위한 기준으로 정렬
    group_sorted = group.sort_values(by=['승점', '골득실차', '득점', '실점'], ascending=[False, False, False, True])
    return group_sorted.iloc[0]  # 1위는 정렬된 첫 번째 행

# 각 조별 1위 추출
winners = grouped.apply(get_group_winner)

# 결과 출력
print(winners[['학반', '승점', '골득실차', '득점', '실점', '조']])
