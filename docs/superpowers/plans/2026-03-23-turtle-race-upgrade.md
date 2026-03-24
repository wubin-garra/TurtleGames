# Turtle Race 乌龟赛跑 游戏升级 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将现有的基础乌龟赛跑游戏升级为一个功能丰富、体验完整的网页小游戏，增加开始画面、下注金额选择、赛前倒计时、道具系统、乌龟商店/升级、音效、本地排行榜和游戏结束总结页面。

**Architecture:** 保持单 HTML 文件架构（内联 CSS + JS），通过模块化的 JS 对象管理游戏状态。使用 localStorage 持久化玩家数据和排行榜。使用 Web Audio API 生成简单音效（无需外部音频文件）。通过 CSS 类切换实现多页面/场景管理。

**Tech Stack:** Vanilla HTML/CSS/JS, Web Audio API, localStorage, CSS Animations

---

## File Structure

- **Modify:** `turtle-race.html` — 唯一文件，所有改动都在这里

当前文件结构（~400 行）：
- L1-164: `<style>` — CSS 样式
- L166-197: `<body>` — HTML 结构
- L199-396: `<script>` — JS 游戏逻辑

升级后预计 ~1200 行，按以下逻辑区块组织：
- CSS: 变量 → 通用 → 场景(start/race/shop/gameover) → 组件 → 动画
- HTML: 场景容器(scene divs) → 模态框
- JS: 音效模块 → 数据定义 → 状态管理 → 场景渲染 → 游戏逻辑 → 存储 → 初始化

---

### Task 1: 场景管理系统 — 多页面切换

**Files:**
- Modify: `turtle-race.html`

当前游戏只有一个固定页面。需要增加场景系统支持：开始画面 → 赛道 → 商店 → 游戏结束。

- [ ] **Step 1: 添加场景 CSS**

在 `<style>` 开头添加 CSS 变量和场景管理样式：

```css
:root {
  --bg-dark: #0A1628;
  --bg-panel: #0D1F3C;
  --bg-race: #0E2240;
  --bg-lane-odd: #162D50;
  --bg-lane-even: #1A3358;
  --border: #1A3A5C;
  --accent: #4EEAAC;
  --gold: #FFD700;
  --danger: #FF6B6B;
  --warn: #FFB347;
  --purple: #A78BFA;
  --text-muted: #6B8AB8;
  --text-secondary: #8BB8E8;
}

.scene { display: none; flex-direction: column; min-height: 100vh; }
.scene.active { display: flex; }
```

- [ ] **Step 2: 重构 HTML 为场景结构**

将现有 HTML body 内容包裹在 `scene-race` 中，并添加 `scene-start` 和 `scene-gameover` 容器：

```html
<body>
  <!-- 开始画面 -->
  <div class="scene active" id="scene-start">
    <div class="start-screen">
      <div class="start-logo">🐢</div>
      <h1 class="start-title">Turtle Race</h1>
      <p class="start-subtitle">乌龟赛跑</p>
      <div class="start-menu">
        <button class="menu-btn primary" onclick="startNewGame()">🏁 开始游戏</button>
        <button class="menu-btn" onclick="showScene('scene-shop')">🛒 乌龟商店</button>
        <button class="menu-btn" onclick="showScene('scene-leaderboard')">📊 排行榜</button>
      </div>
      <div class="start-highscore">最高纪录: <span id="highScore">0</span> 🪙</div>
    </div>
  </div>

  <!-- 赛道画面 (现有内容) -->
  <div class="scene" id="scene-race">
    <!-- ... 现有 top-bar, race-area, bottom-bar ... -->
  </div>

  <!-- 商店画面 -->
  <div class="scene" id="scene-shop">
    <div class="top-bar">
      <button class="back-btn" onclick="showScene('scene-start')">← 返回</button>
      <div class="logo">🛒 乌龟商店</div>
      <div class="stats"><span>🪙 <span id="shopCoins">0</span></span></div>
    </div>
    <div class="shop-area" id="shopArea"></div>
  </div>

  <!-- 排行榜画面 -->
  <div class="scene" id="scene-leaderboard">
    <div class="top-bar">
      <button class="back-btn" onclick="showScene('scene-start')">← 返回</button>
      <div class="logo">📊 排行榜</div>
      <div></div>
    </div>
    <div class="leaderboard-area" id="leaderboardArea"></div>
  </div>

  <!-- 游戏结束画面 -->
  <div class="scene" id="scene-gameover">
    <div class="gameover-screen">
      <div class="gameover-emoji" id="gameoverEmoji">🏆</div>
      <h1 class="gameover-title" id="gameoverTitle">Game Over</h1>
      <div class="gameover-stats" id="gameoverStats"></div>
      <div class="gameover-actions">
        <button class="menu-btn primary" onclick="startNewGame()">🔄 再来一局</button>
        <button class="menu-btn" onclick="showScene('scene-start')">🏠 返回主页</button>
      </div>
    </div>
  </div>

  <!-- 模态框 (保留现有) -->
  <div class="modal-overlay" id="modal">...</div>
  <div class="confetti-container" id="confetti"></div>
</body>
```

