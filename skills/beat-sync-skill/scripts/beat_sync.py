#!/usr/bin/env python3
"""beat_sync.py — BGM 파형 분석으로 비트 싱크 편집을 처방한다.

Claude(또는 사람)가 음악을 직접 못 들어도, 파형에서 편집에 필요한 숫자를 뽑는다:
BPM·비트 간격, 에너지 곡선(인트로/빌드업), 드랍 정확 시점, 편집 처방(컷 길이·버스트·스냅 지점).

사용법:
  python beat_sync.py cuts <오디오|영상> [시작 끝]      # ★본업: 음성 무음 구간 → 안전한 컷 지점 목록
  python beat_sync.py analyze <오디오|영상>            # (실험적) 음악 분석 + 편집 처방
  python beat_sync.py fine <오디오|영상> <시작초> <끝초>  # 특정 구간 0.05초 정밀 스캔
  python beat_sync.py verify <편집본영상> <기대드랍초>    # 편집본에서 드랍이 그 시점에 있는지 검증

의존성: ffmpeg/ffprobe(PATH) + 파이썬 표준 라이브러리만 (numpy 불필요).
mp3/wav/mp4/mov 등 ffmpeg이 읽는 건 다 됨 (영상이면 오디오 트랙 추출).
"""
import subprocess
import sys
import tempfile
import wave
import array
import math
import os

SR = 8000  # 분석용 샘플레이트 (비트/에너지 분석엔 충분, 파일 작고 빠름)


def die(msg):
    print(f"[에러] {msg}")
    sys.exit(1)


def to_wav(src: str) -> str:
    """입력(오디오/영상)을 분석용 모노 WAV로 변환해 임시 파일 경로를 돌려준다."""
    if not os.path.exists(src):
        die(f"파일 없음: {src}")
    fd, wav = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    r = subprocess.run(
        ["ffmpeg", "-y", "-i", src, "-vn", "-ac", "1", "-ar", str(SR),
         "-c:a", "pcm_s16le", wav],
        capture_output=True, text=True)
    if r.returncode != 0:
        die(f"ffmpeg 변환 실패:\n{r.stderr[-400:]}")
    return wav


def load(wav: str):
    w = wave.open(wav)
    d = array.array("h")
    d.frombytes(w.readframes(w.getnframes()))
    w.close()
    return d


