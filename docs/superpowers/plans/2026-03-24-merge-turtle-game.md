# 合成大乌龟 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a single-file HTML game "合成大乌龟" (Merge Turtle) — a 合成大西瓜 clone with turtle theme, playable in WeChat's built-in browser.

**Architecture:** Single HTML file containing all CSS, JS, and game logic. Canvas-based rendering with a custom lightweight 2D physics engine (gravity, circle collision, impulse resolution, friction). Web Audio API for programmatic sound effects. No external dependencies.

**Tech Stack:** HTML5 Canvas, vanilla JavaScript, Web Audio API, localStorage, Vibration API

**Spec:** `docs/superpowers/specs/2026-03-24-merge-turtle-game-design.md`

---

## File Structure

Single file: `merge-turtle.html`

Internal code sections (organized as labeled regions within `<script>`):
1. **Constants & Config** — turtle data, physics params, difficulty settings
2. **Physics Engine** — gravity, collision detection, impulse solver, sleep
3. **Turtle Renderer** — Canvas drawing functions for each turtle type
4. **Audio Engine** — Web Audio API sound effects
5. **Particle System** — merge effects, score popups
6. **Game State** — score, difficulty, game-over logic, localStorage
7. **Input Handler** — touch/mouse events, drop control
8. **UI Layer** — HUD, difficulty selector, game-over panel
9. **Game Loop** — requestAnimationFrame, physics step, render

---

### Task 1: HTML Scaffold + Canvas Setup

**Files:**
- Create: `merge-turtle.html`

- [ ] **Step 1: Create the HTML file with basic structure**

Create `merge-turtle.html` with:
- `<!DOCTYPE html>` with `<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">`
- `<meta name="apple-mobile-web-app-capable" content="yes">`
- CSS: full-screen black background, no margin/padding, `touch-action: none`, `overflow: hidden`, `user-select: none`
- A single `<canvas id="gameCanvas">` element
- `<script>` block with canvas setup: get context, resize to `window.innerWidth` x `window.innerHeight`, handle `resize` event
- A basic `requestAnimationFrame` loop that clears the canvas and draws "合成大乌龟" text centered

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
<meta name="apple-mobile-web-app-capable" content="yes">
<title>合成大乌龟</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:100%;height:100%;overflow:hidden;background:#1a1a2e;touch-action:none;user-select:none;-webkit-user-select:none}
canvas{display:block}
</style>
</head>
<body>
<canvas id="gameCanvas"></canvas>
<script>
// === CANVAS SETUP ===
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

function resize() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
window.addEventListener('resize', resize);
resize();

// === GAME LOOP (placeholder) ===
function gameLoop() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = '#fff';
  ctx.font = 'bold 28px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('🐢 合成大乌龟', canvas.width / 2, canvas.height / 2);
  requestAnimationFrame(gameLoop);
}
gameLoop();
</script>
</body>
</html>
```

- [ ] **Step 2: Open in browser and verify**

Run: `open merge-turtle.html`
Expected: Full-screen dark background with "🐢 合成大乌龟" centered. No scrollbars, no zoom on mobile.

- [ ] **Step 3: Commit**

```bash
git add merge-turtle.html
git commit -m "feat: initial HTML scaffold with canvas setup"
```

---

### Task 2: Constants, Config & Game Layout

**Files:**
- Modify: `merge-turtle.html`

- [ ] **Step 1: Add turtle data and game constants**

Add at the top of the `<script>` block, after canvas setup:

```javascript
// === CONSTANTS & CONFIG ===
const TURTLES = [
  { name: '草龟',       radius: 20, score: 10,  color: '#8BC34A', darkColor: '#689F38' },
  { name: '巴西龟',     radius: 26, score: 30,  color: '#66BB6A', darkColor: '#43A047' },
  { name: '花龟',       radius: 32, score: 60,  color: '#FFCA28', darkColor: '#F9A825' },
  { name: '锦龟',       radius: 39, score: 100, color: '#FF7043', darkColor: '#E64A19' },
  { name: '鳄龟',       radius: 47, score: 150, color: '#78909C', darkColor: '#546E7A' },
  { name: '海龟',       radius: 56, score: 210, color: '#42A5F5', darkColor: '#1E88E5' },
  { name: '苏卡达陆龟', radius: 63, score: 280, color: '#D4A574', darkColor: '#B8895A' },
  { name: '象龟',       radius: 70, score: 360, color: '#A1887F', darkColor: '#795548' },
  { name: '加拉帕戈斯象龟', radius: 80, score: 500, color: '#FFD54F', darkColor: '#FF8F00' },
];

const DIFFICULTY = {
  easy:   { name: '简单', maxDrop: 7 },  // Lv.1-7
  normal: { name: '普通', maxDrop: 6 },  // Lv.1-6
  hard:   { name: '困难', maxDrop: 5 },  // Lv.1-5
};

const PHYSICS = {
  gravity: 980,          // px/s²
  restitution: 0.3,      // bounce factor
  friction: 0.4,         // turtle-turtle friction
  groundFriction: 0.6,   // ground friction
  damping: 0.99,         // velocity damping per frame
  sleepThreshold: 0.5,   // px/s below which turtle can sleep
  sleepDelay: 0.5,       // seconds before sleep activates
  solverIterations: 4,   // collision solver iterations
  fixedDt: 1 / 60,       // fixed physics timestep
};

const GAME = {
  dropCooldown: 0.5,     // seconds between drops
  gameOverDelay: 2.0,    // seconds above line before game over
  wallThickness: 2,
};
```

- [ ] **Step 2: Add game layout computation**

Add layout computation that calculates game area dimensions based on screen size:

```javascript
// === LAYOUT ===
const layout = {};

