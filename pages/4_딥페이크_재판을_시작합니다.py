import streamlit as st
import os
import json

# 저장 파일 경로
DISCUSSION_FILE = "discussion.json"

# JSON 파일이 없으면 초기화
if not os.path.exists(DISCUSSION_FILE):
    with open(DISCUSSION_FILE, "w", encoding="utf-8") as f:
        json.dump({"creator": [], "platform": []}, f, ensure_ascii=False, indent=4)

# 기존 데이터 로드
with open(DISCUSSION_FILE, "r", encoding="utf-8") as f:
    discussion_data = json.load(f)

# 페이지 설정
st.set_page_config(layout="wide")
st.title("⚖️ 딥페이크 재판을 시작합니다!")

st.markdown("### 🧑‍⚖️ **논제:** 딥페이크 합성 콘텐츠로 인한 인격권 침해 문제 발생 시 책임 소재는 누구에게 있을까?")
st.write("👉 아래에 제작자와 플랫폼 측의 책임에 대한 논거를 각각 5가지씩 작성해 주세요.")

# 화면 1:1로 나누기
col1, col2 = st.columns(2)

# 제작자 논거 입력
with col1:
    st.subheader("📌 제작자 책임 논거")
    creator_inputs = []
    for i in range(1, 4):
        text = st.text_area(f"제작자 논거 {i}", key=f"creator_{i}")
        creator_inputs.append(text.strip())

# 플랫폼 논거 입력
with col2:
    st.subheader("📌 플랫폼 책임 논거")
    platform_inputs = []
    for i in range(1, 4):
        text = st.text_area(f"플랫폼 논거 {i}", key=f"platform_{i}")
        platform_inputs.append(text.strip())

# 저장 버튼
if st.button("완료"):
    creator_clean = [x for x in creator_inputs if x]
    platform_clean = [x for x in platform_inputs if x]

    if creator_clean or platform_clean:
        discussion_data["creator"].append(creator_clean)
        discussion_data["platform"].append(platform_clean)

        with open(DISCUSSION_FILE, "w", encoding="utf-8") as f:
            json.dump(discussion_data, f, ensure_ascii=False, indent=4)

        st.success("✅ 논거가 저장되었습니다!")
    else:
        st.warning("⛔ 최소 하나 이상의 논거를 입력해주세요.")
