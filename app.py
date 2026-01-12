import streamlit as st
import random
import streamlit.components.v1 as components

# [1] 기본 설정 및 데이터
st.set_page_config(page_title="정치인 짤 생성기", layout="wide")

# 정치인 데이터베이스 (총 52명)
DATA = {
    "vip": ["윤석열", "김건희"],
    "ruling": [ # 여당 25인
        "한동훈", "오세훈", "홍준표", "안철수", "나경원", "원희룡", "추경호", "배현진", "권성동", "장제원",
        "김기현", "윤상현", "김재섭", "조정훈", "인요한", "김은혜", "박수영", "성일종", "김웅", "박정훈",
        "이상민", "윤희숙", "김민전", "김용태", "유승민"
    ],
    "opposition": [ # 야당 25인
        "이재명", "조국", "추미애", "정청래", "박찬대", "고민정", "이준석", "천하람", "김남국", "최강욱",
        "김민석", "서영교", "장경태", "박지원", "정동영", "박용진", "김동연", "김경수", "임종석", "우상호",
        "이낙연", "김두관", "양문석", "김준혁", "이언주"
    ]
}

# 전체 명단 통합 (검색/직접 선택용)
ALL_CANDIDATES = DATA['vip'] + DATA['ruling'] + DATA['opposition']

# 랜덤 질문 리스트 (매운맛)
RANDOM_QUESTIONS = [
    "역대급 내로남불! 남이 하면 불륜, 내가 하면 로맨스인 자는?",
    "지금 당장 정계 은퇴해야 할 사람은?",
    "다음 대통령으로 절대 뽑히면 안 될 사람은?",
    "말만 번지르르하고 실속은 하나도 없는 사람은?",
    "밥값 못하고 세금만 축내는 월급 루팡은?",
    "무인도에 딱 한 명만 데려간다면 누구?",
    "가장 믿음이 안 가는 관상은?"
]

# [2] 세션 상태 초기화 (새로고침 해도 값 유지)
if 'candidates' not in st.session_state:
    st.session_state.candidates = ["한동훈", "이재명", "조국", "이준석"] # 기본값
if 'question' not in st.session_state:
    st.session_state.question = RANDOM_QUESTIONS[0]

# [3] 사이드바 - 디자인 & 레이아웃 (스크린샷 스타일 반영)
with st.sidebar:
    st.header("🎨 디자인 & 레이아웃")
    
    tab_style, tab_pos, tab_text = st.tabs(["색상/크기", "위치/배치", "문구"])
    
    with tab_style:
        st.subheader("🖍 색상 설정")
        bg_color = st.color_picker("배경색", "#000000")
        text_color = st.color_picker("질문 텍스트 색상", "#FFD700")
        border_color = st.color_picker("테두리/이름 색상", "#FFD700")
        
        st.subheader("📏 크기 설정")
        font_size = st.slider("질문 크기", 20, 60, 28)
        
    with tab_pos:
        st.subheader("📍 위치 조정")
        title_y = st.slider("질문 위치 (Y축)", 0, 50, 10)
        grid_y = st.slider("사진 뭉치 위치 (Y축)", 10, 80, 25)
        grid_w = st.slider("사진 뭉치 너비", 50, 100, 90)

    with tab_text:
        st.info("메인 화면에서 질문을 직접 입력하거나 랜덤으로 선택할 수 있습니다.")

# [4] 메인 화면 - 퀴즈 생성 컨트롤러
st.title("🎵 정치 숏츠 생성기 (매운맛🔥)")

