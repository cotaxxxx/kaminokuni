from pathlib import Path

path = Path("canon/FIRE_DATE_NOTATION_ICHI_LAKE_INDEX_TITLE_SUPPLEMENT_REGISTERED_CANON.md")
text = path.read_text(encoding="utf-8")
old = """## 5．継続する判断待ち

本登録後も、次の判断待ちが残る。

1. 数字表記の統一：`NUMERAL_USA_CITY_LEONIS_CANE_SUPPLEMENT_REGISTERED_CANON.md`により用途別併用規則を確定し、III. FIREの対象月表記を算用数字へ修正済み。`RESOLVED`。
2. `canon/49_CHAPTER_34_REGISTERED_CANON.md`及び`canon/README.md`に残る旧「宇佐市」墓地記述への`SUPERSEDED`明示。
3. 第100話「杖。なし。」と外伝レオニスの杖の扱い（対応案A/B提示済み）。
"""
new = """## 5．後続更新による解決

本登録時点で判断待ちだった次の三件は、`NUMERAL_USA_CITY_LEONIS_CANE_SUPPLEMENT_REGISTERED_CANON.md`及び現行本文により、すべて解決済みである。

1. 数字表記の統一：用途別併用規則を確定し、III. FIREの対象月表記を算用数字へ修正済み。`RESOLVED`。
2. 旧「宇佐市」墓地記述：`canon/49_CHAPTER_34_REGISTERED_CANON.md`、`canon/README.md`及び`canon/SUPERSEDED.md`へ失効を明示済み。`RESOLVED / SUPERSEDED`。
3. 第100話と外伝レオニスの杖：第100話を`杖。地面に置かれている。`へ修正し、外伝の現行描写と整合済み。`RESOLVED`。
"""
if text.count(old) != 1 or new in text:
    raise RuntimeError("Unexpected FIRE supplement state")
path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="")

Path(".github/workflows/close-resolved-pending-items.yml").unlink()
Path("scripts/close_resolved_pending_items.py").unlink()
