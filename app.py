import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os
from io import BytesIO  # <--- 이 줄이 빠져서 에러가 났었습니다! 죄송합니다.

# --- [1. 기본 설정 및 영구 저장소 만들기] ---
st.set_page_config(page_title="JJ 쇼츠 마스터 (영구저장)", page_icon="🏛️", layout="wide")

# 폰트 설정 (같은 폴더에 폰트 파일이 있어야 함)
FONT_FILE = "NanumGothic-ExtraBold.ttf"

# 📁 [핵심] 사진을 저장할 폴더 만들기 (없으면 생성)
SAVE_DIR = "saved_images"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# --- [2. 기능 함수] ---
def get_font(size):
    if os.path.exists(FONT_FILE):
        return ImageFont.truetype(FONT_FILE, size)
    else:
        return ImageFont.load_default()

# 💾 사진 저장 함수 (핵심 기능)
def save_uploaded_file(uploaded_file, name):
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file).convert("RGB")
            save_path = os.path.join(SAVE_DIR, f"{name}.jpg")
            image.save(save_path, quality=95)
            return True
        except Exception as e:
            st.error(f"저장 중 오류 발생: {e}")
            return False
    return False

# 📂 사진 불러오기 함수
def load_saved_image(name):
    path = os.path.join(SAVE_DIR, f"{name}.jpg")
    if os.path.exists(path):
        return Image.open(path).convert("RGB")
    return None

# --- [3. 이미지 생성 엔진] ---
def create_quiz_image(names, d):
    canvas = Image.new('RGB', (1080, 1920), d['bg_color'])
    draw = ImageDraw.Draw(canvas)
    
    font_top = get_font(d['top_fs'])
    font_bot = get_font(d['bot_fs'])
    font_label = get_font(d['label_size'])

    # === [A. 상단 바] ===
    draw.rectangle([(0, 0), (1080, d['top_h'])], fill=d['top_bg'])
    
    try:
        bbox = draw.textbbox((0, 0), d['top_text'], font=font_top, spacing=d['top_lh'])
        draw.text(
            (540, d['top_h'] / 2), 
            d['top_text'], 
            font=font_top, 
            fill=d['top_color'], 
            anchor="mm", 
            align="center",
            spacing=d['top_lh']
        )
    except: pass

    # === [B. 중앙 4분할 그리드] ===
    grid_start_y = d['top_h']
    grid_end_y = 1920 - d['bot_h']
    grid_height = grid_end_y - grid_start_y
    
    cell_w = 1080 // 2
    cell_h = grid_height // 2
    
    positions = [
        (0, grid_start_y), (cell_w, grid_start_y),
        (0, grid_start_y + cell_h), (cell_w, grid_start_y + cell_h)
    ]

    for i, (name, pos) in enumerate(zip(names, positions)):
        img = load_saved_image(name)
        
        if img is None:
            img = Image.new('RGB', (cell_w, cell_h), (50, 50, 50))
            idraw = ImageDraw.Draw(img)
            idraw.text((cell_w/2, cell_h/2), "사진 없음", font=get_font(40), fill="white", anchor="mm")
        
        img_ratio = img.width / img.height
        target_ratio = cell_w / cell_h
        
        if img_ratio > target_ratio:
            new_width = int(img.height * target_ratio)
            offset = (img.width - new_width) // 2
            img = img.crop((offset, 0, offset + new_width, img.height))
        else:
            new_height = int(img.width / target_ratio)
            offset = (img.height - new_height) // 2
            img = img.crop((0, offset, img.width, offset + new_height))
            
        img = img.resize((cell_w, cell_h), Image.LANCZOS)
        canvas.paste(img, pos)
        
        label_text = f"{i+1}. {name}"
        label_h = 70
        label_y = pos[1] + cell_h - label_h
        
        draw.rectangle([pos[0], label_y, pos[0]+cell_w, pos[1]+cell_h], fill=d['label_bg'])
        draw.text((pos[0] + cell_w/2, label_y + label_h/2), label_text, font=font_label, fill=d['label_color'], anchor="mm")
        draw.rectangle([pos[0], pos[1], pos[0]+cell_w, pos[1]+cell_h], outline="black", width=2)

    # === [C. 하단 바] ===
    draw.rectangle([(0, 1920 - d['bot_h']), (1080, 1920)], fill=d['bot_bg'])
    
    try:
        draw.text(
            (540, 1920 - (d['bot_h'] / 2)), 
            d['bot_text'], 
            font=font_bot, 
            fill=d['bot_color'], 
            anchor="mm", 
            align="center",
            spacing=d['bot_lh']
        )
    except: pass

    return canvas

