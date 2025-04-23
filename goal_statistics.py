import streamlit as st
import matplotlib.pyplot as plt

def display_goal_statistics():
    st.subheader("골 수 통계")

    # 예시 통계
    teams = ["1-2", "1-1", "1-4", "2-6", "2-7", "3-7", "2-2", "1-7", "2-5", "2-3"]
    goals = [3, 2, 1, 4, 5, 6, 2, 1, 3, 2]

    # 바 그래프 생성
    plt.bar(teams, goals, color="skyblue")
    plt.xlabel("팀")
    plt.ylabel("골 수")
    plt.title("골 수 통계")
    st.pyplot(plt)
