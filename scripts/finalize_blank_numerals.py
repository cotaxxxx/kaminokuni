from pathlib import Path
import re

BASE_COMMIT = "e45f05e3380e9ab6d2982c8627056ea15c50da1f"
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


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    Path(path).write_text(text, encoding="utf-8", newline="")


def replace_once(path: str, old: str, new: str) -> None:
    text = read(path)
    if text.count(old) != 1:
        raise RuntimeError(f"expected one occurrence in {path}: {old[:80]!r}")
    write(path, text.replace(old, new, 1))


def replace_all(path: str, old: str, new: str, minimum: int = 1) -> int:
    text = read(path)
    count = text.count(old)
    if count < minimum:
        raise RuntimeError(f"expected at least {minimum} occurrences in {path}: {old!r}")
    write(path, text.replace(old, new))
    return count


# 仮適用後の個別補正。
replace_all(TARGETS[0], "一時間", "1時間")

replace_all(TARGETS[2], "七四", "74")
replace_once(TARGETS[2], "本人携行、一部。", "本人携行、1部。")
replace_once(TARGETS[2], "同文記録、一部。", "同文記録、1部。")
replace_all(TARGETS[2], "一時間", "1時間")

replace_all(TARGETS[4], "五十家", "50家")

replace_once(TARGETS[5], "通常手続で10分だ", "通常手続で十分だ")
replace_all(TARGETS[5], "5か年計画", "五か年計画")
replace_once(TARGETS[5], "柚は一部を買った。", "柚は1部を買った。")

replace_once(TARGETS[6], "椅子が四脚。", "椅子が4脚。")
replace_all(TARGETS[6], "赤い十二襞", "赤い12襞")
replace_all(TARGETS[6], "5か年計画", "五か年計画")

replace_all(TARGETS[7], "七四", "74")
replace_all(TARGETS[7], "赤い十二襞", "赤い12襞")
replace_all(TARGETS[7], "三者立会い", "3者立会い")

replace_all(TARGETS[8], "三者が", "3者が")

replace_once(TARGETS[9], "一部は技術院。", "1部は技術院。")
replace_once(TARGETS[9], "一部は主任監査官が封印して携行する。", "1部は主任監査官が封印して携行する。")
replace_all(TARGETS[9], "赤い十二襞", "赤い12襞")

replace_once(TARGETS[10], "製造番号、一から十二。", "製造番号、1から12。")

replace_once(TARGETS[12], "十二まで。", "12まで。")

# 第34話の漢数字小数は値全体として変換し、先頭ゼロを保持する。
DECIMAL_REPLACEMENTS = {
    "1秒間に六十四・21回。前回との差は〇・2回以内です": "1秒間に64.21回。前回との差は0.02回以内です",
    "十三・2度": "13.2度",
    "毎秒二・1メートル": "毎秒2.1メートル",
    "毎秒二十三・4メートル": "毎秒23.4メートル",
    "毎秒四十六・8メートル": "毎秒46.8メートル",
    "毎秒〇・468キロメートル": "毎秒0.0468キロメートル",
}
for old, new in DECIMAL_REPLACEMENTS.items():
    replace_all(TARGETS[14], old, new)

replace_all(TARGETS[15], "一時間", "1時間")
replace_all(TARGETS[15], "零", "0")
replace_once(TARGETS[15], "第2鐘", "第二鐘")

replace_once(TARGETS[16], "一単位の質量", "1単位の質量")

replace_all(TARGETS[17], "5か年計画", "五か年計画")
replace_all(TARGETS[17], "零", "0")
replace_once(TARGETS[17], "十数名", "10数名")

# 記録内の番号付き列挙は算用数字へ統一する。
KANJI_DIGIT = {"一": "1", "二": "2", "三": "3", "四": "4", "五": "5", "六": "6", "七": "7", "八": "8", "九": "9"}
for path in TARGETS:
    text = read(path)
    text = re.sub(r"(?m)^([一二三四五六七八九])、", lambda m: KANJI_DIGIT[m.group(1)] + "、", text)
    write(path, text)

# 最終的な禁止残存と誤変換を検証する。
joined = "\n".join(read(path) for path in TARGETS)
for forbidden in [
    "七四", "一時間", "五十家", "赤い十二襞", "三者立会い", "三者が",
    "椅子が四脚", "製造番号、一から十二", "十二まで。", "第2鐘",
    "通常手続で10分だ", "5か年計画", "十数名", "残額、零", "残額零",
    "六十四・21", "〇・2", "十三・2", "二・1メートル", "二十三・4",
    "四十六・8", "〇・468",
]:
    if forbidden in joined:
        raise RuntimeError(f"forbidden residual: {forbidden}")
