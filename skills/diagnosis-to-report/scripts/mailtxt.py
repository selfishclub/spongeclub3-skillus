# -*- coding: utf-8 -*-
"""검토용 리포트(.md)를 메일에 바로 붙이는 판(.메일용.txt)으로 바꾼다.

- 맨 위의 확인 체크와 매칭표(첫 `---` 줄 위)를 뗀다
- 코드블록(```)을 위아래 가로줄로 바꾼다. 메일에 그대로 붙이면 모양이 깨진다
- 굵게(**)를 뗀다. 메일에서는 별표가 그대로 보인다
- 본문 글자는 바꾸지 않는다

경고만 하고 멈추지 않는 것:
- `---` 줄이 없다 (머리말이 없는 파일이면 통째로 본문으로 본다)
- [확인 필요] 가 남아 있다

쓰는 법:
  python mailtxt.py <검토용.md> [<검토용.md> ...]
"""
import io
import sys

LINE = '────────────────'


def convert(src):
    lines = src.replace('\r\n', '\n').split('\n')
    warn = []
    if '---' in [l.strip() for l in lines]:
        cut = [l.strip() for l in lines].index('---')
        lines = lines[cut + 1:]
    else:
        warn.append('`---` 줄이 없어 머리말을 떼지 않았습니다')
    out = []
    for l in lines:
        out.append(LINE if l.lstrip().startswith('```') else l.replace('**', ''))
    text = '\n'.join(out).strip() + '\n'
    if '[확인 필요]' in text:
        warn.append('[확인 필요] 가 남아 있습니다')
    return text, warn


def main():
    if len(sys.argv) < 2:
        sys.exit('쓰는 법: python mailtxt.py <검토용.md> [...]')
    for path in sys.argv[1:]:
        dst = (path[:-3] if path.endswith('.md') else path) + '.메일용.txt'
        text, warn = convert(io.open(path, encoding='utf-8').read())
        io.open(dst, 'w', encoding='utf-8').write(text)
        sys.stdout.write('ok %s\n' % dst)
        for w in warn:
            sys.stdout.write('  ⚠ %s\n' % w)


if __name__ == '__main__':
    main()