function computeLayout() {
  const W = canvas.width;
  const H = canvas.height;
  const topBarH = 44;
  const diffBarH = 28;
  const previewH = 30;
  const dropZoneH = 50;
  const bottomBarH = 40;

  layout.width = W;
  layout.height = H;
  layout.topBar = { x: 0, y: 0, w: W, h: topBarH };
  layout.diffBar = { x: 0, y: topBarH, w: W, h: diffBarH };
  layout.preview = { x: 0, y: topBarH + diffBarH, w: W, h: previewH };
  layout.dropZone = { x: 0, y: topBarH + diffBarH + previewH, w: W, h: dropZoneH };

  const gameTop = topBarH + diffBarH + previewH + dropZoneH;
  const gameBottom = H - bottomBarH;
  layout.gameArea = { x: 0, y: gameTop, w: W, h: gameBottom - gameTop };
  layout.gameOverLineY = gameTop + 30; // 30px below top of game area
  layout.bottomBar = { x: 0, y: gameBottom, w: W, h: bottomBarH };
}
```

- [ ] **Step 3: Update resize and verify layout**

Update `resize()` to call `computeLayout()`. Replace the placeholder render with a layout debug view that draws colored rectangles for each zone.

Verify in browser: all zones visible and properly stacked. Resize window to confirm layout adapts.

- [ ] **Step 4: Commit**

```bash
git add merge-turtle.html
git commit -m "feat: add turtle data, physics config, difficulty settings, and layout system"
```

---

### Task 3: Turtle Renderer

**Files:**
- Modify: `merge-turtle.html`

- [ ] **Step 1: Implement drawTurtle function**

Add a function that draws a cartoon turtle on canvas given position, level, and scale:

```javascript
// === TURTLE RENDERER ===
function drawTurtle(ctx, x, y, level, scale = 1) {
  const t = TURTLES[level];
  const r = t.radius * scale;
  const s = r / 40; // normalize to base size 40

  ctx.save();
  ctx.translate(x, y);

  // Shell (outer)
  ctx.beginPath();
  ctx.ellipse(0, 2 * s, 28 * s, 22 * s, 0, 0, Math.PI * 2);
  ctx.fillStyle = t.color;
  ctx.fill();

  // Shell (inner, darker)
  ctx.beginPath();
  ctx.ellipse(0, 2 * s, 22 * s, 17 * s, 0, 0, Math.PI * 2);
  ctx.fillStyle = t.darkColor;
  ctx.fill();

  // Shell pattern (varies by level)
  drawShellPattern(ctx, level, s);

  // Legs
  const legColor = t.color;
  ctx.fillStyle = legColor;
  // Front legs
  ctx.beginPath(); ctx.ellipse(-20 * s, 10 * s, 7 * s, 5 * s, -0.3, 0, Math.PI * 2); ctx.fill();
  ctx.beginPath(); ctx.ellipse(20 * s, 10 * s, 7 * s, 5 * s, 0.3, 0, Math.PI * 2); ctx.fill();
  // Back legs
  ctx.beginPath(); ctx.ellipse(-16 * s, 20 * s, 6 * s, 4 * s, -0.2, 0, Math.PI * 2); ctx.fill();
  ctx.beginPath(); ctx.ellipse(16 * s, 20 * s, 6 * s, 4 * s, 0.2, 0, Math.PI * 2); ctx.fill();
  // Tail
  ctx.beginPath(); ctx.ellipse(0, 26 * s, 3 * s, 5 * s, 0, 0, Math.PI * 2); ctx.fill();

  // Head
  ctx.beginPath();
  ctx.arc(0, -16 * s, 10 * s, 0, Math.PI * 2);
  ctx.fillStyle = t.color;
  ctx.fill();

  // Eyes
  ctx.fillStyle = '#333';
  ctx.beginPath(); ctx.arc(-4 * s, -18 * s, 2.5 * s, 0, Math.PI * 2); ctx.fill();
  ctx.beginPath(); ctx.arc(4 * s, -18 * s, 2.5 * s, 0, Math.PI * 2); ctx.fill();

  // Smile
  ctx.beginPath();
  ctx.arc(0, -14 * s, 5 * s, 0.1, Math.PI - 0.1, false);
  ctx.strokeStyle = '#333';
  ctx.lineWidth = 1.5 * s;
  ctx.stroke();

  // Crown for level 8 (Galapagos)
  if (level === 8) {
    drawCrown(ctx, s);
  }

  ctx.restore();
}
```

- [ ] **Step 2: Add shell pattern and crown helpers**

```javascript
function drawShellPattern(ctx, level, s) {
  // Different patterns per turtle type
  if (level === 2) { // 花龟 - spots
    ctx.fillStyle = TURTLES[level].darkColor;
    ctx.globalAlpha = 0.5;
    ctx.beginPath(); ctx.arc(-6 * s, -2 * s, 4 * s, 0, Math.PI * 2); ctx.fill();
    ctx.beginPath(); ctx.arc(5 * s, 5 * s, 3 * s, 0, Math.PI * 2); ctx.fill();
    ctx.globalAlpha = 1;
  } else if (level === 3) { // 锦龟 - zigzag
    ctx.strokeStyle = TURTLES[level].darkColor;
    ctx.lineWidth = 2 * s;
    ctx.beginPath();
    ctx.moveTo(-12 * s, -2 * s); ctx.lineTo(-6 * s, -8 * s); ctx.lineTo(0 * s, -2 * s);
    ctx.lineTo(6 * s, -8 * s); ctx.lineTo(12 * s, -2 * s);
    ctx.stroke();
  } else if (level >= 6 && level <= 8) { // 苏卡达/象龟/加拉帕戈斯 - grid
    ctx.fillStyle = TURTLES[level].darkColor;
    ctx.globalAlpha = 0.4;
    for (let row = 0; row < 2; row++) {
      for (let col = 0; col < 2; col++) {
        const bx = (-8 + col * 14) * s;
        const by = (-6 + row * 14) * s;
        ctx.fillRect(bx, by, 10 * s, 10 * s);
      }
    }
    ctx.globalAlpha = 1;
  }
}

