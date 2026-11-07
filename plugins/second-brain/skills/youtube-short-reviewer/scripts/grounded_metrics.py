"""Measure the objective signals used by the Grounded Retention Score (GRS).
Usage: python grounded_metrics.py VIDEO.mp4 [--voice VOICE.wav] [--out metrics.json]
Every number here is evidence for a GRS line item; the judge must cite them.
"""
import argparse, json, re, subprocess, sys

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stderr

def probe(v):
    out = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration:stream=width,height,r_frame_rate",
                          "-of","json",v],capture_output=True,text=True).stdout
    j = json.loads(out); s = [x for x in j["streams"] if "width" in x][0]
    num, den = s["r_frame_rate"].split("/")
    return float(j["format"]["duration"]), s["width"], s["height"], float(num)/float(den)

def loudness(v):
    e = run(["ffmpeg","-nostats","-i",v,"-af","ebur128=peak=true","-f","null","-"])
    s = e[e.rfind("Summary:"):]
    g = lambda k: float(re.search(k+r":\s+(-?[\d.]+)", s).group(1))
    return {"lufs": g("I"), "lra": g("LRA"), "true_peak_dbfs": g("Peak")}

def voice_gaps(w, thresh=-35, mind=0.25):
    e = run(["ffmpeg","-nostats","-i",w,"-af",f"silencedetect=n={thresh}dB:d={mind}","-f","null","-"])
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", e)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", e)]
    return list(zip(st, en))

def motion(v, fps):
    # mean absolute luma change between consecutive frames (0-255), at a small size
    e = subprocess.run(["ffmpeg","-nostats","-i",v,"-vf","scale=180:-1,signalstats,metadata=print:key=lavfi.signalstats.YDIF:file=-",
                        "-f","null","-"],capture_output=True,text=True).stdout
    vals = [float(x) for x in re.findall(r"YDIF=([\d.]+)", e)]
    t = [i/fps for i in range(len(vals))]
    return t, vals

def cuts(v, th=0.25):
    e = run(["ffmpeg","-nostats","-i",v,"-vf",f"select='gt(scene,{th})',showinfo","-f","null","-"])
    return [round(float(x),2) for x in re.findall(r"pts_time:([\d.]+)", e)]

def luma_at(v, t):
    e = run(["ffmpeg","-nostats","-ss",str(t),"-i",v,"-frames:v","1","-vf","signalstats,metadata=print:key=lavfi.signalstats.YAVG","-f","null","-"])
    m = re.search(r"YAVG=([\d.]+)", e)
    return float(m.group(1)) if m else None

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("--voice"); ap.add_argument("--out")
    a = ap.parse_args()
    dur, w, h, fps = probe(a.video)
    m = {"duration_s": round(dur,2), "resolution": f"{w}x{h}", "fps": fps}
    m.update(loudness(a.video))
    c = cuts(a.video); m["cuts"] = c
    pts = [0]+c+[dur]; m["longest_shot_s"] = round(max(b-a_ for a_,b in zip(pts,pts[1:])),2)
    m["visual_changes_per_10s"] = round(len(c)/dur*10,2)
    t, y = motion(a.video, fps)
    # per-second motion and "static" stretches (no cut and avg YDIF < 1.0 for >= 2s)
    sec = {}
    for ti, yi in zip(t, y): sec.setdefault(int(ti), []).append(yi)
    per_sec = {k: round(sum(v)/len(v),2) for k,v in sec.items()}
    m["motion_per_second"] = per_sec
    static, run_start = [], None
    for k in sorted(per_sec):
        if per_sec[k] < 1.0:
            run_start = k if run_start is None else run_start
        else:
            if run_start is not None and k-run_start >= 2: static.append([run_start, k])
            run_start = None
    if run_start is not None and len(per_sec)-run_start >= 2: static.append([run_start, len(per_sec)])
    m["static_stretches_s"] = static
    m["first_frame_luma"] = luma_at(a.video, 0)
    m["frame_0.5s_luma"] = luma_at(a.video, 0.5)
    m["last_frame_luma"] = luma_at(a.video, max(dur-0.05,0))
    if a.voice:
        g = voice_gaps(a.voice)
        inner = [(s,e) for s,e in g if s > 0.05 and e < dur-0.05]
        m["voice_start_s"] = round(g[0][1],2) if g and g[0][0] == 0 else 0.0
        m["voice_gaps"] = [[round(s,2), round(e-s,2)] for s,e in inner]
        m["dead_air_s"] = round(sum(e-s for s,e in inner),2)
        m["dead_air_pct"] = round(100*m["dead_air_s"]/dur,1)
        m["longest_gap_s"] = round(max([e-s for s,e in inner] or [0]),2)
    js = json.dumps(m, ensure_ascii=False, indent=1)
    if a.out: open(a.out,"w",encoding="utf-8").write(js)
    print(js)

if __name__ == "__main__":
    main()