- [ ] **Step 3: 添加场景切换和基础函数 JS**

在 `<script>` 最顶部添加完整的 state 初始化和基础函数，供后续所有 Task 使用：

```javascript
// === 完整 state（所有 Task 共用，后续 Task 不再单独添加属性） ===
let state = {
  coins: 1000,
  wins: 0,
  totalWins: 0,
  round: 1,
  maxRounds: 5,
  selected: -1,
  racing: false,
  progress: [0, 0, 0, 0],
  finished: [],
  betAmount: 100,
  usedItems: [],
  unlockedTurtles: ['speedy', 'flash', 'bolt', 'slowjoe'],
  highScore: 0,
};

// === 音效占位（Task 5 替换为完整实现） ===
let muted = false;
function playSound(type) { /* 占位，Task 5 实现 */ }
function toggleMute() {
  muted = !muted;
  const btn = document.getElementById('muteBtn');
  if (btn) btn.textContent = muted ? '🔇' : '🔊';
}

// === 场景管理 ===
function showScene(sceneId) {
  document.querySelectorAll('.scene').forEach(s => s.classList.remove('active'));
  document.getElementById(sceneId).classList.add('active');
  if (sceneId === 'scene-leaderboard') renderLeaderboard();
  if (sceneId === 'scene-shop') renderShop();
}

// === 基础游戏流程（后续 Task 会扩展这些函数） ===
function startNewGame() {
  state.round = 1;
  state.wins = 0;
  state.selected = -1;
  state.progress = [0, 0, 0, 0];
  state.finished = [];
  state.betAmount = 100;
  state.usedItems = [];
  showScene('scene-race');
  document.getElementById('raceTitle').textContent = '🏁 Choose Your Turtle & Start Racing!';
  render();
}

// 占位函数（后续 Task 实现）
function renderShop() {}
function renderLeaderboard() {}
```

> **注意:** 此 Step 引入了完整的 state 对象、playSound 占位、startNewGame、showScene 和渲染占位函数。后续 Task 直接使用或替换这些函数，不再需要单独向 state 添加属性。

- [ ] **Step 4: 验证场景切换**

在浏览器中打开文件，确认：
- 初始显示开始画面
- 点击"开始游戏"切换到赛道画面
- 点击"返回"能回到开始画面

- [ ] **Step 5: Commit**

```bash
git add turtle-race.html
git commit -m "feat: add scene management system with start/race/shop/gameover screens"
```

---

### Task 2: 开始画面 UI 样式

**Files:**
- Modify: `turtle-race.html` (CSS section)

- [ ] **Step 1: 添加开始画面 CSS**

```css
.start-screen {
  flex: 1; display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  background: radial-gradient(ellipse at 50% 30%, #0E2240 0%, #0A1628 70%);
  gap: 8px;
}
.start-logo {
  font-size: 96px; animation: turtleBounce 2s ease-in-out infinite;
}
@keyframes turtleBounce {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  25% { transform: translateY(-15px) rotate(-5deg); }
  75% { transform: translateY(-5px) rotate(5deg); }
}
.start-title {
  font-size: 56px; font-weight: 900; color: var(--accent);
  text-shadow: 0 0 40px rgba(78,234,172,0.3);
}
.start-subtitle {
  font-size: 20px; color: var(--text-secondary); margin-bottom: 32px;
}
.start-menu { display: flex; flex-direction: column; gap: 14px; width: 280px; }
.menu-btn {
  border: none; border-radius: 14px; padding: 16px 32px;
  font-size: 18px; font-weight: 700; cursor: pointer;
  background: var(--bg-panel); color: var(--text-secondary);
  border: 2px solid var(--border); transition: all 0.2s;
}
.menu-btn:hover { border-color: var(--accent); color: #fff; transform: translateY(-2px); }
.menu-btn.primary {
  background: linear-gradient(to bottom, var(--accent), #2BC48A);
  color: var(--bg-dark); border-color: transparent;
}
.menu-btn.primary:hover { box-shadow: 0 4px 20px rgba(78,234,172,0.4); }
.start-highscore {
  margin-top: 24px; font-size: 15px; color: var(--text-muted);
}
.back-btn {
  background: none; border: 1px solid var(--border); border-radius: 8px;
  padding: 8px 16px; color: var(--text-secondary); cursor: pointer;
  font-size: 14px; transition: all 0.2s;
}
.back-btn:hover { border-color: var(--accent); color: #fff; }
```

- [ ] **Step 2: 在浏览器中验证开始画面**

确认乌龟 emoji 有弹跳动画，按钮排列正确，hover 效果正常。

