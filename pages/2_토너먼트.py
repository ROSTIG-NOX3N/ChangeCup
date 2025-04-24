import pandas as pd

# CSV 파일 읽기
df = pd.read_csv('Book(Class_Stat).csv')

# 컬럼명에 공백이 있는지 확인 후 제거
df.columns = df.columns.str.strip()

# 컬럼명 확인
print(df.columns)
