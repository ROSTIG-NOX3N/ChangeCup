import streamlit as st
import pandas as pd

match_data = pd.read_csv("Book(Result).csv")
st.set_page_config(page_title="경기 결과", layout="wide")
st.title("🏆 경기 결과 및 득점자")

with open("match_results.json", "r", encoding="utf-8") as f:
    match_data = json.load(f)

for match in match_data:
    st.markdown(f"""
    <div style="border:2px solid #001f3d; border-radius:10px; padding:16px; margin-bottom:20px;">
        <h4>⚽ {match['경기번호']}경기: {match['팀1']} vs {match['팀2']}</h4>
        <p><strong>결과:</strong> {match['결과']}</p>
        <p><strong>득점자:</strong></p>
        <ul>
            <li><strong>{match['팀1']}</strong>: {'없음' if not match['득점자'][match['팀1']] else ', '.join(match['득점자'][match['팀1']])}</li>
            <li><strong>{match['팀2']}</strong>: {'없음' if not match['득점자'][match['팀2']] else ', '.join(match['득점자'][match['팀2']])}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