- [ ] **Step 3: Commit**

```bash
git add turtle-race.html
git commit -m "feat: style start screen with animated turtle logo"
```

---

### Task 3: 下注金额选择

**Files:**
- Modify: `turtle-race.html` (HTML bottom-bar + JS)

当前固定下注 100 金币。改为玩家可选择 50 / 100 / 200 / 500 四档。

- [ ] **Step 1: 添加下注选择器 HTML 和 CSS**

在 bottom-bar 中的 pick-label 前面添加下注选择区域：

```html
<div class="bet-selector">
  <span class="pick-label">下注:</span>
  <div id="betBtns" class="bet-btns"></div>
</div>
```

```css
.bet-selector { display: flex; align-items: center; gap: 8px; }
.bet-btns { display: flex; gap: 6px; }
.bet-btn {
  border: 2px solid var(--border); border-radius: 10px; padding: 8px 14px;
  font-size: 14px; font-weight: 700; cursor: pointer;
  background: var(--bg-dark); color: var(--gold); transition: all 0.15s;
}
.bet-btn:hover { border-color: var(--gold); }
.bet-btn.active { border-color: var(--gold); background: rgba(255,215,0,0.15); }
.bet-btn:disabled { opacity: 0.4; cursor: not-allowed; }
```

- [ ] **Step 2: 添加下注逻辑 JS**

```javascript
const BET_OPTIONS = [50, 100, 200, 500];

// 在 state 中添加
// betAmount: 100,

function renderBetBtns() {
  const container = document.getElementById('betBtns');
  container.innerHTML = '';
  BET_OPTIONS.forEach(amt => {
    const btn = document.createElement('button');
    btn.className = 'bet-btn' + (state.betAmount === amt ? ' active' : '');
    btn.textContent = '🪙' + amt;
    btn.disabled = state.racing || state.coins < amt;
    btn.onclick = () => { state.betAmount = amt; render(); };
    container.appendChild(btn);
  });
}
```

- [ ] **Step 3: 修改 startRace 和 finishRace 使用 betAmount**

```javascript
// startRace 中: state.coins -= state.betAmount;  (先扣除下注金额)
// finishRace 中: state.coins += state.betAmount * 4;  (赢时返还 4 倍，净赚 3 倍)
// modalReward 显示净收益: won ? `+${state.betAmount * 3} coins!` : `-${state.betAmount} coins`
// 说明: 扣 100 + 返 400 = 净赚 300，显示 +300 是正确的
```

- [ ] **Step 4: 在 render() 中调用 renderBetBtns()**

- [ ] **Step 5: 验证下注功能**

- 选择不同金额，确认扣费和奖励正确
- 金币不足时对应按钮置灰
- 比赛中按钮不可点击

- [ ] **Step 6: Commit**

```bash
git add turtle-race.html
git commit -m "feat: add variable bet amount selector (50/100/200/500)"
```

---

### Task 4: 赛前倒计时动画

**Files:**
- Modify: `turtle-race.html`

点击 START RACE 后，不直接开始，先显示 3-2-1-GO! 倒计时。

- [ ] **Step 1: 添加倒计时 CSS**

```css
.countdown-overlay {
  position: fixed; inset: 0; display: flex;
  align-items: center; justify-content: center;
  background: rgba(10,22,40,0.85); z-index: 50;
  backdrop-filter: blur(4px);
}
.countdown-text {
  font-size: 120px; font-weight: 900; color: var(--gold);
  text-shadow: 0 0 60px rgba(255,215,0,0.5);
  animation: countPop 0.8s ease;
}
@keyframes countPop {
  0% { transform: scale(2); opacity: 0; }
  50% { transform: scale(1.1); opacity: 1; }
  100% { transform: scale(1); opacity: 1; }
}
```

- [ ] **Step 2: 添加倒计时 JS**

```javascript
function startCountdown(callback) {
  const overlay = document.createElement('div');
  overlay.className = 'countdown-overlay';
  document.body.appendChild(overlay);

  const nums = ['3', '2', '1', '🏁 GO!'];
  let i = 0;

  function showNext() {
    if (i >= nums.length) {
      overlay.remove();
      callback();
      return;
    }
    overlay.innerHTML = `<div class="countdown-text">${nums[i]}</div>`;
    playSound(i < 3 ? 'tick' : 'go');
    i++;
    setTimeout(showNext, 800);
  }
  showNext();
}
```

- [ ] **Step 3: 修改 startRace 使用倒计时**

```javascript
function startRace() {
  if (state.selected < 0 || state.racing) return;
  state.coins -= state.betAmount;
  state.racing = true;
  render();
  startCountdown(() => {
    // 原有的比赛动画逻辑移到这里
    beginRaceAnimation();
  });
}
```

- [ ] **Step 4: 验证倒计时**

确认 3→2→1→GO! 依次显示，每次有缩放动画，GO! 后比赛开始。

