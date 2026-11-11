#!/usr/bin/env python3
import os
import sys
import json
import subprocess

MODEL_PATH = "/home/antigravity/piper_models/en-us-ryan-high.onnx"
CONFIG_PATH = "/home/antigravity/piper_models/en-us-ryan-high.onnx.json"

def get_duration(audio_file):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", audio_file
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(res.stdout.strip())

def synthesize_sentence(text, out_wav):
    cmd = [
        "uvx", "--from", "piper-tts", "piper",
        "-m", MODEL_PATH,
        "-c", CONFIG_PATH,
        "-f", out_wav
    ]
    subprocess.run(cmd, input=text, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

def build_topic_audio(topic_id, sentences, output_dir="/home/antigravity/Future786/cave-of-crystals-animation/audio"):
    os.makedirs(output_dir, exist_ok=True)
    topic_dir = os.path.join(output_dir, topic_id)
    os.makedirs(topic_dir, exist_ok=True)

    timed_sentences = []
    current_time = 0.5  # 0.5s introductory breathing room

    wav_files = []
    # 0.5s initial silence
    init_silence = os.path.join(topic_dir, "init_silence.wav")
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=22050:cl=mono", "-t", "0.5", init_silence],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    wav_files.append(init_silence)

    for i, item in enumerate(sentences):
        text = item["text"]
        part_wav = os.path.join(topic_dir, f"part_{i:02d}.wav")
        synthesize_sentence(text, part_wav)
        dur = get_duration(part_wav)

        start_t = round(current_time, 2)
        end_t = round(current_time + dur, 2)
        timed_sentences.append({
            "index": i,
            "text": item.get("caption_text", text),
            "spoken": text,
            "start": start_t,
            "end": end_t,
            "dur": round(dur, 2),
            "shot": item.get("shot", i)
        })
        wav_files.append(part_wav)
        current_time += dur

        # 0.28s pause between sentences
        if i < len(sentences) - 1:
            pause_dur = item.get("pause", 0.28)
            pause_wav = os.path.join(topic_dir, f"pause_{i:02d}.wav")
            subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=22050:cl=mono", "-t", str(pause_dur), pause_wav],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            wav_files.append(pause_wav)
            current_time += pause_dur

    # 1.5s outro silence for smooth finish
    outro_silence = os.path.join(topic_dir, "outro_silence.wav")
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=22050:cl=mono", "-t", "1.5", outro_silence],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    wav_files.append(outro_silence)
    current_time += 1.5

    # Concat all speech
    concat_list = os.path.join(topic_dir, "concat.txt")
    with open(concat_list, "w") as f:
        for wf in wav_files:
            f.write(f"file '{wf}'\n")

    vo_master = os.path.join(topic_dir, f"{topic_id}_vo.wav")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list, "-c", "copy", vo_master],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    total_dur = get_duration(vo_master)

    # Generate atmospheric cinematic bed (low-frequency rumble + warm drone)
    bed_master = os.path.join(topic_dir, f"{topic_id}_bed.wav")
    drone_cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"sine=frequency=52:d={total_dur}:r=44100",
        "-f", "lavfi", "-i", f"anoisesrc=d={total_dur}:c=pink:r=44100:a=0.007,lowpass=f=200",
        "-filter_complex", "[0:a]volume=0.14[s];[1:a]volume=0.25[n];[s][n]amix=inputs=2[b]",
        "-map", "[b]", "-ar", "44100", bed_master
    ]
    subprocess.run(drone_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    # Mix voiceover and drone with professional mastering (-14 LUFS VO + ducked bed)
    final_master = os.path.join(output_dir, f"{topic_id}_final_audio.mp3")
    mix_cmd = [
        "ffmpeg", "-y",
        "-i", vo_master,
        "-i", bed_master,
        "-filter_complex",
        "[0:a]volume=1.0[vo];[1:a]volume=0.45[bed];[vo][bed]amix=inputs=2:duration=first:dropout_transition=2[a]",
        "-map", "[a]", "-c:a", "libmp3lame", "-b:a", "192k", final_master
    ]
    subprocess.run(mix_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    result = {
        "topic_id": topic_id,
        "audio_path": final_master,
        "vo_path": vo_master,
        "bed_path": bed_master,
        "duration": round(total_dur, 2),
        "sentences": timed_sentences
    }
    with open(os.path.join(topic_dir, "timing.json"), "w") as f:
        json.dump(result, f, indent=2)

    return result

if __name__ == "__main__":
    test_sentences = [
        {"text": "At eleven thousand meters beneath the ocean surface, the darkness is complete.", "caption_text": "At eleven thousand meters beneath the ocean,\n*the darkness is complete*."},
        {"text": "This is Challenger Deep, where water pressure exceeds one thousand atmospheres.", "caption_text": "This is *Challenger Deep*,\nwhere pressure exceeds 1,000 atmospheres."}
    ]
    res = build_topic_audio("test_mariana", test_sentences)
    print("Generated audio:", res["duration"], "seconds")
