# -*- coding: utf-8 -*-
"""신청자 답만 받아 codes.json 과 쌍둥이 표(twins.md)를 만든다.

이메일·이름 열을 읽지 않는다. 지정한 열(시각 · 자유서술 · 객관식)만 읽는다.
받지 않은 값은 샐 수도 없다.

쓰는 법:
  python codes.py csv <응답.csv> <출력 폴더> --time <열> --free <열> --keys <열1,열2,...>
  python codes.py supabase <.env 경로> <출력 폴더> --table <표> --time <열> \
      [--answers <JSON 열>] --free <키> --keys <키1,키2,...>

선택:
  --keys-file <파일>  객관식 열 이름을 한 줄에 하나씩 (열 이름에 쉼표가 있을 때)
  --min <N>           쌍둥이 문턱. 기본값은 객관식 칸 수의 70% (올림)
  --tz <시간>          supabase 시각을 바꿀 시간대(UTC 기준 시간, 소수 가능). 기본 9

출력 (UTF-8 파일. 화면에는 건수만 찍는다):
  <출력 폴더>/codes.json   [{no, at, free, answers}]
  <출력 폴더>/twins.md     사람마다 쌍둥이(동률 전부) · 겹침 · 갈리는 칸

출력 폴더는 공개 저장소 밖이어야 한다. 답변이 들어 있다.
자유서술에 고객이 직접 적은 이름·연락처는 걸러내지 못한다.
"""
import argparse
import csv
import io
import json
import math
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

PAGE = 1000  # PostgREST 기본 최대 행 수. 넘으면 나눠 받는다


def read_env(path):
    env = {}
    for line in io.open(path, encoding='utf-8'):
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def parse_ts(ts):
    # 3.11 미만의 fromisoformat 은 소수초가 6자리가 아니거나 Z 로 끝나면 못 읽는다
    s = ts.strip().replace(' ', 'T', 1).replace('Z', '+00:00')
    m = re.match(r'^(.*T\d{2}:\d{2}:\d{2})(\.\d+)?(.*)$', s)
    if m:
        frac = (m.group(2) or '')[1:7].ljust(6, '0') if m.group(2) else ''
        s = m.group(1) + ('.' + frac if frac else '') + m.group(3)
    t = datetime.fromisoformat(s)
    return t if t.tzinfo else t.replace(tzinfo=timezone.utc)


def to_local(ts, hours):
    # DB 는 대개 UTC 다. 그대로 자르면 명단 화면의 시간대와 어긋나 엉뚱한 줄을 찾는다
    return parse_ts(ts).astimezone(timezone(timedelta(hours=hours))).strftime('%Y-%m-%d %H:%M')