- [ ] **Step 5: Commit**

```bash
git add turtle-race.html
git commit -m "feat: add 3-2-1-GO countdown before race starts"
```

---

### Task 5: 音效系统 (Web Audio API)

**Files:**
- Modify: `turtle-race.html`

使用 Web Audio API 生成简单的合成音效，不依赖外部文件。

- [ ] **Step 1: 替换 playSound 占位为完整音效模块**

替换 Task 1 中的 `playSound` 占位函数为完整实现。在 `playSound` 函数开头添加 `if (muted) return;`：

```javascript
const AudioCtx = window.AudioContext || window.webkitAudioContext;
let audioCtx = null;

function ensureAudio() {
  if (!audioCtx) audioCtx = new AudioCtx();
}

function playSound(type) {
  try {
    ensureAudio();
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.connect(gain);
    gain.connect(audioCtx.destination);

    const now = audioCtx.currentTime;
    switch (type) {
      case 'tick':
        osc.frequency.value = 600;
        gain.gain.setValueAtTime(0.3, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.15);
        osc.start(now); osc.stop(now + 0.15);
        break;
      case 'go':
        osc.frequency.value = 900;
        gain.gain.setValueAtTime(0.4, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.3);
        osc.start(now); osc.stop(now + 0.3);
        break;
      case 'win':
        osc.frequency.setValueAtTime(523, now);
        osc.frequency.setValueAtTime(659, now + 0.15);
        osc.frequency.setValueAtTime(784, now + 0.3);
        gain.gain.setValueAtTime(0.3, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.5);
        osc.start(now); osc.stop(now + 0.5);
        break;
      case 'lose':
        osc.frequency.setValueAtTime(400, now);
        osc.frequency.setValueAtTime(300, now + 0.2);
        gain.gain.setValueAtTime(0.3, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.4);
        osc.start(now); osc.stop(now + 0.4);
        break;
      case 'select':
        osc.frequency.value = 700;
        osc.type = 'sine';
        gain.gain.setValueAtTime(0.15, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.1);
        osc.start(now); osc.stop(now + 0.1);
        break;
      case 'coin':
        osc.frequency.setValueAtTime(1200, now);
        osc.frequency.setValueAtTime(1600, now + 0.05);
        osc.type = 'sine';
        gain.gain.setValueAtTime(0.2, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.2);
        osc.start(now); osc.stop(now + 0.2);
        break;
    }
  } catch (e) { /* 静默失败，音效非关键功能 */ }
}
```

- [ ] **Step 2: 在关键交互处调用 playSound**

```javascript
// selectTurtle: playSound('select')
// startRace 扣费后: playSound('coin')
// finishRace 赢: playSound('win')
// finishRace 输: playSound('lose')
// 倒计时 tick/go: 已在 Task 4 添加
```

- [ ] **Step 3: 添加音量开关**

在 top-bar 右侧添加静音按钮：

```html
<button class="mute-btn" id="muteBtn" onclick="toggleMute()">🔊</button>
```

```javascript
let muted = false;
function toggleMute() {
  muted = !muted;
  document.getElementById('muteBtn').textContent = muted ? '🔇' : '🔊';
}
// 在 playSound 开头添加: if (muted) return;
```

- [ ] **Step 4: 验证音效**

- 选择乌龟时有清脆的 "叮"
- 倒计时有节拍声
- 胜利有上升音阶，失败有下降音

- [ ] **Step 5: Commit**

```bash
git add turtle-race.html
git commit -m "feat: add synthesized sound effects via Web Audio API"
```

---

### Task 6: 道具系统 — 加速 & 减速

**Files:**
- Modify: `turtle-race.html`

每轮比赛开始前，玩家可以购买道具卡：
- ⚡ 加速卡（150 金币）— 给选中的乌龟额外 +20% 速度
- 🌀 减速卡（200 金币）— 随机一只对手乌龟 -20% 速度
- 🍀 幸运卡（100 金币）— 增加自己乌龟的运气范围

- [ ] **Step 1: 添加道具区 HTML 和 CSS**

在 bottom-bar 中 START RACE 按钮左边添加道具按钮区：

```css
.items-bar { display: flex; gap: 8px; align-items: center; }
.item-btn {
  border: 2px solid var(--border); border-radius: 10px; padding: 8px 12px;
  font-size: 13px; font-weight: 600; cursor: pointer;
  background: var(--bg-dark); color: #fff; transition: all 0.15s;
  position: relative;
}
.item-btn:hover { border-color: var(--accent); }
.item-btn.used { opacity: 0.4; border-color: transparent; }
.item-btn .item-cost { font-size: 11px; color: var(--gold); }
```

- [ ] **Step 2: 添加道具逻辑 JS**

