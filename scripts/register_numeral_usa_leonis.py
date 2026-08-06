from pathlib import Path

BASE_COMMIT = "76ea12b195966d4aff67aa418a52539cd17fb33b"
CANON_PATH = Path("canon/NUMERAL_USA_CITY_LEONIS_CANE_SUPPLEMENT_REGISTERED_CANON.md")
LEDGER_PATH = Path("manuscript/management/数字表記・市墓標・レオニス杖-補足登録台帳.md")


def replace_once(path_str: str, old: str, new: str) -> None:
    path = Path(path_str)
    text = path.read_text(encoding="utf-8")
    old_count = text.count(old)
    new_count = text.count(new)
    if old_count != 1 or new_count != 0:
        raise RuntimeError(
            f"Unexpected state: {path_str}: old={old_count}, new={new_count}, old_text={old!r}"
        )
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="")


# 1. 年月日の月表記を算用数字へ統一する。
DATE_REPLACEMENTS = {
    "manuscript/chapters/13-光の重さ/037-第37話-血の外から.md": (
        "神記2875年（西暦1591年）一月。",
        "神記2875年（西暦1591年）1月。",
    ),
    "manuscript/chapters/14-黒い壁/038-第38話-一人残れ.md": (
        "西暦1591年　一月。",
        "西暦1591年1月。",
    ),
    "manuscript/chapters/14-黒い壁/039-第39話-最初の記録.md": (
        "西暦1591年　一月。",
        "西暦1591年1月。",
    ),
    "manuscript/chapters/14-黒い壁/040-第40話-地図の外.md": (
        "西暦1592年　一月。",
        "西暦1592年1月。",
    ),
    "manuscript/chapters/15-石/041-第41話-山の口.md": (
        "西暦1592年　七月。",
        "西暦1592年7月。",
    ),
    "manuscript/chapters/16-南方の陸地/046-第46話-森本左近.md": (
        "西暦1592年　十月。",
        "西暦1592年10月。",
    ),
}
for rel_path, (old, new) in DATE_REPLACEMENTS.items():
    replace_once(rel_path, old, new)

# 2. 第100話の杖描写を外伝の現行本文へ合わせる。
replace_once(
    "manuscript/chapters/34-終話/100-第100話-海.md",
    "服。\n村のもの。\n\n杖。\nなし。\n\n背。",
    "服。\n村のもの。\n\n杖。\n地面に置かれている。\n\n背。",
)

# 3. 旧正典へ部分失効注記を付す。
replace_once(
    "canon/49_CHAPTER_34_REGISTERED_CANON.md",
    "### 4.5 旧セル市と市の墓\n\nアズナルは出航前に一人で旧セル市へ向かう。",
    "### 4.5 旧セル市と市の墓\n\n状態：`SUPERSEDED IN PART`\n\n本節の`宇佐市`、墓標へ`宇佐`が後から加えられたとする記述、及びこれに基づく説明は、後続の現行本文及び`NUMERAL_USA_CITY_LEONIS_CANE_SUPPLEMENT_REGISTERED_CANON.md`により置換済みである。\n\n現行値は次のとおりである。\n\n- `宇佐`は市の出生地名であり、姓ではない。\n- 市の生前の法的登録名は`市`であり、姓はない。\n- 後代に墓標へ加えられた姓は`長洲`である。\n- 墓標上の名は`長洲　市`である。\n\n以下の旧記述は履歴として保持するが、現行設定には使用しない。\n\nアズナルは出航前に一人で旧セル市へ向かう。",
)

replace_once(
    "canon/LEONIS_FULL_REWRITE_REGISTERED_CANON.md",
    "## 1．作者指示と登録許可\n",
    "## 後続更新（2026年8月6日）\n\n状態：`SUPERSEDED IN PART`\n\n本正典中の市の墓標を`市`一文字に固定し、`長洲　市`としない判断は、後続の現行本文及び`NUMERAL_USA_CITY_LEONIS_CANE_SUPPLEMENT_REGISTERED_CANON.md`により置換済みである。現行の墓標上の名は`長洲　市`である。\n\n杖の描写は有効であり、第100話の老人の杖は地面に置かれているものとして整合する。\n\n## 1．作者指示と登録許可\n",
)

