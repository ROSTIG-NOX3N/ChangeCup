import pandas as pd

# CSV 파일 읽기
df = pd.read_csv('Book(Class_Stat).csv')

# 데이터프레임의 컬럼명과 일부 내용 출력
st.write(df.columns)
st.write(df.head())  # 데이터의 처음 몇 줄을 출력하여 확인