```javascript
const ITEMS = [
  { id: 'boost', emoji: '⚡', name: '加速卡', cost: 150, desc: '你的乌龟 +20% 速度' },
  { id: 'slow', emoji: '🌀', name: '减速卡', cost: 200, desc: '随机对手 -20% 速度' },
  { id: 'lucky', emoji: '🍀', name: '幸运卡', cost: 100, desc: '增大运气范围' },
];

// state 中添加: usedItems: []

function buyItem(itemId) {
  const item = ITEMS.find(i => i.id === itemId);
  if (!item || state.coins < item.cost || state.usedItems.includes(itemId)) return;
  state.coins -= item.cost;
  state.usedItems.push(itemId);
  playSound('coin');
  render();
}
```

- [ ] **Step 3: 在 beginRaceAnimation 中应用道具效果**

```javascript
// 计算 speeds 时:
// if usedItems includes 'boost': speeds[selected] *= 1.2
// if usedItems includes 'slow': 随机选一个非 selected 的 speeds[x] *= 0.8
// if usedItems includes 'lucky': luck 范围从 0.6-1.4 扩大到 0.4-1.6
```

- [ ] **Step 4: 每轮结束后重置 usedItems**

```javascript
// nextRound 中: state.usedItems = [];
```

- [ ] **Step 5: 验证道具功能**

- 购买后金币减少，按钮变灰
- 加速效果肉眼可见
- 金币不够时按钮不可点

- [ ] **Step 6: Commit**

```bash
git add turtle-race.html
git commit -m "feat: add item system with boost, slow, and lucky cards"
```

---

### Task 7: 乌龟商店 — 解锁新乌龟

**Files:**
- Modify: `turtle-race.html`

允许玩家用金币解锁额外乌龟角色（持久化到 localStorage）。

- [ ] **Step 1: 扩展乌龟数据**

```javascript
const ALL_TURTLES = [
  { id: 'speedy', name: 'Speedy', speed: 85, color: '#4EEAAC', gradient: '...', cost: 0, unlocked: true },
  { id: 'flash', name: 'Flash', speed: 78, color: '#FF6B6B', gradient: '...', cost: 0, unlocked: true },
  { id: 'bolt', name: 'Bolt', speed: 72, color: '#FFB347', gradient: '...', cost: 0, unlocked: true },
  { id: 'slowjoe', name: 'Slow Joe', speed: 65, color: '#A78BFA', gradient: '...', cost: 0, unlocked: true },
  { id: 'ninja', name: 'Ninja', speed: 90, color: '#E879F9', gradient: 'linear-gradient(to right, #E879F9, #C850C0)', cost: 500, unlocked: false },
  { id: 'rocket', name: 'Rocket', speed: 95, color: '#F97316', gradient: 'linear-gradient(to right, #F97316, #DC2626)', cost: 1000, unlocked: false },
  { id: 'ghost', name: 'Ghost', speed: 70, color: '#94A3B8', gradient: 'linear-gradient(to right, #94A3B8, #64748B)', cost: 300, unlocked: false },
  { id: 'golden', name: 'Golden', speed: 88, color: '#FACC15', gradient: 'linear-gradient(to right, #FACC15, #EAB308)', cost: 2000, unlocked: false },
];
```

- [ ] **Step 2: 添加商店渲染 CSS 和 JS**

```css
.shop-area {
  flex: 1; display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 16px; padding: 24px 32px; background: var(--bg-race);
}
.shop-card {
  background: var(--bg-lane-odd); border-radius: 16px; padding: 24px;
  display: flex; flex-direction: column; align-items: center; gap: 12px;
  border: 2px solid transparent; transition: all 0.2s;
}
.shop-card:hover { border-color: var(--accent); }
.shop-card.locked { opacity: 0.7; }
.shop-card .turtle-preview { font-size: 48px; }
.shop-card .turtle-stat { font-size: 14px; color: var(--text-muted); }
.shop-buy-btn {
  border: none; border-radius: 10px; padding: 10px 24px;
  font-size: 15px; font-weight: 700; cursor: pointer; transition: all 0.15s;
}
```

```javascript
function renderShop() {
  const area = document.getElementById('shopArea');
  document.getElementById('shopCoins').textContent = state.coins.toLocaleString();
  area.innerHTML = '';
  ALL_TURTLES.forEach(t => {
    const unlocked = state.unlockedTurtles.includes(t.id);
    const card = document.createElement('div');
    card.className = 'shop-card' + (unlocked ? '' : ' locked');
    card.innerHTML = `
      <div class="turtle-preview">🐢</div>
      <div class="turtle-name" style="color:${t.color}">${t.name}</div>
      <div class="turtle-stat">Speed ⚡ ${t.speed}</div>
      ${unlocked
        ? '<div style="color:var(--accent);font-weight:700">✓ 已解锁</div>'
        : `<button class="shop-buy-btn" style="background:${t.color};color:#0A1628"
            onclick="buyTurtle('${t.id}')" ${state.coins < t.cost ? 'disabled' : ''}>
            🪙 ${t.cost} 解锁</button>`}
    `;
    area.appendChild(card);
  });
}
```

