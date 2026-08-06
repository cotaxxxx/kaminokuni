# 全話整合性監査 補足登録台帳――年代表記（III. FIRE・第35話）・外伝湖名・INDEX話題

- 登録日：2026年8月6日
- 作業基準コミット：`df383d120da6e4126be3144b6e39ee370c717cd0`
- 対応正典：`canon/FIRE_DATE_NOTATION_ICHI_LAKE_INDEX_TITLE_SUPPLEMENT_REGISTERED_CANON.md`
- 起草：chat側監査。登録コミットは作者側が実施する。

## 1．変更ファイル一覧

### 年代標識（西暦単独化、7ファイル・各1行）

1. `manuscript/chapters/13-光の重さ/035-第35話-光の重さ.md`（7行目）
2. `manuscript/chapters/14-黒い壁/038-第38話-一人残れ.md`（7行目）
3. `manuscript/chapters/14-黒い壁/039-第39話-最初の記録.md`（7行目）
4. `manuscript/chapters/14-黒い壁/040-第40話-地図の外.md`（7行目）
5. `manuscript/chapters/15-石/041-第41話-山の口.md`（7行目）
6. `manuscript/chapters/16-南方の陸地/046-第46話-森本左近.md`（7行目）
7. `manuscript/chapters/17-帰還/050-第50話-手紙.md`（7行目）

### 湖名（1ファイル・1行）

8. `manuscript/side-stories/市/004-第4話-旅立ち.md`（151行目、ベガ湖→ペガ湖）

### INDEX話題同期（1ファイル・4行）

9. `manuscript/INDEX.md`（第2話・第46話・第65話・第79話の表示題のみ。リンク先パスは不変）

### 新規

10. `canon/FIRE_DATE_NOTATION_ICHI_LAKE_INDEX_TITLE_SUPPLEMENT_REGISTERED_CANON.md`
11. 本台帳

## 2．来歴

- 2026-08-06、chat側の全話整合性監査（III. FIRE初監査＋横断チェック）で、要修正2件（外伝湖名残存・INDEX旧題4件）と判断待ち1件（通常場面の神記併記7箇所）を検出。
- 同日、作者が案AのIII. FIRE・第35話への適用、湖名残存修正及びINDEX同期を承認。
- 本文の意味内容、会話、因果関係への変更はない。全変更が表記・索引の同期に限られる。

## 3．検証結果（chat側）

- 修正後、本文全話の`神記`表記は、御前会議・賢人会議場面、会議記録及び公的記録の引用（第36話記録帳内・第40話五か年計画参照）に限られる。
- 本文全話の湖名grepで`ベガ湖`は0件、`ペガ湖`のみ。`ベガ島`は不変。
- 本文見出し・INDEX.md・TOC.md・正式目次正典の話題が全108話で完全一致。
