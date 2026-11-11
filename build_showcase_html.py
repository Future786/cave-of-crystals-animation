#!/usr/bin/env python3
"""
Builds an interactive, high-retention HTML video showcase and player for all 10 topics.
Features tabbed topic switcher, custom video player, narration script inspector,
direct 1-click download buttons, and visual storyboard sheets.
"""

import os
import json
from topics_config import TOPICS

REPO_DIR = "/home/antigravity/Future786/cave-of-crystals-animation"
OUTPUT_HTML = os.path.join(REPO_DIR, "video_showcase.html")

TOPIC_ICONS = {
    "01_mariana_trench": "🌊",
    "02_kola_borehole": "⛏️",
    "03_the_bloop": "🐋",
    "04_lake_vostok": "❄️",
    "05_darvaza_crater": "🔥",
    "06_tardigrades": "🦠",
    "07_wow_signal": "📡",
    "08_chernobyl_foot": "☢️",
    "09_devils_kettle": "💧",
    "10_silurian_hypothesis": "⏳"
}

def generate_showcase():
    topics_data = []
    for t in TOPICS:
        t_id = t["id"]
        timing_path = os.path.join(REPO_DIR, "audio", t_id, "timing.json")
        duration = 65.0
        sentences = t["sentences"]
        if os.path.exists(timing_path):
            with open(timing_path, "r") as f:
                t_info = json.load(f)
                duration = t_info.get("duration", 65.0)
                sentences = t_info.get("sentences", t["sentences"])

        topics_data.append({
            "id": t_id,
            "title": t["title"],
            "tag": t["tag"],
            "icon": TOPIC_ICONS.get(t_id, "🎬"),
            "duration": round(duration, 1),
            "sentences": sentences,
            "contact_img": f"{t_id}_contact.png",
            "mobile_video": f"videos/{t_id}_Mobile.mp4",
            "hd_video": f"videos/{t_id}_HD.mp4",
            "scene_json": f"scenes/{t_id}.json",
            "audio_file": f"audio/{t_id}_final_audio.mp3"
        })

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Viral Explainer Studio — 10 Topics (Continuous Motion & Complete Subtitles)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --bg: #070d14;
      --card-bg: #0e1724;
      --border: #1a2a3e;
      --accent-cyan: #00f2fe;
      --accent-gold: #f5a623;
      --accent-red: #ef4444;
      --text: #e6edf3;
      --text-muted: #8b949e;
    }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: 'Poppins', sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 32px 16px 80px;
    }}
    header {{
      text-align: center;
      max-width: 960px;
      margin-bottom: 28px;
    }}
    .badge-bar {{
      display: flex;
      justify-content: center;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 14px;
    }}
    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 16px;
      border-radius: 999px;
      background: rgba(0, 242, 254, 0.12);
      color: var(--accent-cyan);
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      border: 1px solid rgba(0, 242, 254, 0.35);
    }}
    .badge-gold {{
      background: rgba(245, 166, 35, 0.12);
      color: var(--accent-gold);
      border-color: rgba(245, 166, 35, 0.35);
    }}
    h1 {{
      font-size: 32px;
      font-weight: 900;
      color: #fff;
      margin-bottom: 8px;
      letter-spacing: -0.5px;
    }}
    p.subtitle {{
      font-size: 15px;
      color: var(--text-muted);
      line-height: 1.6;
    }}
    .topics-nav {{
      display: flex;
      overflow-x: auto;
      gap: 10px;
      max-width: 1200px;
      width: 100%;
      padding: 12px 4px 18px;
      scrollbar-width: thin;
      scrollbar-color: var(--border) transparent;
      margin-bottom: 24px;
    }}
    .tab-btn {{
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 10px 18px;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 14px;
      color: var(--text-muted);
      font-size: 13.5px;
      font-weight: 700;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.2s ease;
      font-family: inherit;
    }}
    .tab-btn:hover {{
      border-color: var(--accent-cyan);
      color: #fff;
      transform: translateY(-2px);
    }}
    .tab-btn.active {{
      background: linear-gradient(135deg, rgba(0, 242, 254, 0.2), rgba(79, 172, 254, 0.1));
      border-color: var(--accent-cyan);
      color: #fff;
      box-shadow: 0 4px 18px rgba(0, 242, 254, 0.25);
    }}
    .tab-btn .tab-icon {{
      font-size: 18px;
    }}
    .main-grid {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 32px;
      max-width: 1200px;
      width: 100%;
    }}
    @media (min-width: 960px) {{
      .main-grid {{
        grid-template-columns: 420px 1fr;
      }}
    }}
    .player-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 20px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .video-wrapper {{
      position: relative;
      width: 100%;
      aspect-ratio: 9 / 16;
      background: #000;
      border-radius: 16px;
      overflow: hidden;
      border: 1px solid #233546;
      box-shadow: 0 8px 30px rgba(0,0,0,0.5);
    }}
    video {{
      width: 100%;
      height: 100%;
      object-fit: contain;
      display: block;
    }}
    .download-btns {{
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}
    .btn {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 12px 18px;
      border-radius: 12px;
      font-size: 13.5px;
      font-weight: 700;
      text-decoration: none;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .btn-primary {{
      background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
      color: #041019;
      box-shadow: 0 4px 14px rgba(0, 242, 254, 0.3);
    }}
    .btn-primary:hover {{
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(0, 242, 254, 0.45);
    }}
    .btn-secondary {{
      background: #14202c;
      color: #e6edf3;
      border: 1px solid #233546;
    }}
    .btn-secondary:hover {{
      background: #1c2c3d;
      border-color: var(--accent-cyan);
      transform: translateY(-2px);
    }}
    .details-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 20px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }}
    .topic-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 12px;
      flex-wrap: wrap;
      border-bottom: 1px solid var(--border);
      padding-bottom: 16px;
    }}
    .topic-title {{
      font-size: 22px;
      font-weight: 800;
      color: #fff;
    }}
    .topic-meta {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-top: 6px;
    }}
    .meta-tag {{
      font-size: 11px;
      font-weight: 700;
      padding: 3px 10px;
      border-radius: 6px;
      background: #142436;
      color: #79c0ff;
      border: 1px solid #233e5c;
    }}
    .script-section h3 {{
      font-size: 16px;
      font-weight: 800;
      color: var(--accent-gold);
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .script-list {{
      display: flex;
      flex-direction: column;
      gap: 12px;
      max-height: 480px;
      overflow-y: auto;
      padding-right: 6px;
    }}
    .script-item {{
      background: #08111c;
      border: 1px solid #162536;
      border-radius: 12px;
      padding: 12px 16px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      transition: all 0.2s;
    }}
    .script-item:hover {{
      border-color: var(--accent-cyan);
    }}
    .script-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 11.5px;
      color: var(--text-muted);
      font-family: 'JetBrains Mono', monospace;
    }}
    .script-time {{
      color: var(--accent-cyan);
      font-weight: 600;
    }}
    .script-text {{
      font-size: 14px;
      line-height: 1.5;
      color: #cbd5e1;
    }}
    .script-caption-box {{
      background: rgba(5, 12, 18, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 8px;
      padding: 6px 12px;
      font-size: 13px;
      font-weight: 700;
      color: #fff;
      display: inline-block;
      margin-top: 4px;
    }}
    .script-caption-box span.hl {{
      color: var(--accent-gold);
    }}
    .script-caption-box span.red {{
      color: var(--accent-red);
    }}
    .storyboard-preview {{
      margin-top: 10px;
      border-radius: 12px;
      overflow: hidden;
      border: 1px solid var(--border);
    }}
    .storyboard-preview img {{
      width: 100%;
      height: auto;
      display: block;
      cursor: pointer;
      transition: transform 0.2s;
    }}
    .storyboard-preview img:hover {{
      transform: scale(1.01);
    }}
    .feature-box {{
      background: #09131f;
      border: 1px solid #1a2a3e;
      border-radius: 14px;
      padding: 16px;
      margin-top: 24px;
    }}
    .feature-box h4 {{
      font-size: 14px;
      font-weight: 800;
      color: var(--accent-cyan);
      margin-bottom: 8px;
    }}
    .feature-box ul {{
      list-style-type: disc;
      padding-left: 20px;
      font-size: 13px;
      color: var(--text-muted);
      line-height: 1.6;
    }}
  </style>
</head>
<body>

  <header>
    <div class="badge-bar">
      <div class="badge">10 New Videos Completed</div>
      <div class="badge badge-gold">100% Full Subtitle Coverage</div>
      <div class="badge">Continuous Procedural Motion</div>
    </div>
    <h1>Viral Scientific Explainer Studio</h1>
    <p class="subtitle">
      10 completely original, narrated nature and extreme science explainer animations.<br>
      Engineered for maximum viewer retention, 9:16 vertical shorts, and complete non-truncated captions.
    </p>
  </header>

  <!-- Topic Selector Tabs -->
  <div class="topics-nav" id="topicsNav"></div>

  <!-- Main Player & Detail Grid -->
  <div class="main-grid">
    <!-- Left: Video Player & Downloads -->
    <div class="player-card">
      <div class="video-wrapper">
        <video id="mainVideo" controls autoplay playsinline loop></video>
      </div>
      <div class="download-btns">
        <a id="btnDownloadMobile" href="#" download class="btn btn-primary">
          📱 Download Mobile Video (540x960 MP4)
        </a>
        <a id="btnDownloadHD" href="#" download class="btn btn-secondary">
          🚀 Download Full HD Video (1080x1920 MP4)
        </a>
        <a id="btnDownloadContact" href="#" download class="btn btn-secondary">
          🖼️ Download Storyboard Sheet (PNG)
        </a>
      </div>
      <div class="feature-box">
        <h4>✨ Key Upgrades & Fixes Applied:</h4>
        <ul>
          <li><strong>Full-Frame 9:16 ViewBox (No Crop / Zoom):</strong> Fixed SVG coordinate scaling so 100% of the frame is visible, centered, and sharp without any top-left zoom or edge cutoff.</li>
          <li><strong>10 Distinct Visual Themes:</strong> Each video now has a completely unique visual atmosphere (Abyss, Magma, Green Sonar Radar, Glacial Frost, Fiery Inferno, SEM Microscope, Nebula Cosmos, Ionizing Radiation, Rhyolite Gorge, Epoch Strata).</li>
          <li><strong>100% Spoken Subtitles (Auto-Wrapping):</strong> Every spoken sentence is dynamically multi-line wrapped in a frosted dark-glass pill box with zero edge clipping and colored keyword accents.</li>
          <li><strong>Rich Vector Infographics:</strong> Custom-tailored scientific diagrams for each topic (Everest scale, derrick cross-section, hydrophone spectrogram, Europa probe, methane vents, tardigrade anatomy, Big Ear dish, Elephant's Foot, gorge split, and cosmic clock).</li>
        </ul>
      </div>
    </div>

    <!-- Right: Script, Timing, and Storyboard Contact Sheet -->
    <div class="details-card">
      <div class="topic-header">
        <div>
          <div class="topic-title" id="topicTitle">Loading...</div>
          <div class="topic-meta" id="topicMeta"></div>
        </div>
      </div>

      <div class="script-section">
        <h3>🎙️ Full Narration Script & Synchronized Subtitles</h3>
        <div class="script-list" id="scriptList"></div>
      </div>

      <div class="script-section">
        <h3>📊 Visual Storyboard Contact Sheet</h3>
        <div class="storyboard-preview">
          <img id="contactImg" src="" alt="Storyboard Contact Sheet">
        </div>
      </div>
    </div>
  </div>

  <script>
    const topics = {json.dumps(topics_data, indent=2)};
    let currentIndex = 0;

    const topicsNav = document.getElementById('topicsNav');
    const mainVideo = document.getElementById('mainVideo');
    const topicTitle = document.getElementById('topicTitle');
    const topicMeta = document.getElementById('topicMeta');
    const scriptList = document.getElementById('scriptList');
    const contactImg = document.getElementById('contactImg');
    const btnDownloadMobile = document.getElementById('btnDownloadMobile');
    const btnDownloadHD = document.getElementById('btnDownloadHD');
    const btnDownloadContact = document.getElementById('btnDownloadContact');

    function renderNav() {{
      topicsNav.innerHTML = '';
      topics.forEach((t, i) => {{
        const btn = document.createElement('button');
        btn.className = 'tab-btn' + (i === currentIndex ? ' active' : '');
        btn.innerHTML = `<span class="tab-icon">${{t.icon}}</span><span>${{i+1}}. ${{t.title}}</span>`;
        btn.onclick = () => selectTopic(i);
        topicsNav.appendChild(btn);
      }});
    }}

    function formatCaption(text) {{
      return text
        .replace(/\\*([^*]+)\\*/g, '<span class="hl">$1</span>')
        .replace(/!([^!]+)!/g, '<span class="red">$1</span>')
        .replace(/\\n/g, '<br>');
    }}

    function selectTopic(index) {{
      currentIndex = index;
      renderNav();
      const t = topics[index];

      // Update Video Source
      mainVideo.src = t.mobile_video;
      mainVideo.load();
      mainVideo.play().catch(() => {{}});

      // Update Title & Meta
      topicTitle.textContent = `${{t.icon}} ${{t.title}}`;
      topicMeta.innerHTML = `
        <span class="meta-tag">⏱️ ${{t.duration}} SECONDS</span>
        <span class="meta-tag">📍 ${{t.tag}}</span>
        <span class="meta-tag">🎬 9:16 VERTICAL SHORTS</span>
      `;

      // Update Downloads
      btnDownloadMobile.href = t.mobile_video;
      btnDownloadHD.href = t.hd_video;
      btnDownloadContact.href = t.contact_img;

      // Update Storyboard
      contactImg.src = t.contact_img;

      // Update Script List
      scriptList.innerHTML = '';
      (t.sentences || []).forEach(s => {{
        const item = document.createElement('div');
        item.className = 'script-item';
        item.innerHTML = `
          <div class="script-top">
            <span class="script-time">⏱️ ${{s.start || 0}}s – ${{s.end || 0}}s</span>
            <span>SHOT #${{(s.shot != null ? s.shot + 1 : 1)}}</span>
          </div>
          <div class="script-text">"${{s.spoken || s.text}}"</div>
          <div>
            <div class="script-caption-box">
              ${{formatCaption(s.text)}}
            </div>
          </div>
        `;
        scriptList.appendChild(item);
      }});
    }}

    // Initialize
    renderNav();
    selectTopic(0);
  </script>
</body>
</html>
"""
    with open(OUTPUT_HTML, "w") as f:
        f.write(html)
    print(f"Wrote {OUTPUT_HTML}")

if __name__ == "__main__":
    generate_showcase()
