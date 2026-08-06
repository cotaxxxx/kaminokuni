from pathlib import Path
import re

BASE = "e45f05e3380e9ab6d2982c8627056ea15c50da1f"
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


def get(path):
    return Path(path).read_text(encoding="utf-8")


def put(path, text):
    Path(path).write_text(text, encoding="utf-8", newline="")


def apply(path, pairs):
    text = get(path)
    for old, new in pairs:
        text = text.replace(old, new)
    put(path, text)


# 仮適用で残った規則1.1対象と、誤変換・規則1.2表現を確定補正する。
apply(TARGETS[0], [("一時間", "1時間")])
apply(TARGETS[2], [
    ("七四", "74"), ("本人携行、一部。", "本人携行、1部。"),
    ("同文記録、一部。", "同文記録、1部。"), ("一時間", "1時間"),
])
apply(TARGETS[4], [("五十家", "50家")])
apply(TARGETS[5], [
    ("通常手続で10分だ", "通常手続で十分だ"),
    ("5か年計画", "五か年計画"), ("柚は一部を買った。", "柚は1部を買った。"),
])
apply(TARGETS[6], [
    ("椅子が四脚。", "椅子が4脚。"), ("赤い十二襞", "赤い12襞"),
    ("5か年計画", "五か年計画"),
])
apply(TARGETS[7], [("七四", "74"), ("赤い十二襞", "赤い12襞"), ("三者立会い", "3者立会い")])
apply(TARGETS[8], [("三者が", "3者が")])
apply(TARGETS[9], [
    ("一部は技術院。", "1部は技術院。"),
    ("一部は主任監査官が封印して携行する。", "1部は主任監査官が封印して携行する。"),
    ("赤い十二襞", "赤い12襞"), ("1度でも", "一度でも"),
])
apply(TARGETS[10], [("製造番号、一から十二。", "製造番号、1から12。")])
apply(TARGETS[12], [
    ("十二まで。", "12まで。"), ("主任監査官が柚へ1度頷く。", "主任監査官が柚へ一度頷く。"),
    ("柚は、その1度を見た。", "柚は、その一度を見た。"),
])
apply(TARGETS[14], [
    ("1秒間に六十四・21回。前回との差は〇・2回以内です", "1秒間に64.21回。前回との差は0.02回以内です"),
    ("十三・2度", "13.2度"), ("毎秒二・1メートル", "毎秒2.1メートル"),
    ("毎秒二十三・4メートル", "毎秒23.4メートル"),
    ("毎秒四十六・8メートル", "毎秒46.8メートル"),
    ("毎秒〇・468キロメートル", "毎秒0.0468キロメートル"),
])
apply(TARGETS[15], [("一時間", "1時間"), ("零", "0"), ("第2鐘", "第二鐘")])
apply(TARGETS[16], [("一単位の質量", "1単位の質量")])
apply(TARGETS[17], [("5か年計画", "五か年計画"), ("零", "0"), ("十数名", "10数名")])

# 記録・公文書の番号付き列挙は算用数字へ統一する。
nums = {"一": "1", "二": "2", "三": "3", "四": "4", "五": "5", "六": "6", "七": "7", "八": "8", "九": "9"}
for path in TARGETS:
    text = get(path)
    text = re.sub(r"(?m)^([一二三四五六七八九])、", lambda m: nums[m.group(1)] + "、", text)
    put(path, text)

# 固有名称は全対象で復旧・固定する。
for path in TARGETS:
    apply(path, [("5か年技術計画", "五か年技術計画"), ("5か年計画", "五か年計画")])