function drawCrown(ctx, s) {
  ctx.fillStyle = '#FFD700';
  ctx.strokeStyle = '#FFA000';
  ctx.lineWidth = 1 * s;
  ctx.beginPath();
  ctx.moveTo(-10 * s, -24 * s);
  ctx.lineTo(-7 * s, -32 * s);
  ctx.lineTo(-3 * s, -26 * s);
  ctx.lineTo(0, -34 * s);
  ctx.lineTo(3 * s, -26 * s);
  ctx.lineTo(7 * s, -32 * s);
  ctx.lineTo(10 * s, -24 * s);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();

  // Glow ring for Galapagos
  ctx.strokeStyle = 'rgba(255, 213, 79, 0.3)';
  ctx.lineWidth = 4 * s;
  ctx.beginPath();
  ctx.ellipse(0, 2 * s, 34 * s, 28 * s, 0, 0, Math.PI * 2);
  ctx.stroke();
}
```

- [ ] **Step 3: Test rendering all 9 turtles**

Replace the placeholder render loop with a test that draws all 9 turtles in a grid. Verify in browser: each turtle is distinct, properly colored, correct relative sizes, Galapagos has crown + glow.

- [ ] **Step 4: Commit**

```bash
git add merge-turtle.html
git commit -m "feat: implement cartoon turtle renderer with 9 levels and unique patterns"
```

---

### Task 4: Physics Engine — Core

**Files:**
- Modify: `merge-turtle.html`

- [ ] **Step 1: Implement physics body and world**

```javascript
// === PHYSICS ENGINE ===
class Body {
  constructor(x, y, level) {
    this.x = x;
    this.y = y;
    this.vx = 0;
    this.vy = 0;
    this.level = level;
    this.radius = TURTLES[level].radius;
    this.mass = this.radius * this.radius; // mass proportional to area
    this.invMass = 1 / this.mass;
    this.sleeping = false;
    this.sleepTimer = 0;
    this.mergeFlag = false; // marked for merge
    this.age = 0; // seconds since spawn, used to skip game-over check for fresh drops
    this.id = Body.nextId++;
  }
}
Body.nextId = 0;

const world = {
  bodies: [],
  mergeQueue: [],  // pairs to merge after solving

  addBody(x, y, level) {
    const b = new Body(x, y, level);
    this.bodies.push(b);
    return b;
  },

  removeBody(body) {
    const idx = this.bodies.indexOf(body);
    if (idx !== -1) this.bodies.splice(idx, 1);
  },
};
```

- [ ] **Step 2: Implement collision detection**

```javascript
function detectCollisions(bodies, area) {
  const pairs = [];

  // Circle-circle
  for (let i = 0; i < bodies.length; i++) {
    for (let j = i + 1; j < bodies.length; j++) {
      const a = bodies[i], b = bodies[j];
      const dx = b.x - a.x;
      const dy = b.y - a.y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      const minDist = a.radius + b.radius;
      if (dist < minDist) {
        const nx = dist > 0.0001 ? dx / dist : 0;
        const ny = dist > 0.0001 ? dy / dist : 1;
        pairs.push({ a, b, nx, ny, overlap: minDist - dist });
      }
    }
  }

  // Circle-wall (left, right, bottom)
  const left = area.x + GAME.wallThickness;
  const right = area.x + area.w - GAME.wallThickness;
  const bottom = area.y + area.h;

  for (const body of bodies) {
    if (body.x - body.radius < left) {
      pairs.push({ a: body, b: null, nx: 1, ny: 0, overlap: left - (body.x - body.radius), wall: 'left' });
    }
    if (body.x + body.radius > right) {
      pairs.push({ a: body, b: null, nx: -1, ny: 0, overlap: (body.x + body.radius) - right, wall: 'right' });
    }
    if (body.y + body.radius > bottom) {
      pairs.push({ a: body, b: null, nx: 0, ny: -1, overlap: (body.y + body.radius) - bottom, wall: 'bottom' });
    }
  }

  return pairs;
}
```

- [ ] **Step 3: Implement impulse solver**

```javascript
function solveCollision(pair) {
  const { a, b, nx, ny, overlap } = pair;

  if (!b) {
    // Wall collision
    const isGround = pair.wall === 'bottom';
    const fric = isGround ? PHYSICS.groundFriction : PHYSICS.friction;
    const e = PHYSICS.restitution;

    // Position correction
    a.x += nx * overlap;
    a.y += ny * overlap;

    // Velocity response
    const vn = a.vx * nx + a.vy * ny;
    if (vn < 0) {
      a.vx -= (1 + e) * vn * nx;
      a.vy -= (1 + e) * vn * ny;

      // Tangent friction
      const tx = -ny, ty = nx;
      const vt = a.vx * tx + a.vy * ty;
      const maxFric = Math.abs(vn * (1 + e)) * fric;
      const fricImpulse = Math.max(-maxFric, Math.min(maxFric, -vt));
      a.vx += fricImpulse * tx;
      a.vy += fricImpulse * ty;
    }

    // Wake up
    a.sleeping = false;
    a.sleepTimer = 0;
    return;
  }

  // Circle-circle collision
  // Check for merge
  if (a.level === b.level && a.level < TURTLES.length - 1 && !a.mergeFlag && !b.mergeFlag) {
    a.mergeFlag = true;
    b.mergeFlag = true;
    world.mergeQueue.push({ a, b });
  }

  // Position correction (mass-weighted)
  const totalInvMass = a.invMass + b.invMass;
  if (totalInvMass > 0) {
    const corrA = (a.invMass / totalInvMass) * overlap * 1.01; // slight bias
    const corrB = (b.invMass / totalInvMass) * overlap * 1.01;
    a.x -= nx * corrA;
    a.y -= ny * corrA;
    b.x += nx * corrB;
    b.y += ny * corrB;
  }

  // Relative velocity along normal
  const dvx = a.vx - b.vx;
  const dvy = a.vy - b.vy;
  const vn = dvx * nx + dvy * ny;

  if (vn > 0) return; // separating

  // Normal impulse
  const e = PHYSICS.restitution;
  const j = -(1 + e) * vn / totalInvMass;

  a.vx += j * a.invMass * nx;
  a.vy += j * a.invMass * ny;
  b.vx -= j * b.invMass * nx;
  b.vy -= j * b.invMass * ny;

  // Tangent friction
  const tx = -ny, ty = nx;
  const vt = dvx * tx + dvy * ty;
  const maxFric = Math.abs(j) * PHYSICS.friction;
  let jt = -vt / totalInvMass;
  jt = Math.max(-maxFric, Math.min(maxFric, jt));

  a.vx += jt * a.invMass * tx;
  a.vy += jt * a.invMass * ty;
  b.vx -= jt * b.invMass * tx;
  b.vy -= jt * b.invMass * ty;

  // Wake both
  a.sleeping = false; a.sleepTimer = 0;
  b.sleeping = false; b.sleepTimer = 0;
}
```

- [ ] **Step 4: Implement physics step with accumulator**

```javascript
let physicsAccumulator = 0;

