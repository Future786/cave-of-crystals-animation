#!/usr/bin/env python3
"""
Batch Video Renderer for Topics 02 through 10 (or specified IDs).
Renders 540x960 24fps Mobile MP4 videos sequentially using scripts/render.mjs
"""

import os
import sys
import time
import subprocess
from topics_config import TOPICS

REPO_DIR = "/home/antigravity/Future786/cave-of-crystals-animation"
VIDEOS_DIR = os.path.join(REPO_DIR, "videos")
SCENES_DIR = os.path.join(REPO_DIR, "scenes")
RENDER_SCRIPT = os.path.join(REPO_DIR, "scripts", "render.mjs")

def render_topics(target_ids=None):
    os.makedirs(VIDEOS_DIR, exist_ok=True)
    targets = [t for t in TOPICS if target_ids is None or t["id"] in target_ids]
    
    total = len(targets)
    start_all = time.time()
    print(f"🎬 Starting batch render of {total} videos...", flush=True)

    for i, t in enumerate(targets):
        t_id = t["id"]
        title = t["title"]
        scene_json = os.path.join(SCENES_DIR, f"{t_id}.json")
        out_mp4 = os.path.join(VIDEOS_DIR, f"{t_id}_Mobile.mp4")

        print(f"\n=======================================================", flush=True)
        print(f"[{i+1}/{total}] Rendering: {t_id} — {title}", flush=True)
        print(f"=======================================================", flush=True)

        t_start = time.time()
        cmd = ["node", RENDER_SCRIPT, scene_json, out_mp4, "--scale", "0.5"]
        res = subprocess.run(cmd)
        if res.returncode != 0:
            print(f"❌ ERROR rendering {t_id}! Return code: {res.returncode}", flush=True)
            sys.exit(res.returncode)

        elapsed = round(time.time() - t_start, 1)
        file_size_mb = round(os.path.getsize(out_mp4) / (1024 * 1024), 2)
        print(f"✅ Completed {t_id} in {elapsed}s ({file_size_mb} MB) -> {out_mp4}", flush=True)

    total_time = round(time.time() - start_all, 1)
    print(f"\n🎉 Finished batch render of {total} videos in {total_time}s!", flush=True)

if __name__ == "__main__":
    ids = sys.argv[1:] if len(sys.argv) > 1 else None
    render_topics(ids)
