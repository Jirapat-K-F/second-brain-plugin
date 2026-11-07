"""Public stats + top comments for posted YouTube videos (YouTube Data API v3, API key only).

  python yt_stats.py --env <Youtube>/.env VIDEO_ID [VIDEO_ID ...] [--comments 20]

Reads YOUTUBE_API_KEY from the environment or from the .env file (never pass the key on the command line,
never print it). Prints JSON: [{id, title, published, views, likes, comments, top_comments: [{text, likes}]}].
Comments work only on public videos with comments enabled. Quota: ~1 unit per call (10,000 units/day free).
"""
import argparse, json, os, sys, urllib.parse, urllib.request

API = "https://www.googleapis.com/youtube/v3/"


def key_from(env_path):
    k = os.environ.get("YOUTUBE_API_KEY")
    if not k and env_path and os.path.exists(env_path):
        for line in open(env_path, encoding="utf-8"):
            if line.strip().startswith("YOUTUBE_API_KEY"):
                k = line.split("=", 1)[1].strip().strip("'\"")
    if not k: sys.exit("no YOUTUBE_API_KEY (add it to the Youtube folder's .env)")
    return k


def get(endpoint, **params):
    url = API + endpoint + "?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=30) as r: return json.load(r)
    except urllib.error.HTTPError as e:   # e.g. comments disabled -> 403; keep going without them
        return {"error": e.code}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("ids", nargs="+"); ap.add_argument("--env"); ap.add_argument("--comments", type=int, default=20)
    a = ap.parse_args(); k = key_from(a.env); out = []
    vids = get("videos", part="snippet,statistics", id=",".join(a.ids), key=k).get("items", [])
    for v in vids:
        s = v.get("statistics", {})
        c = get("commentThreads", part="snippet", videoId=v["id"], order="relevance", maxResults=a.comments, textFormat="plainText", key=k)
        top = [{"text": t["snippet"]["topLevelComment"]["snippet"]["textDisplay"], "likes": t["snippet"]["topLevelComment"]["snippet"].get("likeCount", 0)} for t in c.get("items", [])]
        out.append({"id": v["id"], "title": v["snippet"]["title"], "published": v["snippet"]["publishedAt"], "views": int(s.get("viewCount", 0)),
                    "likes": int(s.get("likeCount", 0)), "comments": int(s.get("commentCount", 0)), "top_comments": top})
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
