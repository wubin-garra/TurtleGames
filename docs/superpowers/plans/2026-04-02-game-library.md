# Game Library Homepage Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a PS5-style game library homepage (`index.html`) that showcases Garra's turtle games with a hero display area and bottom game selector.

**Architecture:** Single HTML file with inline CSS and JS. Game data stored in a JS array for easy extension. PS5 deep-blue color scheme with ambient particles, glow effects, and smooth transitions between games.

**Tech Stack:** Pure HTML/CSS/JS, no dependencies

---

### Task 1: Page Structure & Top Bar

**Files:**
- Create: `index.html`

- [ ] **Step 1: Create index.html with full page structure and top bar**

Create `index.html` with:
- DOCTYPE, html lang="zh-CN", meta viewport
- CSS variables for PS5 color palette
- Full-screen `.game-library` container (100vw x 100vh, flex column)
- Top bar (56px): logo `🎮 GARRA`, nav links (游戏库 active, 最近游玩), clock HH:MM, avatar circle "G"
- Empty hero section placeholder
- Empty selector bar placeholder

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>🎮 Garra's Game Library</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  :root {
    --ps-blue: #0070d8;
    --ps-light: #00b4d8;
    --bg-top: #0a1628;
    --bg-mid: #060e1a;
    --bg-bot: #000;
    --text-desc: #6688aa;
    --text-muted: #556;
  }
  html, body { width: 100%; height: 100%; overflow: hidden; }
  body { font-family: -apple-system, 'Segoe UI', 'Noto Sans SC', sans-serif; background: #000; color: #fff; }

  .game-library {
    width: 100vw; height: 100vh;
    display: flex; flex-direction: column;
    background: linear-gradient(180deg, var(--bg-top) 0%, var(--bg-mid) 50%, var(--bg-bot) 100%);
    position: relative; overflow: hidden;
  }

  /* Ambient particles */
  .game-library::before {
    content: ''; position: absolute; inset: 0; pointer-events: none; z-index: 0;
    background:
      radial-gradient(2px 2px at 15% 20%, rgba(0,112,216,0.25) 50%, transparent 50%),
      radial-gradient(2px 2px at 35% 65%, rgba(0,180,216,0.15) 50%, transparent 50%),
      radial-gradient(1.5px 1.5px at 55% 12%, rgba(255,255,255,0.15) 50%, transparent 50%),
      radial-gradient(2px 2px at 75% 80%, rgba(0,112,216,0.2) 50%, transparent 50%),
      radial-gradient(1.5px 1.5px at 90% 35%, rgba(255,255,255,0.1) 50%, transparent 50%),
      radial-gradient(2px 2px at 25% 85%, rgba(0,180,216,0.15) 50%, transparent 50%),
      radial-gradient(1px 1px at 65% 45%, rgba(255,255,255,0.12) 50%, transparent 50%);
    animation: float 30s linear infinite;
  }
  @keyframes float { 0% { transform: translateY(0); } 100% { transform: translateY(-20px); } }

  /* Top bar */
  .top-bar {
    height: 56px; display: flex; align-items: center; justify-content: space-between;
    padding: 0 40px; z-index: 10; flex-shrink: 0;
  }
  .top-bar-left { display: flex; align-items: center; gap: 24px; }
  .top-bar-logo { font-size: 15px; font-weight: 700; letter-spacing: 1px; }
  .top-bar-nav { display: flex; gap: 20px; }
  .top-bar-nav span { font-size: 13px; color: var(--text-muted); cursor: pointer; padding: 4px 0; }
  .top-bar-nav span.active { color: #fff; border-bottom: 2px solid var(--ps-blue); }
  .top-bar-right { display: flex; align-items: center; gap: 16px; }
  .top-bar-time { font-size: 13px; color: var(--text-muted); }
  .top-bar-avatar {
    width: 32px; height: 32px; border-radius: 50%;
    background: linear-gradient(135deg, var(--ps-blue), var(--ps-light));
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; font-weight: 700;
  }
</style>
</head>
<body>
<div class="game-library">
  <div class="top-bar">
    <div class="top-bar-left">
      <div class="top-bar-logo">🎮 GARRA</div>
      <div class="top-bar-nav">
        <span class="active">游戏库</span>
        <span>最近游玩</span>
      </div>
    </div>
    <div class="top-bar-right">
      <span class="top-bar-time" id="clock"></span>
      <div class="top-bar-avatar">G</div>
    </div>
  </div>

  <!-- Hero and selector added in next tasks -->
</div>
</body>
</html>
```

- [ ] **Step 2: Open in browser and verify top bar renders**

Open `index.html` in browser. Verify: dark blue gradient background, top bar with logo/nav/clock/avatar, ambient particles floating.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "feat: add game library page structure with top bar and ambient particles"
```

---

### Task 2: Hero Area

**Files:**
- Modify: `index.html`

- [ ] **Step 1: Add hero CSS**

Add after the top-bar CSS in `<style>`:

```css
/* Hero area */
.hero {
  flex: 1; display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  position: relative; z-index: 1; min-height: 0; padding-bottom: 20px;
}
.hero-glow {
  position: absolute; width: 600px; height: 400px; border-radius: 50%;
  filter: blur(100px); opacity: 0.15; pointer-events: none;
  transition: background 0.8s ease;
}
.hero-icon {
  font-size: 80px; margin-bottom: 12px; position: relative; z-index: 1;
  filter: drop-shadow(0 0 30px rgba(0,112,216,0.3));
  transition: all 0.5s ease;
}
.hero-title {
  font-size: 42px; font-weight: 900; letter-spacing: 2px;
  margin-bottom: 8px; z-index: 1;
}
.hero-desc {
  font-size: 15px; color: var(--text-desc); margin-bottom: 16px; z-index: 1;
}
.hero-tags { display: flex; gap: 10px; margin-bottom: 28px; z-index: 1; }
.hero-tag {
  padding: 4px 14px; border-radius: 20px; font-size: 12px; font-weight: 500;
  background: rgba(0,112,216,0.15); color: #4499cc;
  border: 1px solid rgba(0,112,216,0.2);
}
.play-btn {
  padding: 14px 48px; border: none; border-radius: 12px;
  font-size: 17px; font-weight: 700; font-family: inherit; cursor: pointer;
  z-index: 1; color: #fff; letter-spacing: 1px;
  background: linear-gradient(135deg, var(--ps-blue), #0090e8);
  box-shadow: 0 4px 24px rgba(0,112,216,0.3);
  transition: all 0.3s;
}
.play-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(0,112,216,0.4);
}
```

- [ ] **Step 2: Add hero HTML**

Add inside `.game-library`, after the top-bar div:

```html
<div class="hero" id="hero">
  <div class="hero-glow" id="heroGlow" style="background: #0070d8;"></div>
  <div class="hero-icon" id="heroIcon">🏁</div>
  <div class="hero-title" id="heroTitle">乌龟赛跑</div>
  <div class="hero-desc" id="heroDesc">装备你的乌龟，征战排位赛，成为赛道之王</div>
  <div class="hero-tags" id="heroTags">
    <span class="hero-tag">🏁 竞速</span>
    <span class="hero-tag">⚔️ 排位赛</span>
    <span class="hero-tag">🛡️ 装备系统</span>
  </div>
  <button class="play-btn" id="playBtn">▶ 开始游戏</button>
</div>
```

- [ ] **Step 3: Verify hero renders centered with glow**

Open in browser. Verify: large emoji icon, title, description, tag pills, blue play button, all centered with blue glow behind.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "feat: add hero area with game info, tags, and play button"
```

---

### Task 3: Bottom Selector Bar

**Files:**
- Modify: `index.html`

- [ ] **Step 1: Add selector bar CSS**

Add after hero CSS:

```css
/* Bottom selector bar */
.selector-bar {
  height: 110px; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center; gap: 20px;
  padding: 0 40px;
  background: linear-gradient(180deg, transparent 0%, rgba(0,0,0,0.7) 30%, rgba(0,0,0,0.9) 100%);
  backdrop-filter: blur(20px); z-index: 10; position: relative;
}
.selector-bar::before {
  content: ''; position: absolute; top: 0; left: 10%; right: 10%; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0,112,216,0.2), transparent);
}
.game-thumb {
  width: 76px; height: 76px; border-radius: 16px;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 4px; cursor: pointer; border: 2.5px solid transparent;
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  position: relative; flex-shrink: 0;
}
.game-thumb .thumb-emoji { font-size: 28px; }
.game-thumb .thumb-name { font-size: 9px; color: var(--text-muted); font-weight: 500; }
.game-thumb.active {
  border-color: #fff; transform: scale(1.15);
  box-shadow: 0 0 24px rgba(0,112,216,0.25), 0 0 60px rgba(0,112,216,0.1);
}
.game-thumb.active .thumb-name { color: #fff; }
.game-thumb:not(.active):hover {
  transform: scale(1.05); border-color: rgba(255,255,255,0.2);
}
```

- [ ] **Step 2: Add selector bar HTML**

Add inside `.game-library`, after the hero div:

```html
<div class="selector-bar">
  <div class="game-thumb active" data-game="0" onclick="selectGame(0)" style="background: linear-gradient(135deg, #0a1a3a, #0d2550);">
    <span class="thumb-emoji">🏁</span>
    <span class="thumb-name">乌龟赛跑</span>
  </div>
  <div class="game-thumb" data-game="1" onclick="selectGame(1)" style="background: linear-gradient(135deg, #0a2a1a, #0d3520);">
    <span class="thumb-emoji">🐢</span>
    <span class="thumb-name">合成大乌龟</span>
  </div>
</div>
```

- [ ] **Step 3: Verify selector bar at bottom with two game thumbnails**

Open in browser. Verify: bottom bar with two game thumbnails, first one active (white border, scaled up).

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "feat: add bottom game selector bar with thumbnails"
```

---

### Task 4: JavaScript — Game Switching & Navigation

**Files:**
- Modify: `index.html`

- [ ] **Step 1: Add game data and interaction logic**

Add before `</body>`:

```html
<script>
const games = [
  {
    icon: '🏁', title: '乌龟赛跑',
    desc: '装备你的乌龟，征战排位赛，成为赛道之王',
    tags: ['🏁 竞速', '⚔️ 排位赛', '🛡️ 装备系统'],
    glow: '#0070d8', url: 'turtle-race.html'
  },
  {
    icon: '🐢', title: '合成大乌龟',
    desc: '合成各种乌龟，解锁稀有品种，探索海洋世界',
    tags: ['🧩 合成', '🌊 海洋主题', '🐢 收集'],
    glow: '#00b860', url: 'merge-turtle.html'
  }
];

let currentGame = 0;
const hero = document.getElementById('hero');

function selectGame(index) {
  if (index === currentGame) return;
  currentGame = index;
  const game = games[index];

  // Update thumbs
  document.querySelectorAll('.game-thumb').forEach((t, i) => {
    t.classList.toggle('active', i === index);
  });

  // Fade out hero
  hero.style.opacity = '0';
  hero.style.transform = 'translateY(10px)';

  setTimeout(() => {
    document.getElementById('heroIcon').textContent = game.icon;
    document.getElementById('heroTitle').textContent = game.title;
    document.getElementById('heroDesc').textContent = game.desc;
    document.getElementById('heroTags').innerHTML =
      game.tags.map(t => `<span class="hero-tag">${t}</span>`).join('');
    document.getElementById('heroGlow').style.background = game.glow;

    // Fade in hero
    hero.style.opacity = '1';
    hero.style.transform = 'translateY(0)';
  }, 250);
}

// Play button
document.getElementById('playBtn').addEventListener('click', () => {
  window.location.href = games[currentGame].url;
});

// Keyboard nav
document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowLeft') selectGame(Math.max(0, currentGame - 1));
  if (e.key === 'ArrowRight') selectGame(Math.min(games.length - 1, currentGame + 1));
  if (e.key === 'Enter') window.location.href = games[currentGame].url;
});

// Hero transition setup
hero.style.transition = 'opacity 0.3s, transform 0.3s';

// Clock
function updateClock() {
  const now = new Date();
  document.getElementById('clock').textContent =
    now.getHours().toString().padStart(2, '0') + ':' +
    now.getMinutes().toString().padStart(2, '0');
}
updateClock();
setInterval(updateClock, 30000);
</script>
```

- [ ] **Step 2: Test all interactions**

Open in browser and verify:
1. Click second thumbnail → hero fades out/in with 合成大乌龟 content, glow turns green
2. Click first thumbnail → switches back to 乌龟赛跑, glow blue
3. Left/right arrow keys switch games
4. Enter key or click "开始游戏" navigates to game HTML
5. Clock shows current time

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "feat: add game switching, keyboard nav, and play button navigation"
```

---

### Task 5: Mobile Responsive

**Files:**
- Modify: `index.html`

- [ ] **Step 1: Add mobile media queries**

Add at the end of `<style>`, before `</style>`:

```css
/* Mobile responsive */
@media (max-width: 600px) {
  .top-bar { padding: 0 16px; height: 48px; }
  .top-bar-logo { font-size: 13px; }
  .top-bar-nav span { font-size: 11px; }
  .top-bar-nav { gap: 12px; }
  .hero-icon { font-size: 56px; }
  .hero-title { font-size: 28px; }
  .hero-desc { font-size: 13px; }
  .hero-tags { gap: 6px; }
  .hero-tag { font-size: 10px; padding: 3px 10px; }
  .play-btn { padding: 12px 36px; font-size: 15px; }
  .selector-bar { height: 90px; gap: 14px; padding: 0 20px; }
  .game-thumb { width: 62px; height: 62px; border-radius: 12px; }
  .game-thumb .thumb-emoji { font-size: 22px; }
  .game-thumb .thumb-name { font-size: 8px; }
}
```

- [ ] **Step 2: Test mobile in browser dev tools**

Open Chrome DevTools, toggle device toolbar, test iPhone SE / iPhone 12 sizes. Verify all elements fit and are readable.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "feat: add mobile responsive layout for game library"
```