function physicsStep(dt) {
  physicsAccumulator += dt;
  const fixedDt = PHYSICS.fixedDt;

  while (physicsAccumulator >= fixedDt) {
    physicsAccumulator -= fixedDt;

    // Apply gravity and integrate
    for (const body of world.bodies) {
      if (body.sleeping) continue;
      body.vy += PHYSICS.gravity * fixedDt;
      body.vx *= PHYSICS.damping;
      body.vy *= PHYSICS.damping;
      body.x += body.vx * fixedDt;
      body.y += body.vy * fixedDt;
    }

    // Detect and solve collisions (iterative)
    for (let iter = 0; iter < PHYSICS.solverIterations; iter++) {
      const pairs = detectCollisions(world.bodies, layout.gameArea);
      for (const pair of pairs) {
        solveCollision(pair);
      }
    }

    // Process merge queue
    processMerges();

    // Sleep check
    for (const body of world.bodies) {
      if (body.sleeping) continue;
      const speed = Math.sqrt(body.vx * body.vx + body.vy * body.vy);
      if (speed < PHYSICS.sleepThreshold) {
        body.sleepTimer += fixedDt;
        if (body.sleepTimer >= PHYSICS.sleepDelay) {
          body.sleeping = true;
        }
      } else {
        body.sleepTimer = 0;
      }
    }
  }
}
```

- [ ] **Step 5: Test physics with a few dropped turtles**

Add a temporary click handler that spawns a random turtle at click X position at top of game area. Verify: turtles fall, bounce off walls and floor, stack on each other, come to rest. Same-level turtles should trigger merge (but merge processing not yet implemented — just verify they get flagged).

- [ ] **Step 6: Commit**

```bash
git add merge-turtle.html
git commit -m "feat: implement physics engine with gravity, collision detection, impulse solver, and sleep"
```

---

### Task 5: Merge Logic + Particle System

**Files:**
- Modify: `merge-turtle.html`

- [ ] **Step 1: Implement merge processing**

```javascript
// === MERGE & PARTICLES ===
const particles = [];
const scorePopups = [];
let chainCount = 0; // for chain merge tracking

function processMerges() {
  for (const { a, b } of world.mergeQueue) {
    const newLevel = a.level + 1;
    const mx = (a.x + b.x) / 2;
    const my = (a.y + b.y) / 2;

    // Remove old bodies
    world.removeBody(a);
    world.removeBody(b);

    // Spawn new turtle
    const newBody = world.addBody(mx, my, newLevel);
    const avgVx = (a.vx + b.vx) / 2;
    const avgVy = (a.vy + b.vy) / 2;
    newBody.vx = avgVx * 0.5;
    newBody.vy = Math.min(avgVy * 0.5, -50); // slight upward bounce

    // Score
    const points = TURTLES[newLevel].score;
    game.score += points;

    // Chain tracking
    chainCount++;

    // Particles
    const particleCount = chainCount > 1 ? 16 : 10;
    spawnMergeParticles(mx, my, TURTLES[newLevel].color, particleCount);

    // Score popup
    const fontSize = chainCount > 1 ? 24 + chainCount * 4 : 20;
    scorePopups.push({ x: mx, y: my, text: `+${points}`, life: 0.8, maxLife: 0.8, fontSize });

    // Vibration
    if (navigator.vibrate) navigator.vibrate(chainCount > 1 ? 100 : 50);

    // Sound (placeholder — implemented in Task 6)
    if (typeof playMergeSound === 'function') playMergeSound(newLevel, chainCount);

    // Final turtle celebration
    if (newLevel === TURTLES.length - 1) {
      spawnCelebration(mx, my);
    }
  }

  if (world.mergeQueue.length === 0) chainCount = 0;
  world.mergeQueue = [];
}
```

- [ ] **Step 2: Implement particle system**

```javascript
function spawnMergeParticles(x, y, color, count) {
  for (let i = 0; i < count; i++) {
    const angle = (Math.PI * 2 * i) / count + (Math.random() - 0.5) * 0.5;
    const speed = 80 + Math.random() * 120;
    particles.push({
      x, y,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed,
      radius: 3 + Math.random() * 3,
      color,
      life: 0.5,
      maxLife: 0.5,
    });
  }
}

function spawnCelebration(x, y) {
  for (let i = 0; i < 40; i++) {
    const angle = Math.random() * Math.PI * 2;
    const speed = 100 + Math.random() * 200;
    particles.push({
      x: x + (Math.random() - 0.5) * 100,
      y: y + (Math.random() - 0.5) * 100,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed - 100,
      radius: 4 + Math.random() * 4,
      color: ['#FFD54F', '#FFD700', '#FFA000', '#FF8F00'][Math.floor(Math.random() * 4)],
      life: 2.0,
      maxLife: 2.0,
    });
  }
  if (navigator.vibrate) navigator.vibrate(200);
}

function updateParticles(dt) {
  for (let i = particles.length - 1; i >= 0; i--) {
    const p = particles[i];
    p.x += p.vx * dt;
    p.y += p.vy * dt;
    p.vy += 200 * dt; // gravity on particles
    p.life -= dt;
    if (p.life <= 0) particles.splice(i, 1);
  }
  for (let i = scorePopups.length - 1; i >= 0; i--) {
    const sp = scorePopups[i];
    sp.y -= 40 * dt;
    sp.life -= dt;
    if (sp.life <= 0) scorePopups.splice(i, 1);
  }
}

