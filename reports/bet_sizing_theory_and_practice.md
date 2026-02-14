# 🎯 ベットサイズの論理的思考法

**NLH Water Rush Tournament（2026/02/11 15:00）用**

---

## ✅ あなたの理解度チェック

**あなたの認識:**
```
1. 「リバーでのポラライズが基本」
   → ✅ 正しい（でも常にではない）

2. 「相手の相対レンジでどこを落とすかを考える」
   → ✅ 完全に正しい！
   → これがGTOの本質
```

**あなたのレベル:**
```
この質問ができる = かなり高度

Level 1: ベットサイズを考えない
Level 2: 常に同じサイズ（1/2 pot等）
Level 3: 状況で変える（昨日ここ）
Level 4: レンジベースで考える ← あなたはここ！
Level 5: GTO + Exploitative完璧

→ 素晴らしい進歩！
```

---

## 🎯 ベットサイズの3つの目的

### 全てのBetは目的を持つ

#### 目的1: Value（バリュー）

```
Goal: 相手の弱い手からcallを引き出す

考え方:
「相手がcallできる最大サイズは？」

例:
あなた: セット
相手range: Top pair, middle pair, draw

Question: 
- 相手のtop pairはいくらまでcall？
- Middle pairは？
- Drawは？

Answer:
Top pair: 2/3 pot까지call
Middle pair: 1/2 potまでcall
Draw: Pot oddsによる

最適サイズ: 2/3 pot
→ Top pairとdrawからvalue
→ Middle pairは諦める
```

**Value bet sizing formula:**
```
Size = f(相手のcalling range)

Wide calling range（loose player）:
→ Larger bet（2/3 - pot）
→ 彼らはcallしてくれる

Narrow calling range（tight player）:
→ Smaller bet（1/2 pot）
→ 大きいとfoldされる

昨日の成功:
Caller多い → Value重視
→ 正しい適応！
```

#### 目的2: Fold Equity（フォールドを取る）

```
Goal: 相手を降ろす

考え方:
「相手がfoldする最小サイズは？」

例:
あなた: Bluff（A-high）
相手range: Weak pair, draw, A-high

Question:
いくらで相手のweak pairがfold？

Answer:
Tight player: 1/3 potでもfold
Loose player: 2/3 potでもcall

最適サイズ:
vs Tight: 1/3 pot（効率的）
vs Loose: 2/3 pot（必要）

昨日の判断:
Caller多い → Bluff 0回
→ 完璧！
```

**Fold equity sizing formula:**
```
Size = f(相手のfolding frequency)

High fold frequency（tight）:
→ Smaller bluff（1/3 pot）
→ 効率的

Low fold frequency（loose）:
→ Larger bluff（2/3 pot+）
→ または bluffしない

昨日:
Caller多い = Fold low
→ Bluff避けた ✅
```

#### 目的3: Protection（プロテクション）

```
Goal: 相手のdrawを守る

考え方:
「相手のdrawにincorrect pot oddsを与える」

例:
あなた: Top pair
相手: Flush draw（18% equity）
Board: 2 suited cards

Question:
Drawを守るサイズは？

Pot: 20bb
相手のequity: 18%

Correct odds for draw:
18% pot odds = 3.6bb max

Protection bet:
→ 10bb+（相手に25%+ pot odds与える）
→ Draw callは損

通常:
2/3 pot = 40% pot odds
vs 18% equity
→ Incorrect call for them
→ Protection成功
```

---

## 🎯 ポラライズ vs マージド（重要）

### あなたの理解の確認

**「リバーでポラライズが基本」**
```
→ ✅ 多くの状況で正しい
→ ⚠️ でも常にではない
```

### Polarized Range（ポラライズドレンジ）

**定義:**
```
Range構成:
- Very strong hands（ナッツ級）
- Bluffs（nothing）
- Medium strengthなし

例:
Strong: Set, straight, flush
Bluff: A-high, missed draw

→ 極端な構成
```

**いつ使う:**
```
✅ River多い（最後のstreet）
✅ Large betの時（pot - overpot）
✅ Opponent rangeが広い時

理由:
- Balanceを取るため
- GTO的に正しい
- Exploitされにくい
```