- [ ] **Step 3: 添加购买逻辑**

```javascript
function buyTurtle(id) {
  const t = ALL_TURTLES.find(x => x.id === id);
  if (!t || state.coins < t.cost || state.unlockedTurtles.includes(id)) return;
  state.coins -= t.cost;
  state.unlockedTurtles.push(id);
  playSound('coin');
  saveGame();
  renderShop();
}
```

- [ ] **Step 4: 比赛时从已解锁乌龟中随机选 4 只作为参赛者**

引入 `raceTurtles` 变量存储当前比赛的参赛乌龟。后续所有引用当前比赛乌龟的地方（render、startRace、race events 等）都使用 `raceTurtles` 而非原来的 `turtles` 常量。

```javascript
let raceTurtles = []; // 当前比赛的 4 只乌龟

function pickRaceTurtles() {
  const pool = ALL_TURTLES.filter(t => state.unlockedTurtles.includes(t.id));
  const shuffled = [...pool].sort(() => Math.random() - 0.5);
  raceTurtles = shuffled.slice(0, Math.min(4, shuffled.length));
}

// 在 startNewGame() 和每轮 nextRound() 中调用 pickRaceTurtles()
// 将 render()、startRace()、finishRace() 中所有 `turtles` 引用改为 `raceTurtles`
// 删除原来的 const turtles = [...] 硬编码数组
```

> **重要:** 这是一个重构步骤。必须全局搜索 `turtles` 并替换为 `raceTurtles`（排除 `ALL_TURTLES`）。

- [ ] **Step 5: 验证商店**

- 已解锁乌龟显示 ✓
- 购买后金币扣除，立即显示已解锁
- 金币不够按钮禁用

- [ ] **Step 6: Commit**

```bash
git add turtle-race.html
git commit -m "feat: add turtle shop with unlockable characters"
```

---

### Task 8: localStorage 持久化

**Files:**
- Modify: `turtle-race.html`

保存玩家金币、已解锁乌龟、最高分到 localStorage。

- [ ] **Step 1: 添加存储函数**

```javascript
const SAVE_KEY = 'turtle-race-save';

function saveGame() {
  const data = {
    coins: state.coins,
    totalWins: state.totalWins,
    unlockedTurtles: state.unlockedTurtles,
    highScore: state.highScore,
  };
  localStorage.setItem(SAVE_KEY, JSON.stringify(data));
}

function loadGame() {
  try {
    const raw = localStorage.getItem(SAVE_KEY);
    if (!raw) return;
    const data = JSON.parse(raw);
    state.coins = data.coins ?? 1000;
    state.totalWins = data.totalWins ?? 0;
    state.unlockedTurtles = data.unlockedTurtles ?? ['speedy','flash','bolt','slowjoe'];
    state.highScore = data.highScore ?? 0;
  } catch (e) { /* 忽略损坏的存档 */ }
}
```

- [ ] **Step 2: 在关键节点调用 saveGame**

```javascript
// finishRace 结束后: saveGame()
// buyTurtle 后: saveGame()
// nextRound 结束后: saveGame()
```

- [ ] **Step 3: 初始化时调用 loadGame**

```javascript
// 在文件末尾的初始化代码中:
loadGame();
document.getElementById('highScore').textContent = state.highScore;
render();
```

- [ ] **Step 4: 验证持久化**

- 刷新页面后金币、解锁状态保留
- 开始画面显示最高纪录

- [ ] **Step 5: Commit**

```bash
git add turtle-race.html
git commit -m "feat: persist player data to localStorage"
```

---

### Task 9: 排行榜

**Files:**
- Modify: `turtle-race.html`

每局游戏结束后记录得分，显示历史前 10 名。

- [ ] **Step 1: 添加排行榜 CSS**

```css
.leaderboard-area {
  flex: 1; padding: 24px 32px; background: var(--bg-race);
  display: flex; flex-direction: column; align-items: center;
}
.leaderboard-list {
  width: 100%; max-width: 500px; display: flex;
  flex-direction: column; gap: 8px;
}
.lb-row {
  display: flex; align-items: center; gap: 16px;
  padding: 14px 20px; border-radius: 12px; background: var(--bg-lane-odd);
}
.lb-rank { font-size: 18px; font-weight: 800; width: 36px; text-align: center; }
.lb-score { margin-left: auto; font-weight: 700; color: var(--gold); }
.lb-date { font-size: 12px; color: var(--text-muted); }
```

- [ ] **Step 2: 添加排行榜逻辑**