if re.search(r"(?m)^[一二三四五六七八九]、", joined):
    raise RuntimeError("kanji list marker remains")

# 既存正典の判断待ちを解決済みへ更新する。
blank_path = "canon/BLANK_DATE_COUNCIL_NAME_NUMERAL_SUPPLEMENT_REGISTERED_CANON.md"
blank_old = """## 4．数字表記

状態：`RESOLVED BY LATER PRIORITY CANON / SUPERSEDED IN PART`

後続の`NUMERAL_USA_CITY_LEONIS_CANE_SUPPLEMENT_REGISTERED_CANON.md`により、数字表記は用途別併用規則として確定した。年月日、測定値、技術値、帳簿・公文書上の数量及び照合対象となる数値は算用数字とし、慣用表現、文学的反復、数量性の弱い通常表現及び固有名称は漢数字を維持する。

第37話の年代標識にある`一月`は`1月`へ修正済みである。以下の旧判断待ち記述は履歴として保持するが、現行の判断待ちではない。

II. BLANKの数字表記は、今回変更しない。

- 第17話〜第19話：`240丁`、`60丁`、`180`等のアラビア数字主体。
- 第20話〜第37話：`百八十丁`、`五十八センチメートル`、`八千二百四十メートル`、`一月`等の漢数字主体。

同一編内の表記差として全編中でも範囲が大きいため、将来の数字表記統一ではII. BLANKを最優先監査対象とする。

将来の統一監査では、地の文、台詞、国内公文書、私的控え、帳簿、技術値、測定値、年月、時刻、距離、数量、序数、慣用表現及び比喩を分離して判断する。

本正典では、アラビア数字又は漢数字のいずれかをII. BLANK全体へ一括適用しない。
"""
blank_new = """## 4．数字表記

状態：`RESOLVED / RULE 1.1 APPLIED THROUGHOUT II. BLANK / NO EDITORIAL EXCEPTION`

後続の`NUMERAL_USA_CITY_LEONIS_CANE_SUPPLEMENT_REGISTERED_CANON.md`により確定した用途別併用規則を、`BLANK_NUMERAL_RULE_1_1_APPLICATION_REGISTERED_CANON.md`によりII. BLANK全体へ適用した。

作者の指示は`例外なし`である。これにより、旧対応案A2を採用し、第20話〜第37話を「漢数字体の編」とする旧対応案B2は採用しない。

- 第17話〜第19話：既存の算用数字表記を維持する。
- 第20話〜第37話：年月日、年齢、人数、人口、金額、距離、日数、数量、照合値、測定値、記録値、識別番号及び番号付き列挙へ規則1.1を適用済み。
- 規則1.2の和語数え、慣用表現、文学的反復及び固有名称は維持する。これは編単位の例外ではなく、数字表記規則そのものの適用である。

したがって、II. BLANKの数字表記に関する判断待ちは存在しない。
"""
replace_once(blank_path, blank_old, blank_new)
replace_once(blank_path, "- 数字表記。", "- 数字表記（本登録時点。後続の優先正典によりII. BLANK全体へ規則1.1適用済み）。")
replace_once(
    blank_path,
    "及びII. BLANKを数字表記統一の最優先監査対象とする判断に限って過去の記録より優先する。",
    "及びII. BLANKを数字表記統一の対象とする旧判断に限って過去の記録より優先する。数字表記の現行値は後続の`BLANK_NUMERAL_RULE_1_1_APPLICATION_REGISTERED_CANON.md`を優先する。",
)

