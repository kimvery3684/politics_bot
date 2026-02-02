import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os
import random
from io import BytesIO

# --- [1. 기본 설정] ---
st.set_page_config(page_title="JJ 쇼츠 마스터 1호점 (Clean Ver)", page_icon="🔥", layout="wide")

FONT_FILE = "NanumGothic-ExtraBold.ttf"
SAVE_DIR = "saved_images"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# --- [2. 멘트 데이터베이스 (줄바꿈 제거됨)] ---
VIRAL_QUESTIONS = [
    # 🩸 생존/본능
    "당장 전쟁 나면 내 목숨, 누구한테 맡기겠습니까?",
    "국가 부도 위기! 지옥에서 우릴 구할 사람은?",
    "무인도에 딱 한 명 데려간다면, 누굴 데려가시겠습니까?",
    "내 전 재산을 믿고 맡길 가장 정직한 사람은?",
    "밤길 마주치면 가장 무서울 것 같은 눈빛은?",

    # 💔 감성/후회
    "지금 생각해보니, 그때가 천국이었다?",
    "가장 억울하게 욕먹은, 비운의 정치인은?",
    "가장 믿었기에, 가장 뼈아프게 배신한 사람은?",
    "타임머신 타고 가서, 반드시 말리고 싶은 사람은?",
    "술 한잔 따라주며 위로해주고 싶은 사람은?",

    # 🎭 풍자/팩폭
    "정치 안 하고 배우 했으면 대박 났을 '연기 대상'은?",
    "입만 열면 빵 터진다! 최고의 '개그맨'은?",
    "얼굴에 철판 깔았다! 뻔뻔함 1티어는 누구?",
    "주변에 간신배가 가장 많았던 사람은?",
    "가장 '쇼(Show)'를 기가 막히게 잘한다고 생각하는 사람은?",

    # 🥊 능력치 비교
    "트럼프랑 맞짱 떠도 안 꿀릴 '협상의 신'은?",
    "추진력 하나는 불도저! 일 머리 최고인 사람은?",
    "말빨로 제압한다! 역대 최강 '토론 싸움꾼'은?",
    "멍청한 참모들 데리고 혼자 하드캐리한 사람은?",
    "부하 직원들이 가장 존경했을 것 같은 리더는?",

    # 🔮 미래/가정
    "다시 투표한다면, 절대 안 뽑을 사람은?",
    "만약 통일 대통령이 나온다면, 누가 가장 적임자인가?",
    "100년 뒤 역사책에서 가장 칭송받을 위인은?",
    "다음 대선, 이 사람 나오면 무조건 찍는다?",
    "은퇴하고 유튜버 하면 구독자 100만 찍을 사람은?",

    # 💣 매운맛 밸런스
    "세금이 가장 아깝다! 월급 압수하고 싶은 사람은?",
    "가장 '내로남불'이 심했다고 생각하는 인물은?",
    "자식 교육을 가장 잘못 시켰다고 생각하는 분은?",
    "깨끗한 척했지만 알고 보니 아니었던 사람은?",
    "제발 정계 은퇴해라! 꼴도 보기 싫은 사람은?"
]

# --- [3. DB 데이터] ---
DB_PRESIDENTS = ["윤석열", "문재인", "박근혜", "이명박", "노무현", "김대중", "김영삼", "노태우", "전두환", "박정희", "이승만"]
DB_POLITICIANS = ["이재명", "한동훈", "조국", "이준석", "홍준표", "오세훈", "안철수", "추미애", "김동연", "나경원", "원희룡", "김기현", "정청래", "고민정"]
DB_BUSINESS = ["이재용", "정의선", "김승연", "최태원"]
ALL_NAMES = sorted(list(set(DB_PRESIDENTS + DB_POLITICIANS + DB_BUSINESS)))

# --- [4. 기능 함수들] ---
def get_font(size):
    if os.path.exists(FONT_FILE): return ImageFont.truetype(FONT_FILE, size)
    else: return ImageFont.load_default()

def save_uploaded_file(uploaded_file, name):
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file).convert("RGB")
            image.save(os.path.join(SAVE_DIR, f"{name}.jpg"), quality=95)
            return True
        except: return False
    return False

def load_saved_image(name):
    path = os.path.join(SAVE_DIR, f"{name}.jpg")
    if os.path.exists(path): return Image.open(path).convert("RGB")
    return None