replace_once(
    "canon/BLANK_DATE_COUNCIL_NAME_NUMERAL_SUPPLEMENT_REGISTERED_CANON.md",
    "## 4．数字表記\n\n状態：`DECISION PENDING / PRIORITY SCOPE / NO TEXT CHANGE`",
    "## 4．数字表記\n\n状態：`RESOLVED BY LATER PRIORITY CANON / SUPERSEDED IN PART`\n\n後続の`NUMERAL_USA_CITY_LEONIS_CANE_SUPPLEMENT_REGISTERED_CANON.md`により、数字表記は用途別併用規則として確定した。年月日、測定値、技術値、帳簿・公文書上の数量及び照合対象となる数値は算用数字とし、慣用表現、文学的反復、数量性の弱い通常表現及び固有名称は漢数字を維持する。\n\n第37話の年代標識にある`一月`は`1月`へ修正済みである。以下の旧判断待ち記述は履歴として保持するが、現行の判断待ちではない。",
)

replace_once(
    "canon/FIRE_DATE_NOTATION_ICHI_LAKE_INDEX_TITLE_SUPPLEMENT_REGISTERED_CANON.md",
    "1. 数字表記の統一（II. BLANKを最優先監査対象とする方針は登録済み。III. FIREの漢数字月を含む）。",
    "1. 数字表記の統一：`NUMERAL_USA_CITY_LEONIS_CANE_SUPPLEMENT_REGISTERED_CANON.md`により用途別併用規則を確定し、III. FIREの対象月表記を算用数字へ修正済み。`RESOLVED`。",
)

# 4. READMEの現行要約と正典案内を更新する。
replace_once(
    "canon/README.md",
    "- 1635年：市の生前の法的登録名は「市」。墓地記録の「宇佐市」は後代登録で、生前姓名を変更しない",
    "- 1635年：市の生前の法的登録名は「市」。宇佐は出生地名であり姓ではない。後代に墓標へ「長洲」が加えられ、墓標上の名は「長洲　市」。旧「宇佐市」設定は`SUPERSEDED`",
)
replace_once(
    "canon/README.md",
    "## 承認設計\n",
    "## 補足優先正典\n\n- [`NUMERAL_USA_CITY_LEONIS_CANE_SUPPLEMENT_REGISTERED_CANON.md`](./NUMERAL_USA_CITY_LEONIS_CANE_SUPPLEMENT_REGISTERED_CANON.md)：数字表記の用途別併用、市の出生地名・姓・墓標旧値の失効及び第100話と外伝のレオニスの杖を確定。\n\n## 承認設計\n",
)

# 5. SUPERSEDED台帳へ旧値を追加する。
superseded_path = Path("canon/SUPERSEDED.md")
superseded_text = superseded_path.read_text(encoding="utf-8")
superseded_heading = "## 追補：市の出生地名・姓・墓標（2026年8月6日）"
if superseded_heading in superseded_text:
    raise RuntimeError("SUPERSEDED追補が既に存在する")
superseded_append = f"""

{superseded_heading}

| 旧値 | 現行値 | 状態 |
|---|---|---|
| `宇佐市`を後代の墓地登録名又は墓標上の名とする | `宇佐`は出生地名であり姓ではない。生前の法的登録名は`市`。後代に`長洲`が加えられ、墓標上の名は`長洲　市` | `SUPERSEDED` |
| 墓標へ`宇佐`が後から加えられた | 墓標へ後から加えられた姓は`長洲` | `SUPERSEDED` |
| 市の墓標を`市`一文字へ固定し、`長洲　市`としない | 現行本文の墓標上の名は`長洲　市` | `SUPERSEDED` |

市の生前の法的登録名が`市`であり、姓がなかったことは維持する。
"""
superseded_path.write_text(superseded_text.rstrip() + superseded_append + "\n", encoding="utf-8", newline="")

