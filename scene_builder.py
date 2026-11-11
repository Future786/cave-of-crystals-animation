#!/usr/bin/env python3
"""
Generates rich, distinct KazChart Scene JSONs for 10 unique scientific documentary topics.
Each topic possesses its own unique preset, atmospheric background generator,
custom SVG vector artwork, synchronized non-truncated subtitles, and procedural animation.
"""

import json
import os
from topics_config import TOPICS

def build_topic_scenes(topic, timing_data, output_dir="/home/antigravity/Future786/cave-of-crystals-animation/scenes"):
    os.makedirs(output_dir, exist_ok=True)
    topic_id = topic["id"]
    sentences = timing_data["sentences"]
    total_dur = timing_data["duration"]
    preset_mode = topic.get("preset", "abyss")

    # Group sentences by shot index
    shot_groups = {}
    for s in sentences:
        shot_idx = s["shot"]
        if shot_idx not in shot_groups:
            shot_groups[shot_idx] = []
        shot_groups[shot_idx].append(s)

    num_shots = len(shot_groups)
    shots = []
    
    # Calculate shot start and end times based on sentence timestamps
    for s_idx in range(num_shots):
        group = shot_groups[s_idx]
        shot_start = 0.0 if s_idx == 0 else group[0]["start"] - 0.15
        if s_idx == num_shots - 1:
            shot_end = total_dur
        else:
            next_group = shot_groups[s_idx + 1]
            shot_end = next_group[0]["start"] - 0.15

        dur = shot_end - shot_start

        # Elements for this shot
        elements = [
            {
                "type": "tag",
                "text": topic["tag"],
                "x": 80,
                "y": 180,
                "size": 34,
                "box": True
            }
        ]

        # Add topic-specific custom visual vector art and infographic elements
        visuals = get_shot_visuals(topic_id, s_idx, dur)
        elements.extend(visuals)

        # Add complete synchronized captions for all sentences in this shot
        for sent in group:
            t0 = max(0.1, round(sent["start"] - shot_start, 2))
            t1 = min(round(dur - 0.05, 2), round(sent["end"] - shot_start + 0.15, 2))
            elements.append({
                "type": "caption",
                "text": sent["text"],
                "y": 1680,
                "size": 42,
                "t0": t0,
                "t1": t1,
                "fade": 0.22,
                "box": True
            })

        # Camera & background styling
        depth_val = 0.4 + (s_idx / max(1, num_shots - 1)) * 0.55
        shot_bg = {
            "mode": preset_mode,
            "depth": round(depth_val, 2),
            "particleCount": 45
        }
        if topic_id == "01_mariana_trench":
            shot_bg["rays"] = (s_idx in [0, 1, 6])
            if s_idx == 2:
                shot_bg["spotlight"] = {"x": 540, "w": 420}

        shots.append({
            "start": round(shot_start, 2),
            "end": round(shot_end, 2),
            "bg": shot_bg,
            "camera": {
                "zoomFrom": 1.0,
                "zoomTo": 1.12,
                "x": 540,
                "y": 960,
                "panX": 20 if s_idx % 2 == 1 else -20
            },
            "fadeIn": 0.35 if s_idx == 0 else 0,
            "fadeOut": 0.4 if s_idx == num_shots - 1 else 0,
            "elements": elements
        })

    scene_data = {
        "preset": preset_mode,
        "width": 1080,
        "height": 1920,
        "fps": 24,
        "grain": 0.04,
        "tokens": topic.get("tokens", {}),
        "audio": timing_data["audio_path"],
        "shots": shots
    }

    scene_file = os.path.join(output_dir, f"{topic_id}.json")
    with open(scene_file, "w") as f:
        json.dump(scene_data, f, indent=2)

    return scene_file