def rms_db(d, i, win):
    seg = d[i:i + win]
    if len(seg) < win:
        return -99.0
    s = 0
    for x in seg[::2]:
        s += x * x
    rms = math.sqrt(s / (len(seg) // 2)) / 32768.0 + 1e-9
    return 20 * math.log10(rms), rms


def energy_curve(d, win_sec=1.0):
    """win_sec 창 RMS 목록 [(초, rms)] — 인트로/빌드업/드랍 후보 파악용."""
    win = int(SR * win_sec)
    out = []
    for i in range(0, len(d) - win, win):
        _, rms = rms_db(d, i, win)
        out.append((i / SR, rms))
    return out


def find_drop(d):
    """드랍(에너지가 확 올라가 유지되는 지점)을 거칠게 찾고 → 0.05초 정밀 스캔으로 확정."""
    curve = energy_curve(d, 1.0)
    if len(curve) < 8:
        return None
    # 거칠게: 이후 3초 평균이 이전 3초 평균의 1.5배를 넘는 첫 지점
    best_t, best_ratio = None, 1.5
    vals = [v for _, v in curve]
    for k in range(3, len(vals) - 3):
        prev = sum(vals[k - 3:k]) / 3
        nxt = sum(vals[k:k + 3]) / 3
        if prev > 0.005 and nxt / (prev + 1e-9) > best_ratio:
            best_ratio = nxt / (prev + 1e-9)
            best_t = curve[k][0]
    if best_t is None:
        return None
    # 정밀: best_t 주변(앞 -2.5초 ~ 뒤 +4초)을 0.05초 창으로.
    # (뒤를 넉넉히 잡아야 1초 앞뒤 평균창이 진짜 드랍 위치까지 평가할 수 있다 — 좁으면 후보가 잘림)
    # 드랍 = "지속되는 큰 소리(H)가 시작되는 첫 지점" — 빌드업(중간 크기 상승)과 구분해야 한다:
    #   앞 1초 평균은 아직 낮고(< 0.6H), 뒤 1.5초 평균은 이미 크게(> 0.75H) 유지되는 첫 t.
    win = int(SR * 0.05)
    start = max(0, int((best_t - 2.5) * SR))
    end = min(len(d) - win, int((best_t + 4.0) * SR))
    local = []
    for i in range(start, end, win):
        _, rms = rms_db(d, i, win)
        local.append((i / SR, rms))
    if len(local) < 30:
        return best_t
    vals = [v for _, v in local]
    # 계단 에지 검출: "뒤 1초 평균 - 앞 1초 평균"(step)이 큰 지점들 = 소리가 확 커지는 경계 후보.
    # 빌드업 시작도 step이 크게 나올 수 있어서(실측: 빌드업 0.111 vs 드랍 0.105로 박빙),
    # 후보들 중 "이후 도달 음량(fwd)이 가장 큰" 지점을 드랍으로 고른다 — 드랍은 곡의 최대 에너지로 진입한다.
    k = 20  # 1.0초 (0.05초 창 기준)
    steps = []
    for idx in range(k, len(local) - k):
        fwd = sum(vals[idx:idx + k]) / k
        back = sum(vals[idx - k:idx]) / k
        steps.append((idx, fwd - back, fwd))
    if not steps:
        return best_t
    max_step = max(s for _, s, _ in steps)
    cands = [(idx, s, fwd) for idx, s, fwd in steps if s > max_step * 0.55]
    # 후보 중 fwd(이후 1초 평균 음량) 최대인 지점 — 동률이면 늦은 쪽(본격 진입)
    best_idx = max(cands, key=lambda x: (round(x[2], 3), local[x[0]][0]))[0]
    return local[best_idx][0]


def find_drop_candidates(d, n=3):
    """전체 곡에서 드랍 '후보' 상위 n개를 [(시각, 강도점수)]로 돌려준다 (강도순).
    음악 구조는 곡마다 달라 단일 정답을 단정할 수 없다 — 후보를 여럿 주고 사람이 귀로 확정하게 한다."""
    win = int(SR * 0.05)
    k = 20  # 1초 평균창
    step_list = []
    vals_all = []
    for i in range(0, len(d) - win, win):
        _, rms = rms_db(d, i, win)
        vals_all.append((i / SR, rms))
    v = [x for _, x in vals_all]
    for idx in range(k, len(v) - k):
        fwd = sum(v[idx:idx + k]) / k
        back = sum(v[idx - k:idx]) / k
        step_list.append((idx, fwd - back, fwd))
    if not step_list:
        return [], 0.0
    max_step = max(s for _, s, _ in step_list)
    # 확신도: 곡의 '큰 소리 레벨(H)' 대비 최대 단차 비율.
    # 실측 캘리브레이션 — 드랍 있는 곡: 0.44(쿰비아)/0.46/1.06, 드랍 없는 곡(풀에너지 그루브): 0.37.
    # 경계가 얇으므로 이진 판정 대신 등급을 붙여 정직하게 알린다.
    H = sorted(v)[int(len(v) * 0.85)]
    ratio = max_step / (H + 1e-9)
    if max_step <= 0.02 or ratio < 0.40:
        return [], ratio  # 섹션 전환 수준 — 드랍 없음으로 판정
    # 후보: 단차가 최대의 45% 이상 + 서로 2초 이상 떨어진 지점들, (단차×도달음량) 점수순
    picked = []
    for idx, s, fwd in sorted(step_list, key=lambda x: -(x[1] * (0.5 + x[2]))):
        if s < max_step * 0.45:
            continue
        t = vals_all[idx][0]
        if any(abs(t - pt) < 2.0 for pt, _ in picked):
            continue
        picked.append((t, s * (0.5 + fwd)))
        if len(picked) >= n:
            break
    return picked, ratio


def find_bpm(d, analyze_sec=60):
    """온셋 엔벨로프(0.02초) 자기상관으로 비트 간격 추정. (반배/두배 모호성 있음)"""
    w2 = int(SR * 0.02)
    n_env = min(len(d) // w2, int(analyze_sec / 0.02))
    env = []
    for i in range(0, n_env * w2, w2):
        s = 0
        for x in d[i:i + w2:2]:
            s += abs(x)
        env.append(s)
    onset = [max(0, env[i] - env[i - 1]) for i in range(1, len(env))]
    n = len(onset)
    if n < 100:
        return None
    mean = sum(onset) / n
    o = [x - mean for x in onset]
    best = (0, 0)
    for lag in range(15, 61):  # 0.3~1.2초
        c = sum(o[i] * o[i + lag] for i in range(n - lag))
        if c > best[0]:
            best = (c, lag)
    return best[1] * 0.02 if best[1] else None


def bar(v, scale=90):
    return "#" * max(0, int(v * scale))


def cmd_analyze(src):
    wav = to_wav(src)
    try:
        d = load(wav)
        dur = len(d) / SR
        print(f"파일: {os.path.basename(src)}")
        print(f"길이: {int(dur // 60)}:{int(dur % 60):02d} ({dur:.1f}초)\n")

        # 1) 에너지 곡선 (앞 60초 또는 전체)
        print("[에너지 곡선 — 1초 단위, 막대 길수록 큼]")
        curve = energy_curve(d, 1.0)
        mx = max(v for _, v in curve) if curve else 1
        for t, v in curve[:60]:
            print(f"{int(t):4d}s {bar(v / mx, 40)}")
        if len(curve) > 60:
            print(f"  … (총 {len(curve)}초, 뒤는 생략 — 필요하면 fine으로)")

        # 2) BPM
        beat = find_bpm(d)
        print()
        if beat:
            print(f"비트 간격 ≈ {beat:.2f}초  (BPM ≈ {60 / beat:.0f} — 반배/두배 모호성 있음)")
            print(f"  반박자 = {beat / 2:.2f}초")
        else:
            print("비트 간격을 못 찾음 (비트가 약한 곡일 수 있음)")

        # 3) 드랍 — 단정하지 않고 후보로 (음악 구조 분석은 추정이다)
        cands, ratio = find_drop_candidates(d)
        drop = cands[0][0] if cands else None
        print()
        if cands:
            conf = "낮음 — 드랍이 약한 곡, 반드시 들어서 확정" if ratio < 0.55 else ("보통" if ratio < 0.8 else "높음")
            print(f"드랍 후보 (강도순 · 확신도 {conf} · 단차비율 {ratio:.2f}):")
            for i, (t, score) in enumerate(cands, 1):
                tag = "  ← 가장 유력" if i == 1 else ""
                print(f"  후보{i}: {t:.2f}초{tag}")
            print("  ⚠️ 어디까지나 파형 추정 — 후보 근처를 직접 들어보고 확정할 것")
        else:
            print(f"뚜렷한 드랍 없음 (단차비율 {ratio:.2f} — 처음부터 일정한 에너지의 곡)")
            print("  → 처방: 곡을 0초부터 깔고, 하이라이트 강조는 효과음/자막 펀치나 'BGM 뚝 끊었다 복귀'(가짜 드랍)로")

        # 4) 편집 처방
        print("\n===== 편집 처방 =====")
        if drop is not None:
            print(f"· 하이라이트 컷(매치컷/반전)을 영상 {drop:.2f}초 드랍에 스냅")
            print(f"  - 곡을 영상 0초부터 깔면: 하이라이트가 {drop:.2f}초에 오게 앞 컷을 배치")
            print(f"  - 하이라이트가 더 늦으면: 곡 시작을 (하이라이트시점 - {drop:.2f})초로 밀기")
            print(f"· 드랍 전({drop:.1f}초까지) = 조용한 도입 컷(외관·설정·빌드업)")
        if beat:
            print(f"· 컷 경계는 비트 간격의 배수로: {beat:.2f}s / {beat * 2:.2f}s / {beat * 3:.2f}s")
            print(f"· 사진 버스트(촤라락): 장당 {beat / 2:.2f}초 (반박자)")
            print(f"· 컷 편집 앱의 비트 마커와 대조: 마커 간격 ≈ {beat:.2f}초면 일치")
    finally:
        os.unlink(wav)


def cmd_fine(src, a, b):
    wav = to_wav(src)
    try:
        d = load(wav)
        win = int(SR * 0.05)
        print(f"{os.path.basename(src)}  {a:.2f}~{b:.2f}초 — 0.05초 정밀 스캔")
        print("(급증=드랍/온셋 후보, -50dB 이하=무음)")
        prev = None
        for i in range(int(a * SR), min(int(b * SR), len(d) - win), win):
            db, rms = rms_db(d, i, win)
            t = i / SR
            mark = ""
            if prev is not None and rms > prev * 1.8 and rms > 0.12:
                mark = "  <<< 급증"
            elif db < -50:
                mark = "  ·무음"
            print(f"{t:7.2f}s {db:6.1f}dB {bar(rms, 90)}{mark}")
            prev = rms
    finally:
        os.unlink(wav)


def cmd_cuts(src, a=None, b=None):
    """음성(나레이션) 컷 지점 추천 — 깊은 무음 구간을 찾아 '여기서 자르면 안전' 목록을 낸다.
    whisper 타임스탬프로 자르면 단어 여운/첫음이 잘리는 문제의 해답 (이 스킬의 본업)."""
    wav = to_wav(src)
    try:
        d = load(wav)
        dur = len(d) / SR
        a = 0.0 if a is None else a
        b = dur if b is None else b
        win = int(SR * 0.03)  # 0.03초 창 — 붙은 단어 사이 dip까지 보임
        silences = []  # (시작, 끝)
        cur = None
        for i in range(int(a * SR), min(int(b * SR), len(d) - win), win):
            db, _ = rms_db(d, i, win)
            t = i / SR
            if db < -50:
                cur = t if cur is None else cur
            else:
                if cur is not None and t - cur >= 0.12:
                    silences.append((cur, t))
                cur = None
        if cur is not None and b - cur >= 0.12:
            silences.append((cur, b))
        print(f"{os.path.basename(src)}  {a:.1f}~{b:.1f}초 — 무음(-50dB↓, 0.12초+) 구간 {len(silences)}개")
        print("컷은 무음의 '가운데'가 가장 안전 (앞말 여운·뒷말 첫음 둘 다 보호):\n")
        for s, e in silences:
            mid = (s + e) / 2
            print(f"  {s:7.2f} ~ {e:7.2f}초  (길이 {e - s:.2f})  → 컷 추천: {mid:.2f}초")
        if not silences:
            print("  깊은 무음 없음 — 발화가 붙어 있음. fine으로 dip(약한 골)을 눈으로 찾아 자를 것")
    finally:
        os.unlink(wav)


def cmd_verify(src, expect):
    wav = to_wav(src)
    try:
        d = load(wav)
        drop = find_drop(d)
        print(f"편집본: {os.path.basename(src)}")
        if drop is None:
            print("드랍을 못 찾음 — fine으로 수동 확인 필요")
            return
        off = drop - expect
        print(f"기대 드랍: {expect:.2f}초 / 실제 드랍: {drop:.2f}초 / 오차: {off:+.2f}초")
        if abs(off) <= 0.15:
            print("✅ 싱크 OK (오차 0.15초 이내)")
        else:
            print(f"⚠️ {abs(off):.2f}초 어긋남 — 하이라이트 컷(또는 곡 시작점)을 {-off:+.2f}초 이동")
    finally:
        os.unlink(wav)


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)
    cmd = args[0]
    if cmd == "analyze" and len(args) >= 2:
        cmd_analyze(args[1])
    elif cmd == "cuts" and len(args) >= 2:
        cmd_cuts(args[1], float(args[2]) if len(args) > 2 else None, float(args[3]) if len(args) > 3 else None)
    elif cmd == "fine" and len(args) >= 4:
        cmd_fine(args[1], float(args[2]), float(args[3]))
    elif cmd == "verify" and len(args) >= 3:
        cmd_verify(args[1], float(args[2]))
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