water_path = "canon/WATER_NUMERAL_RULE_APPLICATION_REGISTERED_CANON.md"
water_old = """## 3．適用しなかった範囲――II. BLANK（判断待ち）

II. BLANK 第20話〜第37話は、話・章単位で漢数字が主体の文体で書かれている（例：小銃`二百四十丁`／`百八十丁`／`六十丁`計18箇所、`十二箱`、`十五丁`、`八千二百四十メートル`、第34話の光速測定ブロック`毎秒二十九万九千二百キロメートル`等）。

丁数18箇所のみを算用化すると、同じ場面内の箱数・寸法等が漢数字のまま残り、話内の不整合がかえって拡大するため、本登録では変更していない。編単位の扱いとして、次のいずれかの作者判断を要する。

- 対応案A2：II. BLANK第20〜37話の規則1.1該当箇所を編単位で一括算用化する（推定200箇所超。第34話の測定値ブロックを含む。chat側で修正一式の作成可）。
- 対応案B2：II. BLANK第20〜37話を「漢数字体の編」として規則1.2側の例外に正典明記し、現状を維持する（第17〜19話の算用はそのまま）。

いずれの案でも、第12・13話の算用統一（登録済み）及び本正典の第91〜96話適用は変更されない。
"""
water_new = """## 3．後続更新――II. BLANK（解決済み）

作者は、II. BLANK第20話〜第37話の数字表記について`例外なし`と指示した。

これにより対応案A2を採用し、規則1.1該当箇所を編単位で算用数字へ統一した。対応案B2の「漢数字体の編」とする例外は採用しない。

現行値は`BLANK_NUMERAL_RULE_1_1_APPLICATION_REGISTERED_CANON.md`及び現行本文を優先する。規則1.2該当表現及び固有名称の漢数字は維持する。
"""
replace_once(water_path, water_old, water_new)
replace_once(
    water_path,
    "II. BLANK第20〜37話の数字表記は、対応案A2又はB2の作者判断を待つ。",
    "II. BLANK第20〜37話は対応案A2を採用し、規則1.1を例外なく適用済みである。",
)

# 新規優先正典。
canon_text = f"""# 『The Black Wall』II. BLANK数字表記規則1.1 全編適用 優先正典

## 状態

- 作品：**The Black Wall**
- 対象：II. BLANK第20話〜第37話
- 登録日：2026年8月6日
- 状態：`REGISTERED-CANON / PRIORITY / LOCKED`
- 種別：`NUMERAL RULE 1.1 APPLICATION / NO EDITORIAL EXCEPTION / II. BLANK COMPLETE`
- 作業基準コミット：`{BASE_COMMIT}`
- 作者指示：`例外なし`

本正典は、`NUMERAL_USA_CITY_LEONIS_CANE_SUPPLEMENT_REGISTERED_CANON.md`の規則1.1をII. BLANK第20話〜第37話へ編単位で適用した結果を固定する。

## 1．作者判断

旧対応案A2を採用する。

- II. BLANK第20話〜第37話の規則1.1該当箇所を算用数字へ統一する。
- II. BLANKを「漢数字体の編」とする旧対応案B2は採用しない。
- 編、章又は話を単位とする数字表記上の例外は設けない。

作者の`例外なし`は、規則1.2を廃止する意味ではない。和語数え、慣用表現、文学的反復及び固有名称は、用途別併用規則に従って漢数字を維持する。

## 2．規則1.1の適用範囲

次を算用数字とする。

- 年月日、時刻、年齢及び期間。
- 人数、人口、金額、距離及び数量。
- 武器数、箱数、設備数、文書部数及び番号付き列挙。
- 帳簿、公文書、記録欄及び照合記録の数値。
- 測定値、技術値、誤差、比率及び計算値。
- 貨車、倉庫、施設、路線、条件等の識別番号。
- 数値として用いる`零`。

代表例：

- `午後九時四十分` → `午後9時40分`
- `二百四十丁` → `240丁`
- `十二箱`／`十五丁` → `12箱`／`15丁`
- `八千二百四十メートル` → `8,240メートル`
- `毎秒二十九万九千二百キロメートル` → `毎秒299,200キロメートル`
- `六十四・二一回` → `64.21回`
- `〇・〇二回` → `0.02回`
- `〇・〇四六八キロメートル` → `0.0468キロメートル`
- `残額、零` → `残額、0`
- `一、設計` → `1、設計`

## 3．規則1.2として維持する表現

次は漢数字を維持する。

- `一つ`、`二つ`、`五つ`等の和語数え。
- `一度だけ`、`一度も`、`もう一度`、`一年ごと`、`一箱ずつ`等の慣用又はリズム表現。
- `一部`が数量ではなく「部分」を意味する場合、`一方`、`一時`、`二重`等の語彙化した表現。
- `三枚の翼`、`三翼運送社`、`三つの欄`、`五か年技術計画`、`五か年計画`、`第一鐘`、`第二鐘`、`三卿`、`四卿`等の確定名称又は制度語。

文書の部数を示す`一部`は`1部`とし、「一部分」を意味する`一部`は漢数字を維持する。

## 4．本文適用

第20話〜第37話の18本文ファイルへ適用した。

数値の値、単位、算術関係、事件順序、人物関係、会話の意味及び物語内容は変更していない。

第17話〜第19話は既存の算用数字表記が規則1.1と一致しているため、本文を変更していない。

## 5．優先関係

本正典は、II. BLANKの数字表記に限り、次の旧判断より優先する。

- 第20話〜第37話を漢数字主体のまま保留する判断。
- 対応案A2又はB2の作者判断を待つ状態。
- II. BLANKを「漢数字体の編」とする例外案。

抵触しない本文、規則1.2、固有名称及び旧正典の履歴的記録は維持する。

## 6．登録宣言

II. BLANKには、編、章又は話を単位とする数字表記上の例外を設けない。

第17話〜第37話の規則1.1該当数値は、算用数字である。

II. BLANKの数字表記に関する判断待ちは解消した。

将来の変更には、作者の新たな明示指示を必要とする。
"""
write("canon/BLANK_NUMERAL_RULE_1_1_APPLICATION_REGISTERED_CANON.md", canon_text)