def from_csv(path, a):
    # utf-8-sig: 스프레드시트·엑셀 CSV 앞의 BOM 을 떼어야 첫 열 이름이 맞는다
    with io.open(path, encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            sys.exit('CSV 가 비어 있거나 첫 줄(열 이름)이 없습니다.')
        missing = [c for c in [a.time, a.free] + a.keys if c and c not in reader.fieldnames]
        if missing:
            sys.exit('CSV 에 없는 열: %s\n있는 열 이름은 파일 첫 줄을 보세요.' % ', '.join(missing))
        return [{
            'at': (r.get(a.time) or '').strip(),
            'free': (r.get(a.free) or '').strip() if a.free else '',
            'answers': {k: (r.get(k) or '').strip() for k in a.keys},
        } for r in reader]


def from_supabase(env_path, a):
    if not a.table:
        sys.exit('supabase 에서는 --table 로 표 이름을 주세요.')
    env = read_env(env_path)
    url = (env.get('SUPABASE_URL') or env.get('NEXT_PUBLIC_SUPABASE_URL') or '').rstrip('/')
    key = env.get('SUPABASE_SECRET_KEY') or env.get('SUPABASE_SERVICE_ROLE_KEY')
    if not url or not key:
        sys.exit('.env 에 SUPABASE_URL(또는 NEXT_PUBLIC_SUPABASE_URL)과 '
                 'SUPABASE_SECRET_KEY(또는 SUPABASE_SERVICE_ROLE_KEY)가 필요합니다.')
    if a.answers:
        cols = [a.time, a.answers]
    else:
        cols = [a.time] + ([a.free] if a.free else []) + a.keys
    base = '%s/rest/v1/%s?select=%s&order=%s.asc' % (
        url, urllib.parse.quote(a.table), urllib.parse.quote(','.join(cols)), urllib.parse.quote(a.time))

    data, offset = [], 0
    while True:
        req = urllib.request.Request('%s&limit=%d&offset=%d' % (base, PAGE, offset),
                                     headers={'apikey': key, 'Authorization': 'Bearer ' + key})
        chunk = json.load(urllib.request.urlopen(req, timeout=30))
        data.extend(chunk)
        if len(chunk) < PAGE:
            break
        offset += PAGE

    rows = []
    for r in data:
        src = r.get(a.answers) if a.answers else r
        if isinstance(src, str):  # 답 열이 jsonb 가 아니라 text 일 때
            try:
                src = json.loads(src)
            except ValueError:
                src = {}
        src = src or {}
        rows.append({
            'at': to_local(r[a.time], a.tz),
            'free': str(src.get(a.free) or '').strip() if a.free else '',
            'answers': {k: '' if src.get(k) is None else str(src.get(k)) for k in a.keys},
        })
    return rows


def cell(v):
    return str(v).replace('|', '\\|').replace('\r', ' ').replace('\n', ' ')


def twins(people, keys, tmin):
    n = len(keys)
    lines = ['# 쌍둥이 표', '',
             '객관식 %d칸 중 %d칸 이상 같으면 쌍둥이. 빈 답끼리는 같은 답으로 세지 않는다. 동률은 전부 적는다.' % (n, tmin), '',
             '| # | 신청 | 쌍둥이 | 최대 겹침 | 갈리는 칸 |', '|---|---|---|---|---|']
    for p in people:
        a = p['answers']
        scored = [(sum(1 for k in keys if a.get(k) and a.get(k) == o['answers'].get(k)), o)
                  for o in people if o is not p]
        top = max(s for s, _ in scored) if scored else 0
        if top < tmin:
            lines.append('| %d | %s | 없음 | %d/%d | |' % (p['no'], cell(p['at']), top, n))
            continue
        for s, o in scored:
            if s != top:
                continue
            diff = ' · '.join('%s(%s≠%s)' % (cell(k), cell(a.get(k)), cell(o['answers'].get(k)))
                              for k in keys if not (a.get(k) and a.get(k) == o['answers'].get(k)))
            lines.append('| %d | %s | %d번 (%s) | %d/%d | %s |' % (
                p['no'], cell(p['at']), o['no'], cell(o['at']), s, n, diff))
    return '\n'.join(lines) + '\n'


def main():
    ap = argparse.ArgumentParser(description='신청자 답만 받아 쌍둥이 표를 만든다 (이메일·이름은 읽지 않는다)')
    ap.add_argument('source', choices=['csv', 'supabase'])
    ap.add_argument('input', help='CSV 파일, 또는 .env 경로')
    ap.add_argument('out', help='출력 폴더 (공개 저장소 밖)')
    ap.add_argument('--time', required=True)
    ap.add_argument('--free', default='')
    ap.add_argument('--keys', default='')
    ap.add_argument('--keys-file', default='')
    ap.add_argument('--table', default='')
    ap.add_argument('--answers', default='')
    ap.add_argument('--min', type=int, default=0)
    ap.add_argument('--tz', type=float, default=9)
    a = ap.parse_args()

    if a.keys_file:
        a.keys = [l.strip() for l in io.open(a.keys_file, encoding='utf-8') if l.strip()]
    else:
        a.keys = [k.strip() for k in a.keys.split(',') if k.strip()]
    if not a.keys:
        sys.exit('--keys 또는 --keys-file 로 객관식 열을 하나 이상 주세요.')

    rows = from_csv(a.input, a) if a.source == 'csv' else from_supabase(a.input, a)
    people = [dict(no=i, **r) for i, r in enumerate(rows, 1)]
    tmin = a.min or math.ceil(len(a.keys) * 0.7)

    os.makedirs(a.out, exist_ok=True)
    io.open(os.path.join(a.out, 'codes.json'), 'w', encoding='utf-8').write(
        json.dumps(people, ensure_ascii=False, indent=1))
    io.open(os.path.join(a.out, 'twins.md'), 'w', encoding='utf-8').write(twins(people, a.keys, tmin))
    sys.stdout.write('ok %d명 · 객관식 %d칸 · 쌍둥이 문턱 %d\n' % (len(people), len(a.keys), tmin))


if __name__ == '__main__':
    main()
