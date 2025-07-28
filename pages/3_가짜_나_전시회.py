import streamlit as st
import os
import json
import time

# 폴더 및 파일 경로
UPLOAD_DIR = "uploaded_images"
FEEDBACK_FILE = "feedback.json"
os.makedirs(UPLOAD_DIR + "/real", exist_ok=True)
os.makedirs(UPLOAD_DIR + "/fake", exist_ok=True)

# 빈 JSON 파일이면 초기화
if not os.path.exists(FEEDBACK_FILE):
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)

# JSON 불러오기
try:
    with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
        feedback = json.load(f)
except json.JSONDecodeError:
    feedback = {}

# 페이지 설정
st.set_page_config(layout="wide")
st.markdown("## 🖼️ 가짜 나, 전시회")

left_col, right_col = st.columns([3, 1])

# -------------------- 오른쪽: 이미지 업로드 --------------------
with right_col:
    st.markdown("<h4 style='font-size:20px;'>🗂 이미지 업로드</h4>", unsafe_allow_html=True)
    student_id = st.text_input("학번 입력")
    student_name = st.text_input("이름 입력")
    real_image = st.file_uploader("실제 이미지 업로드", type=["jpg", "jpeg", "png"], key="real")
    fake_image = st.file_uploader("딥페이크 이미지 업로드", type=["jpg", "jpeg", "png"], key="fake")

    if st.button("전시회에 업로드"):
        if student_id and student_name and real_image and fake_image:
            timestamp = str(int(time.time()))
            real_path = os.path.join(UPLOAD_DIR, "real", f"{timestamp}_{student_id}_{student_name}_real.jpg")
            fake_path = os.path.join(UPLOAD_DIR, "fake", f"{timestamp}_{student_id}_{student_name}_fake.jpg")
            with open(real_path, "wb") as f:
                f.write(real_image.read())
            with open(fake_path, "wb") as f:
                f.write(fake_image.read())
            feedback[timestamp] = {
                "student_id": student_id,
                "student_name": student_name,
                "real": real_path.replace("\\", "/"),
                "fake": fake_path.replace("\\", "/"),
                "comments": [],
                "hearts": 0,
                "show_comment_box": False,
                "show_comments": False
            }
            with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
                json.dump(feedback, f, indent=4, ensure_ascii=False)
            st.success("이미지가 전시되었습니다!")
        else:
            st.warning("모든 정보를 입력해 주세요.")

# -------------------- 왼쪽: 전시된 이미지 --------------------
with left_col:
    st.markdown("### 👩‍🎨 전시된 이미지")

    for timestamp, item in sorted(feedback.items(), reverse=True):
        st.markdown(f"**{item['student_name']} ({item['student_id']})**")
        img_col1, img_col2, btn_col = st.columns([1, 1, 1])

        for label, key in [("실제", "real"), ("딥페이크", "fake")]:
            path = item.get(key)
            if path and os.path.exists(path):
                with (img_col1 if label == "실제" else img_col2):
                    st.image(path, width=150, caption=f"{label} 이미지")

                            # 댓글 작성 버튼 토글
        if st.button("💬 댓글 작성", key=f"comment_input_toggle_{timestamp}"):
            feedback[timestamp]["show_comment_box_2"] = not item.get("show_comment_box_2", False)
            with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
                json.dump(feedback, f, indent=4, ensure_ascii=False)

        # 댓글 입력창 (Enter 입력 시 자동 저장)
        if item.get("show_comment_box_2", False):
            comment_input = st.text_input("댓글을 입력 후 Enter를 누르세요", key=f"comment_input_{timestamp}")
            if comment_input:
                feedback[timestamp]["comments"].append(comment_input)
                feedback[timestamp]["show_comment_box_2"] = False  # 댓글창 자동 닫기
                with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
                    json.dump(feedback, f, indent=4, ensure_ascii=False)
                st.success("댓글이 저장되었어!")


        # 댓글보기 버튼
        with btn_col:
            if st.button(f"💬 댓글보기", key=f"comment_toggle_{timestamp}"):
                feedback[timestamp]["show_comments"] = not item.get("show_comments", False)
                with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
                    json.dump(feedback, f, indent=4, ensure_ascii=False)

        # 댓글 목록 표시
        if item.get("show_comments", False):
            if item["comments"]:
                st.markdown("**💬 댓글 목록**")
                updated = False
                new_comments = []
                for i, c in enumerate(item["comments"]):
                    comment_col, del_col = st.columns([6, 1])
                    with comment_col:
                        st.markdown(f"- {c}")
                    with del_col:
                        if st.button("❌", key=f"del_{timestamp}_{i}"):
                            updated = True
                        else:
                            new_comments.append(c)
                if updated:
                    feedback[timestamp]["comments"] = new_comments
                    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
                        json.dump(feedback, f, indent=4, ensure_ascii=False)
                    st.success("댓글이 삭제되었습니다.")
            else:
                st.info("아직 댓글이 없습니다.")

        # 하트 버튼
        if st.button(f"❤️ {item['hearts']}", key=f"heart_{timestamp}"):
            feedback[timestamp]["hearts"] += 1
            with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
                json.dump(feedback, f, indent=4, ensure_ascii=False)
