#!/usr/bin/env python3
"""
Generates rich KazChart Scene JSONs for the 10 scientific documentary topics.
Integrates exact audio timestamps, procedural continuous motion, vector diagrams,
and complete synchronized subtitles with dark glass pills and golden highlights.
"""

import json
import os
from topics_config import TOPICS

def build_topic_scenes(topic, timing_data, output_dir="/home/antigravity/Future786/cave-of-crystals-animation/scenes"):
    os.makedirs(output_dir, exist_ok=True)
    topic_id = topic["id"]
    sentences = timing_data["sentences"]
    total_dur = timing_data["duration"]

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
        if not visuals:
            hl_col = topic.get("tokens", {}).get("hl", "#ffd166")
            visuals = [
                {
                    "type": "reticle",
                    "x": 540, "y": 850, "r": 120, "t0": 0.4
                },
                {
                    "type": "circle",
                    "x": 540, "y": 850, "rx": 260, "ry": 260,
                    "color": hl_col, "width": 4, "t0": 0.8
                }
            ]
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
            "depth": round(depth_val, 2),
            "rays": s_idx in [0, 1, 6],
            "particleCount": 45
        }
        if s_idx == 2:
            shot_bg["spotlight"] = {"x": 540, "w": 420}

        shots.append({
            "start": round(shot_start, 2),
            "end": round(shot_end, 2),
            "bg": shot_bg,
            "camera": {
                "zoomFrom": 1.0,
                "zoomTo": 1.14,
                "x": 540,
                "y": 960,
                "panX": 25 if s_idx % 2 == 1 else -25
            },
            "fadeIn": 0.35 if s_idx == 0 else 0,
            "fadeOut": 0.4 if s_idx == num_shots - 1 else 0,
            "elements": elements
        })

    scene_data = {
        "preset": topic.get("preset", "abyss"),
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
    """Returns vector artwork, big numbers, pills, stamps, and graphics tailored to each scene."""
    elements = []

    # 1. Mariana Trench
    if "mariana" in topic_id:
        if s_idx == 0:
            elements.append({
                "type": "bignumber",
                "from": 0, "to": 10994, "suffix": " m",
                "x": 540, "y": 780, "size": 130, "color": "#00f2fe", "dur": 3.0, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "PACIFIC HADAL ZONE",
                "x": 310, "y": 880, "size": 24, "t0": 0.6
            })
            elements.append({
                "type": "svg",
                "markup": """
                <g opacity="0.8">
                  <path d="M 120 400 L 460 1200 L 620 1200 L 960 400" stroke="#00f2fe" stroke-width="6" fill="none" opacity="0.4"/>
                  <line x1="540" y1="400" x2="540" y2="1200" stroke="#ffd166" stroke-width="4" stroke-dasharray="14,10" opacity="0.6"/>
                  <circle cx="540" cy="1180" r="14" fill="#ff3b30"/>
                  <rect x="510" y="700" width="60" height="90" fill="#081822" stroke="#00f2fe" stroke-width="4" rx="10"/>
                </g>
                """
            })
        elif s_idx == 1:
            elements.append({
                "type": "bracket",
                "x1": 240, "y1": 550, "x2": 840, "y2": 550,
                "label": "MOUNT EVEREST: 8,848M", "color": "#ffd166"
            })
            elements.append({
                "type": "stamp",
                "text": "COMPLETELY SUBMERGED",
                "color": "#ff3b30",
                "x": 540, "y": 950, "size": 52, "rotate": -5, "t0": 1.8
            })
        elif s_idx == 2:
            elements.append({
                "type": "meter",
                "x": 160, "y": 820, "w": 760, "value": 1.0,
                "number": 1086, "unit": " ATM", "title": "WATER PRESSURE TELEMETRY", "dur": 2.2, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "8 TONS PER SQUARE INCH",
                "tone": "red",
                "x": 280, "y": 940, "size": 26, "t0": 1.5
            })
        elif s_idx == 3:
            elements.append({
                "type": "creature",
                "kind": "squid",
                "x": 540, "y": 850, "scale": 1.2,
                "swim": {"vx": 20, "vy": -10}, "bob": True
            })
            elements.append({
                "type": "circle",
                "x": 540, "y": 850, "rx": 280, "ry": 180, "color": "#00f2fe", "width": 4, "t0": 1.0
            })
        elif s_idx == 4:
            elements.append({
                "type": "creature",
                "kind": "fish",
                "x": 540, "y": 820, "scale": 1.6,
                "mode": "ghost", "swim": {"vx": 25, "vy": 5}
            })
            elements.append({
                "type": "pill",
                "text": "TRANSLUCENT • ZERO SCALES",
                "x": 270, "y": 1050, "size": 24, "t0": 1.0
            })
        elif s_idx == 5:
            elements.append({
                "type": "bignumber",
                "from": 1, "to": 20, "suffix": " cm",
                "x": 540, "y": 800, "size": 120, "color": "#ffd166", "dur": 2.0, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "GIANT SINGLE-CELLED XENOPHYOPHORE",
                "x": 210, "y": 920, "size": 24, "t0": 0.8
            })
        elif s_idx == 6:
            elements.append({
                "type": "stamp",
                "text": "THE HADAL ABYSS",
                "color": "#00f2fe",
                "x": 540, "y": 850, "size": 56, "rotate": -4, "t0": 1.2
            })

    # 2. Kola Superdeep Borehole
    elif "kola" in topic_id:
        if s_idx == 0:
            elements.append({
                "type": "bignumber",
                "from": 0, "to": 12262, "suffix": " m",
                "x": 540, "y": 780, "size": 125, "color": "#f5a623", "dur": 2.8, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "SG-3 BOREHOLE • 40,230 FT",
                "x": 290, "y": 880, "size": 24, "t0": 0.6
            })
        elif s_idx == 1:
            elements.append({
                "type": "bracket",
                "x1": 300, "y1": 500, "x2": 780, "y2": 500,
                "label": "BALTIC CONTINENTAL CRUST", "color": "#f5a623"
            })
            elements.append({
                "type": "pill",
                "text": "7.6 MILES DEEP",
                "x": 370, "y": 620, "size": 26, "t0": 0.8
            })
        elif s_idx == 2:
            elements.append({
                "type": "pill",
                "text": "BOILING HYDROTHERMAL FLUID",
                "tone": "red",
                "x": 260, "y": 820, "size": 24, "t0": 0.6
            })
            elements.append({
                "type": "stamp",
                "text": "FRACTURED GRANITE",
                "color": "#f5a623",
                "x": 540, "y": 950, "size": 50, "t0": 1.8
            })
        elif s_idx == 3:
            elements.append({
                "type": "bignumber",
                "from": 20, "to": 180, "suffix": " °C",
                "x": 540, "y": 760, "size": 130, "color": "#ff3b30", "dur": 2.2, "t0": 0.3
            })
            elements.append({
                "type": "stamp",
                "text": "ROCK TURNS TO PLASTIC",
                "color": "#ff3b30",
                "x": 540, "y": 920, "size": 48, "rotate": -6, "t0": 1.5
            })
        elif s_idx == 4:
            elements.append({
                "type": "pill",
                "text": "DRILL BITS MELTED",
                "tone": "red",
                "x": 330, "y": 800, "size": 26, "t0": 0.6
            })
            elements.append({
                "type": "redx",
                "x": 540, "y": 960, "size": 80, "t0": 1.4
            })
        elif s_idx == 5:
            elements.append({
                "type": "circle",
                "x": 540, "y": 820, "rx": 300, "ry": 160, "color": "#f5a623", "width": 5, "t0": 0.8
            })
            elements.append({
                "type": "pill",
                "text": "ACOUSTIC SEISMIC SENSORS",
                "x": 280, "y": 920, "size": 24, "t0": 1.2
            })
        elif s_idx == 6:
            elements.append({
                "type": "stamp",
                "text": "WELDED SHUT FOREVER",
                "color": "#e0453a",
                "x": 540, "y": 860, "size": 52, "rotate": -5, "t0": 1.2
            })

    # 3. The Bloop
    elif "bloop" in topic_id:
        if s_idx == 0:
            elements.append({
                "type": "pill",
                "text": "NOAA SOSUS HYDROPHONE ARRAY",
                "x": 240, "y": 800, "size": 24, "t0": 0.5
            })
        elif s_idx == 1:
            elements.append({
                "type": "bignumber",
                "from": 0, "to": 5000, "suffix": " km",
                "x": 540, "y": 780, "size": 130, "color": "#3ecf6a", "dur": 2.5, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "TRANSMISSION DISTANCE",
                "x": 330, "y": 880, "size": 24, "t0": 0.6
            })
        elif s_idx == 2:
            elements.append({
                "type": "bignumber",
                "from": 0, "to": 270, "suffix": " sec",
                "x": 540, "y": 780, "size": 130, "color": "#38bdf8", "dur": 2.2, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "FREQUENCY SWEEP DURATION",
                "x": 300, "y": 880, "size": 24, "t0": 0.6
            })
        elif s_idx == 3:
            elements.append({
                "type": "creature",
                "kind": "whale",
                "x": 540, "y": 800, "scale": 1.4,
                "mode": "silhouette", "swim": {"vx": 15, "vy": 0}
            })
            elements.append({
                "type": "stamp",
                "text": "LOUDER THAN BLUE WHALE",
                "color": "#ff3b30",
                "x": 540, "y": 960, "size": 48, "rotate": -5, "t0": 1.5
            })
        elif s_idx == 4:
            elements.append({
                "type": "circle",
                "x": 540, "y": 820, "rx": 260, "ry": 260, "color": "#ffd166", "width": 4, "t0": 0.8
            })
            elements.append({
                "type": "pill",
                "text": "UNCLASSIFIED DEEP SEA BEAST?",
                "x": 260, "y": 920, "size": 24, "t0": 1.2
            })
        elif s_idx == 5:
            elements.append({
                "type": "stamp",
                "text": "ANTARCTIC ICEQUAKE",
                "color": "#38bdf8",
                "x": 540, "y": 850, "size": 52, "rotate": -4, "t0": 1.0
            })
        elif s_idx == 6:
            elements.append({
                "type": "bignumber",
                "from": 100, "to": 80, "suffix": " %",
                "x": 540, "y": 780, "size": 140, "color": "#ffd166", "dur": 2.0, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "OCEANS UNMAPPED AND UNEXPLORED",
                "x": 230, "y": 890, "size": 24, "t0": 0.6
            })

    # 4. Lake Vostok
    elif "vostok" in topic_id:
        if s_idx == 0:
            elements.append({
                "type": "bignumber",
                "from": 0, "to": 4000, "suffix": " m",
                "x": 540, "y": 780, "size": 130, "color": "#38bdf8", "dur": 2.5, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "SEALED FOR 15,000,000 YEARS",
                "x": 280, "y": 880, "size": 24, "t0": 0.6
            })
        elif s_idx == 1:
            elements.append({
                "type": "pill",
                "text": "SURFACE AIR: -89.2°C",
                "tone": "red",
                "x": 330, "y": 750, "size": 24, "t0": 0.4
            })
            elements.append({
                "type": "pill",
                "text": "SUBGLACIAL LIQUID WATER: -3°C",
                "x": 280, "y": 850, "size": 24, "t0": 1.2
            })
        elif s_idx == 2:
            elements.append({
                "type": "meter",
                "x": 160, "y": 820, "w": 760, "value": 0.9,
                "number": 350, "unit": " ATM", "title": "GLACIAL HYDROSTATIC OVERBURDEN", "dur": 2.0, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "50X OXYGEN HYPERSATURATION",
                "x": 280, "y": 940, "size": 24, "t0": 1.4
            })
        elif s_idx == 3:
            elements.append({
                "type": "pill",
                "text": "STERILE CORE DRILLING PROTOCOL",
                "x": 260, "y": 820, "size": 24, "t0": 0.6
            })
        elif s_idx == 4:
            elements.append({
                "type": "stamp",
                "text": "NOVEL DNA DISCOVERED",
                "color": "#38bdf8",
                "x": 540, "y": 860, "size": 52, "rotate": -5, "t0": 1.2
            })
        elif s_idx == 5:
            elements.append({
                "type": "pill",
                "text": "FEEDING ON BEDROCK MINERALS",
                "x": 280, "y": 840, "size": 24, "t0": 0.6
            })
        elif s_idx == 6:
            elements.append({
                "type": "stamp",
                "text": "EUROPA & ENCELADUS ANALOG",
                "color": "#ffd166",
                "x": 540, "y": 860, "size": 48, "rotate": -4, "t0": 1.2
            })

    # 5. Darvaza Crater
    elif "darvaza" in topic_id:
        if s_idx == 0:
            elements.append({
                "type": "pill",
                "text": "KARAKUM DESERT • TURKMENISTAN",
                "x": 260, "y": 800, "size": 24, "t0": 0.5
            })
        elif s_idx == 1:
            elements.append({
                "type": "bignumber",
                "from": 1971, "to": 2026, "prefix": "BURNING SINCE ",
                "x": 540, "y": 780, "size": 90, "color": "#f97316", "dur": 2.0, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "70M WIDE • 30M DEEP PIT",
                "x": 330, "y": 880, "size": 24, "t0": 0.6
            })
        elif s_idx == 2:
            elements.append({
                "type": "stamp",
                "text": "DRILLING RIG COLLAPSED",
                "color": "#ff3b30",
                "x": 540, "y": 860, "size": 50, "rotate": -6, "t0": 1.2
            })
        elif s_idx == 3:
            elements.append({
                "type": "pill",
                "text": "ENGINEERS IGNITED METHANE",
                "x": 280, "y": 820, "size": 24, "t0": 0.6
            })
            elements.append({
                "type": "stamp",
                "text": "EXPECTED: 3 WEEKS",
                "color": "#ffd166",
                "x": 540, "y": 940, "size": 48, "t0": 1.6
            })
        elif s_idx == 4:
            elements.append({
                "type": "meter",
                "x": 160, "y": 820, "w": 760, "value": 0.95,
                "number": 400, "unit": " °C", "title": "GROUND FLAME TEMPERATURE", "dur": 2.0, "t0": 0.3
            })
        elif s_idx == 5:
            elements.append({
                "type": "pill",
                "text": "HEAT-SUIT DESCENT MISSION",
                "x": 290, "y": 820, "size": 24, "t0": 0.6
            })
        elif s_idx == 6:
            elements.append({
                "type": "stamp",
                "text": "EXTREMOPHILES IN THE FIRE",
                "color": "#f97316",
                "x": 540, "y": 860, "size": 50, "rotate": -4, "t0": 1.2
            })

    # 6. Tardigrades
    elif "tardigrades" in topic_id:
        if s_idx == 0:
            elements.append({
                "type": "bignumber",
                "from": 0, "to": 0.5, "suffix": " mm",
                "x": 540, "y": 780, "size": 140, "color": "#3ecf6a", "dur": 2.0, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "MICROSCOPIC WATER BEAR",
                "x": 320, "y": 880, "size": 24, "t0": 0.6
            })
        elif s_idx == 1:
            elements.append({
                "type": "stamp",
                "text": "CRYPTOBIOSIS INITIATED",
                "color": "#ffd166",
                "x": 540, "y": 850, "size": 52, "rotate": -5, "t0": 1.2
            })
        elif s_idx == 2:
            elements.append({
                "type": "meter",
                "x": 160, "y": 820, "w": 760, "value": 0.01,
                "number": 0.01, "unit": " %", "title": "METABOLIC ACTIVITY RATE", "dur": 2.2, "t0": 0.3
            })
        elif s_idx == 3:
            elements.append({
                "type": "pill",
                "text": "CELLULAR BIOLOGICAL GLASS",
                "x": 280, "y": 820, "size": 24, "t0": 0.6
            })
        elif s_idx == 4:
            elements.append({
                "type": "pill",
                "text": "-272°C TO +150°C",
                "tone": "red",
                "x": 360, "y": 760, "size": 26, "t0": 0.4
            })
            elements.append({
                "type": "stamp",
                "text": "SPACE VACUUM SURVIVOR",
                "color": "#3ecf6a",
                "x": 540, "y": 880, "size": 50, "t0": 1.5
            })
        elif s_idx == 5:
            elements.append({
                "type": "bignumber",
                "from": 1, "to": 1000, "suffix": "x",
                "x": 540, "y": 780, "size": 140, "color": "#ff3b30", "dur": 2.2, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "HUMAN LETHAL RADIATION DOSE",
                "x": 260, "y": 890, "size": 24, "t0": 0.6
            })
        elif s_idx == 6:
            elements.append({
                "type": "stamp",
                "text": "IMMORTAL MICRO-METAZOA",
                "color": "#3ecf6a",
                "x": 540, "y": 860, "size": 52, "rotate": -4, "t0": 1.2
            })

    # 7. Wow! Signal
    elif "wow" in topic_id:
        if s_idx == 0:
            elements.append({
                "type": "pill",
                "text": "OHIO STATE • BIG EAR OBSERVATORY",
                "x": 240, "y": 800, "size": 24, "t0": 0.5
            })
        elif s_idx == 1:
            elements.append({
                "type": "bignumber",
                "from": 0, "to": 72, "suffix": " sec",
                "x": 540, "y": 780, "size": 150, "color": "#f59e0b", "dur": 2.0, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "NARROWBAND RADIO TRANSMISSION",
                "x": 260, "y": 900, "size": 24, "t0": 0.6
            })
        elif s_idx == 2:
            elements.append({
                "type": "bignumber",
                "prefix": "", "from": 0, "to": 1, "suffix": "",
                "x": 540, "y": 780, "size": 100, "color": "#ff3b30", "dur": 0.5, "t0": 0.3
            })
            elements.append({
                "type": "stamp",
                "text": "6EQUJ5 TELEMETRY",
                "color": "#ff3b30",
                "x": 540, "y": 850, "size": 60, "rotate": -6, "t0": 1.0
            })
        elif s_idx == 3:
            elements.append({
                "type": "circle",
                "x": 540, "y": 820, "rx": 280, "ry": 180, "color": "#ff3b30", "width": 6, "t0": 0.5
            })
            elements.append({
                "type": "stamp",
                "text": "WOW!",
                "color": "#ff3b30",
                "x": 540, "y": 820, "size": 90, "rotate": -8, "t0": 1.0
            })
        elif s_idx == 4:
            elements.append({
                "type": "bignumber",
                "from": 0, "to": 1420.4, "suffix": " MHz",
                "x": 540, "y": 780, "size": 115, "color": "#38bdf8", "dur": 2.2, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "21-CENTIMETER HYDROGEN LINE",
                "x": 280, "y": 890, "size": 24, "t0": 0.6
            })
        elif s_idx == 5:
            elements.append({
                "type": "pill",
                "text": "EXTRATERRESTRIAL CANDIDATE #1",
                "x": 260, "y": 820, "size": 24, "t0": 0.6
            })
        elif s_idx == 6:
            elements.append({
                "type": "stamp",
                "text": "THE SIGNAL NEVER RETURNED",
                "color": "#f59e0b",
                "x": 540, "y": 860, "size": 48, "rotate": -4, "t0": 1.2
            })

    # 8. Chernobyl Elephant's Foot
    elif "chernobyl" in topic_id:
        if s_idx == 0:
            elements.append({
                "type": "pill",
                "text": "CHERNOBYL UNIT 4 SUB-BASEMENT",
                "tone": "red",
                "x": 260, "y": 800, "size": 24, "t0": 0.5
            })
        elif s_idx == 1:
            elements.append({
                "type": "stamp",
                "text": "CORIUM LAVA FLOW",
                "color": "#ef4444",
                "x": 540, "y": 850, "size": 52, "rotate": -5, "t0": 1.0
            })
        elif s_idx == 2:
            elements.append({
                "type": "bignumber",
                "from": 0, "to": 2000, "suffix": " °C",
                "x": 540, "y": 780, "size": 130, "color": "#ef4444", "dur": 2.2, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "CORE MELTDOWN TEMPERATURE",
                "x": 280, "y": 880, "size": 24, "t0": 0.6
            })
        elif s_idx == 3:
            elements.append({
                "type": "meter",
                "x": 160, "y": 820, "w": 760, "value": 1.0,
                "number": 10000, "unit": " R/HR", "title": "IONIZING RADIATION FIELD", "dur": 2.0, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "300 SECONDS = LETHAL DOSE",
                "tone": "red",
                "x": 280, "y": 940, "size": 26, "t0": 1.5
            })
        elif s_idx == 4:
            elements.append({
                "type": "pill",
                "text": "GAMMA-RAY FILM DEGRADATION",
                "x": 270, "y": 820, "size": 24, "t0": 0.6
            })
        elif s_idx == 5:
            elements.append({
                "type": "stamp",
                "text": "RADIOTROPHIC FUNGI",
                "color": "#ffd166",
                "x": 540, "y": 860, "size": 52, "rotate": -4, "t0": 1.2
            })

    # 9. Devil's Kettle
    elif "devils_kettle" in topic_id:
        if s_idx == 0:
            elements.append({
                "type": "pill",
                "text": "BRULE RIVER • MINNESOTA",
                "x": 310, "y": 800, "size": 24, "t0": 0.5
            })
        elif s_idx == 1:
            elements.append({
                "type": "stamp",
                "text": "RIVER SPLITS IN TWO",
                "color": "#10b981",
                "x": 540, "y": 850, "size": 52, "rotate": -5, "t0": 1.0
            })
        elif s_idx == 2:
            elements.append({
                "type": "pill",
                "text": "VOLCANIC RHYOLITE POTHOLE",
                "x": 280, "y": 820, "size": 24, "t0": 0.6
            })
        elif s_idx == 3:
            elements.append({
                "type": "circle",
                "x": 540, "y": 820, "rx": 280, "ry": 280, "color": "#10b981", "width": 5, "t0": 0.5
            })
            elements.append({
                "type": "stamp",
                "text": "NO VISIBLE EXIT POINT",
                "color": "#ffd166",
                "x": 540, "y": 820, "size": 50, "rotate": -6, "t0": 1.2
            })
        elif s_idx == 4:
            elements.append({
                "type": "pill",
                "text": "DYES • PING-PONG BALLS • GPS",
                "x": 260, "y": 820, "size": 24, "t0": 0.6
            })
            elements.append({
                "type": "stamp",
                "text": "VANISHED COMPLETELY",
                "color": "#ff3b30",
                "x": 540, "y": 940, "size": 48, "t0": 1.5
            })
        elif s_idx == 5:
            elements.append({
                "type": "pill",
                "text": "ACOUSTIC DOPPLER VELOCIMETRY",
                "x": 250, "y": 820, "size": 24, "t0": 0.6
            })
        elif s_idx == 6:
            elements.append({
                "type": "stamp",
                "text": "UNDERGROUND RESURGENCE",
                "color": "#10b981",
                "x": 540, "y": 860, "size": 48, "rotate": -4, "t0": 1.2
            })

    # 10. Silurian Hypothesis
    elif "silurian" in topic_id:
        if s_idx == 0:
            elements.append({
                "type": "bignumber",
                "from": 0, "to": 50, "suffix": "M BC",
                "x": 540, "y": 780, "size": 130, "color": "#c084fc", "dur": 2.2, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "PRE-HUMAN DEEP TIME",
                "x": 330, "y": 880, "size": 24, "t0": 0.6
            })
        elif s_idx == 1:
            elements.append({
                "type": "pill",
                "text": "NASA GODDARD ASTROBIOLOGY",
                "x": 280, "y": 820, "size": 24, "t0": 0.6
            })
        elif s_idx == 2:
            elements.append({
                "type": "bignumber",
                "from": 0, "to": 0.01, "suffix": " %",
                "x": 540, "y": 780, "size": 130, "color": "#ffd166", "dur": 2.0, "t0": 0.3
            })
            elements.append({
                "type": "pill",
                "text": "HUMAN ERA VS EARTH TIMELINE",
                "x": 270, "y": 890, "size": 24, "t0": 0.6
            })
        elif s_idx == 3:
            elements.append({
                "type": "stamp",
                "text": "FOSSILIZATION IS RARE",
                "color": "#c084fc",
                "x": 540, "y": 850, "size": 52, "rotate": -5, "t0": 1.2
            })
        elif s_idx == 4:
            elements.append({
                "type": "pill",
                "text": "CITIES CRUMBLE IN 5,000 YEARS",
                "tone": "red",
                "x": 270, "y": 820, "size": 24, "t0": 0.6
            })
        elif s_idx == 5:
            elements.append({
                "type": "pill",
                "text": "ISOTOPES • PLASTICS • CARBON SPIKES",
                "x": 230, "y": 820, "size": 24, "t0": 0.6
            })
            elements.append({
                "type": "stamp",
                "text": "IMMORTAL TECHNO-FOSSILS",
                "color": "#ffd166",
                "x": 540, "y": 940, "size": 48, "t0": 1.5
            })
        elif s_idx == 6:
            elements.append({
                "type": "stamp",
                "text": "A WHISPER IN DEEP TIME",
                "color": "#c084fc",
                "x": 540, "y": 860, "size": 52, "rotate": -4, "t0": 1.2
            })

    return elements

if __name__ == "__main__":
    print("scene_builder ready for 10 topics.")