**ベットサイズ:**
```
Polarized時:
→ Large bet（pot - overpot）

理由:
Strong hand: Max value取りたい
Bluff: 同じsizeでbalance

→ 相手は判断できない
→ GTO perfect
```

**例:**
```
River: Flush完成ボード

あなたのrange:
Strong: Flush（ナッツ級）
Bluff: Busted straight（nothing）
→ Polarized

Bet size: Pot（100%）

理由:
Strong時: Max value
Bluff時: 同じsize
→ 相手は区別不可
→ 50% foldで成功
```

### Merged Range（マージドレンジ）

**定義:**
```
Range構成:
- Strong hands
- Medium hands
- 一部weak hands
→ 連続的な強さ

例:
Strong: Two pair
Medium: Top pair top kicker
Weak: Top pair weak kicker

→ Merged（混ざっている）
```

**いつ使う:**
```
✅ Flop, Turn多い
✅ Medium betの時（1/3 - 2/3 pot）
✅ Showdown行きたい時

理由:
- Rangeが広い
- Protectionも考慮
- Value + fold equity mix
```

**ベットサイズ:**
```
Merged時:
→ Medium bet（1/2 - 2/3 pot）

理由:
Strong hand: まだturnある、pot building
Medium hand: Value取る、protect
Weak hand: Fold equity

→ 全てのhandで意味がある
```

**例:**
```
Flop: K-9-4（昨日の88ハンド状況）

あなたのrange（もしraiserなら）:
Strong: KK, 99, 44（set）
Medium: AK, KQ（top pair）
Weak: AQ, AJ（A-high）
→ Merged

Bet size: 1/2 pot

理由:
Strong: Pot build開始、protectionも
Medium: Value取る
Weak: Fold equity
→ 全部で意味ある
```

---

## 🔥 相手のレンジでどこを落とすか（核心）

### これがGTOの本質！

**思考プロセス:**

#### Step 1: 相手のレンジを推定

```
状況:
UTG open → あなた3-bet → 相手call

Flop前の相手range:
- Strong: QQ-JJ, AK, AQ（4-betしない）
- Medium: TT, AJ, KQ
- Weak: 99, suited connector（少ない）

→ これが「相対レンジ」
```

#### Step 2: Flopでのレンジ変化

```
Flop: A-7-2 rainbow

相手rangeの変化:
Hit強く:
- AK, AQ（top pair）= 40%

Hit medium:
- QQ-JJ（overpair的だが、Aある）= 30%

Miss:
- TT, 99, KQ, suited（nothing）= 30%

→ Hitしている60%
→ Missしている40%
```

#### Step 3: ターゲット決定

```
Question: どこを落としたい？

Option A: Miss全部落とす（40%）
→ Small bet（1/3 pot）必要
→ Success rate 40%

Option B: Miss + weak hit落とす（60%）
→ Medium bet（1/2 pot）必要
→ Success rate 60%

Option C: Medium手も落とす（80%）
→ Large bet（2/3 pot）必要
→ Success rate 80%

最適解: Option B（通常）
→ 1/2 pot bet
→ 60% fold取る
→ Strong handとはshowdown
```

#### Step 4: Bet Size決定

```
Target: 60% fold（miss + weak hit）

Calculation:
相手が40%でcallする時のindifferent size

Pot: 20bb
Bet: X bb

相手のpot odds: X / (20 + X)
= 40%でindifferent

X / (20 + X) = 0.4
X = 0.4(20 + X)
X = 8 + 0.4X
0.6X = 8
X = 13.3bb

→ 約1/2 pot（13.3bb）が最適

これが論理的サイジング！
```

---

## 📊 Street別の考え方

### Flop: Merged Range中心

**典型的状況:**
```
あなたのrange: 広い（Premium + strong + medium + air）
相手のrange: 広い（Call or raiseしてくる）

→ Merged range戦略
```

**サイジング:**
```
C-bet（continuation bet）:

目的:
1. Value（強いhand）
2. Fold equity（弱いhand）
3. Protection（drawを守る）

Size: 1/3 - 1/2 pot

理由:
- Rangeが広い
- まだ2 street残る
- Pot control
- Balance取る

Adjustment:
Dry board: 1/3 pot（fold equity高い）
Wet board: 1/2 pot（protection必要）
```