```javascript
const LB_KEY = 'turtle-race-leaderboard';

function addLeaderboardEntry(coins, wins, rounds) {
  const entries = JSON.parse(localStorage.getItem(LB_KEY) || '[]');
  entries.push({ coins, wins, rounds, date: new Date().toLocaleDateString('zh-CN') });
  entries.sort((a, b) => b.coins - a.coins);
  localStorage.setItem(LB_KEY, JSON.stringify(entries.slice(0, 10)));
}

function renderLeaderboard() {
  const area = document.getElementById('leaderboardArea');
  const entries = JSON.parse(localStorage.getItem(LB_KEY) || '[]');
  area.innerHTML = entries.length === 0
    ? '<p style="color:var(--text-muted);margin-top:40px">暂无记录，先去比赛吧!</p>'
    : '<div class="leaderboard-list">' + entries.map((e, i) =>
        `<div class="lb-row">
          <div class="lb-rank" style="color:${rankColors[i] || '#fff'}">#${i+1}</div>
          <div>
            <div style="font-weight:600">🪙 ${e.coins} coins</div>
            <div class="lb-date">${e.date} · ${e.wins} wins / ${e.rounds} rounds</div>
          </div>
        </div>`
      ).join('') + '</div>';
}
```

- [ ] **Step 3: 游戏结束时记录**

```javascript
// 在 showGameOver 中调用:
addLeaderboardEntry(state.coins, state.wins, state.round);
```

- [ ] **Step 4: 场景切换到排行榜时渲染**

```javascript
// showScene 中添加:
if (sceneId === 'scene-leaderboard') renderLeaderboard();
if (sceneId === 'scene-shop') renderShop();
```

- [ ] **Step 5: 验证排行榜**

- 完成游戏后排行榜有新记录
- 按金币降序排列
- 最多显示 10 条

- [ ] **Step 6: Commit**

```bash
git add turtle-race.html
git commit -m "feat: add local leaderboard with top 10 scores"
```

---

### Task 10: 游戏结束总结页面

**Files:**
- Modify: `turtle-race.html`

用精美的总结页面替代现在的 `alert()`。

- [ ] **Step 1: 添加游戏结束页 CSS**

```css
.gameover-screen {
  flex: 1; display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  background: radial-gradient(ellipse at 50% 40%, #0E2240 0%, #0A1628 70%);
  gap: 16px;
}
.gameover-emoji { font-size: 80px; animation: turtleBounce 2s ease-in-out infinite; }
.gameover-title { font-size: 42px; font-weight: 900; color: var(--accent); }
.gameover-stats {
  display: grid; grid-template-columns: 1fr 1fr; gap: 16px;
  margin: 24px 0; width: 360px;
}
.stat-card {
  background: var(--bg-panel); border-radius: 14px; padding: 20px;
  text-align: center; border: 1px solid var(--border);
}
.stat-card .stat-value { font-size: 28px; font-weight: 800; color: var(--gold); }
.stat-card .stat-label { font-size: 13px; color: var(--text-muted); margin-top: 4px; }
.gameover-actions { display: flex; gap: 14px; margin-top: 8px; }
```

- [ ] **Step 2: 替换 alert 为 showGameOver**

```javascript
function showGameOver() {
  // 更新最高分
  if (state.coins > state.highScore) {
    state.highScore = state.coins;
  }
  saveGame();
  addLeaderboardEntry(state.coins, state.wins, state.maxRounds);

  document.getElementById('gameoverEmoji').textContent = state.wins >= 3 ? '🏆' : '🐢';
  document.getElementById('gameoverTitle').textContent =
    state.wins >= 3 ? '太厉害了!' : state.wins > 0 ? '不错的比赛!' : '再接再厉!';

  document.getElementById('gameoverStats').innerHTML = `
    <div class="stat-card"><div class="stat-value">🪙 ${state.coins}</div><div class="stat-label">最终金币</div></div>
    <div class="stat-card"><div class="stat-value">🏆 ${state.wins}</div><div class="stat-label">胜利场次</div></div>
    <div class="stat-card"><div class="stat-value">${state.maxRounds}</div><div class="stat-label">总轮次</div></div>
    <div class="stat-card"><div class="stat-value">${state.highScore}</div><div class="stat-label">历史最高</div></div>
  `;

  if (state.wins >= 3) showConfetti();
  showScene('scene-gameover');
}
```

- [ ] **Step 3: 在 nextRound 中调用 showGameOver 替代 alert**

```javascript
// nextRound 中:
if (state.round >= state.maxRounds) {
  showGameOver();
  return;
}
```

- [ ] **Step 4: 验证游戏结束页**

- 5 轮结束后显示总结页
- 统计数据正确
- "再来一局"和"返回主页"按钮正常工作

- [ ] **Step 5: Commit**

```bash
git add turtle-race.html
git commit -m "feat: add polished game over summary screen"
```

---

### Task 11: 赛道动态事件

**Files:**
- Modify: `turtle-race.html`