ledger_lines = "\n".join(f"{i}. `{path}`" for i, path in enumerate(TARGETS, 1))
ledger_text = f"""# II. BLANK数字表記規則1.1 全編適用 登録台帳

- 登録日：2026年8月6日
- 作業基準コミット：`{BASE_COMMIT}`
- 対応正典：`canon/BLANK_NUMERAL_RULE_1_1_APPLICATION_REGISTERED_CANON.md`
- 作者指示：`例外なし`
- 採用案：旧対応案A2
- 不採用案：旧対応案B2

## 1．登録内容

II. BLANK第20話〜第37話について、規則1.1該当箇所を編単位で算用数字へ統一した。

規則1.2の和語数え、慣用表現、文学的反復及び固有名称は維持した。

## 2．変更本文

{ledger_lines}

## 3．正典更新

- `canon/BLANK_NUMERAL_RULE_1_1_APPLICATION_REGISTERED_CANON.md`を新規登録。
- `canon/BLANK_DATE_COUNCIL_NAME_NUMERAL_SUPPLEMENT_REGISTERED_CANON.md`の判断待ちを解決済みへ更新。
- `canon/WATER_NUMERAL_RULE_APPLICATION_REGISTERED_CANON.md`のA2／B2判断待ちをA2採用へ更新。
- `canon/README.md`へ補足優先正典を追加。

## 4．検証

- 第20話〜第37話の18本文を対象とした。
- 小銃数、箱数、人数、期間、距離、設備数、識別番号及び測定値の値は変更していない。
- 第34話の小数は値全体を変換し、先頭ゼロを保持した。
- `十分`を時間値へ誤変換しないことを確認した。
- 固有名称`五か年技術計画`、`五か年計画`、`第一鐘`、`第二鐘`、`三翼運送社`等を維持した。
- 一時監査ファイル及び処理スクリプトは最終ツリーへ残さない。

## 5．登録状態

`REGISTERED / LOCKED`
"""
write("manuscript/management/II-BLANK数字規則1.1-登録台帳.md", ledger_text)

# READMEへ登録。
readme_path = "canon/README.md"
readme_old = "- [`NUMERAL_USA_CITY_LEONIS_CANE_SUPPLEMENT_REGISTERED_CANON.md`](./NUMERAL_USA_CITY_LEONIS_CANE_SUPPLEMENT_REGISTERED_CANON.md)：数字表記の用途別併用、市の出生地名・姓・墓標旧値の失効及び第100話と外伝のレオニスの杖を確定。"
readme_new = readme_old + "\n- [`WATER_NUMERAL_RULE_APPLICATION_REGISTERED_CANON.md`](./WATER_NUMERAL_RULE_APPLICATION_REGISTERED_CANON.md)：V. WATER第91・92・93・96話への数字表記規則1.1適用を確定。\n- [`BLANK_NUMERAL_RULE_1_1_APPLICATION_REGISTERED_CANON.md`](./BLANK_NUMERAL_RULE_1_1_APPLICATION_REGISTERED_CANON.md)：作者の`例外なし`指示に基づき、II. BLANK第20〜37話へ規則1.1を編単位で適用し、判断待ちを解消。"
replace_once(readme_path, readme_old, readme_new)

# 一時監査物と処理機構を除去する。
for temporary in [
    ".github/workflows/audit-blank-numerals.yml",
    ".github/workflows/apply-blank-numeral-draft.yml",
    ".github/workflows/finalize-blank-numerals.yml",
    "scripts/audit_blank_numerals.py",
    "scripts/apply_blank_numeral_draft.py",
    "scripts/finalize_blank_numerals.py",
    "manuscript/management/_tmp_blank_numeral_audit.md",
    "manuscript/management/_tmp_blank_numeral_residual.md",
]:
    p = Path(temporary)
    if p.exists():
        p.unlink()
