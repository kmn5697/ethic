import streamlit as st
import re

# 페이지 설정
st.set_page_config(page_title="Home", layout="wide")

# 앱의 타이틀
st.title('Find real me')

# 사이드바 버튼
show_by_student = st.sidebar.button('📋 학생별 답변 조회')

# ---------------------- 메인 화면 분할 ----------------------
left_col, right_col = st.columns([4, 1])

# ---------------------- 오른쪽 좁은 영역 (Tips) ----------------------
with right_col:
    st.header('💡 Tips...')
    st.markdown("""
- 딥페이크 콘텐츠는 현실과 구분이 어려워 사회적 혼란을 일으킬 수 있어요.  
- 동의 없이 개인 얼굴이 합성될 경우, **초상권**과 **사생활 침해** 문제가 발생합니다.  
""")
    st.header('💡 Tips...')
    st.markdown("""
- 이 영상은 인공지능 윤리의 핵심 개념을 소개합니다.  
- 딥페이크의 위험성과 정보 판별 능력의 중요성에 주목해 보세요.  
""")

# ---------------------- 왼쪽 넓은 content 영역 ----------------------
with left_col:
    st.header('📸 첫번째 레슨. 진짜 미나쌤을 찾아라!')

    # 2x2 이미지 표시
    image_paths = ["딥페이크 합성_박명수.png", "딥페이크 합성_차은우.png", "자신의 얼굴 실제 사진.jpg", "딥페이크 합성_카리나.png"]  # 너 이미지 폴더에 맞게 수정해줘!
    row1 = st.columns(2)
    row2 = st.columns(2)

    for i in range(2):
        with row1[i]:
            st.image(image_paths[i], width=230)
    for i in range(2):
        with row2[i]:
            st.image(image_paths[i+2], width=230)

    st.markdown("""
딥페이크 기술은 AI 기반 영상 합성 기술로, 연예인·정치인·일반인의 얼굴을 허위 콘텐츠에 합성할 수 있습니다.  
이로 인해 사회적 신뢰 저하, 허위 정보 확산, **인격권 침해** 등 심각한 문제가 발생할 수 있습니다.
""")
    
    # ---------------- 이미지 선택 체크박스 ----------------
st.subheader('🔍 진짜 미나쌤은 어디있을까요? (1개만 선택)')

# 체크박스 상태 저장용 변수
selections = [False] * 4
check_cols = st.columns(2)

# 사용자 선택 저장
selected_index = None
for i in range(2):
    with check_cols[i]:
        if st.checkbox(f"{i+1}번", key=f"chk_{i}"):
            selections[i] = True

for i in range(2):
    with check_cols[i]:
        if st.checkbox(f"{i+3}번", key=f"chk_{i+2}"):
            selections[i+2] = True

# 여러 개 선택한 경우 경고
if selections.count(True) > 1:
    st.warning("❗ 하나만 선택해주세요!")
elif selections.count(True) == 1:
    selected_index = selections.index(True)

# 결과 확인 버튼
if st.button("🎯 결과 확인하기"):
    if selected_index is None:
        st.info("먼저 사진을 하나 선택해주세요!")
    elif selected_index == 2:
        st.success("🎉 정답입니다! 진짜 미나쌤을 찾았어요!")
    else:
        st.error("🙈 아쉽지만 틀렸어요. 다시 도전해보세요!")



    # ---------------- 학번 / 이름 입력 ----------------
    st.subheader('🙋 학생 정보 입력')
    col1, col2 = st.columns([1, 1])

    with col1:
        student_id = st.text_input('', placeholder='학번 입력', key='student_id', label_visibility="collapsed")
    with col2:
        student_name = st.text_input('', placeholder='이름 입력', key='student_name', label_visibility="collapsed")


# ---------------- 의견 입력 2 ----------------
st.subheader('✍️ 진짜 미나쌤을 어떻게 찾았나요?')
user_input2 = st.text_area('진짜 미나쌤을 어떻게 찾았는지 설명해 봅시다.', key='input2', height=150)

# ---------------- 통합된 제출 버튼 ----------------
if st.button('제출하기'):
    if student_id.strip() and student_name.strip() and user_input2.strip():
        try:
            with open('data.txt', 'a', encoding='utf-8') as f:
                f.write(f"[학번: {student_id}] [이름: {student_name}]\n")
                f.write(f"[진짜 미나쌤을 어떻게 찾았나요?]\n{user_input2}\n{'-'*50}\n")
            st.success('성공적으로 저장되었습니다!')
        except Exception as e:
            st.error(f'저장 중 오류가 발생했어: {e}')
    else:
        st.warning('학번, 이름, 의견을 모두 입력해줘!')



    # ---------------- 학생별 의견 보기 ----------------
    if show_by_student:
        st.subheader('📋 학생별 의견 조회')
        try:
            with open('data.txt', 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # 학번+이름 조합 추출
            students = []
            for line in lines:
                match = re.search(r"\[학번: (.+?)\] \[이름: (.+?)\]", line)
                if match:
                    student_key = f"{match.group(2)} ({match.group(1)})"
                    if student_key not in students:
                        students.append(student_key)

            if students:
                selected_student = st.selectbox('학생 선택', students)
                selected_id = re.search(r"\((.+?)\)", selected_student).group(1)
                selected_name = re.search(r"(.+?) \(", selected_student).group(1)

                # 해당 학생 의견 필터링
                result = ""
                collecting = False
                for line in lines:
                    if f"[학번: {selected_id}]" in line and f"[이름: {selected_name}]" in line:
                        collecting = True
                        result += line
                    elif collecting:
                        result += line
                        if line.strip() == "-" * 50:
                            collecting = False
                            result += "\n"

                if result.strip():
                    st.text_area('선택한 학생의 의견', result.strip(), height=300)
                else:
                    st.info('이 학생의 의견이 없습니다.')
            else:
                st.info('저장된 학생 정보가 없습니다.')
        except FileNotFoundError:
            st.warning('data.txt 파일이 존재하지 않습니다.')

# ---------------- 학생별 의견 시간순 조회 ----------------
if show_by_student:
    st.subheader('📋 학생별 의견 시간순 보기')

    try:
        with open('data.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()

        entry = ''
        all_entries = []
        for line in lines:
            entry += line
            if line.strip() == '-' * 50:
                all_entries.append(entry.strip())
                entry = ''

        if all_entries:
            for i, e in enumerate(all_entries[::-1], 1):  # 최근 것이 위로 오도록 역순 정렬
                with st.expander(f"🗂 의견 {len(all_entries) - i + 1}"):
                    st.text(e)
        else:
            st.info('저장된 의견이 아직 없어.')
    except FileNotFoundError:
        st.warning('data.txt 파일을 찾을 수 없어.')