function renderParticles(ctx) {
  for (const p of particles) {
    const alpha = p.life / p.maxLife;
    ctx.globalAlpha = alpha;
    ctx.fillStyle = p.color;
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.globalAlpha = 1;

  for (const sp of scorePopups) {
    const alpha = sp.life / sp.maxLife;
    ctx.globalAlpha = alpha;
    ctx.fillStyle = '#fff';
    ctx.font = `bold ${sp.fontSize}px sans-serif`;
    ctx.textAlign = 'center';
    ctx.fillText(sp.text, sp.x, sp.y);
  }
  ctx.globalAlpha = 1;
}
```

- [ ] **Step 3: Test merge and particles**

Click to drop same-level turtles near each other. Verify: they merge on collision, spawn particles, show score popup, new higher-level turtle appears with slight upward bounce. Test chain merge by setting up aligned turtles.

- [ ] **Step 4: Commit**

```bash
git add merge-turtle.html
git commit -m "feat: implement merge logic with particle effects, score popups, and chain combos"
```

---

### Task 6: Audio Engine

**Files:**
- Modify: `merge-turtle.html`

- [ ] **Step 1: Implement Web Audio sound effects**

```javascript
// === AUDIO ENGINE ===
let audioCtx = null;

function initAudio() {
  if (audioCtx) return;
  audioCtx = new (window.AudioContext || window.webkitAudioContext)();
}

function playDropSound() {
  if (!audioCtx) return;
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.connect(gain);
  gain.connect(audioCtx.destination);
  osc.frequency.setValueAtTime(400, audioCtx.currentTime);
  osc.frequency.exponentialRampToValueAtTime(200, audioCtx.currentTime + 0.1);
  gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.1);
  osc.start();
  osc.stop(audioCtx.currentTime + 0.1);
}

function playMergeSound(level, chain) {
  if (!audioCtx) return;
  const baseFreq = 300 + level * 80;
  const t = audioCtx.currentTime;

  // Main tone
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.type = 'sine';
  osc.connect(gain);
  gain.connect(audioCtx.destination);
  osc.frequency.setValueAtTime(baseFreq, t);
  osc.frequency.exponentialRampToValueAtTime(baseFreq * 1.5, t + 0.15);
  gain.gain.setValueAtTime(0.3, t);
  gain.gain.exponentialRampToValueAtTime(0.01, t + 0.3);
  osc.start(t);
  osc.stop(t + 0.3);

  // Harmony for chains
  if (chain > 1) {
    const osc2 = audioCtx.createOscillator();
    const gain2 = audioCtx.createGain();
    osc2.type = 'triangle';
    osc2.connect(gain2);
    gain2.connect(audioCtx.destination);
    osc2.frequency.setValueAtTime(baseFreq * 1.25, t);
    osc2.frequency.exponentialRampToValueAtTime(baseFreq * 1.75, t + 0.2);
    gain2.gain.setValueAtTime(0.2, t);
    gain2.gain.exponentialRampToValueAtTime(0.01, t + 0.3);
    osc2.start(t);
    osc2.stop(t + 0.3);
  }
}

function playFinalMergeSound() {
  if (!audioCtx) return;
  const t = audioCtx.currentTime;
  [523, 659, 784].forEach((freq, i) => {
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = 'square';
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.frequency.setValueAtTime(freq, t + i * 0.15);
    gain.gain.setValueAtTime(0.2, t + i * 0.15);
    gain.gain.exponentialRampToValueAtTime(0.01, t + i * 0.15 + 0.4);
    osc.start(t + i * 0.15);
    osc.stop(t + i * 0.15 + 0.4);
  });
}

function playGameOverSound() {
  if (!audioCtx) return;
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.type = 'sawtooth';
  osc.connect(gain);
  gain.connect(audioCtx.destination);
  osc.frequency.setValueAtTime(300, audioCtx.currentTime);
  osc.frequency.exponentialRampToValueAtTime(80, audioCtx.currentTime + 0.5);
  gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.5);
  osc.start();
  osc.stop(audioCtx.currentTime + 0.5);
}
```

- [ ] **Step 2: Wire audio init to first user interaction**

Add to the touch/click handler: `initAudio()` on first interaction (WeChat requires user gesture to unlock AudioContext).

- [ ] **Step 3: Test all sound effects**

Drop a turtle (hear drop sound), merge two (hear merge sound ascending by level), test chain merge (hear harmony). Verify no errors on devices that don't support Web Audio (graceful fallback).

- [ ] **Step 4: Commit**

```bash
git add merge-turtle.html
git commit -m "feat: implement Web Audio programmatic sound effects for drop, merge, chain, and game over"
```

---

### Task 7: Input Handler + Drop Mechanics

**Files:**
- Modify: `merge-turtle.html`

- [ ] **Step 1: Implement game state object**

```javascript
// === GAME STATE ===
const game = {
  state: 'menu',  // 'menu' | 'playing' | 'gameover'
  difficulty: 'normal',
  score: 0,
  highScore: parseInt(localStorage.getItem('turtle_merge_high_score') || '0'),
  currentTurtle: null,  // { level, x } — turtle being aimed
  nextLevel: 0,
  dropX: 0,
  canDrop: true,
  dropCooldownTimer: 0,
  gameOverTimer: 0,     // time any body above line
  discoveredLevels: new Set(),

  reset() {
    this.score = 0;
    this.state = 'playing';
    this.canDrop = true;
    this.dropCooldownTimer = 0;
    this.gameOverTimer = 0;
    this.discoveredLevels = new Set();
    world.bodies = [];
    world.mergeQueue = [];
    particles.length = 0;
    scorePopups.length = 0;
    this.spawnNext();
  },

  spawnNext() {
    const maxDrop = DIFFICULTY[this.difficulty].maxDrop;
    this.nextLevel = Math.floor(Math.random() * maxDrop);
    if (this.currentTurtle === null) {
      this.currentTurtle = { level: this.nextLevel, x: layout.width / 2 };
      this.nextLevel = Math.floor(Math.random() * maxDrop);
    }
  },

  dropTurtle() {
    if (!this.canDrop || this.state !== 'playing') return;
    const t = this.currentTurtle;
    const dropY = layout.dropZone.y + layout.dropZone.h;
    const body = world.addBody(t.x, dropY, t.level);
    this.discoveredLevels.add(t.level);
    playDropSound();
    this.canDrop = false;
    this.dropCooldownTimer = GAME.dropCooldown;
    this.currentTurtle = { level: this.nextLevel, x: layout.width / 2 };
    const maxDrop = DIFFICULTY[this.difficulty].maxDrop;
    this.nextLevel = Math.floor(Math.random() * maxDrop);
  },
};
```

- [ ] **Step 2: Implement touch/mouse input**

```javascript
// === INPUT HANDLER ===
let touching = false;