# 6. 新規優先正典を登録する。
canon_content = f"""# 『The Black Wall』数字表記・市墓標旧値・レオニス杖 整合補足優先正典

## 状態

- 作品：**The Black Wall**
- 登録日：2026年8月6日
- 状態：`REGISTERED-CANON / PRIORITY / LOCKED`
- 種別：`NUMERAL STYLE RULE / SUPERSEDED NAME RECORD / CANE CONTINUITY`
- 作業基準コミット：`{BASE_COMMIT}`
- 対象：II. BLANK、III. FIRE、第100話、外伝「レオニス」、市の墓標関連正典

本正典は、作者の承認に基づき、数字表記、市の旧`宇佐市`設定及びレオニスの杖の三件を確定する。

## 1．数字表記

状態：`RESOLVED / USAGE-BASED MIXED RULE / TEXT REVISED`

漢数字又は算用数字のいずれかを全本文へ一括適用しない。数字の機能により次のとおり使い分ける。

### 1.1 算用数字

次は算用数字を用いる。

- 年月日、年齢、人口及び金額。
- 距離、重量、時間、期間及び割合。
- 武器、箱、部品等の照合対象となる数量。
- 技術値、測定値及び計算式。
- 章番号、話数、資料番号。
- 帳簿、公文書、一覧及び記録欄に記載される数。

### 1.2 漢数字

次は漢数字を維持する。

- `一人で行く`、`二つに分ける`、`三度目`、`一歩`、`一方`等の数量性の弱い通常表現。
- 慣用句、比喩及び文学的反復。
- `五か年技術計画`、`三欄式`、`第一鐘`等の固有名称又は制度上固定された表現。
- 話題及び題名として確定した表現。

### 1.3 今回の本文修正

年月日の月表記を算用数字へ統一した。

| 話 | 修正前 | 修正後 |
|---|---|---|
| 第37話 | `神記2875年（西暦1591年）一月。` | `神記2875年（西暦1591年）1月。` |
| 第38話 | `西暦1591年　一月。` | `西暦1591年1月。` |
| 第39話 | `西暦1591年　一月。` | `西暦1591年1月。` |
| 第40話 | `西暦1592年　一月。` | `西暦1592年1月。` |
| 第41話 | `西暦1592年　七月。` | `西暦1592年7月。` |
| 第46話 | `西暦1592年　十月。` | `西暦1592年10月。` |

既存の漢数字表現は、本規則に照らして有効なものを一律置換しない。これにより、旧`DECISION PENDING`は解消する。

## 2．市の出生地名、姓及び墓標

状態：`RESOLVED / OLD USA-ICHI VALUE SUPERSEDED`

現行値を次のとおり確定する。

- `宇佐`は市の出生地名であり、姓ではない。
- 市の生前の法的登録名は`市`であり、姓はない。
- 後代に墓標へ加えられた姓は`長洲`である。
- 墓標上の名は`長洲　市`である。

次の旧値は`SUPERSEDED`とする。

- `宇佐市`を後代の墓地登録名又は墓標上の名とする。
- 墓標へ`宇佐`が後から加えられたとする。
- 墓標を`市`一文字へ固定し、`長洲　市`としない。

旧正典本文は履歴として保持するが、上記旧値を現行設定へ使用しない。

## 3．レオニスの杖

状態：`RESOLVED / TEXT REVISED`

第100話の左右の耳の形が異なる老人と、外伝「レオニス」の老人は同一人物線上にある。

外伝では、レオニスが高齢になって杖を使用し、丘へ到着後に杖を地面へ置く描写が反復される。この現行本文を基準とする。

第100話の次の記述を修正した。

- 修正前：`杖。なし。`
- 修正後：`杖。地面に置かれている。`

これにより、レオニスは杖を用いて丘へ来て、海を見る際に杖を地面へ置いているものとして、本編と外伝が一致する。

## 4．優先関係

本正典は、次の事項に限って既存正典及び旧登録記録より優先する。

1. 数字表記の用途別併用規則及び今回修正した月表記。
2. 市の`宇佐市`、`宇佐`追刻及び墓標一文字固定の旧値。
3. 第100話及び外伝におけるレオニスの杖。

抵触しない本文、設定及び旧正典の履歴的記録は維持する。

## 5．登録宣言

数字表記は、数値の機能に応じて算用数字と漢数字を使い分ける。

市の墓標上の名は`長洲　市`であり、`宇佐市`ではない。

第100話のレオニスの杖は、地面に置かれている。

将来の変更には、作者の新たな明示指示を必要とする。
"""
CANON_PATH.write_text(canon_content, encoding="utf-8", newline="")

