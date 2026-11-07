
# Grounded Retention Score (GRS)

The aim is to predict whether viewers stop scrolling and keep watching, with no unsupported opinions.

## The groundedness rule
Every line item needs **evidence**: a number from `grounded_metrics.py`, a timestamp plus frame, a quoted script line with its time, or a source link.
- If there's no evidence, the item scores 0 and is marked `NO EVIDENCE`.
- If the judge cannot perceive something (for example, an AI can't hear voice tone), the item is marked `NOT JUDGED`. It is removed from the total, and the score is rescaled to 100.
- Feelings ("viewers will feel bored here") are allowed only when they're tied to evidence (for example, "3 s static at 0:09-0:12 + 0.7 s voice gap").
- **Groundedness %** = cited items / scored items. It must be 100% before the score is reported.

## Step 1: measure
```
python tools/grounded_metrics.py <video.mp4> --voice <clean voice track.wav> --out <review>/metrics.json
```
Then make contact sheets (4 fps for 0-4 s, 1 fps for the whole video) and look at them.

## Step 2: score (100 pts)

### A. Hook, 0-3 s (25)
| # | Item | Full | Half | 0 |
|---|---|---|---|---|
| A1 | First frame readable (`first_frame_luma`) | ≥40 at 0 s (4) | ≥40 at 0.5 s (2) | darker |
| A2 | Voice starts (`voice_start_s`) | ≤0.5 s (4) | ≤1.0 s (2) | later |
| A3 | Visual change early | cut or motion ≥2.0 between 0.5-2 s (5) | first cut ≤3 s (2) | none |
| A4 | Curiosity gap (myth-bust, question, surprising claim) said by 3 s; quote it | strong + by 3 s (8) | weak or late (4) | none |
| A5 | Big hook text on screen (≤6 words, readable at a glance) | (4) | small or long (1-2) | none |

### B. Pacing (25)
| # | Item | Full | Half | 0 |
|---|---|---|---|---|
| B1 | `dead_air_pct` (no voice) | ≤8% (7) | ≤15% (3) | >15% |
| B2 | `longest_gap_s` | ≤0.4 (4) | ≤0.7 (2) | >0.7 |
| B3 | Static time = sum of `static_stretches_s` / duration | ≤10% (7) | ≤25% (3) | >25% |
| B4 | `visual_changes_per_10s` | ≥3.3 (4) | ≥2.0 (2) | <2 |
| B5 | `longest_shot_s` | ≤4 (3) | ≤6 (1) | >6 |

### C. Story and payoff (20). Quote the line and its time for each item.
| # | Item | Pts |
|---|---|---|
| C1 | Clear shape: hook → steps → reveal | 5 |
| C2 | Mid-video re-hook (a turn like "แต่...", a question or a twist) before 50% | 5 |
| C3 | Main payoff lands before 80% of the runtime | 5 |
| C4 | Clean end: ≤0.8 s after the last word, no fade to black, last frame can loop to the first | 5 |

### D. Phone readability (10)
| # | Item | Pts |
|---|---|---|
| D1 | Captions sit between 15% and 70% of the height (out of the Shorts title/button zone) | 4 |
| D2 | Caption chunks ≤ ~25 Thai chars / 6 words, text height ≥4% of the frame | 4 |
| D3 | Resolution 1080x1920 (720x1280 = 1) | 2 |

### E. Audio (10)
| # | Item | Pts |
|---|---|---|
| E1 | `lufs` between -15 and -13 | 4 |
| E2 | `true_peak_dbfs` ≤ -1 | 3 |
| E3 | Voice energy fits the style asked for (needs a human ear, otherwise NOT JUDGED) | 3 |

### F. Accuracy and trust (10)
| # | Item | Pts |
|---|---|---|
| F1 | Every factual claim checked against a source (link it); deduct 1-2 per imprecise claim | 6 |
| F2 | No overclaim; CTA is specific and fits the episode (affiliate link only where planned) | 4 |

## Step 3: verdict
- **85+** ready to post. **70-84** post, but fix the top issue next time. **55-69** fix before posting. **<55** rework.
- Write a viewer walkthrough: second by second, how the viewer feels and where they swipe, each point citing evidence.
- List the top 3 fixes with the points each would win back.
- The predicted "stayed past 3 s" and "average % viewed" are **hypotheses**. After posting, log the real YouTube Analytics numbers (Viewed vs swiped away, Average percentage viewed) beside the GRS in `review/score-log.md`. Re-weight items that don't predict the real numbers.