function getEventX(e) {
  if (e.touches && e.touches.length > 0) return e.touches[0].clientX;
  return e.clientX;
}

canvas.addEventListener('touchstart', (e) => {
  e.preventDefault();
  initAudio();
  touching = true;
  handlePointerMove(getEventX(e));
}, { passive: false });

canvas.addEventListener('touchmove', (e) => {
  e.preventDefault();
  if (touching) handlePointerMove(getEventX(e));
}, { passive: false });

canvas.addEventListener('touchend', (e) => {
  e.preventDefault();
  if (touching && game.state === 'playing') {
    game.dropTurtle();
  }
  touching = false;
}, { passive: false });

// Mouse fallback
canvas.addEventListener('mousedown', (e) => {
  initAudio();
  touching = true;
  handlePointerMove(e.clientX);
});
canvas.addEventListener('mousemove', (e) => {
  if (touching) handlePointerMove(e.clientX);
});
canvas.addEventListener('mouseup', () => {
  if (touching && game.state === 'playing') {
    game.dropTurtle();
  }
  touching = false;
});

function handlePointerMove(x) {
  if (game.state === 'playing' && game.currentTurtle) {
    const r = TURTLES[game.currentTurtle.level].radius;
    const left = layout.gameArea.x + GAME.wallThickness + r;
    const right = layout.gameArea.x + layout.gameArea.w - GAME.wallThickness - r;
    game.currentTurtle.x = Math.max(left, Math.min(right, x));
  }
}
```

- [ ] **Step 3: Test drop mechanics**

Start game, slide finger/mouse to aim, release to drop. Verify: turtle falls from drop zone, cooldown prevents rapid fire, next turtle preview updates.

- [ ] **Step 4: Commit**

```bash
git add merge-turtle.html
git commit -m "feat: implement touch/mouse input handler and drop mechanics with cooldown"
```

---

### Task 8: UI Layer (HUD, Difficulty, Game Over)

**Files:**
- Modify: `merge-turtle.html`

- [ ] **Step 1: Implement HUD rendering**

```javascript
// === UI LAYER ===
function renderHUD(ctx) {
  const tb = layout.topBar;

  // Top bar background
  ctx.fillStyle = '#12122a';
  ctx.fillRect(tb.x, tb.y, tb.w, tb.h);

  // Score
  ctx.fillStyle = '#888';
  ctx.font = '10px sans-serif';
  ctx.textAlign = 'left';
  ctx.fillText('分数', tb.x + 12, tb.y + 14);
  ctx.fillStyle = '#FFD54F';
  ctx.font = 'bold 18px sans-serif';
  ctx.fillText(game.score.toLocaleString(), tb.x + 12, tb.y + 34);

  // Title
  ctx.fillStyle = '#fff';
  ctx.font = 'bold 16px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('🐢 合成大乌龟', tb.x + tb.w / 2, tb.y + 28);

  // High score
  ctx.fillStyle = '#888';
  ctx.font = '10px sans-serif';
  ctx.textAlign = 'right';
  ctx.fillText('最高', tb.x + tb.w - 12, tb.y + 14);
  ctx.fillStyle = '#aaa';
  ctx.font = '14px sans-serif';
  ctx.fillText(game.highScore.toLocaleString(), tb.x + tb.w - 12, tb.y + 34);
}
```

- [ ] **Step 2: Implement difficulty selector and preview**

```javascript
function renderDifficultyBar(ctx) {
  const db = layout.diffBar;
  ctx.fillStyle = '#12122a';
  ctx.fillRect(db.x, db.y, db.w, db.h);

  const diffs = ['easy', 'normal', 'hard'];
  const labels = ['简单', '普通', '困难'];
  const colors = ['#8BC34A', '#FFD54F', '#FF5252'];
  const btnW = 50, btnH = 18;
  const startX = db.x + (db.w - diffs.length * (btnW + 8)) / 2;

  diffs.forEach((d, i) => {
    const bx = startX + i * (btnW + 8);
    const by = db.y + (db.h - btnH) / 2;
    const active = game.difficulty === d;

    ctx.fillStyle = active ? colors[i] : '#2a2a4a';
    ctx.beginPath();
    ctx.roundRect(bx, by, btnW, btnH, 9);
    ctx.fill();

    ctx.fillStyle = active ? (d === 'normal' ? '#333' : '#fff') : '#888';
    ctx.font = `${active ? 'bold ' : ''}10px sans-serif`;
    ctx.textAlign = 'center';
    ctx.fillText(labels[i], bx + btnW / 2, by + 13);
  });
}

function renderPreview(ctx) {
  const pv = layout.preview;
  ctx.fillStyle = '#12122a';
  ctx.fillRect(pv.x, pv.y, pv.w, pv.h);

  ctx.fillStyle = '#666';
  ctx.font = '10px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('下一个:', pv.x + pv.w / 2 - 15, pv.y + 19);
  drawTurtle(ctx, pv.x + pv.w / 2 + 20, pv.y + 15, game.nextLevel, 0.35);
}
```

- [ ] **Step 3: Implement drop zone, game area, and bottom bar rendering**

```javascript
function renderDropZone(ctx) {
  const dz = layout.dropZone;

  // Guide line
  if (game.currentTurtle && game.canDrop) {
    const t = game.currentTurtle;
    ctx.setLineDash([4, 4]);
    ctx.strokeStyle = `${TURTLES[t.level].color}44`;
    ctx.beginPath();
    ctx.moveTo(t.x, dz.y);
    ctx.lineTo(t.x, layout.gameArea.y + layout.gameArea.h);
    ctx.stroke();
    ctx.setLineDash([]);

    // Draw current turtle
    drawTurtle(ctx, t.x, dz.y + dz.h / 2, t.level, 0.8);
  }
}

