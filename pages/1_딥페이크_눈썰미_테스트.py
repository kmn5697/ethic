import streamlit as st
import os
import random
from PIL import Image

# 페이지 설정
st.set_page_config(page_title="딥페이크 눈썰미 테스트", layout="wide")
st.title('🧠 딥페이크 눈썰미 테스트')

# 이미지 경로
base_dir = 'data/sample_images/sample_images'
fake_dir = os.path.join(base_dir, 'fake')
real_dir = os.path.join(base_dir, 'real')

# 세션 상태에 이미지 저장 (랜덤 섞기 1회만 수행)
if 'shuffled_images' not in st.session_state:
    fake_images = [os.path.join(fake_dir, f) for f in os.listdir(fake_dir) if f.lower().endswith(('jpg', 'jpeg', 'png'))]
    real_images = [os.path.join(real_dir, f) for f in os.listdir(real_dir) if f.lower().endswith(('jpg', 'jpeg', 'png'))]
    sample_images = random.sample(fake_images, 5) + random.sample(real_images, 4)
    random.shuffle(sample_images)
    st.session_state['shuffled_images'] = sample_images
else:
    sample_images = st.session_state['shuffled_images']

# 정답 딕셔너리
answer_dict = {os.path.basename(p): ('fake' if 'fake' in p else 'real') for p in sample_images}

st.markdown("아래 9장의 이미지 중에서 **딥페이크(가짜)** 라고 생각되는 이미지를 선택해 보세요.")

# 사용자 선택 저장
user_selection = []

# 3x3 이미지 출력
for i in range(0, 9, 3):
    cols = st.columns(3)
    for j in range(3):
        idx = i + j
        img_path = sample_images[idx]
        fname = os.path.basename(img_path)
        img = Image.open(img_path)

        # 이미지 출력
        cols[j].image(img, use_container_width=True)

        # 번호 + 체크박스 출력
        with cols[j]:
            checkbox_label = f"**{idx+1}번**"
            selected = st.checkbox(checkbox_label, key=f"cb_{idx}")

            # 체크박스 크기 확대 + 가운데 정렬
            st.markdown("""
                <style>
                [data-testid="stCheckbox"] > div:first-child {
                    transform: scale(1.5);
                    margin-left: auto;
                    margin-right: auto;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
                </style>
            """, unsafe_allow_html=True)

            if selected:
                user_selection.append(fname)

# 제출 버튼
if st.button("제출하기"):
    correct = 0
    total_fakes = sum(1 for v in answer_dict.values() if v == 'fake')

    for fname, label in answer_dict.items():
        if label == 'fake' and fname in user_selection:
            correct += 1
        elif label == 'real' and fname in user_selection:
            correct -= 1

    st.markdown(f"### ✅ 맞춘 딥페이크 수: {correct} / {total_fakes}")

    st.markdown("#### 📊 결과 상세 분석")
    for idx, img_path in enumerate(sample_images):
        fname = os.path.basename(img_path)
        true_label = answer_dict[fname]
        user_chose = fname in user_selection

        if true_label == 'fake' and user_chose:
            st.success(f"{idx+1}번: 딥페이크 ✔️")
        elif true_label == 'fake' and not user_chose:
            st.warning(f"{idx+1}번: 딥페이크 ❌ (선택하지 않음)")
        elif true_label == 'real' and user_chose:
            st.error(f"{idx+1}번: 실제 사진 ❌ (틀림)")
        else:
            st.info(f"{idx+1}번: 실제 사진 ✔️")
