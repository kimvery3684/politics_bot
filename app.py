import streamlit as st
import random
import streamlit.components.v1 as components

# [1] 기본 설정 및 데이터
st.set_page_config(page_title="정치인 퀴즈 생성기", layout="wide")

# 정치인 데이터베이스
DATA = {
    "vip": [
        {"name": "윤석열", "party": "대통령"},
        {"name": "김건희", "party": "영부인"}
    ],
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

# 세션 상태 초기화 (현재 선택된 후보 명단 저장)
if 'candidates' not in st.session_state:
    st.session_state.candidates = random.sample(DATA['ruling'], 4)
    st.session_state.candidate_type = "ruling"

# [2] 사이드바 - 디자인 & 레이아웃 패널
with st.sidebar:
    st.header("🎨 디자인 & 레이아웃")
    
    tab1, tab2, tab3 = st.tabs(["위치/배치", "색상/크기", "문구"])
    
    with tab1:
        st.caption("💡 요소의 위치를 조절하세요")
        title_y = st.slider("질문 위치 (Y좌표 %)", 0, 90, 10)
        grid_y = st.slider("사진 뭉치 위치 (Y좌표 %)", 0, 90, 30)
        grid_w = st.slider("사진 뭉치 너비 (%)", 50, 100, 90)

    with tab2:
        st.caption("💡 스타일을 변경하세요")
        font_size = st.slider("질문 폰트 크기 (px)", 14, 60, 24)
        border_color = st.color_picker("테두리 및 강조 색상", "#FFD700")
        
    with tab3:
        st.caption("💡 문구를 입력하세요")
        main_text = st.text_area("상단 문구", "역대급 내로남불! 남이 하면 불륜,\n내가 하면 로맨스인 자는?", height=100)
        main_text_html = main_text.replace("\n", "<br>") # 줄바꿈 처리

# [3] 메인 화면 - 데이터 선택 및 미리보기
st.title("🔥 정치인 퀴즈 생성기 (Admin)")

# 상단 버튼 그룹
col1, col2, col3, col4 = st.columns([1,1,1,2])
with col1:
    if st.button("🔴 여당 (국힘)"):
        st.session_state.candidates = random.sample(DATA['ruling'], 4)
        st.session_state.candidate_type = "ruling"
with col2:
    if st.button("🔵 야당 (범야권)"):
        st.session_state.candidates = random.sample(DATA['opposition'], 4)
        st.session_state.candidate_type = "opposition"
with col3:
    if st.button("👑 VIP (대통령)"):
        vip = DATA['vip'] # VIP 2명 고정
        others = random.sample(DATA['ruling'] + DATA['opposition'], 2) # 나머지 2명 랜덤
        pool = vip + [{"name": p, "party": "기타"} for p in others]
        st.session_state.candidates = pool
        st.session_state.candidate_type = "vip"

# 현재 선택된 후보 리스트 준비
display_list = []
for p in st.session_state.candidates:
    name = p["name"] if isinstance(p, dict) else p
    display_list.append(name)

# [4] 미리보기 화면 생성 (HTML/CSS Injection)
# 파이썬 변수를 HTML 문자열에 삽입합니다.
html_code = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    body {{
        margin: 0; padding: 0;
        background-color: #111;
        font-family: 'Pretendard', sans-serif;
        display: flex; justify-content: center; align-items: center;
        height: 600px; overflow: hidden;
    }}
    .phone-frame {{
        width: 360px; height: 600px;
        background-color: #000;
        position: relative;
        border: 4px solid #333;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 0 20px rgba(0,0,0,0.5);
    }}
    .title {{
        position: absolute;
        top: {title_y}%;
        width: 100%;
        text-align: center;
        color: #fff;
        font-size: {font_size}px;
        font-weight: 900;
        line-height: 1.3;
        z-index: 10;
        padding: 0 10px; box-sizing: border-box;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
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
    }}
    .img-box {{
        width: 100%; padding-top: 100%; position: relative; background: #555;
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
        font-size: 16px;
    }}
</style>
</head>
<body>
    <div class="phone-frame">
        <div class="title">{main_text_html}</div>
        <div class="grid-container">
            <div class="card">
                <div class="img-box"><img src="https://via.placeholder.com/150/333/fff?text={display_list[0]}" /></div>
                <div class="name-tag">1. {display_list[0]}</div>
            </div>
            <div class="card">
                <div class="img-box"><img src="https://via.placeholder.com/150/333/fff?text={display_list[1]}" /></div>
                <div class="name-tag">2. {display_list[1]}</div>
            </div>
            <div class="card">
                <div class="img-box"><img src="https://via.placeholder.com/150/333/fff?text={display_list[2]}" /></div>
                <div class="name-tag">3. {display_list[2]}</div>
            </div>
            <div class="card">
                <div class="img-box"><img src="https://via.placeholder.com/150/333/fff?text={display_list[3]}" /></div>
                <div class="name-tag">4. {display_list[3]}</div>
            </div>
        </div>
    </div>
</body>
</html>
"""

# 미리보기 출력 (높이 고정)
st.write("### 📱 실시간 미리보기")
components.html(html_code, height=620)

# 다운로드 버튼 (기능 예시)
st.button("🚀 이 디자인으로 이미지 생성하기 (기능 준비중)", type="primary")