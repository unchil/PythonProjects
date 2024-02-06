# -*- coding: utf8 -*-

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib


def main():

    st.title("Grid Chart Test")

    matplotlib.rc('font', family='AppleGothic')

    fig = plt.figure()

    plt.subplot(1,2,1) #1개의 figure에 2개의 차트 그리기 : 1행 2열 중 첫 번째 차트로 지정

    plt.plot([1,2,3,4], [1,2,3,4])

    plt.xlabel('X 축')  #라벨 한글 출력을 위해 유니코드 스트링으로 지정

    plt.ylabel('Y 축', labelpad=16, rotation= 0 )

    plt.title("Chart Test")

    plt.grid(False)

    plt.subplot(1,2,2)  #1개의 figure에 2개의 차트 그리기 : 1행 2열 중 두 번째 차트로 지정

    plt.plot([1,2,3,4], [2,4,6,8])

    plt.xlabel('X 축')

    plt.ylabel('Y 축', labelpad=10, rotation= 0 )

    plt.title('Grid Chart Test')

    plt.grid(True) #차트에 그리드 표시하기

    plt.show()     #차트 띄우기

    st.pyplot(fig)

if __name__ == "__main__":
    main()
    
