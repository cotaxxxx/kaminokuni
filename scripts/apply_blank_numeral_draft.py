from pathlib import Path
import re

TARGETS = [
    "manuscript/chapters/07-リデル炎上/020-第20話-赤い空.md",
    "manuscript/chapters/07-リデル炎上/021-第21話-倒れる方向.md",
    "manuscript/chapters/07-リデル炎上/022-第22話-うまくいった.md",
    "manuscript/chapters/08-選民/023-第23話-三つの欄.md",
    "manuscript/chapters/08-選民/024-第24話-選民.md",
    "manuscript/chapters/09-扉を開く者/025-第25話-口をつぐむ.md",
    "manuscript/chapters/09-扉を開く者/026-第26話-寒いところ.md",
    "manuscript/chapters/09-扉を開く者/027-第27話-同じ机.md",
    "manuscript/chapters/10-三枚の翼/028-第28話-三枚の翼.md",
    "manuscript/chapters/10-三枚の翼/029-第29話-歓迎.md",
    "manuscript/chapters/11-記録の行方/030-第30話-全部ある.md",
    "manuscript/chapters/11-記録の行方/031-第31話-同じ番号.md",
    "manuscript/chapters/12-箱/032-第32話-箱に入らないもの.md",
    "manuscript/chapters/12-箱/033-第33話-二つの届け先.md",
    "manuscript/chapters/13-光の重さ/034-第34話-同じ速さ.md",
    "manuscript/chapters/13-光の重さ/035-第35話-光の重さ.md",
    "manuscript/chapters/13-光の重さ/036-第36話-空いた椅子.md",
    "manuscript/chapters/13-光の重さ/037-第37話-血の外から.md",
]