blank_section = """## 4．数字表記

状態：`RESOLVED / RULE 1.1 APPLIED THROUGHOUT II. BLANK / NO EDITORIAL EXCEPTION`

後続の`NUMERAL_USA_CITY_LEONIS_CANE_SUPPLEMENT_REGISTERED_CANON.md`により確定した用途別併用規則を、`BLANK_NUMERAL_RULE_1_1_APPLICATION_REGISTERED_CANON.md`によりII. BLANK全体へ適用した。

作者の指示は`例外なし`である。旧対応案A2を採用し、第20話〜第37話を「漢数字体の編」とする旧対応案B2は採用しない。

- 第17話〜第19話：既存の算用数字表記を維持する。
- 第20話〜第37話：年月日、年齢、人数、人口、金額、距離、日数、数量、照合値、測定値、記録値、識別番号及び番号付き列挙へ規則1.1を適用済み。
- 規則1.2の和語数え、慣用表現、文学的反復及び固有名称は維持する。これは編単位の例外ではなく、数字表記規則そのものの適用である。

したがって、II. BLANKの数字表記に関する判断待ちは存在しない。

"""
path = "canon/BLANK_DATE_COUNCIL_NAME_NUMERAL_SUPPLEMENT_REGISTERED_CANON.md"
text = get(path)
text = re.sub(r"## 4．数字表記\n.*?(?=## 5．整合性判断)", blank_section, text, flags=re.S)
text = text.replace("- 数字表記。", "- 数字表記（本登録時点。後続の優先正典によりII. BLANK全体へ規則1.1適用済み）。")
text = text.replace(
    "及びII. BLANKを数字表記統一の最優先監査対象とする判断に限って過去の記録より優先する。",
    "及びII. BLANKを数字表記統一の対象とする旧判断に限って過去の記録より優先する。数字表記の現行値は後続の`BLANK_NUMERAL_RULE_1_1_APPLICATION_REGISTERED_CANON.md`を優先する。",
)
put(path, text)

water_section = """## 3．後続更新――II. BLANK（解決済み）

作者は、II. BLANK第20話〜第37話の数字表記について`例外なし`と指示した。

これにより対応案A2を採用し、規則1.1該当箇所を編単位で算用数字へ統一した。対応案B2の「漢数字体の編」とする例外は採用しない。

現行値は`BLANK_NUMERAL_RULE_1_1_APPLICATION_REGISTERED_CANON.md`及び現行本文を優先する。規則1.2該当表現及び固有名称の漢数字は維持する。

"""
path = "canon/WATER_NUMERAL_RULE_APPLICATION_REGISTERED_CANON.md"
text = get(path)
text = re.sub(r"## 3．.*?(?=## 4．非変更範囲)", water_section, text, flags=re.S)
text = text.replace(
    "II. BLANK第20〜37話の数字表記は、対応案A2又はB2の作者判断を待つ。",
    "II. BLANK第20〜37話は対応案A2を採用し、規則1.1を例外なく適用済みである。",
)
put(path, text)

canon = f"""# 『The Black Wall』II. BLANK数字表記規則1.1 全編適用 優先正典

## 状態

- 作品：**The Black Wall**
- 対象：II. BLANK第20話〜第37話
- 登録日：2026年8月6日
- 状態：`REGISTERED-CANON / PRIORITY / LOCKED`
- 種別：`NUMERAL RULE 1.1 APPLICATION / NO EDITORIAL EXCEPTION / II. BLANK COMPLETE`
- 作業基準コミット：`{BASE}`
- 作者指示：`例外なし`

本正典は、`NUMERAL_USA_CITY_LEONIS_CANE_SUPPLEMENT_REGISTERED_CANON.md`の規則1.1をII. BLANK第20話〜第37話へ編単位で適用した結果を固定する。

## 1．作者判断

旧対応案A2を採用する。第20話〜第37話を「漢数字体の編」とする旧対応案B2は採用せず、編、章又は話を単位とする数字表記上の例外を設けない。

作者の`例外なし`は規則1.2の廃止を意味しない。和語数え、慣用表現、文学的反復及び固有名称は、用途別併用規則に従って漢数字を維持する。

## 2．規則1.1の適用範囲

年月日、時刻、年齢、期間、人数、人口、金額、距離、数量、武器数、箱数、設備数、文書部数、番号付き列挙、帳簿・公文書・記録欄の数値、測定値、技術値、誤差、比率、計算値及び識別番号を算用数字とする。

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

`一つ`等の和語数え、`一度だけ`・`一度も`・`もう一度`等の慣用又はリズム表現、数量ではない`一部`・`一方`・`一時`・`二重`、及び`三枚の翼`、`三翼運送社`、`三つの欄`、`五か年技術計画`、`五か年計画`、`第一鐘`、`第二鐘`、`三卿`、`四卿`等の確定名称又は制度語は漢数字を維持する。

文書の部数を示す`一部`は`1部`とし、「一部分」を意味する`一部`は漢数字を維持する。

## 4．本文適用

第20話〜第37話の18本文ファイルへ適用した。数値の値、単位、算術関係、事件順序、人物関係、会話の意味及び物語内容は変更していない。

第17話〜第19話は既存の算用数字表記が規則1.1と一致しているため、本文を変更していない。

## 5．優先関係

本正典は、II. BLANKの数字表記に限り、第20話〜第37話を漢数字主体のまま保留する判断、A2又はB2の作者判断を待つ状態、及びII. BLANKを「漢数字体の編」とする例外案より優先する。

抵触しない本文、規則1.2、固有名称及び旧正典の履歴的記録は維持する。

## 6．登録宣言

II. BLANKには、編、章又は話を単位とする数字表記上の例外を設けない。

第17話〜第37話の規則1.1該当数値は算用数字であり、II. BLANKの数字表記に関する判断待ちは解消した。

将来の変更には、作者の新たな明示指示を必要とする。
"""
put("canon/BLANK_NUMERAL_RULE_1_1_APPLICATION_REGISTERED_CANON.md", canon)

