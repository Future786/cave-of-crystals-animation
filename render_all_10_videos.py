#!/usr/bin/env python3
"""
Master Production Pipeline for 10 Viral Scientific Documentary Animations
Phased Execution:
  Phase 1: Synthesize all 10 audio tracks, build scene JSONs, and render contact sheets (Fast: ~2 mins)
  Phase 2: Render all 10 Mobile MP4 videos (540x960, 24fps)
  Phase 3: Render Full HD MP4 videos (1080x1920, 24fps)
"""

import os
import sys
import time
import json
import subprocess
from topics_config import TOPICS
from audio_generator import build_topic_audio
from scene_builder import build_topic_scenes

REPO_DIR = "/home/antigravity/Future786/cave-of-crystals-animation"
VIDEOS_DIR = os.path.join(REPO_DIR, "videos")
SCENES_DIR = os.path.join(REPO_DIR, "scenes")
AUDIO_DIR = os.path.join(REPO_DIR, "audio")
RENDER_SCRIPT = os.path.join(REPO_DIR, "scripts", "render.mjs")

os.makedirs(VIDEOS_DIR, exist_ok=True)
os.makedirs(SCENES_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

def main():
    total_start = time.time()
    total = len(TOPICS)
    manifest = []

    print(f"===========================================================", flush=True)
    print(f"🚀 PHASE 1: GENERATING AUDIO, SCENES & STORYBOARDS (10 TOPICS)", flush=True)
    print(f"===========================================================", flush=True)

    for i, topic in enumerate(TOPICS):
        t_id = topic["id"]
        title = topic["title"]
        print(f"\n[{i+1}/{total}] Setting up: {title}", flush=True)

        # 1. Audio
        timing_file = os.path.join(AUDIO_DIR, t_id, "timing.json")
        if os.path.exists(timing_file):
            with open(timing_file, "r") as f:
                timing = json.load(f)
            print(f"   ✓ Audio ready ({timing['duration']}s)", flush=True)
        else:
            timing = build_topic_audio(t_id, topic["sentences"], AUDIO_DIR)
            print(f"   ✓ Synthesized voiceover & mixed bed ({timing['duration']}s)", flush=True)

        # 2. Scene JSON
        scene_file = build_topic_scenes(topic, timing, SCENES_DIR)
        print(f"   ✓ Scene JSON built ({scene_file})", flush=True)

        # 3. Contact Sheet
        contact_png = os.path.join(REPO_DIR, f"{t_id}_contact.png")
        if not os.path.exists(contact_png):
            cmd_contact = ["node", RENDER_SCRIPT, scene_file, contact_png, "--contact"]
            subprocess.run(cmd_contact, check=True)
            print(f"   ✓ Contact sheet rendered ({contact_png})", flush=True)
        else:
            print(f"   ✓ Contact sheet exists", flush=True)

        manifest.append({
            "id": t_id,
            "title": title,
            "duration": timing["duration"],
            "sentences": timing["sentences"],
            "contact_png": contact_png,
            "scene_json": scene_file,
            "mobile_mp4": os.path.join(VIDEOS_DIR, f"{t_id}_Mobile.mp4"),
            "hd_mp4": os.path.join(VIDEOS_DIR, f"{t_id}_HD.mp4")
        })

    phase1_time = round(time.time() - total_start, 1)
    print(f"\n✨ Phase 1 Complete in {phase1_time}s! All 10 storyboards and audio tracks ready.", flush=True)

    print(f"\n===========================================================", flush=True)
    print(f"📱 PHASE 2: RENDERING 10 MOBILE VIDEOS (540x960, 24 FPS)", flush=True)
    print(f"===========================================================", flush=True)

    for i, item in enumerate(manifest):
        t_id = item["id"]
        title = item["title"]
        mobile_path = item["mobile_mp4"]

        print(f"\n🎬 [{i+1}/{total}] Rendering Mobile Video: {title}", flush=True)
        t_start = time.time()
        cmd_mobile = ["node", RENDER_SCRIPT, item["scene_json"], mobile_path, "--scale", "0.5"]
        subprocess.run(cmd_mobile, check=True)
        elapsed = round(time.time() - t_start, 1)
        print(f"   ✓ Finished {title} Mobile MP4 in {elapsed}s: {mobile_path}", flush=True)

    # Save manifest
    with open(os.path.join(VIDEOS_DIR, "production_manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)

    total_time = round(time.time() - total_start, 1)
    print(f"\n🎉 ALL 10 VIDEOS SUCCESSFULLY GENERATED IN {total_time}s!", flush=True)

if __name__ == "__main__":
    main()
