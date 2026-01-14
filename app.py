import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os
from io import BytesIO

# --- [1. 기본 설정 및 영구 저장소] ---
st.set_page_config(page_title="JJ 쇼츠 마스터 (디자인 수정판)", page_icon="🎨", layout="wide")

FONT_FILE = "NanumGothic-ExtraBold.ttf"
SAVE_DIR = "saved_images"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# --- [2. 기능 함수] ---
def get_font(size):
    if os.path.exists(FONT_FILE):
        return ImageFont.truetype(FONT_FILE, size)
    else:
        return ImageFont.load_default()

def save_uploaded_file(uploaded_file, name):
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file).convert("RGB")
            save_path = os.path.join(SAVE_DIR, f"{name}.jpg")
            image.save(save_path, quality=95)
            return True
        except: return False
    return False

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
    font_label = get_font(d['label_fs'])

    # === [A. 상단 바] ===
    draw.rectangle([(0, 0), (1080, d['top_h'])], fill=d['top_bg'])
    try:
        draw.text((540, d['top_h'] / 2), d['top_text'], font=font_top, fill=d['top_color'], anchor="mm", align="center", spacing=d['top_lh'])
    except: pass

    # === [B. 중앙 그리드 & 사진] ===
    grid_start_y = d['top_h']
    grid_end_y = 1920 - d['bot_h']
    grid_height = grid_end_y - grid_start_y
    
    cell_w = 1080 // 2
    cell_h = grid_height // 2
    
    positions = [
        (0, grid_start_y), (cell_w, grid_start_y),
        (0, grid_start_y + cell_h), (cell_w, grid_start_y + cell_h)
    ]

    target_names = names[:4]

    for i, (name, pos) in enumerate(zip(target_names, positions)):
        img = load_saved_image(name)
        if img is None:
            img = Image.new('RGB', (cell_w, cell_h), (50, 50, 50))
            ImageDraw.Draw(img).text((cell_w/2, cell_h/2), "사진 없음", font=get_font(40), fill="white", anchor="mm")
        
        # 이미지 줌(확대/축소) 로직 적용
        zoom = d['img_zoom']
        
        # 1. 기본 Center Crop 계산
        img_ratio = img.width / img.height
        target_ratio = cell_w / cell_h
        
        if img_ratio > target_ratio:
            new_width = int(img.height * target_ratio)
            crop_x = (img.width - new_width) // 2
            img_cropped = img.crop((crop_x, 0, crop_x + new_width, img.height))
        else:
            new_height = int(img.width / target_ratio)
            crop_y = (img.height - new_height) // 2
            img_cropped = img.crop((0, crop_y, img.width, crop_y + new_height))

        # 2. 줌 적용 (Zoom In)
        if zoom > 1.0:
            w, h = img_cropped.size
            crop_w = int(w / zoom)
            crop_h = int(h / zoom)
            cx, cy = w // 2, h // 2
            img_cropped = img_cropped.crop((cx - crop_w//2, cy - crop_h//2, cx + crop_w//2, cy + crop_h//2))
            
        img_final = img_cropped.resize((cell_w, cell_h), Image.LANCZOS)
        canvas.paste(img_final, pos)
        
        # 이름표 높이 조절
        label_h = d['label_h']
        label_y = pos[1] + cell_h - label_h
        
        # 이름표 배경 & 글자
        draw.rectangle([pos[0], label_y, pos[0]+cell_w, pos[1]+cell_h], fill=d['label_bg'])
        
        # [수정됨] 이름 앞에 숫자(i+1) 제거. 이름만 표시.
        draw.text((pos[0] + cell_w/2, label_y + label_h/2), name, font=font_label, fill=d['label_color'], anchor="mm")
        
        # 테두리
        draw.rectangle([pos[0], pos[1], pos[0]+cell_w, pos[1]+cell_h], outline="black", width=2)

    # === [C. 하단 바] ===
    draw.rectangle([(0, 1920 - d['bot_h']), (1080, 1920)], fill=d['bot_bg'])
    try:
        draw.text((540, 1920 - (d['bot_h'] / 2)), d['bot_text'], font=font_bot, fill=d['bot_color'], anchor="mm", align="center", spacing=d['bot_lh'])
    except: pass

    return canvas

# --- [4. 메인 UI] ---
st.title("🎨 쇼츠 이미지 생성기 (수정판)")

col_L, col_R = st.columns([1, 1.3])

with col_L:
    with st.expander("📸 인물 목록 & 사진 등록", expanded=True):
        default_names = "이재명, 한동훈, 조국, 이준석, 김건희, 김정숙, 김혜경, 이순자"
        names_input = st.text_area("인물 목록 (상위 4명 적용)", default_names, height=80)
        
        all_names = [n.strip() for n in names_input.split(',') if n.strip()]
        while len(all_names) < 4: all_names.append(f"인물 {len(all_names)+1}")
        target_names = all_names[:4]

        st.write(f"👇 **현재 선택: {', '.join(target_names)}**")
        for name in target_names:
            c1, c2 = st.columns([3,1])
            with c1:
                f = st.file_uploader(f"'{name}' 사진", type=['jpg','png','jpeg'], key=f"u_{name}")
                if f: save_uploaded_file(f, name)
            with c2:
                img = load_saved_image(name)
                if img: st.image(img, width=50)

    # === [디자인 조절 패널] ===
    st.header("🎚️ 디자인 세부 조절")
    
    with st.expander("1. 상단 바 (Top Bar)", expanded=False):
        top_text = st.text_area("상단 문구", "차기 대통령으로\n누구를\n가장 선호하나요?")
        # [수정됨] 기본 높이를 250 -> 400으로 늘려 사진 영역을 줄임
        top_h = st.slider("상단 높이", 50, 600, 400)
        top_fs = st.slider("상단 글자 크기", 20, 150, 55)
        top_lh = st.slider("상단 줄간격", 0, 100, 20)
        c1, c2 = st.columns(2)
        top_bg = c1.color_picker("배경색", "#000000", key="tb")
        top_color = c2.color_picker("글자색", "#FFFF00", key="tc")

    with st.expander("2. 사진 & 이름표 (Photo & Name)", expanded=True):
        st.markdown("### 🖼️ 사진 조절")
        img_zoom = st.slider("사진 확대/축소 (배율)", 1.0, 3.0, 1.0, 0.1, help="얼굴 위주로 확대할 때 사용하세요.")
        
        st.markdown("### 🏷️ 이름표 조절")
        label_h = st.slider("이름표 높이(두께)", 30, 200, 70)
        label_fs = st.slider("이름 글자 크기", 20, 100, 40)
        c3, c4 = st.columns(2)
        label_bg = c3.color_picker("이름표 배경", "#FF0000", key="lb")
        label_color = c4.color_picker("이름표 글자", "#FFFF00", key="lc")

    with st.expander("3. 하단 바 (Bottom Bar)", expanded=False):
        bot_text = st.text_area("하단 문구", "정답을 댓글에 달면 정답을\n알려드립니다!!")
        # [수정됨] 기본 높이를 200 -> 350으로 늘려 사진 영역을 줄임
        bot_h = st.slider("하단 높이", 50, 600, 350)
        bot_fs = st.slider("하단 글자 크기", 20, 150, 40)
        bot_lh = st.slider("하단 줄간격", 0, 100, 20)
        c5, c6 = st.columns(2)
        bot_bg = c5.color_picker("배경색", "#000000", key="bb")
        bot_color = c6.color_picker("글자색", "#FFFFFF", key="bc")

    bg_color = st.color_picker("전체 배경 (빈공간)", "#000000")

    design = {
        'bg_color': bg_color,
        'top_text': top_text, 'top_h': top_h, 'top_fs': top_fs, 'top_lh': top_lh, 'top_bg': top_bg, 'top_color': top_color,
        'bot_text': bot_text, 'bot_h': bot_h, 'bot_fs': bot_fs, 'bot_lh': bot_lh, 'bot_bg': bot_bg, 'bot_color': bot_color,
        'label_h': label_h, 'label_fs': label_fs, 'label_bg': label_bg, 'label_color': label_color,
        'img_zoom': img_zoom
    }

with col_R:
    st.subheader("🖼️ 미리보기")
    if st.button("🔄 이미지 생성 (적용)", type="primary", use_container_width=True):
        st.session_state.gen = True
        
    final_img = create_quiz_image(all_names, design)
    st.image(final_img, caption="최종 결과물", use_container_width=True)
    
    buf = BytesIO()
    final_img.save(buf, format="JPEG", quality=100)
    st.download_button("💾 이미지 다운로드", buf.getvalue(), "shorts_quiz.jpg", "image/jpeg", use_container_width=True)