items = "\n".join(f"{i}. `{p}`" for i, p in enumerate(TARGETS, 1))
ledger = f"""# II. BLANK数字表記規則1.1 全編適用 登録台帳

- 登録日：2026年8月6日
- 作業基準コミット：`{BASE}`
- 対応正典：`canon/BLANK_NUMERAL_RULE_1_1_APPLICATION_REGISTERED_CANON.md`
- 作者指示：`例外なし`
- 採用案：旧対応案A2
- 不採用案：旧対応案B2

## 1．登録内容

II. BLANK第20話〜第37話について、規則1.1該当箇所を編単位で算用数字へ統一した。規則1.2の和語数え、慣用表現、文学的反復及び固有名称は維持した。

## 2．変更本文

{items}

## 3．正典更新

- 新規優先正典を登録。
- `BLANK_DATE_COUNCIL_NAME_NUMERAL_SUPPLEMENT_REGISTERED_CANON.md`の判断待ちを解決済みへ更新。
- `WATER_NUMERAL_RULE_APPLICATION_REGISTERED_CANON.md`のA2／B2判断待ちをA2採用へ更新。
- `canon/README.md`へ補足優先正典を追加。

## 4．検証

第34話の小数は値全体を変換し先頭ゼロを保持した。`十分`の誤変換を復旧し、固有名称を維持した。数値の値、単位、算術関係、事件順序、人物関係及び物語内容は変更していない。一時監査物は最終ツリーへ残さない。

## 5．登録状態

`REGISTERED / LOCKED`
"""
put("manuscript/management/II-BLANK数字規則1.1-登録台帳.md", ledger)

path = "canon/README.md"
text = get(path)
anchor = "- [`NUMERAL_USA_CITY_LEONIS_CANE_SUPPLEMENT_REGISTERED_CANON.md`](./NUMERAL_USA_CITY_LEONIS_CANE_SUPPLEMENT_REGISTERED_CANON.md)：数字表記の用途別併用、市の出生地名・姓・墓標旧値の失効及び第100話と外伝のレオニスの杖を確定。"
addition = anchor + "\n- [`WATER_NUMERAL_RULE_APPLICATION_REGISTERED_CANON.md`](./WATER_NUMERAL_RULE_APPLICATION_REGISTERED_CANON.md)：V. WATER第91・92・93・96話への数字表記規則1.1適用を確定。\n- [`BLANK_NUMERAL_RULE_1_1_APPLICATION_REGISTERED_CANON.md`](./BLANK_NUMERAL_RULE_1_1_APPLICATION_REGISTERED_CANON.md)：作者の`例外なし`指示に基づき、II. BLANK第20〜37話へ規則1.1を編単位で適用し、判断待ちを解消。"
if "BLANK_NUMERAL_RULE_1_1_APPLICATION_REGISTERED_CANON.md" not in text:
    text = text.replace(anchor, addition)
put(path, text)

# 最終ツリーから作業用ファイルを除去する。
for name in [
    ".github/workflows/audit-blank-numerals.yml", ".github/workflows/apply-blank-numeral-draft.yml",
    ".github/workflows/finalize-blank-numerals.yml", "scripts/audit_blank_numerals.py",
    "scripts/apply_blank_numeral_draft.py", "scripts/finalize_blank_numerals.py",
    "manuscript/management/_tmp_blank_numeral_audit.md", "manuscript/management/_tmp_blank_numeral_residual.md",
]:
    p = Path(name)
    if p.exists():
        p.unlink()
