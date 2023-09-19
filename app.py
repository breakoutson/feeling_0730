import json
import re
from bs4 import BeautifulSoup
import urllib.request as req
import streamlit as st
import time
import requests

import urllib.parse as par


def get_sentiment(text):
    client_id = "qjobv0kx51"  # client id를 꼭 넣어주세요!
    client_secret = "PGq7xd0BggAAdom7sC68FGTzmd7lRnoxIj2F8hh6"  # client seceret을 꼭 넣어주세요!
    url = "https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret,
        "Content-Type": "application/json"
    }
    data = {
        "content": text[:min(len(text), 1000)]
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    result = json.loads(response.text)

    sentiment = result["document"]["sentiment"]
    confidence = result["document"]["confidence"][sentiment]

    sentiment_ko = {
        'positive': '긍정',
        'negative': '부정',
        'neutral': '중립'
    }[sentiment]

    return {'result': sentiment_ko, 'score': confidence}


########################################################

st.title('감성분석기')
user_input = st.text_input('본문 또는 URL 입력')

if 'blog.naver.com' in user_input:
    url = user_input

    if not 'm.blog.naver.com' in url:
        url = url.replace('blog.naver.com', 'm.blog.naver.com')

    code = req.urlopen(url)
    soup = BeautifulSoup(code, 'html.parser')

    title = soup.select_one('#SE-b28e8031-860b-4891-9f6b-228ccf1c844f')
    str = soup.select_one('div.se-main-container')
    str_content = str.text
    # str = str.text.replace('\n', '').strip()
else:
    str_content = user_input


if str_content != '':
    # 블로그 에디터 창에서 안보이지만 따라오는 단어들
    remove_list = ['\u200b', '대표사진 삭제', '사진 설명을 입력하세요.', '출처 입력', '사진 삭제', '이미지 썸네일 삭제', '동영상 정보 상세 보기',
                   '동영상 설명을 입력하세요.', 'blog.naver.com']
    print(str_content)
    # 따라온 단어들 삭제
    for i in remove_list:
        str_content = str_content.replace(i, '')

    str_content = str_content.replace('blog.naver.com', '')
    # 공백과 줄바꿈 삭제
    str_re = re.sub('\n| ', '', str_content)

    str_without_line = str_content.replace('\n', '').strip()  # 줄바꿈만 정리한 것

    # # 알파벳, 숫자, 공백문자가 아닌 모든 문자 (기호 제거)
    # str_content = re.sub(r'[^\w\s]', '', str_content)

    # 이모지와 기호 제거
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    str_without_line_emoji = emoji_pattern.sub(r'', str_without_line)
    str_conent_without_line_emoji = emoji_pattern.sub(r'', str_content)
    str_result = re.sub('\n+| +', ' ', str_conent_without_line_emoji)





# 감성분석 전체분석
if st.button("분석 시작"):
    with st.spinner('Wait for it...'):
        time.sleep(1)
    sentiment_result = get_sentiment(str_result)
    st.progress(100)
    
    st.write(str_result)
    
    if sentiment_result["result"] == '긍정':
        st.subheader(f'{sentiment_result["score"]:.2f}%의 확률로 {sentiment_result["result"]}적인 글입니다')
        st.balloons()
    elif sentiment_result["result"] == '부정':
        st.subheader(f'{sentiment_result["score"]:.2f}%의 확률로 {sentiment_result["result"]}적인 글입니다')
        st.snow()
    
    else :
        st.subheader(f'이 글은 {sentiment_result["result"]}적인 글입니다')
        pass
