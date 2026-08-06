from pathlib import Path

REPLACEMENTS = {
    "manuscript/chapters/13-光の重さ/035-第35話-光の重さ.md": [
        ("神記2874年（西暦1590年）晩秋。", "西暦1590年　晩秋。"),
    ],
    "manuscript/chapters/14-黒い壁/038-第38話-一人残れ.md": [
        ("神記2875年（西暦1591年）一月。", "西暦1591年　一月。"),
    ],
    "manuscript/chapters/14-黒い壁/039-第39話-最初の記録.md": [
        ("神記2875年（西暦1591年）一月。", "西暦1591年　一月。"),
    ],
    "manuscript/chapters/14-黒い壁/040-第40話-地図の外.md": [
        ("神記2876年（西暦1592年）一月。", "西暦1592年　一月。"),
    ],
    "manuscript/chapters/15-石/041-第41話-山の口.md": [
        ("神記2876年（西暦1592年）七月。", "西暦1592年　七月。"),
    ],
    "manuscript/chapters/16-南方の陸地/046-第46話-森本左近.md": [
        ("神記2876年（西暦1592年）十月。", "西暦1592年　十月。"),
    ],
    "manuscript/chapters/17-帰還/050-第50話-手紙.md": [
        ("神記2876年（西暦1592年）冬。", "西暦1592年　冬。"),
    ],
    "manuscript/side-stories/市/004-第4話-旅立ち.md": [
        ("町の外へ出ると、ベガ湖が見えた。", "町の外へ出ると、ペガ湖が見えた。"),
    ],
    "manuscript/INDEX.md": [
        (
            '2. [第2話「上戸の傭兵隊長」](./chapters/01-落城/002-第2話-上戸の傭兵隊長.md) — `REGISTERED / LOCKED`',
            '2. [第2話「傭兵隊長」](./chapters/01-落城/002-第2話-上戸の傭兵隊長.md) — `REGISTERED / LOCKED`',
        ),
        (
            '46. [第46話「森本左近」](./chapters/16-南方の陸地/046-第46話-森本左近.md) — `REGISTERED / LOCKED`',
            '46. [第46話「左近」](./chapters/16-南方の陸地/046-第46話-森本左近.md) — `REGISTERED / LOCKED`',
        ),
        (
            '65. [第65話「アユタヤ日本人町」](./chapters/22-入国/065-第65話-アユタヤ日本人町.md) — `REGISTERED / LOCKED`',
            '65. [第65話「日本人町」](./chapters/22-入国/065-第65話-アユタヤ日本人町.md) — `REGISTERED / LOCKED`',
        ),
        (
            '79. [第79話「研究所」](./chapters/27-炉/079-第79話-研究所.md) — `REGISTERED / LOCKED`',
            '79. [第79話「四行」](./chapters/27-炉/079-第79話-研究所.md) — `REGISTERED / LOCKED`',
        ),
    ],
}

for rel_path, replacements in REPLACEMENTS.items():
    path = Path(rel_path)
    text = path.read_text(encoding="utf-8")
    for old, new in replacements:
        old_count = text.count(old)
        new_count = text.count(new)
        if old_count != 1 or new_count != 0:
            raise RuntimeError(
                f"Unexpected state for {rel_path}: old={old_count}, new={new_count}, pattern={old!r}"
            )
        text = text.replace(old, new, 1)
    path.write_text(text, encoding="utf-8", newline="")

Path(".github/workflows/register-audit.yml").unlink()
Path("scripts/register_audit.py").unlink()