function renderGameArea(ctx) {
  const ga = layout.gameArea;

  // Background gradient
  const grad = ctx.createLinearGradient(0, ga.y, 0, ga.y + ga.h);
  grad.addColorStop(0, '#1a1a2e');
  grad.addColorStop(1, '#162447');
  ctx.fillStyle = grad;
  ctx.fillRect(ga.x, ga.y, ga.w, ga.h);

  // Walls
  ctx.fillStyle = '#2a2a4a';
  ctx.fillRect(ga.x, ga.y, GAME.wallThickness, ga.h);
  ctx.fillRect(ga.x + ga.w - GAME.wallThickness, ga.y, GAME.wallThickness, ga.h);

  // Game over line
  ctx.setLineDash([6, 4]);
  ctx.strokeStyle = 'rgba(255,0,0,0.3)';
  ctx.beginPath();
  ctx.moveTo(ga.x, layout.gameOverLineY);
  ctx.lineTo(ga.x + ga.w, layout.gameOverLineY);
  ctx.stroke();
  ctx.setLineDash([]);

  // Bodies
  for (const body of world.bodies) {
    drawTurtle(ctx, body.x, body.y, body.level);
    game.discoveredLevels.add(body.level);
  }

  // Particles
  renderParticles(ctx);
}

function renderBottomBar(ctx) {
  const bb = layout.bottomBar;
  ctx.fillStyle = '#12122a';
  ctx.fillRect(bb.x, bb.y, bb.w, bb.h);

  const totalW = TURTLES.length * 28;
  let startX = bb.x + (bb.w - totalW) / 2;

  TURTLES.forEach((t, i) => {
    ctx.globalAlpha = game.discoveredLevels.has(i) ? 1 : 0.25;
    drawTurtle(ctx, startX + i * 28 + 14, bb.y + bb.h / 2, i, 0.25);
  });
  ctx.globalAlpha = 1;
}
```

- [ ] **Step 4: Implement game over panel**

```javascript
function renderGameOverPanel(ctx) {
  // Dim overlay
  ctx.fillStyle = 'rgba(0,0,0,0.6)';
  ctx.fillRect(0, 0, layout.width, layout.height);

  // Panel
  const pw = 260, ph = 220;
  const px = (layout.width - pw) / 2;
  const py = (layout.height - ph) / 2;

  ctx.fillStyle = '#1e1e3a';
  ctx.beginPath();
  ctx.roundRect(px, py, pw, ph, 16);
  ctx.fill();
  ctx.strokeStyle = '#3a3a6a';
  ctx.lineWidth = 2;
  ctx.stroke();

  // Title
  ctx.fillStyle = '#fff';
  ctx.font = 'bold 22px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('游戏结束', px + pw / 2, py + 40);

  // Score
  ctx.fillStyle = '#FFD54F';
  ctx.font = 'bold 36px sans-serif';
  ctx.fillText(game.score.toLocaleString(), px + pw / 2, py + 90);

  ctx.fillStyle = '#888';
  ctx.font = '13px sans-serif';
  ctx.fillText(`最高分: ${game.highScore.toLocaleString()}`, px + pw / 2, py + 115);

  // Buttons: restart + share
  // Restart
  ctx.fillStyle = '#4CAF50';
  ctx.beginPath();
  ctx.roundRect(px + 20, py + 140, 100, 40, 10);
  ctx.fill();
  ctx.fillStyle = '#fff';
  ctx.font = 'bold 15px sans-serif';
  ctx.fillText('再来一局', px + 70, py + 165);

  // Share
  ctx.fillStyle = '#2196F3';
  ctx.beginPath();
  ctx.roundRect(px + 140, py + 140, 100, 40, 10);
  ctx.fill();
  ctx.fillStyle = '#fff';
  ctx.fillText('分享', px + 190, py + 165);

  // Store button rects for click detection
  game.restartBtn = { x: px + 20, y: py + 140, w: 100, h: 40 };
  game.shareBtn = { x: px + 140, y: py + 140, w: 100, h: 40 };
}
```

- [ ] **Step 5: Add click handlers for menu, difficulty, restart, share**

Wire up click/touch detection for:
- Difficulty buttons (only in menu/before first drop)
- Game over restart button → `game.reset()`
- Game over share button → copy score text to clipboard

```javascript
function handleTap(x, y) {
  if (game.state === 'gameover') {
    if (hitTest(x, y, game.restartBtn)) {
      game.reset();
      return;
    }
    if (hitTest(x, y, game.shareBtn)) {
      shareScore();
      return;
    }
    return;
  }

  // Difficulty selection (only before first drop or when no bodies)
  if (world.bodies.length === 0) {
    const db = layout.diffBar;
    const diffs = ['easy', 'normal', 'hard'];
    const btnW = 50, btnH = 18;
    const startX = db.x + (db.w - diffs.length * (btnW + 8)) / 2;
    diffs.forEach((d, i) => {
      const bx = startX + i * (btnW + 8);
      const by = db.y + (db.h - btnH) / 2;
      if (x >= bx && x <= bx + btnW && y >= by && y <= by + btnH) {
        game.difficulty = d;
        localStorage.setItem('turtle_merge_difficulty', d);
        game.reset();
      }
    });
  }
}

function hitTest(x, y, rect) {
  return rect && x >= rect.x && x <= rect.x + rect.w && y >= rect.y && y <= rect.y + rect.h;
}

function shareScore() {
  const maxTurtle = Math.max(...game.discoveredLevels);
  const name = TURTLES[maxTurtle]?.name || '草龟';
  const text = `🐢 我在【合成大乌龟】中获得了 ${game.score} 分！最高合成到了${name}！来挑战我吧 →`;
  navigator.clipboard?.writeText(text).then(() => {
    scorePopups.push({ x: layout.width / 2, y: layout.height / 2 - 50, text: '已复制到剪贴板!', life: 1.5, maxLife: 1.5, fontSize: 16 });
  });
}
```

- [ ] **Step 6: Test full UI flow**

Test: see HUD with score, difficulty buttons work, preview shows next turtle, bottom bar lights up discovered turtles. Trigger game over (stack above line), see panel with score, restart and share buttons work.

- [ ] **Step 7: Commit**

```bash
git add merge-turtle.html
git commit -m "feat: implement complete UI layer with HUD, difficulty selector, game over panel, and share"
```

---

### Task 9: Game Loop + Game Over Logic

**Files:**
- Modify: `merge-turtle.html`

- [ ] **Step 1: Implement the main game loop**

Replace the placeholder game loop with the real one:

```javascript
// === GAME LOOP ===
let lastTime = 0;