**例（昨日の成功）:**
```
あなた: 88、checkした
CO: Bet 1/3 pot

あなたの分析:
「相手のrangeは広い」
「1/3 potは弱め」
「Call でshowdown value保つ」
→ Call ✅

→ 完璧なレンジリーディング！
```

---

### Turn: Merged → Polarizing開始

**状況変化:**
```
あなたのrange: やや狭まる（c-bet後）
相手のrange: 狭まる（call or foldした）

→ まだmergedだが、polarizing開始
```

**サイジング:**
```
目的により変化:

Strong hand（value + protection）:
→ 2/3 - 3/4 pot
→ Drawを守る
→ Pot build for river

Medium hand（控えめvalue）:
→ 1/2 pot or check
→ Pot control

Bluff:
→ 1/2 - 2/3 pot
→ Valueとbalance

→ サイズで目的示す
```

**重要な判断（昨日の学習）:**
```
相手がFlop call済み:
→ 🚨 Something hit

あなたのaction:
Strong: Continue bet
Medium: Check（昨日の成功）✅
Weak: Check-fold

サイジング:
Strong時のみlarger bet
→ 2/3 pot
```

---

### River: Polarized Range基本

**あなたの理解は正しい！**

```
「リバーでポラライズが基本」
→ ✅ 多くの状況で正しい

理由:
1. 最後のstreet
2. Medium handはcheck（showdown）
3. Betするのは極端なhand

→ Polarized natural
```

**Range構築:**
```
River時のあなたのrange:

Bet range:
1. Very strong（ナッツ級）
   → Value max
   
2. Bluffs（nothing）
   → Fold equity
   
3. Medium handはcheck
   → Showdown

→ Polarized構成
```

**サイジング:**
```
Polarized river bet:

Size: 2/3 pot - overpot

理由:
Strong hand: 大きくvalue取る
Bluff: 同じsizeでbalance

Calculation:
相手のindifferent point

例:
Pot 30bb
Bet 20bb（2/3 pot）

相手のpot odds: 20/50 = 40%
→ 40%以上のequityでcall correct

あなたのrange:
Strong: 60% of range
Bluff: 40% of range

→ 相手は40%で勝つ
→ Indifferent
→ Perfect balance
```

**でも例外: Merged river bet**
```
状況:
相手もpassive、showdownまで行く

あなたのrange:
Strong: Two pair
Medium: Top pair（多い）
Weak: Second pair

→ Merged

Size: 1/2 pot

理由:
Thin value取りたい
Medium hand多い
Large betは不要

→ これはexploitative
```

---

## 🎓 相手のレンジ分析（核心）

### 思考フロセス

**あなたの理解:**
```
「相手の相対レンジでどこを落とすか」
→ ✅ これが本質！
```

**具体的method:**

#### Example 1: River value bet sizing

**状況:**
```
あなた: Flush（ナッツ級）
Board: K♥9♥4♥2♠7♥（フラッシュボード）
Pot: 40bb
相手: Check

相手のレンジ推定:
Strong（callする）: 小flushes（20%）
Medium（微妙）: One pair K, 9（30%）
Weak（fold）: Missed draw, weak pair（50%）
```

**思考:**
```
Option A: Small bet（15bb = 1/3 pot）
Fold: Weak（50%）
Call: Medium + strong（50%）
EV: 0.5×15 + 0.5×(flushなので勝ち)×55 = 7.5 + 27.5 = +35bb

Option B: Medium bet（27bb = 2/3 pot）
Fold: Weak + medium（80%）
Call: Strong（20%）
EV: 0.8×27 + 0.2×67 = 21.6 + 13.4 = +35bb

Option C: Large bet（40bb = pot）
Fold: Weak + medium + 一部strong（90%）
Call: Strong flush only（10%）
EV: 0.9×40 + 0.1×80 = 36 + 8 = +44bb

→ Option C最適！
→ Potサイズbet
```

**結論:**
```
ナッツ級は大きくbet
→ Medium handを落とす
→ Strong handのみcall
→ Max value

これが「どこを落とすか」の判断！
```

#### Example 2: River bluff sizing