def get_shot_visuals(topic_id, s_idx, dur):
    """Returns rich, topic-specific vector artwork, diagrams, meters, and HUD telemetry."""
    elements = []

    # =========================================================================
    # 1. MARIANA TRENCH (Challenger Deep)
    # =========================================================================
    if "mariana" in topic_id:
        if s_idx == 0:
            elements.append({
                "type": "svg",
                "markup": """
                <g opacity="0.85">
                  <path d="M 80 440 L 440 1150 L 640 1150 L 1000 440" stroke="#00f2fe" stroke-width="6" fill="none" opacity="0.5"/>
                  <path d="M 440 1150 L 540 1350 L 640 1150 Z" fill="#00f2fe" opacity="0.25"/>
                  <line x1="540" y1="440" x2="540" y2="1350" stroke="#ffd166" stroke-width="3" stroke-dasharray="14,10" opacity="0.7"/>
                  <circle cx="540" cy="1350" r="14" fill="#ff3b30"/>
                  <text x="540" y="1400" font-family="Poppins" font-size="28" font-weight="800" fill="#ff3b30" text-anchor="middle">CHALLENGER DEEP: -10,994M</text>
                </g>
                """
            })
            elements.append({
                "type": "bignumber",
                "from": 0, "to": 10994, "suffix": " m",
                "x": 540, "y": 720, "size": 130, "color": "#00f2fe", "dur": 2.8, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "PACIFIC HADAL ZONE",
                "x": 310, "y": 820, "size": 26, "t0": 0.6
            })
        elif s_idx == 1:
            elements.append({
                "type": "svg",
                "markup": """
                <g opacity="0.9">
                  <!-- Bathyscaphe Trieste Submersible -->
                  <rect x="360" y="680" width="360" height="130" rx="30" fill="#e2e8f0" stroke="#00f2fe" stroke-width="4"/>
                  <circle cx="540" cy="850" r="70" fill="#475569" stroke="#ffd166" stroke-width="6"/>
                  <circle cx="540" cy="850" r="28" fill="#00f2fe" opacity="0.8"/>
                  <!-- Searchlight Beams -->
                  <polygon points="560,860 920,1100 840,1180 540,880" fill="#00f2fe" opacity="0.25"/>
                  <text x="540" y="750" font-family="Poppins" font-size="30" font-weight="900" fill="#0f172a" text-anchor="middle">TRIESTE 1960</text>
                </g>
                """
            })
            elements.append({
                "type": "pill",
                "text": "DEEP SEA BATHYSCAPHE",
                "x": 310, "y": 980, "size": 24, "t0": 0.8
            })
        elif s_idx == 2:
            elements.append({
                "type": "svg",
                "markup": """
                <g opacity="0.85">
                  <!-- Mount Everest Inverted Comparison -->
                  <polygon points="540,650 360,1100 720,1100" fill="none" stroke="#ffd166" stroke-width="5" stroke-dasharray="10,6"/>
                  <line x1="280" y1="520" x2="800" y2="520" stroke="#00f2fe" stroke-width="4"/>
                  <text x="540" y="500" font-family="Poppins" font-size="28" font-weight="700" fill="#00f2fe" text-anchor="middle">SURFACE OCEAN LEVEL</text>
                  <text x="540" y="880" font-family="Poppins" font-size="34" font-weight="800" fill="#ffd166" text-anchor="middle">MT. EVEREST (8,848M)</text>
                </g>
                """
            })
            elements.append({
                "type": "stamp",
                "text": "BURIED UNDER 2,000M WATER",
                "color": "#ff3b30",
                "x": 540, "y": 1020, "size": 44, "rotate": -4, "t0": 1.4
            })
        elif s_idx == 3:
            elements.append({
                "type": "meter",
                "x": 160, "y": 740, "w": 760, "value": 1.0,
                "number": 1080, "unit": " ATM", "title": "HYDROSTATIC WATER PRESSURE", "dur": 2.2, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "8 TONS CRUSHING FORCE PER SQ INCH",
                "tone": "red",
                "x": 220, "y": 860, "size": 26, "t0": 1.2
            })
        elif s_idx == 4:
            elements.append({
                "type": "creature",
                "kind": "fish",
                "x": 540, "y": 760, "scale": 1.7,
                "mode": "ghost", "swim": {"vx": 22, "vy": 6}
            })
            elements.append({
                "type": "pill",
                "text": "MARIANA SNAILFISH • CARTILAGE SKELETON",
                "x": 200, "y": 940, "size": 24, "t0": 0.8
            })
        elif s_idx == 5:
            elements.append({
                "type": "svg",
                "markup": """
                <g opacity="0.85">
                  <!-- Giant Xenophyophore Cell -->
                  <circle cx="540" cy="780" r="110" fill="#00f2fe" opacity="0.15" stroke="#00f2fe" stroke-width="4"/>
                  <circle cx="540" cy="780" r="60" fill="#00f2fe" opacity="0.3"/>
                  <line x1="430" y1="780" x2="650" y2="780" stroke="#ffd166" stroke-width="3"/>
                  <line x1="540" y1="670" x2="540" y2="890" stroke="#ffd166" stroke-width="3"/>
                </g>
                """
            })
            elements.append({
                "type": "bignumber",
                "from": 1, "to": 20, "suffix": " cm",
                "x": 540, "y": 750, "size": 110, "color": "#ffd166", "dur": 2.0, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "GIANT SINGLE-CELLED XENOPHYOPHORE",
                "x": 210, "y": 920, "size": 24, "t0": 0.8
            })
        else:
            elements.append({
                "type": "stamp",
                "text": "LIFE CONQUERED THE ABYSS",
                "color": "#00f2fe",
                "x": 540, "y": 800, "size": 52, "rotate": -3, "t0": 1.0
            })

    # =========================================================================
    # 2. KOLA SUPERDEEP BOREHOLE
    # =========================================================================
    elif "kola" in topic_id:
        if s_idx == 0:
            elements.append({
                "type": "svg",
                "markup": """
                <g opacity="0.85">
                  <!-- Drilling Derrick & Subterranean Shaft -->
                  <polygon points="540,420 460,650 620,650" fill="none" stroke="#ff9f1c" stroke-width="6"/>
                  <line x1="540" y1="650" x2="540" y2="1250" stroke="#ff9f1c" stroke-width="8"/>
                  <rect x="420" y="650" width="240" height="20" fill="#ff9f1c"/>
                  <text x="540" y="630" font-family="Poppins" font-size="26" font-weight="800" fill="#ff9f1c" text-anchor="middle">DERRICK SG-3</text>
                </g>
                """
            })
            elements.append({
                "type": "bignumber",
                "from": 0, "to": 12262, "suffix": " m",
                "x": 540, "y": 780, "size": 125, "color": "#ff9f1c", "dur": 2.8, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "DEEPEST ARTIFICIAL HOLE ON EARTH",
                "x": 250, "y": 880, "size": 24, "t0": 0.6
            })
        elif s_idx == 1:
            elements.append({
                "type": "svg",
                "markup": """
                <g opacity="0.85">
                  <!-- Strata Cross Section -->
                  <rect x="180" y="520" width="720" height="120" fill="#2d2218" stroke="#ff9f1c" stroke-width="3"/>
                  <text x="540" y="590" font-family="Poppins" font-size="28" font-weight="700" fill="#fff" text-anchor="middle">BALTIC CONTINENTAL SHIELD</text>
                  <rect x="180" y="670" width="720" height="150" fill="#1f1610" stroke="#ff9f1c" stroke-width="3"/>
                  <text x="540" y="750" font-family="Poppins" font-size="28" font-weight="700" fill="#ff9f1c" text-anchor="middle">METAMORPHIC FRACTURE ZONE</text>
                </g>
                """
            })
            elements.append({
                "type": "pill",
                "text": "7.6 MILES INTO EARTH'S CRUST",
                "x": 310, "y": 920, "size": 26, "t0": 0.8
            })
        elif s_idx == 2:
            elements.append({
                "type": "pill",
                "text": "BOILING HYDROTHERMAL FLUID & HYDROGEN",
                "tone": "red",
                "x": 200, "y": 760, "size": 24, "t0": 0.6
            })
            elements.append({
                "type": "stamp",
                "text": "FRACTURED CRUST",
                "color": "#ff9f1c",
                "x": 540, "y": 880, "size": 52, "t0": 1.5
            })
        elif s_idx == 3:
            elements.append({
                "type": "svg",
                "markup": """
                <g opacity="0.85">
                  <!-- Micro-Fossil in Lens -->
                  <circle cx="540" cy="740" r="120" fill="#1c130d" stroke="#ff9f1c" stroke-width="5"/>
                  <circle cx="540" cy="740" r="60" fill="none" stroke="#ffd600" stroke-width="3" stroke-dasharray="8,6"/>
                  <path d="M510,720 Q540,680 570,720 Q590,750 570,780 Q540,800 510,770 Z" fill="#ffd600" opacity="0.6"/>
                </g>
                """
            })
            elements.append({
                "type": "pill",
                "text": "2-BILLION-YEAR-OLD PLANKTON FOSSILS",
                "x": 220, "y": 920, "size": 24, "t0": 0.8
            })
        elif s_idx == 4:
            elements.append({
                "type": "bignumber",
                "from": 20, "to": 180, "suffix": " °C",
                "x": 540, "y": 740, "size": 130, "color": "#ff3b30", "dur": 2.2, "t0": 0.3
            })
            elements.append({
                "type": "stamp",
                "text": "ROCK TURNS TO PLASTIC",
                "color": "#ff3b30",
                "x": 540, "y": 900, "size": 48, "rotate": -6, "t0": 1.4
            })
        elif s_idx == 5:
            elements.append({
                "type": "pill",
                "text": "DRILL BITS MELTED BY FLOWING ROCK",
                "tone": "red",
                "x": 240, "y": 800, "size": 26, "t0": 0.6
            })
            elements.append({
                "type": "redx",
                "x": 540, "y": 940, "size": 80, "t0": 1.4
            })
        else:
            elements.append({
                "type": "svg",
                "markup": """
                <g opacity="0.9">
                  <!-- Welded Steel Borehole Cap -->
                  <circle cx="540" cy="720" r="130" fill="#475569" stroke="#94a3b8" stroke-width="8"/>
                  <circle cx="540" cy="720" r="90" fill="#1e293b" stroke="#f59e0b" stroke-width="4"/>
                  <!-- Bolts -->
                  <circle cx="540" cy="620" r="12" fill="#cbd5e1"/>
                  <circle cx="540" cy="820" r="12" fill="#cbd5e1"/>
                  <circle cx="440" cy="720" r="12" fill="#cbd5e1"/>
                  <circle cx="640" cy="720" r="12" fill="#cbd5e1"/>
                  <text x="540" y="730" font-family="Poppins" font-size="28" font-weight="900" fill="#f8fafc" text-anchor="middle">SG-3 • 12,262M</text>
                </g>
                """
            })
            elements.append({
                "type": "stamp",
                "text": "WELDED SHUT FOREVER",
                "color": "#e0453a",
                "x": 540, "y": 930, "size": 52, "rotate": -5, "t0": 1.2
            })

    # =========================================================================
    # 3. THE BLOOP (Deep Ocean Acoustic Anomaly)
    # =========================================================================
    elif "bloop" in topic_id:
        if s_idx == 0:
            elements.append({
                "type": "pill",
                "text": "NOAA SOSUS HYDROPHONE ARRAY",
                "x": 250, "y": 760, "size": 26, "t0": 0.5
            })
            elements.append({
                "type": "svg",
                "markup": """
                <g opacity="0.8">
                  <!-- Hydrophone Array Grid -->
                  <rect x="200" y="520" width="680" height="340" fill="none" stroke="#00ff66" stroke-width="3" stroke-dasharray="10,8"/>
                  <circle cx="340" cy="620" r="18" fill="#00ff66"/>
                  <circle cx="740" cy="660" r="18" fill="#00ff66"/>
                  <circle cx="540" cy="780" r="22" fill="#ff3b30"/>
                  <line x1="340" y1="620" x2="540" y2="780" stroke="#00ff66" stroke-width="2"/>
                  <line x1="740" y1="660" x2="540" y2="780" stroke="#00ff66" stroke-width="2"/>
                </g>
                """
            })
        elif s_idx == 1:
            elements.append({
                "type": "bignumber",
                "from": 0, "to": 5000, "suffix": " km",
                "x": 540, "y": 740, "size": 130, "color": "#00ff66", "dur": 2.5, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "ACOUSTIC RANGE ACROSS PACIFIC",
                "x": 260, "y": 860, "size": 24, "t0": 0.6
            })
        elif s_idx == 2:
            elements.append({
                "type": "svg",
                "markup": """
                <g opacity="0.85">
                  <!-- Audio Spectrogram Waterfall -->
                  <rect x="160" y="550" width="760" height="280" fill="#02140a" stroke="#00ff66" stroke-width="4"/>
                  <!-- Rising Frequency Curve -->
                  <path d="M 220 780 Q 420 770 540 680 T 860 590" fill="none" stroke="#00ff66" stroke-width="8"/>
                  <text x="200" y="590" font-family="Poppins" font-size="24" font-weight="700" fill="#00ff66">40 Hz</text>
                  <text x="200" y="790" font-family="Poppins" font-size="24" font-weight="700" fill="#00ff66">10 Hz</text>
                </g>
                """
            })
            elements.append({
                "type": "pill",
                "text": "SPECTROGRAM FREQUENCY SWEEP",
                "x": 270, "y": 890, "size": 24, "t0": 0.8
            })
        elif s_idx == 3:
            elements.append({
                "type": "creature",
                "kind": "whale",
                "x": 540, "y": 750, "scale": 1.5,
                "mode": "silhouette", "swim": {"vx": 18, "vy": 0}
            })
            elements.append({
                "type": "stamp",
                "text": "LOUDER THAN BLUE WHALE",
                "color": "#ff3b30",
                "x": 540, "y": 920, "size": 48, "rotate": -5, "t0": 1.4
            })
        elif s_idx == 4:
            elements.append({
                "type": "bignumber",
                "from": 100, "to": 200, "suffix": "+ ft",
                "x": 540, "y": 740, "size": 130, "color": "#00ff66", "dur": 2.2, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "THEORETICAL ORGANIC BIOMASS",
                "x": 280, "y": 860, "size": 24, "t0": 0.8
            })
        elif s_idx == 5:
            elements.append({
                "type": "svg",
                "markup": """
                <g opacity="0.85">
                  <!-- Fracturing Antarctic Iceberg -->
                  <polygon points="240,540 840,540 760,860 320,860" fill="#0b2a3a" stroke="#80deea" stroke-width="5"/>
                  <path d="M 540 540 L 520 660 L 560 740 L 530 860" stroke="#00e5ff" stroke-width="8" fill="none"/>
                  <text x="540" y="700" font-family="Poppins" font-size="34" font-weight="900" fill="#fff" text-anchor="middle">CRYOSEISM</text>
                </g>
                """
            })
            elements.append({
                "type": "stamp",
                "text": "MASSIVE ICEQUAKE CALVING",
                "color": "#80deea",
                "x": 540, "y": 930, "size": 48, "rotate": -4, "t0": 1.2
            })
        else:
            elements.append({
                "type": "stamp",
                "text": "WHAT ELSE SINGS IN THE DARK?",
                "color": "#00ff66",
                "x": 540, "y": 800, "size": 48, "rotate": -3, "t0": 1.0
            })

    # =========================================================================
    # 4. LAKE VOSTOK (Antarctic Subglacial Time Capsule)
    # =========================================================================
    elif "vostok" in topic_id:
        if s_idx == 0:
            elements.append({
                "type": "svg",
                "markup": """
                <g opacity="0.85">
                  <!-- 4km Ice Column Cross Section -->
                  <rect x="240" y="440" width="600" height="420" fill="#0a2a40" stroke="#80deea" stroke-width="5"/>
                  <rect x="240" y="860" width="600" height="200" fill="#00e5ff" opacity="0.4" stroke="#80deea" stroke-width="5"/>
                  <text x="540" y="520" font-family="Poppins" font-size="28" font-weight="800" fill="#e0f7fa" text-anchor="middle">4,000M GLACIAL ICE</text>
                  <text x="540" y="960" font-family="Poppins" font-size="32" font-weight="900" fill="#fff" text-anchor="middle">LIQUID LAKE VOSTOK</text>
                </g>
                """
            })
            elements.append({
                "type": "bignumber",
                "from": 0, "to": 4000, "suffix": " m",
                "x": 540, "y": 720, "size": 120, "color": "#00e5ff", "dur": 2.5, "t0": 0.3
            })
        elif s_idx == 1:
            elements.append({
                "type": "pill",
                "text": "SURFACE: -89.2°C • WATER: -3°C LIQUID",
                "tone": "red",
                "x": 220, "y": 760, "size": 24, "t0": 0.4
            })
            elements.append({
                "type": "stamp",
                "text": "SIZE OF LAKE ONTARIO",
                "color": "#80deea",
                "x": 540, "y": 880, "size": 50, "rotate": -4, "t0": 1.2
            })
        elif s_idx == 2:
            elements.append({
                "type": "meter",
                "x": 160, "y": 750, "w": 760, "value": 0.9,
                "number": 350, "unit": " ATM", "title": "GLACIAL HYDROSTATIC PRESSURE", "dur": 2.0, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "50X OXYGEN HYPERSATURATION",
                "x": 280, "y": 870, "size": 24, "t0": 1.2
            })
        elif s_idx == 3:
            elements.append({
                "type": "svg",
                "markup": """
                <g opacity="0.85">
                  <!-- Hot Water Core Drill Probe -->
                  <polygon points="540,880 500,520 580,520" fill="#94a3b8" stroke="#38bdf8" stroke-width="4"/>
                  <circle cx="540" cy="880" r="16" fill="#00e5ff"/>
                </g>
                """
            })
            elements.append({
                "type": "pill",
                "text": "STERILE KEROSENE FLUID BARRIER",
                "x": 260, "y": 940, "size": 24, "t0": 0.8
            })
        elif s_idx == 4:
            elements.append({
                "type": "stamp",
                "text": "NOVEL DNA SEQUENCES",
                "color": "#00e5ff",
                "x": 540, "y": 820, "size": 52, "rotate": -5, "t0": 1.0
            })
        else:
            elements.append({
                "type": "svg",
                "markup": """
                <g opacity="0.85">
                  <!-- Europa Ocean Moon Comparison -->
                  <circle cx="540" cy="740" r="130" fill="#0f172a" stroke="#80deea" stroke-width="6"/>
                  <circle cx="540" cy="740" r="100" fill="#0284c7" opacity="0.5"/>
                  <text x="540" y="750" font-family="Poppins" font-size="34" font-weight="900" fill="#fff" text-anchor="middle">MOON EUROPA</text>
                </g>
                """
            })
            elements.append({
                "type": "stamp",
                "text": "ALIEN OCEAN ANALOG",
                "color": "#ffd166",
                "x": 540, "y": 940, "size": 48, "rotate": -4, "t0": 1.2
            })

    # =========================================================================
    # 5. DARVAZA GAS CRATER (The Door to Hell)
    # =========================================================================
    elif "darvaza" in topic_id:
        if s_idx == 0:
            elements.append({
                "type": "svg",
                "markup": """
                <g opacity="0.9">
                  <!-- Flaming Crater Rim -->
                  <ellipse cx="540" cy="740" rx="360" ry="140" fill="#3d0a02" stroke="#ff3d00" stroke-width="8"/>
                  <ellipse cx="540" cy="740" rx="260" ry="80" fill="#ff3d00" opacity="0.6"/>
                  <ellipse cx="540" cy="740" rx="140" ry="40" fill="#ffea00" opacity="0.8"/>
                </g>
                """
            })
            elements.append({
                "type": "pill",
                "text": "KARAKUM DESERT • 70-METER CRATER",
                "x": 230, "y": 930, "size": 24, "t0": 0.6
            })
        elif s_idx == 1:
            elements.append({
                "type": "bignumber",
                "from": 1971, "to": 2026, "prefix": "BURNING SINCE ",
                "x": 540, "y": 740, "size": 85, "color": "#ff9100", "dur": 2.0, "t0": 0.3
            })
            elements.append({
                "type": "stamp",
                "text": "55 YEARS UNSTOPPABLE BLAZE",
                "color": "#ff3d00",
                "x": 540, "y": 870, "size": 44, "rotate": -5, "t0": 1.2
            })
        elif s_idx == 2:
            elements.append({
                "type": "svg",
                "markup": """
                <g opacity="0.85">
                  <!-- Collapsing Rig Diagram -->
                  <polygon points="540,550 480,720 600,720" fill="none" stroke="#ff9100" stroke-width="5" transform="rotate(35 540 640)"/>
                  <path d="M 300 760 Q 540 920 780 760" stroke="#ff3d00" stroke-width="6" fill="none"/>
                  <text x="540" y="860" font-family="Poppins" font-size="28" font-weight="800" fill="#ff3d00" text-anchor="middle">METHANE CAVERN COLLAPSE</text>
                </g>
                """
            })
            elements.append({
                "type": "pill",
                "text": "1971 SOVIET DRILLING ACCIDENT",
                "tone": "red",
                "x": 250, "y": 940, "size": 24, "t0": 0.8
            })
        elif s_idx == 3:
            elements.append({
                "type": "stamp",
                "text": "EXPECTED TO BURN A FEW WEEKS",
                "color": "#ffd700",
                "x": 540, "y": 800, "size": 42, "rotate": -4, "t0": 1.0
            })
        elif s_idx == 4:
            elements.append({
                "type": "bignumber",
                "from": 0, "to": 400, "suffix": " °C",
                "x": 540, "y": 740, "size": 130, "color": "#ff3d00", "dur": 2.2, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "HUNDREDS OF ACTIVE METHANE VENTS",
                "x": 230, "y": 870, "size": 24, "t0": 0.8
            })
        else:
            elements.append({
                "type": "stamp",
                "text": "EXTREMOPHILE BACTERIA IN FIRE",
                "color": "#ff9100",
                "x": 540, "y": 820, "size": 48, "rotate": -3, "t0": 1.0
            })

    # =========================================================================
    # 6. TARDIGRADES (Indestructible Extremophiles)
    # =========================================================================
    elif "tardigrades" in topic_id:
        if s_idx == 0:
            elements.append({
                "type": "svg",
                "markup": """
                <g opacity="0.85">
                  <!-- Tardigrade Water Bear Anatomy -->
                  <ellipse cx="540" cy="700" rx="200" ry="110" fill="#143324" stroke="#76ff03" stroke-width="5"/>
                  <!-- Segments & Claws -->
                  <ellipse cx="400" cy="700" rx="60" ry="90" fill="none" stroke="#76ff03" stroke-width="3"/>
                  <ellipse cx="540" cy="700" rx="60" ry="100" fill="none" stroke="#76ff03" stroke-width="3"/>
                  <ellipse cx="680" cy="700" rx="50" ry="90" fill="none" stroke="#76ff03" stroke-width="3"/>
                  <circle cx="340" cy="700" r="16" fill="#76ff03"/>
                </g>
                """
            })
            elements.append({
                "type": "bignumber",
                "from": 0, "to": 0.5, "suffix": " mm",
                "x": 540, "y": 870, "size": 110, "color": "#76ff03", "dur": 1.8, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "EIGHT-LEGGED MICRO-METAZOAN",
                "x": 280, "y": 970, "size": 24, "t0": 0.8
            })
        elif s_idx == 1:
            elements.append({
                "type": "stamp",
                "text": "SURVIVED 5 MASS EXTINCTIONS",
                "color": "#76ff03",
                "x": 540, "y": 800, "size": 48, "rotate": -5, "t0": 1.2
            })
        elif s_idx == 2:
            elements.append({
                "type": "bignumber",
                "from": 0, "to": 99, "suffix": " %",
                "x": 540, "y": 740, "size": 140, "color": "#00e5ff", "dur": 2.2, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "BODY WATER EXPELLED IN CRYPTOBIOSIS",
                "x": 220, "y": 870, "size": 24, "t0": 0.8
            })
        elif s_idx == 3:
            elements.append({
                "type": "svg",
                "markup": """
                <g opacity="0.85">
                  <!-- Tun State Armored Sphere -->
                  <circle cx="540" cy="720" r="110" fill="#082114" stroke="#76ff03" stroke-width="6"/>
                  <circle cx="540" cy="720" r="80" fill="none" stroke="#00e5ff" stroke-width="3" stroke-dasharray="10,6"/>
                  <text x="540" y="730" font-family="Poppins" font-size="30" font-weight="900" fill="#76ff03" text-anchor="middle">TUN STATE</text>
                </g>
                """
            })
            elements.append({
                "type": "pill",
                "text": "METABOLISM REDUCED TO 0.01%",
                "x": 260, "y": 890, "size": 24, "t0": 0.8
            })
        elif s_idx == 4:
            elements.append({
                "type": "pill",
                "text": "-272°C TO +150°C",
                "tone": "red",
                "x": 350, "y": 740, "size": 28, "t0": 0.4
            })
            elements.append({
                "type": "stamp",
                "text": "SURVIVES VACUUM OF SPACE",
                "color": "#76ff03",
                "x": 540, "y": 880, "size": 48, "t0": 1.4
            })
        elif s_idx == 5:
            elements.append({
                "type": "bignumber",
                "from": 1, "to": 1000, "suffix": "x",
                "x": 540, "y": 740, "size": 140, "color": "#ff3b30", "dur": 2.2, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "HUMAN LETHAL RADIATION DOSE",
                "x": 260, "y": 870, "size": 24, "t0": 0.8
            })
        else:
            elements.append({
                "type": "stamp",
                "text": "REHYDRATES AND WALKS AWAY",
                "color": "#76ff03",
                "x": 540, "y": 820, "size": 48, "rotate": -3, "t0": 1.0
            })

    # =========================================================================
    # 7. THE WOW! SIGNAL (Cosmic Radio Astronomy)
    # =========================================================================
    elif "wow" in topic_id:
        if s_idx == 0:
            elements.append({
                "type": "svg",
                "markup": """
                <g opacity="0.85">
                  <!-- Big Ear Parabolic Radio Telescope -->
                  <path d="M 220 780 Q 540 500 860 780" stroke="#ffd700" stroke-width="6" fill="none"/>
                  <line x1="540" y1="640" x2="540" y2="440" stroke="#ffd700" stroke-width="4"/>
                  <circle cx="540" cy="440" r="22" fill="#ffd700"/>
                  <text x="540" y="850" font-family="Poppins" font-size="28" font-weight="800" fill="#ffd700" text-anchor="middle">BIG EAR RADIO TELESCOPE</text>
                </g>
                """
            })
            elements.append({
                "type": "pill",
                "text": "OHIO STATE UNIVERSITY • 1977",
                "x": 260, "y": 920, "size": 24, "t0": 0.8
            })
        elif s_idx == 1:
            elements.append({
                "type": "bignumber",
                "from": 0, "to": 72, "suffix": " sec",
                "x": 540, "y": 740, "size": 140, "color": "#ffd700", "dur": 2.0, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "EARTH ROTATION BEAM DURATION",
                "x": 260, "y": 870, "size": 24, "t0": 0.8
            })
        elif s_idx == 2:
            elements.append({
                "type": "bignumber",
                "from": 1, "to": 30, "suffix": "x",
                "x": 540, "y": 740, "size": 140, "color": "#ff3b30", "dur": 2.2, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "STRONGER THAN DEEP SPACE NOISE",
                "tone": "red",
                "x": 230, "y": 870, "size": 24, "t0": 0.8
            })
        elif s_idx == 3:
            elements.append({
                "type": "svg",
                "markup": """
                <g opacity="0.95">
                  <!-- Vintage 1977 Computer Printout Strip -->
                  <rect x="200" y="600" width="680" height="240" fill="#f8fafc" stroke="#475569" stroke-width="4"/>
                  <text x="540" y="730" font-family="Courier New, monospace" font-size="70" font-weight="900" fill="#0f172a" text-anchor="middle" letter-spacing="16">6EQUJ5</text>
                  <!-- Red Circled Ink -->
                  <ellipse cx="540" cy="705" rx="200" ry="70" fill="none" stroke="#dc2626" stroke-width="8" transform="rotate(-6 540 705)"/>
                  <text x="760" y="680" font-family="Brush Script MT, cursive, sans-serif" font-size="64" font-weight="900" fill="#dc2626">Wow!</text>
                </g>
                """
            })
            elements.append({
                "type": "pill",
                "text": "ASTRONOMER JERRY EHMAN'S NOTATION",
                "x": 230, "y": 910, "size": 24, "t0": 1.2
            })
        elif s_idx == 4:
            elements.append({
                "type": "bignumber",
                "from": 0, "to": 1420.4, "suffix": " MHz",
                "x": 540, "y": 740, "size": 110, "color": "#ffd700", "dur": 2.2, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "21-CENTIMETER HYDROGEN LINE",
                "x": 280, "y": 860, "size": 24, "t0": 0.8
            })
        else:
            elements.append({
                "type": "stamp",
                "text": "THE SIGNAL NEVER RETURNED",
                "color": "#ffd700",
                "x": 540, "y": 800, "size": 48, "rotate": -4, "t0": 1.0
            })

    # =========================================================================
    # 8. CHERNOBYL'S ELEPHANT'S FOOT (Nuclear Corium)
    # =========================================================================
    elif "chernobyl" in topic_id:
        if s_idx == 0:
            elements.append({
                "type": "pill",
                "text": "CHERNOBYL REACTOR 4 SUB-BASEMENT",
                "tone": "red",
                "x": 230, "y": 760, "size": 26, "t0": 0.5
            })
            elements.append({
                "type": "svg",
                "markup": """
                <g opacity="0.85">
                  <!-- Trefoil Radiation Symbol -->
                  <circle cx="540" cy="580" r="100" fill="#ffd600"/>
                  <circle cx="540" cy="580" r="24" fill="#000"/>
                  <path d="M540,580 L500,430 A100,100 0 0,1 580,430 Z" fill="#000"/>
                  <path d="M540,580 L670,510 A100,100 0 0,1 630,670 Z" fill="#000"/>
                  <path d="M540,580 L410,670 A100,100 0 0,1 370,510 Z" fill="#000"/>
                </g>
                """
            })
        elif s_idx == 1:
            elements.append({
                "type": "svg",
                "markup": """
                <g opacity="0.9">
                  <!-- Elephant's Foot Corium Mass -->
                  <path d="M 300 850 C 320 680, 480 620, 540 640 C 620 620, 760 690, 780 850 C 740 920, 340 920, 300 850 Z" fill="#1c1917" stroke="#ffd600" stroke-width="5"/>
                  <path d="M 360 720 Q 540 760 720 720" stroke="#78716c" stroke-width="4" fill="none"/>
                  <path d="M 380 780 Q 540 820 700 780" stroke="#78716c" stroke-width="4" fill="none"/>
                  <text x="540" y="870" font-family="Poppins" font-size="30" font-weight="900" fill="#ffd600" text-anchor="middle">2 METRIC TONS CORIUM</text>
                </g>
                """
            })
            elements.append({
                "type": "pill",
                "text": "SOLIDIFIED NUCLEAR LAVA MASS",
                "x": 280, "y": 950, "size": 24, "t0": 0.8
            })
        elif s_idx == 2:
            elements.append({
                "type": "bignumber",
                "from": 0, "to": 2000, "suffix": " °C",
                "x": 540, "y": 740, "size": 130, "color": "#ff3b30", "dur": 2.2, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "MELTING URANIUM, ZIRCONIUM & CONCRETE",
                "tone": "red",
                "x": 200, "y": 860, "size": 24, "t0": 0.8
            })
        elif s_idx == 3:
            elements.append({
                "type": "meter",
                "x": 160, "y": 750, "w": 760, "value": 1.0,
                "number": 10000, "unit": " R/HR", "title": "IONIZING GAMMA RADIATION LEVEL", "dur": 2.2, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "300 SECONDS = LETHAL HUMAN DOSE",
                "tone": "red",
                "x": 250, "y": 870, "size": 24, "t0": 1.2
            })
        elif s_idx == 4:
            elements.append({
                "type": "stamp",
                "text": "GAMMA RAYS DESTROYED FILM",
                "color": "#ffd600",
                "x": 540, "y": 800, "size": 48, "rotate": -5, "t0": 1.0
            })
        elif s_idx == 5:
            elements.append({
                "type": "pill",
                "text": "ARMOR-PIERCING AK-47 ROUNDS FIRED FOR SAMPLES",
                "x": 160, "y": 800, "size": 24, "t0": 0.8
            })
        else:
            elements.append({
                "type": "stamp",
                "text": "RADIOTROPHIC FUNGI EAT RADIATION",
                "color": "#76ff03",
                "x": 540, "y": 800, "size": 44, "rotate": -4, "t0": 1.0
            })

    # =========================================================================
    # 9. THE DEVIL'S KETTLE (Vanishing Waterfall)
    # =========================================================================
    elif "devils_kettle" in topic_id:
        if s_idx == 0:
            elements.append({
                "type": "svg",
                "markup": """
                <g opacity="0.85">
                  <!-- Brule River Canyon Gorge -->
                  <path d="M 220 450 L 320 850 L 460 850 L 460 1200" stroke="#00e5ff" stroke-width="12" fill="none"/>
                  <path d="M 460 850 L 620 850 L 760 1200" stroke="#00e5ff" stroke-width="12" fill="none"/>
                  <polygon points="540,780 480,920 600,920" fill="#2d2218" stroke="#78716c" stroke-width="4"/>
                  <text x="540" y="740" font-family="Poppins" font-size="28" font-weight="800" fill="#fff" text-anchor="middle">ROCK SPLITS RIVER</text>
                </g>
                """
            })
            elements.append({
                "type": "pill",
                "text": "BRULE RIVER • MINNESOTA",
                "x": 310, "y": 980, "size": 26, "t0": 0.6
            })
        elif s_idx == 1:
            elements.append({
                "type": "stamp",
                "text": "EAST FALLS TO LAKE SUPERIOR",
                "color": "#00e5ff",
                "x": 540, "y": 780, "size": 46, "rotate": -4, "t0": 1.0
            })
            elements.append({
                "type": "stamp",
                "text": "WEST DISAPPEARS INTO POTHOLE",
                "color": "#ff3b30",
                "x": 540, "y": 900, "size": 44, "rotate": 4, "t0": 2.0
            })
        elif s_idx == 2:
            elements.append({
                "type": "svg",
                "markup": """
                <g opacity="0.85">
                  <!-- The Bottomless Pothole Abyss -->
                  <ellipse cx="540" cy="740" rx="160" ry="100" fill="#000" stroke="#00e5ff" stroke-width="6"/>
                  <!-- Swirling Vortex -->
                  <path d="M 420 740 Q 540 680 640 740 Q 540 800 460 740" stroke="#00e5ff" stroke-width="4" fill="none"/>
                  <text x="540" y="890" font-family="Poppins" font-size="28" font-weight="800" fill="#ff3b30" text-anchor="middle">THE KETTLE ABYSS</text>
                </g>
                """
            })
            elements.append({
                "type": "pill",
                "text": "WATER VANISHES WITHOUT A TRACE",
                "x": 260, "y": 950, "size": 24, "t0": 0.8
            })
        elif s_idx == 3:
            elements.append({
                "type": "pill",
                "text": "DYES, PING-PONG BALLS & GPS TAGS VANISHED",
                "tone": "red",
                "x": 190, "y": 780, "size": 24, "t0": 0.6
            })
            elements.append({
                "type": "redx",
                "x": 540, "y": 900, "size": 80, "t0": 1.4
            })
        elif s_idx == 4:
            elements.append({
                "type": "bignumber",
                "from": 0, "to": 123, "suffix": " CFS",
                "x": 540, "y": 740, "size": 130, "color": "#00e5ff", "dur": 2.2, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "ACOUSTIC DOPPLER FLOW BALANCE: 123 IN = 123 OUT",
                "x": 160, "y": 860, "size": 22, "t0": 0.8
            })
        else:
            elements.append({
                "type": "stamp",
                "text": "SURGES UP IN PLUNGE POOL GRAVEL",
                "color": "#00e5ff",
                "x": 540, "y": 800, "size": 44, "rotate": -3, "t0": 1.0
            })

    # =========================================================================
    # 10. THE SILURIAN HYPOTHESIS (Deep Time Civilizations)
    # =========================================================================
    elif "silurian" in topic_id:
        if s_idx == 0:
            elements.append({
                "type": "svg",
                "markup": """
                <g opacity="0.85">
                  <!-- Cosmic 4.5B Year Clock -->
                  <circle cx="540" cy="700" r="140" fill="none" stroke="#ffab40" stroke-width="6"/>
                  <line x1="540" y1="700" x2="540" y2="580" stroke="#ffab40" stroke-width="5"/>
                  <line x1="540" y1="700" x2="550" y2="590" stroke="#ff3b30" stroke-width="4"/>
                  <text x="540" y="890" font-family="Poppins" font-size="28" font-weight="800" fill="#ffab40" text-anchor="middle">4.5 BILLION YEAR CLOCK</text>
                </g>
                """
            })
            elements.append({
                "type": "pill",
                "text": "HUMANS EXISTED FOR <0.01% OF EARTH TIME",
                "x": 220, "y": 960, "size": 24, "t0": 0.8
            })
        elif s_idx == 1:
            elements.append({
                "type": "pill",
                "text": "GAVIN SCHMIDT (NASA) & ADAM FRANK",
                "x": 240, "y": 760, "size": 24, "t0": 0.6
            })
            elements.append({
                "type": "stamp",
                "text": "THE SILURIAN HYPOTHESIS",
                "color": "#ffab40",
                "x": 540, "y": 880, "size": 52, "rotate": -4, "t0": 1.2
            })
        elif s_idx == 2:
            elements.append({
                "type": "bignumber",
                "from": 0, "to": 56, "suffix": "M BC",
                "x": 540, "y": 740, "size": 130, "color": "#ffab40", "dur": 2.2, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "PALEOCENE-EOCENE THERMAL MAXIMUM (+8°C)",
                "tone": "red",
                "x": 190, "y": 860, "size": 22, "t0": 0.8
            })
        elif s_idx == 3:
            elements.append({
                "type": "bignumber",
                "from": 100, "to": 0.1, "suffix": " %",
                "x": 540, "y": 740, "size": 140, "color": "#ff3b30", "dur": 2.2, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "SPECIES EVER PRESERVED AS FOSSILS",
                "x": 250, "y": 870, "size": 24, "t0": 0.8
            })
        elif s_idx == 4:
            elements.append({
                "type": "stamp",
                "text": "CITIES CRUMBLE TO DUST IN 5,000 YRS",
                "color": "#ffab40",
                "x": 540, "y": 820, "size": 44, "rotate": -5, "t0": 1.0
            })
        elif s_idx == 5:
            elements.append({
                "type": "svg",
                "markup": """
                <g opacity="0.85">
                  <!-- Technosignature Strata Layer -->
                  <rect x="180" y="660" width="720" height="40" fill="#00e5ff" stroke="#fff" stroke-width="2"/>
                  <text x="540" y="690" font-family="Poppins" font-size="24" font-weight="900" fill="#0f172a" text-anchor="middle">SYNTHETIC PLASTICS & PLUTONIUM-244</text>
                </g>
                """
            })
            elements.append({
                "type": "pill",
                "text": "IMMORTAL TECHNOSIGNATURE LAYER",
                "x": 260, "y": 760, "size": 24, "t0": 0.8
            })
        elif s_idx == 6:
            elements.append({
                "type": "bignumber",
                "from": 100, "to": 2, "suffix": " mm",
                "x": 540, "y": 740, "size": 140, "color": "#ffab40", "dur": 2.2, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "HUMAN CIVILIZATION COMPRESSED INTO ROCK",
                "x": 210, "y": 870, "size": 24, "t0": 0.8
            })
        else:
            elements.append({
                "type": "stamp",
                "text": "A WHISPER IN DEEP TIME",
                "color": "#ffab40",
                "x": 540, "y": 800, "size": 52, "rotate": -3, "t0": 1.0
            })

    return elements