function gameLoop(timestamp) {
  const dt = Math.min((timestamp - lastTime) / 1000, 0.05); // cap at 50ms
  lastTime = timestamp;

  if (game.state === 'playing') {
    // Drop cooldown
    if (!game.canDrop) {
      game.dropCooldownTimer -= dt;
      if (game.dropCooldownTimer <= 0) {
        game.canDrop = true;
      }
    }

    // Physics
    physicsStep(dt);

    // Age tracking (skip game-over check for freshly dropped turtles)
    for (const body of world.bodies) body.age += dt;

    // Game over check: any body above line for 2 seconds (skip bodies younger than 1s)
    let anyAbove = false;
    for (const body of world.bodies) {
      if (body.age > 1.0 && body.y - body.radius < layout.gameOverLineY) {
        anyAbove = true;
        break;
      }
    }
    if (anyAbove) {
      game.gameOverTimer += dt;
      if (game.gameOverTimer >= GAME.gameOverDelay) {
        game.state = 'gameover';
        if (game.score > game.highScore) {
          game.highScore = game.score;
          localStorage.setItem('turtle_merge_high_score', game.highScore.toString());
        }
        playGameOverSound();
        if (navigator.vibrate) navigator.vibrate(200);
      }
    } else {
      game.gameOverTimer = 0;
    }
  }

  // Update particles (always, even during game over)
  updateParticles(dt);

  // === RENDER ===
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  renderHUD(ctx);
  renderDifficultyBar(ctx);
  renderPreview(ctx);
  renderDropZone(ctx);
  renderGameArea(ctx);
  renderBottomBar(ctx);

  if (game.state === 'gameover') {
    renderGameOverPanel(ctx);
  }

  requestAnimationFrame(gameLoop);
}

// === INIT ===
game.difficulty = localStorage.getItem('turtle_merge_difficulty') || 'normal';
computeLayout();
game.reset();
requestAnimationFrame(gameLoop);
```

- [ ] **Step 2: Test complete game flow**

Full play test:
1. Open game → see menu with difficulty selector
2. Select difficulty → tap to aim → release to drop turtle
3. Merge same turtles → particles + sound + score
4. Stack above line for 2 seconds → game over panel
5. Restart → fresh game
6. Share → clipboard text
7. Close and reopen → high score and difficulty persist

- [ ] **Step 3: Commit**

```bash
git add merge-turtle.html
git commit -m "feat: implement main game loop with game over detection and complete game flow"
```

---

### Task 10: Polish + Performance + Mobile Compatibility

**Files:**
- Modify: `merge-turtle.html`

- [ ] **Step 1: Add safe area handling for notched phones**

```css
body { padding: env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left); }
```

Update `resize()` to account for safe area insets in layout computation.

- [ ] **Step 2: Add spatial grid optimization for collision detection**

When body count exceeds ~20, switch to spatial grid for broad-phase collision detection:

```javascript
function detectCollisionsOptimized(bodies, area) {
  if (bodies.length < 20) return detectCollisions(bodies, area);

  const cellSize = 80; // slightly larger than biggest turtle
  const grid = {};
  // ... spatial grid implementation
}
```

- [ ] **Step 3: Add roundRect polyfill for older browsers**

```javascript
if (!CanvasRenderingContext2D.prototype.roundRect) {
  CanvasRenderingContext2D.prototype.roundRect = function(x, y, w, h, r) {
    if (typeof r === 'number') r = [r, r, r, r];
    this.moveTo(x + r[0], y);
    this.lineTo(x + w - r[1], y);
    this.quadraticCurveTo(x + w, y, x + w, y + r[1]);
    this.lineTo(x + w, y + h - r[2]);
    this.quadraticCurveTo(x + w, y + h, x + w - r[2], y + h);
    this.lineTo(x + r[3], y + h);
    this.quadraticCurveTo(x, y + h, x, y + h - r[3]);
    this.lineTo(x, y + r[0]);
    this.quadraticCurveTo(x, y, x + r[0], y);
    this.closePath();
  };
}
```

- [ ] **Step 4: Prevent WeChat browser quirks**

Add at top of `<script>`:
```javascript
// Prevent pull-to-refresh and bounce scroll in WeChat
document.addEventListener('touchmove', (e) => e.preventDefault(), { passive: false });
// Prevent double-tap zoom
let lastTouchEnd = 0;
document.addEventListener('touchend', (e) => {
  const now = Date.now();
  if (now - lastTouchEnd < 300) e.preventDefault();
  lastTouchEnd = now;
}, { passive: false });
```

- [ ] **Step 5: Final play test on mobile**

Test on actual phone (or mobile simulator):
- WeChat browser: open link, verify no scroll/zoom interference
- Touch aim + drop works smoothly
- Performance: 60fps with 30+ turtles
- Sound plays after first tap
- Vibration feedback works
- Game over → share → clipboard works
- Difficulty persists across sessions

- [ ] **Step 6: Commit**

```bash
git add merge-turtle.html
git commit -m "feat: add mobile compatibility, performance optimization, and WeChat browser fixes"
```

---

## Summary

| Task | Description | Key Files |
|------|-------------|-----------|
| 1 | HTML scaffold + Canvas | `merge-turtle.html` (create) |
| 2 | Constants, config, layout | `merge-turtle.html` |
| 3 | Turtle renderer (9 types) | `merge-turtle.html` |
| 4 | Physics engine core | `merge-turtle.html` |
| 5 | Merge logic + particles | `merge-turtle.html` |
| 6 | Audio engine (Web Audio) | `merge-turtle.html` |
| 7 | Input handler + drop | `merge-turtle.html` |
| 8 | UI layer (HUD, panels) | `merge-turtle.html` |
| 9 | Game loop + game over | `merge-turtle.html` |
| 10 | Polish + mobile compat | `merge-turtle.html` |