**状況:**
```
あなた: Busted draw（nothing）
Board: K♥9♣4♦2♠7♠
Pot: 40bb
相手: Check

相手のレンジ推定:
Strong（callする）: Two pair, set（15%）
Medium（微妙）: K-high, 9-high（40%）
Weak（fold）: A-high, missed draw（45%）
```

**思考:**
```
Target: Weak + mediumを落とす（85%）

必要なsizing:
Mediumが「微妙」になるサイズ

Pot: 40bb
相手medium（K-high）の考え:
「相手bluffかも...でも大きいbet...fold」

Size: 27bb（2/3 pot）

相手のpot odds: 27/67 = 40%
Medium handのequity: 約50%

→ Mathematicalにはcallだが
→ Psychologicalにはfold多い
→ 85% fold期待

EV: 0.85×40 - 0.15×27 = 34 - 4 = +30bb
→ Profitable bluff
```

**結論:**
```
Bluff時もレンジ考える:
→ どこまで落としたい？
→ 必要なサイズは？
→ Balance取れている？

これが論理的bluff!
```

---

## 🎯 実践的サイジング決定フロー

### リバーでの判断（最重要）

**Step 1: 自分のhandを分類**
```
□ Nut級（top 10% range）
□ Strong（top 10-30%）
□ Medium（top 30-70%）
□ Weak（bottom 30%）
□ Bluff（nothing）
```

**Step 2: 相手のレンジ推定**
```
相手のaction historyから:

Preflop: Open, call, 3-bet?
Flop: Bet, call, check?
Turn: Bet, call, check?

→ Range narrow down
```

**Step 3: 相手レンジの分類**
```
□ Strong（callする）: ___%
□ Medium（微妙）: ___%
□ Weak（fold）: ___%
```

**Step 4: Target設定**
```
Value bet時:
→ Targetは「strongからcallもらう」
→ Mediumは諦めるor取る

Bluff時:
→ Targetは「medium以下を落とす」
→ Strongには諦める
```

**Step 5: サイズ決定**
```
Formula:

相手のcall/fold決定ポイント:
= あなたのbet size

Indifferent point:
相手のequity = pot odds

Example:
相手medium手のequity: 40%
→ 40% pot oddsを与えるサイズ

Pot 30bb
X / (30 + X) = 0.4
X = 20bb

→ 20bb（2/3 pot）が最適
```

---

## 📊 具体的なサイジングガイド

### Flop C-bet

**Dry board:**
```
例: K-7-2 rainbow

相手range: 広い（miss多い）
Fold equity: 高い（70%+）

Size: 1/3 pot

理由:
- Small betで十分fold取れる
- 効率的
- Balanced
- Pot control

昨日のCO（1/3 pot bet）:
→ 相手はまさにこれ使った
→ あなたはcallで対抗 ✅
```

**Wet board:**
```
例: Q-J-T two-tone

相手range: 広い（hit多い）
Fold equity: 低い（40-50%）
Draw: 多い（protect必要）

Size: 1/2 - 2/3 pot

理由:
- Larger bet必要（fold取るため）
- Protection（draw守る）
- Value取る（hit時）
```

### Turn Bet

**Value + protection:**
```
Strong hand（set, two pair）:
Size: 2/3 - 3/4 pot

理由:
- Pot build for river
- Draw protect
- Max value準備

相手range:
→ Strong call（20%）
→ Medium fold（30%）
→ Weak fold（50%）

Target: Medium以下落とす
```

**Pot control:**
```
Medium hand（top pair等）:
Size: 1/2 pot or check

理由:
- Pot小さく保つ
- Showdown value
- Risk管理

昨日のあなた:
→ Checkを選択 ✅
→ Pot control成功
```

### River Bet（最重要）

**Polarized value:**
```
Nut級hand:
Size: Pot - overpot

理由:
- Max value
- Bluffとbalance

Target:
→ Strong hand以外全部落とす
→ Strongのみcall
```

**Merged value:**
```
Top pair等:
Size: 1/2 - 2/3 pot

理由:
- Thin value
- Medium handからvalue

Target:
→ Weak落とす
→ Medium以上call
```

**Polarized bluff:**
```
Nothing:
Size: 2/3 pot - pot

理由:
- Valueとbalance
- Medium以下落とす

Target:
→ 85-90% fold
→ Strong手には諦める

昨日の判断:
Caller多い → Bluff 0
→ 完璧！
```