比赛中随机触发事件，增加趣味性：
- 🌊 海浪：随机一只乌龟被减速 2 秒
- 💨 顺风：随机一只乌龟临时加速
- 🪨 石头：最前面的乌龟短暂停顿

- [ ] **Step 1: 添加事件提示 CSS**

```css
.race-event {
  position: fixed; top: 80px; left: 50%; transform: translateX(-50%);
  background: rgba(13,31,60,0.95); border: 2px solid var(--gold);
  border-radius: 14px; padding: 12px 28px; font-size: 18px;
  font-weight: 700; z-index: 60; animation: eventSlide 0.3s ease;
  white-space: nowrap;
}
@keyframes eventSlide {
  from { transform: translateX(-50%) translateY(-20px); opacity: 0; }
  to { transform: translateX(-50%) translateY(0); opacity: 1; }
}
```

- [ ] **Step 2: 添加事件逻辑**

```javascript
const RACE_EVENTS = [
  { emoji: '🌊', text: '海浪来袭！{name} 被减速了!', effect: 'slow_random' },
  { emoji: '💨', text: '顺风！{name} 加速前进!', effect: 'boost_random' },
  { emoji: '🪨', text: '前方落石！{name} 紧急刹车!', effect: 'slow_leader' },
];

function triggerRaceEvent(speeds) {
  const evt = RACE_EVENTS[Math.floor(Math.random() * RACE_EVENTS.length)];
  let targetIdx;

  if (evt.effect === 'slow_leader') {
    targetIdx = state.progress.indexOf(Math.max(...state.progress));
  } else {
    targetIdx = Math.floor(Math.random() * 4);
  }

  const multiplier = evt.effect.startsWith('boost') ? 1.5 : 0.5;
  const originalSpeed = speeds[targetIdx];
  speeds[targetIdx] *= multiplier;

  // 2 秒后恢复
  setTimeout(() => { speeds[targetIdx] = originalSpeed; }, 2000);

  // 显示事件
  const div = document.createElement('div');
  div.className = 'race-event';
  div.textContent = evt.emoji + ' ' + evt.text.replace('{name}', raceTurtles[targetIdx]?.name || '乌龟');
  document.body.appendChild(div);
  setTimeout(() => div.remove(), 2500);
}
```

- [ ] **Step 3: 在 tick 中随机触发事件**

```javascript
// 在 tick() 中，比赛进行到 30%-70% 时，有小概率触发:
// if (avgProgress > 30 && avgProgress < 70 && Math.random() < 0.003) triggerRaceEvent(speeds);
```

- [ ] **Step 4: 验证事件系统**

- 比赛中偶尔弹出事件提示
- 效果确实影响了对应乌龟的速度
- 提示自动消失

- [ ] **Step 5: Commit**

```bash
git add turtle-race.html
git commit -m "feat: add random race events (waves, wind, rocks)"
```

---

### Task 12: 最终整合与润色

**Files:**
- Modify: `turtle-race.html`

- [ ] **Step 1: 替换所有硬编码颜色为 CSS 变量**

遍历现有 CSS，将重复的颜色值替换为 `:root` 中定义的变量。

- [ ] **Step 2: 验证 state 和 startNewGame**

确认 Task 1 Step 3 中定义的完整 state 和 startNewGame 函数包含了所有 Task 引入的属性。此时应已包含: coins, wins, totalWins, round, maxRounds, selected, racing, progress, finished, betAmount, usedItems, unlockedTurtles, highScore。如有遗漏，在此补充。

- [ ] **Step 4: 添加移动端适配 CSS**

```css
@media (max-width: 768px) {
  .top-bar { padding: 0 16px; height: 56px; }
  .logo { font-size: 20px; }
  .stats { font-size: 14px; gap: 12px; }
  .race-area { padding: 12px 16px; }
  .lane { padding: 10px 12px; gap: 8px; min-height: 56px; }
  .turtle-emoji { font-size: 26px; }
  .turtle-info { width: 70px; }
  .turtle-name { font-size: 13px; }
  .bottom-bar { gap: 8px; padding: 12px 16px; }
  .pick-btn { padding: 8px 12px; font-size: 13px; }
  .start-btn { padding: 10px 20px; font-size: 15px; }
  .start-title { font-size: 36px; }
  .start-logo { font-size: 64px; }
}
```

- [ ] **Step 5: 全面测试**

在浏览器中完整跑一遍游戏流程：
1. 开始画面 → 点击开始
2. 选择乌龟 → 调整下注 → 购买道具 → 开始比赛
3. 倒计时 → 比赛动画 → 随机事件 → 结果弹窗
4. 重复 5 轮 → 游戏结束总结
5. 查看排行榜 → 进入商店 → 购买乌龟
6. 刷新页面验证持久化
7. 缩小窗口验证移动端适配

- [ ] **Step 6: Commit**

```bash
git add turtle-race.html
git commit -m "feat: final polish - CSS variables, mobile responsive, state cleanup"
```
