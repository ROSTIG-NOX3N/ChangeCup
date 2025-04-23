import pandas as pd

def load_team_data(file_path):
    # CSV 파일을 읽어서 DataFrame으로 변환
    df = pd.read_csv(file_path, header=None, names=['Group', 'Team'])
    
    # 각 조별로 팀 정보를 그룹화하여 딕셔너리로 반환
    groups = df.groupby('Group')['Team'].apply(list).to_dict()
    
    return groups