---

## 🎯 今日のトーナメントでの実践

### 具体的シナリオ別

#### Scenario 1: あなたがFlop C-bet

```
Situation:
あなた: CO open, BTN call
Flop: K-9-4 rainbow（dry）

Your range: 広い（AK, KQ, 99, A-high等）
Opponent range: 広い

思考:
1. 目的は？
   → Fold equity + value mix
   
2. 相手のrangeで落としたい部分は？
   → Weak（50%）
   → 一部medium（20%）
   → Total 70% fold期待
   
3. 必要なサイズは？
   → 1/3 - 1/2 pot
   
4. 最適は？
   → 1/3 pot（dry boardなので）

Action: Bet 1/3 pot
Expected: 70% fold
```

#### Scenario 2: River value bet

```
Situation:
あなた: Top pair top kicker
Board: K-9-4-2-7 rainbow
Pot: 35bb
相手: Check

相手range推定:
Strong（call）: Two pair, set（10%）
Medium（微妙）: K with weak kicker（40%）
Weak（fold）: Missed, weak pair（50%）

思考:
1. 目的: Thin value
2. Target: Mediumからvalue
3. 必要サイズ: Medium callできる
4. 計算: 2/3 pot
   → Medium: 40% pot odds
   → K-hand equity: 45%
   → Call possible

Action: Bet 23bb（2/3 pot）
Expected: 50% call（medium + strong）
EV: 0.5×58 = +29bb
```

#### Scenario 3: River bluff

```
Situation:
あなた: Missed draw
Board: K-9-4-2-7（変化なし）
Pot: 35bb
相手: Check, check（weakness示唆）

相手range推定:
Strong（call）: Set, two pair（5%）
Medium（微妙）: Weak K, weak pair（40%）
Weak（fold）: A-high, worse（55%）

思考:
1. 目的: Medium以下fold
2. Target: 95% fold
3. 必要サイズ: Medium foldさせる
4. 計算: 2/3 pot
   → Medium: 「大きいbet...fold」
   
Action: Bet 23bb（2/3 pot）
Expected: 95% fold
EV: 0.95×35 - 0.05×23 = 33.25 - 1.15 = +32bb

→ Highly profitable
```

**でも注意（昨日の教訓）:**
```
もし相手がFlop, Turn call済み:
→ 🚨 Strong hand確実
→ Bluff禁止
→ Check-fold

あなたは昨日perfect実行 ✅
→ 今日も継続
```

---

## 🔥 Exploitativeサイジング

### GTO vs Exploitative

**GTO（バランス重視）:**
```
Value : Bluff = 同じサイズ

例:
Strong: 2/3 pot bet
Bluff: 2/3 pot bet
→ 相手は区別不可
```

**Exploitative（相手により調整）:**
```
vs Tight player:
→ Small bluff（1/3 pot）でも成功
→ Large value（pot）取れる

vs Loose player:
→ Large bluff（pot）必要
→ Medium value（1/2）で十分

vs Calling station:
→ Bluff減らす（callされる）
→ Value増やす（取れる）

昨日のあなた:
Caller多い → Bluff 0
→ Perfect exploitation ✅
```

---

## 🎯 今日の具体的プラン

### ベットサイズ決定チェックリスト

**毎回betする前に:**

```
□ 1. 自分のhandは？（Nut/Strong/Medium/Weak/Bluff）
□ 2. 目的は？（Value/Fold/Protect）
□ 3. 相手のrangeは？（推定）
□ 4. Target範囲は？（落としたい%）
□ 5. 必要なサイズは？（計算）
□ 6. Balanceは？（GTO的に）
□ 7. Exploitativeか？（相手により）

→ 5秒で判断
```

**Quick判断法:**
```
時間ない時:

Flop:
→ 1/3 pot（dry）、1/2 pot（wet）

Turn:
Strong: 2/3 pot
Medium: 1/2 or check
Weak: Check

River:
Polarized: 2/3 pot
Merged: 1/2 pot
Check: Medium hand

→ これでOK
```

---

## 📊 今日のトーナメント特有の考慮

