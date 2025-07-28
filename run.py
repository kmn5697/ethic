import streamlit as st

# 페이지 설정: 오타 'latout' → 'layout', 제목 문자열 따옴표 수정
st.set_page_config(layout='wide', page_title='EthicApp')

# 앱의 타이틀 텍스트
st.title('Ethic is good for us')

# 앱의 사이드바 메뉴
# (사이드바 버튼 추가): "학생데이터 가져오기" 버튼을 추가하고, 클릭했을 때, CONTENT영역에 저장된 학생 데이터(data.txt)를 불러와서 제시합니다.
st.sidebar.subheader('Menu...')
st.sidebar.markdown("""
- 홈  
- 윤리 영상 보기  
- 딥페이크 윤리 교육  
""")

# 사이드바 버튼 추가
show_data = st.sidebar.button('📂 학생데이터 가져오기(더블클릭)')

# 버튼 클릭 시 왼쪽 컬럼에 데이터 표시 (left_col은 이미 선언되어 있다고 가정)
if show_data:
    with left_col:
        st.subheader('🗂 저장된 학생 의견 모음')
        try:
            with open('data.txt', 'r', encoding='utf-8') as f:
                data = f.read()
            st.text_area('학생들이 작성한 내용', data, height=300)
        except FileNotFoundError:
            st.warning('아직 저장된 데이터가 없어!')


# 내용 제시 영역 및 화면 분할과 컴포넌트 배치
# 컬럼을 2개로 나누되, 영역의 크기를 (4,1) 튜플 크기로 배치
left_col, right_col = st.columns([4, 1])

# 왼쪽 넓은 영역: 유튜브 영상 삽입 및 의견 기록 기능 추가
with left_col:
    st.header('📺 AI 윤리 교육 영상')
    st.video('https://www.youtube.com/watch?v=XyEOEBsa8I4')  # 예시 URL로 대체

    # 학생의 생각 입력
    st.subheader('✍️ 나의 생각 기록')
    user_input = st.text_area('이 영상에 대한 너의 생각을 자유롭게 적어보세요.', height=150)

    # 제출 버튼 클릭 시 텍스트 파일에 저장
    if st.button('제출하기'):
        if user_input.strip() != "":
            try:
                with open('data.txt', 'a', encoding='utf-8') as f:
                    f.write(user_input + '\n' + '-'*50 + '\n')
                st.success('생각이 성공적으로 저장되었어!')
            except Exception as e:
                st.error(f'저장 중 오류가 발생했어: {e}')
        else:
            st.warning('내용을 입력한 후 제출해줘!')

# 오른쪽 좁은 영역: 도움말 제공
with right_col:
    st.header('💡 Tips...')
    st.markdown("""
- 이 영상은 인공지능 윤리의 핵심 개념을 소개합니다.
- 딥페이크의 위험성과 정보 판별 능력의 중요성에 주목해 보세요.
- 사이드바 메뉴에서 다른 교육 콘텐츠도 확인할 수 있습니다.
""")