def create_quiz_image(content_list, d):
    canvas = Image.new('RGB', (1080, 1920), d['bg_color'])
    draw = ImageDraw.Draw(canvas)
    
    font_top = get_font(d['top_fs'])
    font_bot = get_font(d['bot_fs'])
    font_label = get_font(d['label_fs'])

    # 상단 바
    draw.rectangle([(0, 0), (1080, d['top_h'])], fill=d['top_bg'])
    try:
        lines = d['top_text'].split('\n')
        total_text_h = (len(lines) * d['top_fs']) + ((len(lines) - 1) * d['top_lh'])
        current_y = (d['top_h'] - total_text_h) / 2 + d['top_y_adj']
        
        for i, line in enumerate(lines):
            fill_color = d['top_color_1'] if i == 0 else d['top_color_2']
            draw.text((540, current_y), line, font=font_top, fill=fill_color, anchor="mt")
            current_y += d['top_fs'] + d['top_lh']
    except: pass

    # 중앙 그리드
    grid_start_y = d['top_h']
    grid_end_y = 1920 - d['bot_h']
    grid_height = grid_end_y - grid_start_y
    cell_w, cell_h = 1080 // 2, grid_height // 2
    positions = [(0, grid_start_y), (cell_w, grid_start_y), (0, grid_start_y + cell_h), (cell_w, grid_start_y + cell_h)]

    for i, (pos, (name, img)) in enumerate(zip(positions, content_list)):
        if img is None:
            img = Image.new('RGB', (cell_w, cell_h), (50, 50, 50))
            ImageDraw.Draw(img).text((cell_w/2, cell_h/2), "사진 없음", font=get_font(40), fill="white", anchor="mm")
        
        zoom = d['img_zoom']
        img_ratio, target_ratio = img.width / img.height, cell_w / cell_h
        if img_ratio > target_ratio:
            new_w = int(img.height * target_ratio)
            img = img.crop(((img.width - new_w) // 2, 0, (img.width + new_w) // 2, img.height))
        else:
            new_h = int(img.width / target_ratio)
            img = img.crop((0, (img.height - new_h) // 2, img.width, (img.height + new_h) // 2))

        if zoom > 1.0:
            w, h = img.size
            cw, ch = int(w / zoom), int(h / zoom)
            img = img.crop(((w-cw)//2, (h-ch)//2, (w+cw)//2, (h+ch)//2))
            
        img = img.resize((cell_w, cell_h), Image.LANCZOS)
        canvas.paste(img, pos)
        
        label_h = d['label_h']
        label_y = pos[1] + cell_h - label_h
        draw.rectangle([pos[0], label_y, pos[0]+cell_w, pos[1]+cell_h], fill=d['label_bg'])
        draw.text((pos[0] + cell_w/2, label_y + label_h/2), name, font=font_label, fill=d['label_color'], anchor="mm")
        draw.rectangle([pos[0], pos[1], pos[0]+cell_w, pos[1]+cell_h], outline="black", width=2)

    # 하단 바
    draw.rectangle([(0, 1920 - d['bot_h']), (1080, 1920)], fill=d['bot_bg'])
    try:
        bot_text_x = 540
        bot_text_y = (1920 - (d['bot_h'] / 2)) + d['bot_y_adj']
        draw.text((bot_text_x, bot_text_y), d['bot_text'], font=font_bot, fill=d['bot_color'], anchor="mm", align="center", spacing=d['bot_lh'])
    except: pass
    
    return canvas

# --- [5. 메인 UI] ---
st.title("🔥 1호점: 매운맛 (줄바꿈 자유 버전)")
col_L, col_R = st.columns([1, 1.3])

with col_L:
    st.header("1. 인물 구성")
    mode = st.radio("모드 선택", ["🎲 DB 랜덤", "✅ DB 선택", "🛠️ 완전 자유 입력(추천)"], index=2, horizontal=True)

    final_content = []

    if mode == "🛠️ 완전 자유 입력(추천)":
        st.info("원하는 이름과 사진을 4개 순서대로 넣으세요.")
        for i in range(4):
            with st.container(border=True):
                c1, c2 = st.columns([1, 2])
                with c1: input_name = st.text_input(f"{i+1}번 이름표", value=f"인물 {i+1}", key=f"custom_name_{i}")
                with c2: input_file = st.file_uploader(f"{i+1}번 사진", type=['jpg','png','jpeg'], key=f"custom_file_{i}")
                img_obj = None
                if input_file: img_obj = Image.open(input_file).convert("RGB")
                final_content.append((input_name, img_obj))

    elif mode == "✅ DB 선택":
        if 'c_names' not in st.session_state: st.session_state.c_names = ["윤석열", "이재명", "한동훈", "조국"]
        sel = st.multiselect("4명 선택", ALL_NAMES, default=st.session_state.c_names[:4])
        current_selection = sel if len(sel) == 4 else (sel + ["윤석열", "이재명", "한동훈", "조국"])[:4]
        st.write("---")
        with st.popover("📸 DB 사진 관리"):
            for name in current_selection:
                f = st.file_uploader(f"{name} 사진 업로드", type=['jpg','png','jpeg'], key=f"u_{name}")
                if f: save_uploaded_file(f, name)
        for name in current_selection:
            img = load_saved_image(name)
            final_content.append((name, img))

    else:
        if st.button("🔄 다시 뽑기", use_container_width=True): st.session_state.rand_names = random.sample(ALL_NAMES, 4)
        if 'rand_names' not in st.session_state: st.session_state.rand_names = ["윤석열", "이재명", "한동훈", "조국"]
        current_selection = st.session_state.rand_names
        for name in current_selection:
            img = load_saved_image(name)
            final_content.append((name, img))

    st.header("💬 질문 설정")
    with st.container(border=True):
        if 'q_text' not in st.session_state: st.session_state.q_text = VIRAL_QUESTIONS[0]
        c_q1, c_q2 = st.columns([1, 2])
        with c_q1:
            if st.button("🎲 질문 랜덤", type="primary", use_container_width=True): st.session_state.q_text = random.choice(VIRAL_QUESTIONS)
        with c_q2:
            selected_q = st.selectbox("질문 목록", VIRAL_QUESTIONS, index=0)
            if selected_q != VIRAL_QUESTIONS[0]: st.session_state.q_text = selected_q

        # [수정됨] 안내 문구 변경
        top_text = st.text_area("상단 문구 (원하는 곳에서 엔터를 쳐주세요)", st.session_state.q_text, height=80)
    
    st.header("🎨 디자인 (매운맛)")
    with st.expander("⬆️ 상단 바 (Top Bar) 설정", expanded=True):
        c_h1, c_h2 = st.columns(2)
        with c_h1: top_h = st.slider("배경 높이", 100, 600, 400)
        with c_h2: top_bg = st.color_picker("배경색", "#000000", key="tbg") 
        
        st.markdown("---")
        col_t1, col_t2 = st.columns(2)
        with col_t1: top_fs = st.slider("🅰️ 글자 크기", 20, 150, 100)
        with col_t2: top_y_adj = st.slider("↕️ 글자 위치 조절", -200, 200, 0)
        
        st.caption("줄별 색상 (엔터 기준 1줄/2줄)")
        c_tc1, c_tc2 = st.columns(2)
        with c_tc1: top_color_1 = st.color_picker("1번째 줄", "#FF0000", key="tc1") 
        with c_tc2: top_color_2 = st.color_picker("2번째 줄", "#FFFFFF", key="tc2")
        top_lh = st.slider("행간", 0, 150, 20)

    with st.expander("⬇️ 하단 바 설정", expanded=False):
        bot_text = st.text_area("하단 문구", "사진을 두번 톡톡 누르고,\n댓글 남겨주세요!!")
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            bot_h = st.slider("배경 높이", 100, 600, 350, key="bh")
            bot_bg = st.color_picker("배경색", "#FF0000", key="bbg")
        with col_b2:
            bot_fs = st.slider("글자 크기", 20, 150, 45, key="bfs")
            bot_color = st.color_picker("글자색", "#FFFFFF", key="bc")
        bot_lh = st.slider("행간", 0, 150, 20, key="blh")
        bot_y_adj = st.slider("위치 조절", -200, 200, 0, key="bya")

    with st.expander("🖼️ 사진 & 이름표 설정", expanded=False):
        img_zoom = st.slider("사진 확대", 1.0, 3.0, 1.0, 0.1)
        label_h = st.slider("이름표 높이", 30, 200, 80)
        label_fs = st.slider("이름 크기", 20, 100, 45)
        c3, c4 = st.columns(2)
        label_bg = c3.color_picker("이름표 배경", "#FF0000", key="lbg")
        label_color = c4.color_picker("이름표 글자", "#FFFFFF", key="lc")
            
    bg_color = st.color_picker("전체 배경", "#000000")

    design = {
        'bg_color': bg_color, 
        'top_text': top_text, 'top_h': top_h, 'top_fs': top_fs, 'top_lh': top_lh, 'top_y_adj': top_y_adj, 'top_bg': top_bg,
        'top_color_1': top_color_1, 'top_color_2': top_color_2, 
        'bot_text': bot_text, 'bot_h': bot_h, 'bot_fs': bot_fs, 'bot_lh': bot_lh, 'bot_y_adj': bot_y_adj, 'bot_bg': bot_bg, 'bot_color': bot_color,
        'label_h': label_h, 'label_fs': label_fs, 'label_bg': label_bg, 'label_color': label_color, 'img_zoom': img_zoom
    }

with col_R:
    st.subheader("🖼️ 결과물")
    if len(final_content) == 4:
        final_img = create_quiz_image(final_content, design)
        st.image(final_img, use_container_width=True)
        buf = BytesIO()
        final_img.save(buf, format="JPEG", quality=100)
        st.download_button("💾 이미지 다운로드", buf.getvalue(), "shorts_season2.jpg", "image/jpeg", use_container_width=True)
    else:
        st.error("오류: 4명의 인물 데이터가 필요합니다.")