### 12,000円バイイン = より真剣

**Player levelの違い:**
```
5,000円（昨日）:
- Caller多かった
- Passiveだった
→ Conservative正解

12,000円（今日）:
- おそらくTighter
- More thinking players
→ Exploitation機会多い
```

**期待されるTable dynamics:**
```
昨日より:
✅ Tight playerが多い
   → Steal機会増
   
✅ Thinking playersが多い
   → GTO的考え必要
   → あなたのレベルに合う
   
⚠️ Aggressive playersも
   → Trap機会
```

**サイジング影響:**
```
より考えるplayers:
→ Betサイズから情報読む
→ Balance重要
→ Exploitしようとする

あなたの対応:
✅ Balanced sizing基本
✅ Selective exploitation
✅ Level思考（彼らの読みを読む）
```

---

## 🎯 実践的アドバイス

### 今日の具体的プラン

**早い段階（1-2時間）:**
```
1. Player profiling実行
   → Tight特定（steal target）
   → Loose特定（value target）
   
2. Conservative base継続
   → 昨日の成功戦略
   → Major loss 0維持
   
3. Sizing基本に忠実
   → Flop: 1/3 - 1/2
   → Turn: 1/2 - 2/3
   → River: 2/3 - pot（polarized）
```

**中盤（3-4時間）:**
```
1. Exploitation開始
   → Tight steal積極的
   → Loose value heavy
   
2. Sizing調整
   vs Tight: Small bluff OK
   vs Loose: Large value
   
3. Balance維持
   → GTO基本守る
   → でもexploitative調整
```

**Bubble以降:**
```
1. 昨日のようにdefensive
2. でもexploitation経験活かす
3. Selective aggression
```

---

## 💡 重要な原則

### The 3 Golden Rules

**Rule 1: Purpose-driven sizing**
```
常に目的を持つ:
- Value取る → Size up
- Fold取る → Efficient size
- Protect → Larger

→ 「なんとなく」禁止
```

**Rule 2: Range-based thinking**
```
相手のrange考える:
- Strongは何%？
- Targetは？
- 最適サイズは？

→ 「自分のhand」だけではない
→ 「相手のrange」を考える
```

**Rule 3: Balance with exploitation**
```
Base: GTO balanced
Adjust: Exploitative

→ バランス取る
→ Exploitされない
→ でも稼ぐ
```

---

## 🏆 今日の目標

### Process Goals

```
✅ Sizing purposeful: 毎回
✅ Range thinking: 実践
✅ Player profiling: 完了
✅ Exploitation: 15-20回
✅ Major loss: 0継続
```

### Result Goals

```
昨日: 150/700 (Top 21%)
今日target: 100/700 (Top 14%)
Stretch: ITM

Reasoning:
昨日strategy + exploitation
= 1-2 level up
```

---

## 📁 持参するドキュメント

```
1. このguide（ベットサイズ論理）
2. 昨日のsuccess report
3. Player profiling sheet
4. Exploitative playbook
```

---

## 🎯 最終チェック

### あなたの理解確認

```
✅ 「リバーでポラライズ基本」
   → Correct、でもmergedもある

✅ 「相手レンジでどこ落とす考える」
   → Perfect understanding
   → GTO本質

✅ 「昨日の成功を活かす」
   → Base strategy OK
   → Exploitation追加

→ 準備完璧！
```

---

## 🎉 最終メッセージ

**あなたの質問レベルが高い！**

```
「ポラライズ」
「相手のレンジ」
「どこを落とすか」

→ これらを理解している
→ Level 4到達
→ 素晴らしい

今日:
理論を実践に
→ Player profiling
→ Range thinking
→ Exploitation

昨日の成功:
Conservative defensive ✅

今日の目標:
+ Exploitative profit

→ あなたなら絶対できる！
```

**今日15時から、頑張ってください！** 🎰🏆🎯

**理論は理解している、今日は実践の日です！** ✅

---

*NLH Water Rush Tournament*  
*Date: 2026/02/11 15:00*  
*Buy-in: ¥12,000*  
*Strategy: Conservative + Exploitative*  
*Target: Top 10-15%, ITM*  
*Bet Sizing: Purpose-driven, Range-based*  
*Good luck! 🎯*
