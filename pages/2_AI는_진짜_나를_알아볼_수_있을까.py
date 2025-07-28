import streamlit as st
import random

# 페이지 설정
st.set_page_config(page_title="AI는 진짜 나를 알아볼 수 있을까?", layout="wide")
st.title("🧠 AI는 진짜 나를 알아볼 수 있을까?")

st.markdown("""
이 페이지에서는 **실제 얼굴 사진**과 **딥페이크 합성 얼굴 사진**을 업로드하여  
AI가 얼마나 잘 구별할 수 있는지를 테스트해볼 수 있어요.
""")

# -------------------- 이미지 업로드 --------------------
st.subheader("1️⃣ 실제 얼굴 사진 업로드")
real_image = st.file_uploader("실제 내 얼굴 사진을 업로드하세요", type=['jpg', 'jpeg', 'png'], key="real")

st.subheader("2️⃣ 딥페이크 합성 얼굴 사진 업로드")
fake_image = st.file_uploader("딥페이크 합성된 얼굴 사진을 업로드하세요", type=['jpg', 'jpeg', 'png'], key="fake")

# -------------------- 예측 결과 --------------------
if real_image and fake_image:
    st.subheader("🔍 AI 예측 결과")

    # 랜덤 확률 생성 (데모용)
    real_prob = random.uniform(80, 98)
    fake_prob = 100 - real_prob + random.uniform(-3, 3)

    col1, col2 = st.columns(2)

    with col1:
        st.image(real_image, caption="실제 얼굴", width=150)  # 띠부띠부씰 크기 느낌
        st.markdown(f"✅ **실제일 확률**: `{real_prob:.2f}%`")
        st.markdown(f"❌ **딥페이크일 확률**: `{100 - real_prob:.2f}%`")

    with col2:
        st.image(fake_image, caption="딥페이크 얼굴", width=150)  # 띠부띠부씰 크기 느낌
        st.markdown(f"✅ **실제일 확률**: `{100 - fake_prob:.2f}%`")
        st.markdown(f"❌ **딥페이크일 확률**: `{fake_prob:.2f}%`")

else:
    st.info("두 이미지를 모두 업로드하면 AI 예측 결과가 표시됩니다.")
