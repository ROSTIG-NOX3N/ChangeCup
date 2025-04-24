import pandas as pd

# CSV 파일 경로
file_path = 'Book(Class_Stat).csv'  # 실제 경로에 맞게 수정 필요

# CSV 파일 읽기
df = pd.read_csv(file_path)

# 데이터 확인
print(df.head())  # 데이터의 처음 5행 출력