DIGITS = {"〇": 0, "零": 0, "一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
SMALL = {"十": 10, "百": 100, "千": 1000}
LARGE = {"万": 10_000, "億": 100_000_000, "兆": 1_000_000_000_000}
KANJI = "〇零一二三四五六七八九十百千万億兆"

# 規則1.2、語彙化した表現、及び確定固有名称。
PROTECTED_PATTERNS = [
    r"[一二三四五六七八九十百千万]+つ",
    r"一度だけ", r"一度も", r"年に一度", r"一度目", r"二度目", r"もう一度",
    r"一枚を取った", r"一枚取った", r"一箱ずつ", r"一年ごと", r"一人で",
    r"一部", r"一方", r"一時", r"一緒", r"一瞬", r"一定", r"一旦", r"一律",
    r"一切", r"一生", r"一筋", r"一帯", r"一層", r"一端", r"一連", r"一斉",
    r"二重", r"二度と", r"三角形", r"三枚の翼", r"三つの欄", r"三欄式",
    r"五か年技術計画", r"第一鐘",
]
PROTECT_RE = re.compile("|".join(f"(?:{p})" for p in PROTECTED_PATTERNS))

COUNTERS = [
    "キロメートル", "センチメートル", "ミリメートル", "キログラム", "メートル",
    "パーセント", "居住区", "か月", "か所", "箇所", "人分",
    "時間", "週間", "か年", "世帯", "ページ",
    "歳", "人", "名", "枚", "冊", "本", "丁", "箱", "棟", "軒", "階", "段",
    "駅", "行", "頁", "日", "月", "年", "時", "分", "秒", "度", "回", "台",
    "基", "室", "張", "艘", "隻", "席", "部", "件", "個", "発", "両", "列",
    "班", "組", "区", "割", "週", "夜", "昼", "朝", "晩", "鐘", "番", "周",
    "代", "か国", "か所", "か所", "箇所", "か条", "条", "校", "館", "戸", "門",
    "名分", "種類", "地点", "系統", "方向", "項目", "段階", "倍", "字", "文字",
]
COUNTER_RE = "|".join(sorted(map(re.escape, COUNTERS), key=len, reverse=True))
NUM_RE = f"[{KANJI}]+"


def jp_to_int(s: str) -> int:
    if not any(ch in SMALL or ch in LARGE for ch in s):
        return int("".join(str(DIGITS[ch]) for ch in s))
    total = 0
    section = 0
    number = 0
    for ch in s:
        if ch in DIGITS:
            number = DIGITS[ch]
        elif ch in SMALL:
            section += (number or 1) * SMALL[ch]
            number = 0
        elif ch in LARGE:
            section += number
            total += (section or 1) * LARGE[ch]
            section = 0
            number = 0
        else:
            raise ValueError(ch)
    return total + section + number


def format_number(value: int, suffix: str = "", prefix: str = "") -> str:
    # 暦年、神記年、識別番号は桁区切りを入れない。
    if suffix in {"年", "番"} and value < 10_000:
        return str(value)
    if prefix == "第" and value < 10_000:
        return str(value)
    return f"{value:,}" if value >= 1000 else str(value)


def protect(text: str):
    store = []
    def repl(m):
        store.append(m.group(0))
        return f"⟦P{len(store)-1:04d}⟧"
    return PROTECT_RE.sub(repl, text), store


def restore(text: str, store):
    for i, value in enumerate(store):
        text = text.replace(f"⟦P{i:04d}⟧", value)
    return text


def convert_text(text: str) -> str:
    text, store = protect(text)

    # 第三倉庫、第一号等の識別・序数。
    def repl_ordinal(m):
        value = jp_to_int(m.group("num"))
        return "第" + format_number(value, prefix="第")
    text = re.sub(rf"第(?P<num>{NUM_RE})", repl_ordinal, text)

    # 数量、年月日、測定値、記録値。
    def repl_counter(m):
        raw = m.group("num")
        suffix = m.group("suffix")
        value = jp_to_int(raw)
        return format_number(value, suffix=suffix) + suffix
    text = re.sub(rf"(?P<num>{NUM_RE})(?P<suffix>{COUNTER_RE})", repl_counter, text)

    # 十二の襞など、数が名詞を直接限定する表現。
    def repl_no(m):
        value = jp_to_int(m.group("num"))
        return format_number(value) + "の"
    text = re.sub(rf"(?P<num>{NUM_RE})の", repl_no, text)

    # 七四などの記録番号・符号。
    def repl_digit_code(m):
        raw = m.group(0)
        return str(jp_to_int(raw))
    text = re.sub(r"(?<![ぁ-んァ-ヶ一-龯])(?:[〇零一二三四五六七八九]{2,})(?![ぁ-んァ-ヶ一-龯])", repl_digit_code, text)

    # 独立した記録値。
    def repl_standalone(m):
        raw = m.group("num")
        return m.group("lead") + format_number(jp_to_int(raw)) + m.group("tail")
    text = re.sub(rf"(?m)^(?P<lead>\s*)(?P<num>{NUM_RE})(?P<tail>[。．、]?\s*)$", repl_standalone, text)

    return restore(text, store)


summary = []
for target in TARGETS:
    p = Path(target)
    before = p.read_text(encoding="utf-8")
    after = convert_text(before)
    if after != before:
        p.write_text(after, encoding="utf-8", newline="")
        summary.append((target, sum(a != b for a, b in zip(before.splitlines(), after.splitlines()))))
    else:
        summary.append((target, 0))

# 残存漢数字をレビュー用に出力する。
residual = ["# II. BLANK 数字表記変換後の残存監査（一時報告）", ""]
for target in TARGETS:
    p = Path(target)
    text = p.read_text(encoding="utf-8")
    residual += [f"## `{target}`", ""]
    found = False
    for lineno, line in enumerate(text.splitlines(), 1):
        tokens = re.findall(NUM_RE, line)
        if tokens:
            found = True
            residual.append(f"- L{lineno}: `{line.replace('`', '\\`')}`  ")
            residual.append(f"  tokens: `{', '.join(tokens)}`")
    if not found:
        residual.append("- 該当なし")
    residual.append("")
residual += ["## 変更行概数", ""]
for target, count in summary:
    residual.append(f"- `{target}`: {count}")
Path("manuscript/management/_tmp_blank_numeral_residual.md").write_text("\n".join(residual) + "\n", encoding="utf-8")
