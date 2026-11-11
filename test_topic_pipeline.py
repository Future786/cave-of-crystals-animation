#!/usr/bin/env python3
import os
import subprocess
from topics_config import TOPICS
from audio_generator import build_topic_audio
from scene_builder import build_topic_scenes

def test_pipeline():
    topic = TOPICS[0] # Mariana Trench
    print(f"=== Testing Pipeline for Topic 1: {topic['title']} ===")

    # 1. Build Audio
    print("1. Synthesizing voiceover and mixing audio bed...")
    timing = build_topic_audio(topic["id"], topic["sentences"])
    print(f"   Audio completed! Duration: {timing['duration']}s, Sentences: {len(timing['sentences'])}")

    # 2. Build Scene JSON
    print("2. Building Scene JSON...")
    scene_file = build_topic_scenes(topic, timing)
    print(f"   Scene JSON created at: {scene_file}")

    # 3. Render Contact Sheet
    print("3. Rendering Contact Sheet...")
    contact_png = f"/home/antigravity/Future786/cave-of-crystals-animation/{topic['id']}_contact.png"
    render_script = "/home/antigravity/Future786/cave-of-crystals-animation/scripts/render.mjs"
    cmd_contact = ["node", render_script, scene_file, contact_png, "--contact"]
    subprocess.run(cmd_contact, check=True)
    print(f"   Contact sheet rendered: {contact_png}")

    # 4. Render 5-second sample clip to verify video & audio muxing
    print("4. Rendering 5-second sample MP4...")
    sample_mp4 = f"/tmp/{topic['id']}_sample.mp4"
    cmd_mp4 = ["node", render_script, scene_file, sample_mp4, "--scale", "0.5", "--to", "5"]
    subprocess.run(cmd_mp4, check=True)
    print(f"   Sample MP4 rendered: {sample_mp4}")

    print("=== Pipeline Test Succeeded! ===")

if __name__ == "__main__":
    test_pipeline()