# 7. 登録台帳を作成する。
ledger_content = f"""# 数字表記・市墓標・レオニス杖 補足登録台帳

## 状態

- 作品：**The Black Wall**
- 登録日：2026年8月6日
- 状態：`REGISTERED / LOCKED`
- 作業基準コミット：`{BASE_COMMIT}`
- 対応正典：`canon/NUMERAL_USA_CITY_LEONIS_CANE_SUPPLEMENT_REGISTERED_CANON.md`

## 1．作者承認

作者は、数字表記、市の旧`宇佐市`記述及び第100話と外伝のレオニスの杖について提示された改善案を承認し、修正及び登録を指示した。

## 2．本文修正

### 2.1 月表記

次の6ファイルで年月日の月を算用数字へ修正した。

1. `manuscript/chapters/13-光の重さ/037-第37話-血の外から.md`
2. `manuscript/chapters/14-黒い壁/038-第38話-一人残れ.md`
3. `manuscript/chapters/14-黒い壁/039-第39話-最初の記録.md`
4. `manuscript/chapters/14-黒い壁/040-第40話-地図の外.md`
5. `manuscript/chapters/15-石/041-第41話-山の口.md`
6. `manuscript/chapters/16-南方の陸地/046-第46話-森本左近.md`

### 2.2 レオニスの杖

`manuscript/chapters/34-終話/100-第100話-海.md`の`杖。なし。`を`杖。地面に置かれている。`へ修正した。

## 3．正典管理修正

次を更新した。

- `canon/BLANK_DATE_COUNCIL_NAME_NUMERAL_SUPPLEMENT_REGISTERED_CANON.md`
- `canon/FIRE_DATE_NOTATION_ICHI_LAKE_INDEX_TITLE_SUPPLEMENT_REGISTERED_CANON.md`
- `canon/49_CHAPTER_34_REGISTERED_CANON.md`
- `canon/LEONIS_FULL_REWRITE_REGISTERED_CANON.md`
- `canon/SUPERSEDED.md`
- `canon/README.md`

旧記述は履歴として保持し、部分失効又は`SUPERSEDED`を明示した。

## 4．新規登録

- 優先正典：`canon/NUMERAL_USA_CITY_LEONIS_CANE_SUPPLEMENT_REGISTERED_CANON.md`
- 本登録台帳：`manuscript/management/数字表記・市墓標・レオニス杖-補足登録台帳.md`

## 5．非変更範囲

- 数量性の弱い通常表現、慣用句、比喩、文学的反復及び固有名称の漢数字。
- 市の生前の法的登録名が`市`であり、姓がなかったこと。
- レオニス外伝の杖描写。
- 上記対象外の本文及び設定。

## 6．固定

数字表記の旧判断待ちは解消した。

旧`宇佐市`設定は失効し、墓標上の名は`長洲　市`である。

第100話と外伝の杖描写は整合した。
"""
LEDGER_PATH.write_text(ledger_content, encoding="utf-8", newline="")

# 8. 一時処理ファイルを最終ツリーから除去する。
Path(".github/workflows/register-numeral-usa-leonis.yml").unlink()
Path("scripts/register_numeral_usa_leonis.py").unlink()