# --- [4. 메인 UI] ---
st.title("🏛️ 정치/인물 퀴즈 (영부인/배우자 편)")

col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.info("✅ 여기에 등록한 사진은 껐다 켜도 유지됩니다!")
    
    with st.expander("📸 인물 사진 등록 (영구 저장)", expanded=True):
        names_input = st.text_input("인물 이름 4명 (쉼표로 구분)", "김건희, 김정숙, 김혜경, 이순자")
        names = [n.strip() for n in names_input.split(',')]
        while len(names) < 4: names.append(f"인물 {len(names)+1}")
        names = names[:4]

        st.write("---")
        for name in names:
            col_u1, col_u2 = st.columns([3, 1])
            with col_u1:
                uploaded = st.file_uploader(f"'{name}' 사진 업로드", type=['jpg', 'png', 'jpeg'], key=f"up_{name}")
                if uploaded:
                    if save_uploaded_file(uploaded, name):
                        st.success(f"저장됨!")
            with col_u2:
                saved_img = load_saved_image(name)
                if saved_img:
                    st.image(saved_img, width=50)
                else:
                    st.caption("없음")

    with st.expander("⬆️ 상단바 디자인", expanded=False):
        top_text = st.text_area("상단 문구", "역대 영부인/배우자 중\n누구를\n가장 선호하나요?")
        top_h = st.slider("높이", 50, 400, 250)
        top_fs = st.slider("글자 크기", 20, 100, 55)
        top_lh = st.slider("줄 간격", 0, 100, 20, key="tlh")
        c1, c2 = st.columns(2)
        top_bg = c1.color_picker("배경색", "#000000", key="tbg")
        top_color = c2.color_picker("글자색", "#FFFF00", key="tc")

    with st.expander("⬇️ 하단바 디자인", expanded=False):
        bot_text = st.text_area("하단 문구", "정답을 댓글에 달면 정답을\n알려드립니다!!")
        bot_h = st.slider("높이", 50, 400, 200, key="bh")
        bot_fs = st.slider("글자 크기", 20, 100, 40, key="bfs")
        bot_lh = st.slider("줄 간격", 0, 100, 20, key="blh")
        c3, c4 = st.columns(2)
        bot_bg = c3.color_picker("배경색", "#000000", key="bbg")
        bot_color = c4.color_picker("글자색", "#FFFFFF", key="bc")

    with st.expander("🏷️ 이름표 디자인", expanded=False):
        label_size = st.slider("이름 크기", 20, 80, 40)
        c5, c6 = st.columns(2)
        label_bg = c5.color_picker("배경색", "#FF0000")
        label_color = c6.color_picker("글자색", "#FFFF00")
    
    bg_color = st.color_picker("전체 배경 (빈공간)", "#000000")

    design = {
        'bg_color': bg_color,
        'top_text': top_text, 'top_h': top_h, 'top_fs': top_fs, 'top_lh': top_lh, 'top_bg': top_bg, 'top_color': top_color,
        'bot_text': bot_text, 'bot_h': bot_h, 'bot_fs': bot_fs, 'bot_lh': bot_lh, 'bot_bg': bot_bg, 'bot_color': bot_color,
        'label_bg': label_bg, 'label_color': label_color, 'label_size': label_size
    }

with col_right:
    st.subheader("🖼️ 결과물 확인")
    
    if st.button("🚀 이미지 생성 (새로고침)", type="primary", use_container_width=True):
        st.session_state.gen = True
        
    final_img = create_quiz_image(names, design)
    st.image(final_img, caption="최종 결과물", use_container_width=True)
    
    buf = BytesIO()
    final_img.save(buf, format="JPEG", quality=100)
    st.download_button("💾 이미지 다운로드", buf.getvalue(), "shorts_quiz.jpg", "image/jpeg", use_container_width=True)