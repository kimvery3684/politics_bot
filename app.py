<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>정치인 퀴즈 생성기 - Admin</title>
    <style>
        :root {
            --primary-red: #ff4d4d;
            --bg-gray: #f4f6f8;
            --panel-width: 350px;
        }
        * { box-sizing: border-box; outline: none; }
        body {
            margin: 0;
            padding: 0;
            font-family: 'Pretendard', sans-serif;
            background-color: var(--bg-gray);
            display: flex;
            height: 100vh;
            overflow: hidden;
        }

        /* [Left Sidebar - Design & Layout] */
        aside {
            width: var(--panel-width);
            background: #fff;
            border-right: 1px solid #ddd;
            display: flex;
            flex-direction: column;
            padding: 20px;
            box-shadow: 2px 0 10px rgba(0,0,0,0.05);
            z-index: 10;
        }

        .panel-header {
            font-size: 1.2rem;
            font-weight: 800;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        /* Tabs */
        .tabs {
            display: flex;
            border-bottom: 2px solid #eee;
            margin-bottom: 20px;
        }
        .tab {
            flex: 1;
            text-align: center;
            padding: 10px 0;
            font-size: 0.9rem;
            color: #888;
            cursor: pointer;
            position: relative;
        }
        .tab.active {
            color: var(--primary-red);
            font-weight: 700;
        }
        .tab.active::after {
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            width: 100%;
            height: 2px;
            background-color: var(--primary-red);
        }

        /* Controls */
        .control-group {
            margin-bottom: 25px;
        }
        .control-label {
            font-size: 0.85rem;
            color: #555;
            margin-bottom: 10px;
            font-weight: 600;
            display: flex;
            justify-content: space-between;
        }
        .val-display { color: var(--primary-red); font-size: 0.8rem; }
        
        input[type="range"] {
            width: 100%;
            -webkit-appearance: none;
            background: transparent;
        }
        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            height: 16px;
            width: 16px;
            border-radius: 50%;
            background: var(--primary-red);
            cursor: pointer;
            margin-top: -6px;
        }
        input[type="range"]::-webkit-slider-runnable-track {
            width: 100%;
            height: 4px;
            background: #ddd;
            border-radius: 2px;
        }

        .color-picker-row {
            display: flex;
            gap: 10px;
        }
        .color-box {
            width: 30px; height: 30px;
            border-radius: 4px;
            border: 1px solid #ccc;
            cursor: pointer;
        }

        /* [Right Content - Preview] */
        main {
            flex: 1;
            padding: 40px;
            display: flex;
            flex-direction: column;
            align-items: center;
            overflow-y: auto;
        }

        .toolbar {
            width: 100%;
            max-width: 900px;
            background: #fff;
            padding: 15px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: flex;
            gap: 20px;
            align-items: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        .btn {
            padding: 8px 16px;
            border: 1px solid #ddd;
            background: #fff;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 600;
            transition: 0.2s;
        }
        .btn:hover { background: #f0f0f0; }
        .btn-red { background: var(--primary-red); color: white; border: none; }
        .btn-red:hover { background: #e04444; }

        /* Preview Area (Phone Scale) */
        .preview-container {
            width: 360px; /* Mobile width */
            height: 640px; /* Mobile height */
            background-color: #000;
            position: relative;
            overflow: hidden;
            box-shadow: 0 0 30px rgba(0,0,0,0.3);
            border-radius: 20px;
            border: 8px solid #333;
        }

        /* Dynamic Elements */
        #preview-title {
            position: absolute;
            width: 100%;
            text-align: center;
            color: #ffd700; /* Default yellow */
            font-weight: 900;
            z-index: 10;
            padding: 0 10px;
            line-height: 1.3;
        }
        
        .grid-container {
            position: absolute;
            display: grid;
            grid-template-columns: 1fr 1fr;
            grid-template-rows: 1fr 1fr;
            gap: 10px;
            width: 90%;
            left: 5%;
        }

        .p-card {
            background: #222;
            border-radius: 8px;
            overflow: hidden;
            position: relative;
            display: flex;
            flex-direction: column;
        }
        .p-img {
            flex: 1;
            background-color: #555;
            overflow: hidden;
        }
        .p-img img { width: 100%; height: 100%; object-fit: cover; }
        .p-name {
            background: #000;
            color: #fff;
            text-align: center;
            padding: 5px 0;
            font-weight: bold;
            border-top: 2px solid #ffd700;
        }

        .guide-box {
            background: #e3f2fd;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 0.9rem;
            color: #1565c0;
            line-height: 1.4;
        }
    </style>
</head>
<body>

    <aside>
        <div class="panel-header">
            🎨 디자인 & 레이아웃
        </div>

        <div class="tabs">
            <div class="tab active" onclick="switchTab('layout')">위치/배치</div>
            <div class="tab" onclick="switchTab('style')">색상/크기</div>
            <div class="tab" onclick="switchTab('text')">문구</div>
        </div>

        <div class="guide-box">
            💡 여기서 위치와 크기를 조절하세요. <br>실시간으로 우측 화면에 반영됩니다.
        </div>

        <div id="tab-layout" class="tab-content">
            <div class="control-group">
                <div class="control-label">질문 위치 (Y좌표) <span class="val-display" id="val-title-y">10%</span></div>
                <input type="range" id="input-title-y" min="0" max="90" value="10" oninput="updatePreview()">
            </div>
            
            <div class="control-group">
                <div class="control-label">사진 뭉치 위치 (Y좌표) <span class="val-display" id="val-grid-y">30%</span></div>
                <input type="range" id="input-grid-y" min="0" max="90" value="30" oninput="updatePreview()">
            </div>

            <div class="control-group">
                <div class="control-label">사진 뭉치 너비 <span class="val-display" id="val-grid-w">90%</span></div>
                <input type="range" id="input-grid-w" min="50" max="100" value="90" oninput="updatePreview()">
            </div>
        </div>

        <div id="tab-style" class="tab-content" style="display:none;">
             <div class="control-group">
                <div class="control-label">질문 폰트 크기 <span class="val-display" id="val-font-s">24px</span></div>
                <input type="range" id="input-font-s" min="14" max="60" value="24" oninput="updatePreview()">
            </div>
            <div class="control-group">
                <div class="control-label">테두리 색상</div>
                <div class="color-picker-row">
                    <div class="color-box" style="background:#ffd700" onclick="changeBorder('#ffd700')"></div>
                    <div class="color-box" style="background:#ff00ff" onclick="changeBorder('#ff00ff')"></div>
                    <div class="color-box" style="background:#00ffff" onclick="changeBorder('#00ffff')"></div>
                    <div class="color-box" style="background:#ffffff" onclick="changeBorder('#ffffff')"></div>
                </div>
            </div>
        </div>

        <div id="tab-text" class="tab-content" style="display:none;">
            <div class="control-group">
                <div class="control-label">상단 문구 내용</div>
                <textarea id="input-title-text" rows="4" style="width:100%; border:1px solid #ddd; padding:10px; border-radius:4px;" oninput="updatePreview()">역대급 내로남불! 남이 하면 불륜, 내가 하면 로맨스인 자는?</textarea>
            </div>
        </div>
    </aside>

    <main>
        <div class="toolbar">
            <strong>🔥 데이터 소스:</strong>
            <button class="btn" onclick="loadCandidates('ruling')">🔴 여당 (국힘)</button>
            <button class="btn" onclick="loadCandidates('opposition')">🔵 야당 (민주/조국)</button>
            <button class="btn" onclick="loadCandidates('vip')">👑 VIP (대통령)</button>
            <div style="flex-grow:1"></div>
            <button class="btn btn-red">🚀 퀴즈 이미지 생성</button>
        </div>

        <div class="preview-container">
            <h1 id="preview-title">역대급 내로남불! 남이 하면 불륜, 내가 하면 로맨스인 자는?</h1>
            
            <div class="grid-container" id="preview-grid">
                <div class="p-card"><div class="p-img"></div><div class="p-name">1. 후보</div></div>
                <div class="p-card"><div class="p-img"></div><div class="p-name">2. 후보</div></div>
                <div class="p-card"><div class="p-img"></div><div class="p-name">3. 후보</div></div>
                <div class="p-card"><div class="p-img"></div><div class="p-name">4. 후보</div></div>
            </div>
        </div>
    </main>

    <script>
        // [Data: Political Figures for High Traffic]
        const data = {
            vip: [
                { name: "윤석열", party: "대통령" },
                { name: "김건희", party: "영부인" }
            ],
            ruling: [ // People Power Party & Key Figures (25)
                "한동훈", "오세훈", "홍준표", "안철수", "나경원", 
                "원희룡", "추경호", "배현진", "권성동", "장제원", 
                "김기현", "윤상현", "김재섭", "조정훈", "인요한",
                "김은혜", "박수영", "성일종", "김웅", "박정훈",
                "이상민", "윤희숙", "김민전", "김용태", "유승민"
            ].map(name => ({ name, party: "국민의힘" })),
            
            opposition: [ // Democratic Party & Opposition Block (25)
                "이재명", "조국", "추미애", "정청래", "박찬대",
                "고민정", "이준석", "천하람", "김남국", "최강욱",
                "김민석", "서영교", "장경태", "박지원", "정동영",
                "박용진", "김동연", "김경수", "임종석", "우상호",
                "이낙연", "김두관", "양문석", "김준혁", "이언주"
            ].map(name => ({ name, party: "야권" }))
        };

        // [Logic: Tab Switching]
        function switchTab(tabName) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            event.target.classList.add('active');
            
            document.querySelectorAll('.tab-content').forEach(c => c.style.display = 'none');
            document.getElementById('tab-' + tabName).style.display = 'block';
        }

        // [Logic: Live Preview Update]
        function updatePreview() {
            // Get Values
            const titleY = document.getElementById('input-title-y').value;
            const gridY = document.getElementById('input-grid-y').value;
            const gridW = document.getElementById('input-grid-w').value;
            const fontS = document.getElementById('input-font-s').value;
            const titleText = document.getElementById('input-title-text').value;

            // Apply Values
            const titleEl = document.getElementById('preview-title');
            const gridEl = document.getElementById('preview-grid');

            // Text
            titleEl.innerText = titleText;
            titleEl.style.top = titleY + '%';
            titleEl.style.fontSize = fontS + 'px';

            // Grid
            gridEl.style.top = gridY + '%';
            gridEl.style.width = gridW + '%';
            gridEl.style.left = ((100 - gridW) / 2) + '%'; // Center align
            
            // Labels
            document.getElementById('val-title-y').innerText = titleY + '%';
            document.getElementById('val-grid-y').innerText = gridY + '%';
            document.getElementById('val-grid-w').innerText = gridW + '%';
            document.getElementById('val-font-s').innerText = fontS + 'px';
        }

        function changeBorder(color) {
            const cards = document.querySelectorAll('.p-name');
            cards.forEach(card => {
                card.style.borderTopColor = color;
                card.style.color = color === '#ffffff' ? '#000' : color;
                if(color === '#ffffff') card.style.background = '#fff';
                else card.style.background = '#000';
            });
            document.getElementById('preview-title').style.color = color;
        }

        // [Logic: Load Candidates]
        function loadCandidates(type) {
            let pool = [];
            if (type === 'vip') {
                pool = data.vip;
                // VIP는 2명이므로 나머지 2명은 랜덤 채움
                const extras = [...data.ruling, ...data.opposition].sort(() => 0.5 - Math.random()).slice(0, 2);
                pool = [...pool, ...extras];
            } else {
                pool = data[type].sort(() => 0.5 - Math.random()).slice(0, 4);
            }

            const gridEl = document.getElementById('preview-grid');
            gridEl.innerHTML = ''; // Clear

            pool.forEach((person, index) => {
                const imgUrl = `https://via.placeholder.com/150/333/fff?text=${encodeURIComponent(person.name)}`;
                
                const html = `
                    <div class="p-card">
                        <div class="p-img">
                            <img src="${imgUrl}" alt="${person.name}">
                        </div>
                        <div class="p-name" style="border-top-color: #ffd700">
                            ${index + 1}. ${person.name}
                        </div>
                    </div>
                `;
                gridEl.innerHTML += html;
            });
            
            // Re-apply current border style
            updatePreview(); 
        }

        // Init
        loadCandidates('ruling');
        updatePreview();

    </script>
</body>
</html>