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
PAT = re.compile(r"[〇零一二三四五六七八九十百千万億兆]+")

out = ["# II. BLANK 数字表記監査（一時報告）", ""]
count = 0
for target in TARGETS:
    p = Path(target)
    text = p.read_text(encoding="utf-8")
    out += [f"## `{target}`", ""]
    file_count = 0
    for lineno, line in enumerate(text.splitlines(), 1):
        matches = PAT.findall(line)
        if matches:
            file_count += len(matches)
            count += len(matches)
            escaped = line.replace("`", "\\`")
            out.append(f"- L{lineno}: `{escaped}`  ")
            out.append(f"  tokens: `{', '.join(matches)}`")
    if file_count == 0:
        out.append("- 該当なし")
    out.append("")
out.insert(2, f"総トークン数：{count}")
out.insert(3, "")
Path("manuscript/management/_tmp_blank_numeral_audit.md").write_text("\n".join(out) + "\n", encoding="utf-8")