# 컨테이너 박스로 영역 구분
with st.container(border=True):
    st.subheader("퀴즈 생성")
    
    col1, col2 = st.columns(2)
    
    # --- 좌측: 인물 구성 ---
    with col1:
        st.markdown("**인물 구성**")
        cand_mode = st.radio("인물 선택 방식", ["랜덤", "직접 (최대 4명)"], horizontal=True, key="cand_mode_radio")
        
        if cand_mode == "랜덤":
            c_btn1, c_btn2, c_btn3 = st.columns(3)
            if c_btn1.button("🔴 여당 랜덤"):
                st.session_state.candidates = random.sample(DATA['ruling'], 4)
            if c_btn2.button("🔵 야당 랜덤"):
                st.session_state.candidates = random.sample(DATA['opposition'], 4)
            if c_btn3.button("👑 VIP 포함"):
                others = random.sample(DATA['ruling'] + DATA['opposition'], 2)
                st.session_state.candidates = DATA['vip'] + others
                
        else: # 직접 선택
            selected = st.multiselect(
                "명단에서 4명을 선택하세요", 
                ALL_CANDIDATES, 
                default=st.session_state.candidates[:4],
                max_selections=4
            )
            if len(selected) > 0:
                st.session_state.candidates = selected
                # 4명이 안 되면 빈칸 채우기 (에러 방지)
                while len(st.session_state.candidates) < 4:
                    st.session_state.candidates.append("?")

    # --- 우측: 질문 선택 ---
    with col2:
        st.markdown("**질문 선택**")
        q_mode = st.radio("질문 선택 방식", ["랜덤", "직접"], horizontal=True, key="q_mode_radio")
        
        if q_mode == "랜덤":
            if st.button("🎲 질문 뽑기 (클릭)"):
                st.session_state.question = random.choice(RANDOM_QUESTIONS)
            st.info(f"선택된 질문: {st.session_state.question}")
        else:
            user_q = st.text_input("질문을 입력하세요", value=st.session_state.question)
            st.session_state.question = user_q

# [5] 미리보기 및 생성 버튼
st.divider()
st.button("🚀 퀴즈 이미지 생성 (다운로드)", type="primary", use_container_width=True)

st.subheader("🔥 미리보기")

# HTML/CSS 생성 로직
display_cands = st.session_state.candidates
# 4명 미만일 경우 처리
final_cands = display_cands + ["?"] * (4 - len(display_cands))

html_code = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    body {{
        margin: 0; padding: 0;
        background-color: {bg_color};
        font-family: 'Pretendard', sans-serif;
        display: flex; justify-content: center; align-items: center;
        height: 600px; overflow: hidden;
    }}
    .phone-frame {{
        width: 360px; height: 600px;
        background-color: {bg_color};
        position: relative;
        border: 1px solid #333;
        box-shadow: 0 0 20px rgba(0,0,0,0.5);
    }}
    .title {{
        position: absolute;
        top: {title_y}%;
        width: 100%;
        text-align: center;
        color: {text_color};
        font-size: {font_size}px;
        font-weight: 900;
        line-height: 1.3;
        z-index: 10;
        padding: 0 15px; box-sizing: border-box;
        word-break: keep-all;
    }}
    .grid-container {{
        position: absolute;
        top: {grid_y}%;
        left: {(100 - grid_w) / 2}%;
        width: {grid_w}%;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
    }}
    .card {{
        background: #222;
        border-radius: 8px;
        overflow: hidden;
        display: flex; flex-direction: column;
        border: 1px solid #444;
    }}
    .img-box {{
        width: 100%; padding-top: 100%; position: relative; background: #333;
    }}
    .img-box img {{
        position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover;
    }}
    .name-tag {{
        background: #000;
        color: {border_color};
        text-align: center;
        padding: 8px 0;
        font-weight: 700;
        border-top: 3px solid {border_color};
        font-size: 18px;
    }}
    .number {{ color: #fff; margin-right: 5px; }}
</style>
</head>
<body>
    <div class="phone-frame">
        <div class="title">{st.session_state.question}</div>
        <div class="grid-container">
            <div class="card">
                <div class="img-box"><img src="https://via.placeholder.com/150/333/fff?text={final_cands[0]}" /></div>
                <div class="name-tag"><span class="number">1</span>{final_cands[0]}</div>
            </div>
            <div class="card">
                <div class="img-box"><img src="https://via.placeholder.com/150/333/fff?text={final_cands[1]}" /></div>
                <div class="name-tag"><span class="number">2</span>{final_cands[1]}</div>
            </div>
            <div class="card">
                <div class="img-box"><img src="https://via.placeholder.com/150/333/fff?text={final_cands[2]}" /></div>
                <div class="name-tag"><span class="number">3</span>{final_cands[2]}</div>
            </div>
            <div class="card">
                <div class="img-box"><img src="https://via.placeholder.com/150/333/fff?text={final_cands[3]}" /></div>
                <div class="name-tag"><span class="number">4</span>{final_cands[3]}</div>
            </div>
        </div>
    </div>
</body>
</html>
"""

# 미리보기 출력
components.html(html_code, height=620)