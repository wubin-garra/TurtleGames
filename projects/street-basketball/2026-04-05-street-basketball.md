# 街头篮球 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a graffiti-style 2D side-view basketball shooting game with swipe controls, 15 levels + endless mode, combo system, 6 characters, weather effects, and power-ups using Phaser 3.

**Architecture:** Single HTML file with Phaser 3 loaded via CDN. Three Phaser Scenes (MenuScene, GameScene, ResultScene) handle all game states. All assets are programmatically drawn using Canvas 2D graphics — no external images. Data persists in localStorage under the `streetball` key.

**Tech Stack:** Phaser 3 (CDN), Arcade Physics, Web Audio API, Canvas 2D drawing, localStorage

---

## File Structure

- **Create:** `street-basketball.html` — the entire game (single file, all scenes, all logic)
- **Modify:** `index.html` — add street basketball to the game library selector

---

### Task 1: Phaser Boilerplate + Graffiti Background

Set up the Phaser 3 game instance, create a placeholder GameScene, and render the graffiti-style court background.

**Files:**
- Create: `street-basketball.html`

- [ ] **Step 1: Create the HTML shell with Phaser CDN**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>🏀 Street Basketball - 街头篮球</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 100%; height: 100%; overflow: hidden; background: #f5f0e0; }
canvas { display: block; margin: 0 auto; }
</style>
</head>
<body>
<script src="https://cdn.jsdelivr.net/npm/phaser@3.60.0/dist/phaser.min.js"></script>
<script>
// Game config
const CONFIG = {
  WIDTH: 800,
  HEIGHT: 450,
  GROUND_Y: 340, // y position of the ground line
  GRAVITY: 800,
  COLORS: {
    paper: '#f5f0e0',
    paperDark: '#e8dcc8',
    ink: '#333333',
    red: '#ff3366',
    blue: '#3366ff',
    orange: '#ff8833',
    green: '#44cc44',
    yellow: '#ffcc00',
    purple: '#6666cc',
    brown: '#8B7355',
    brownLight: '#9B8365',
    white: '#ffffff',
    rimRed: '#ff3300',
  }
};

// --- GameScene placeholder ---
class GameScene extends Phaser.Scene {
  constructor() { super('GameScene'); }
  create() {
    this.drawCourt();
  }

  drawCourt() {
    const g = this.add.graphics();
    // Paper background
    g.fillStyle(0xf5f0e0);
    g.fillRect(0, 0, CONFIG.WIDTH, CONFIG.HEIGHT);
    // Paper lines (notebook texture)
    g.lineStyle(1, 0x000000, 0.03);
    for (let y = 0; y < CONFIG.HEIGHT; y += 29) {
      g.lineBetween(0, y, CONFIG.WIDTH, y);
    }
    // Brick wall (upper portion)
    this.drawBrickWall(g);
    // Ground
    g.fillStyle(0x8B7355);
    g.fillRect(0, CONFIG.GROUND_Y, CONFIG.WIDTH, CONFIG.HEIGHT - CONFIG.GROUND_Y);
    // Ground line
    g.lineStyle(3, 0x333333, 0.6);
    g.lineBetween(0, CONFIG.GROUND_Y, CONFIG.WIDTH, CONFIG.GROUND_Y);
    // Court line
    g.lineStyle(2, 0xffffff, 0.4);
    g.lineBetween(CONFIG.WIDTH * 0.25, CONFIG.HEIGHT - 30, CONFIG.WIDTH * 0.7, CONFIG.HEIGHT - 30);
  }

  drawBrickWall(g) {
    const wallH = CONFIG.GROUND_Y;
    const brickW = 46;
    const brickH = 22;
    const mortarW = 2;
    g.fillStyle(0xc4a070, 0.35);
    for (let row = 0; row < Math.ceil(wallH / (brickH + mortarW)); row++) {
      const offsetX = (row % 2) * (brickW / 2);
      for (let col = -1; col < Math.ceil(CONFIG.WIDTH / (brickW + mortarW)) + 1; col++) {
        const x = col * (brickW + mortarW) + offsetX;
        const y = row * (brickH + mortarW);
        g.fillRect(x, y, brickW, brickH);
      }
    }
  }
}

// --- Phaser Game ---
const game = new Phaser.Game({
  type: Phaser.CANVAS,
  width: CONFIG.WIDTH,
  height: CONFIG.HEIGHT,
  backgroundColor: CONFIG.COLORS.paper,
  parent: document.body,
  physics: {
    default: 'arcade',
    arcade: { gravity: { y: CONFIG.GRAVITY }, debug: false }
  },
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH
  },
  scene: [GameScene]
});
</script>
</body>
</html>
```

- [ ] **Step 2: Open in browser to verify**

Open `street-basketball.html` in browser. Expected: a canvas with notebook-textured paper background, faint brick wall pattern in the upper area, brown ground at the bottom with a dark line separating wall from ground, and a faint white court line.

- [ ] **Step 3: Commit**

```bash
git add street-basketball.html
git commit -m "feat(streetball): init Phaser 3 boilerplate with graffiti court background"
```

---

### Task 2: Hoop, Backboard, and Graffiti Decorations

Draw the basketball hoop (pole, backboard, rim, net) and wall graffiti decorations using hand-drawn style graphics.

**Files:**
- Modify: `street-basketball.html`

- [ ] **Step 1: Add hand-drawn line helper and hoop drawing**

Add a `drawWobblyLine` utility that draws lines with slight random offsets to simulate hand-drawn style. Then add `drawHoop` method that draws the pole, backboard, rim, and a dashed net. Place it at approximately x=600, with the rim at y=185.

```javascript
// Add to GameScene class:

drawWobblyLine(g, x1, y1, x2, y2, thickness, color, alpha) {
  g.lineStyle(thickness, color, alpha || 1);
  const points = [];
  const steps = Math.max(4, Math.floor(Math.hypot(x2 - x1, y2 - y1) / 15));
  for (let i = 0; i <= steps; i++) {
    const t = i / steps;
    const wobble = (i === 0 || i === steps) ? 0 : (Math.random() - 0.5) * 3;
    points.push({
      x: x1 + (x2 - x1) * t + wobble,
      y: y1 + (y2 - y1) * t + wobble
    });
  }
  g.beginPath();
  g.moveTo(points[0].x, points[0].y);
  for (let i = 1; i < points.length; i++) {
    g.lineTo(points[i].x, points[i].y);
  }
  g.strokePath();
}

drawHoop(g) {
  const poleX = 610;
  const rimX = 620;
  const rimY = 185;
  const rimW = 50;
  // Pole
  g.fillStyle(0x666666);
  g.fillRect(poleX - 4, rimY - 5, 8, CONFIG.GROUND_Y - rimY + 5);
  g.lineStyle(2, 0x444444);
  g.strokeRect(poleX - 4, rimY - 5, 8, CONFIG.GROUND_Y - rimY + 5);
  // Backboard
  g.fillStyle(0xffffff, 0.85);
  g.fillRect(poleX - 28, rimY - 40, 55, 38);
  g.lineStyle(3, 0x333333);
  g.strokeRect(poleX - 28, rimY - 40, 55, 38);
  // Rim
  g.lineStyle(4, 0xff3300);
  g.beginPath();
  g.arc(rimX + rimW / 2, rimY + 4, rimW / 2, 0, Math.PI, false);
  g.strokePath();
  // Net (dashed lines)
  g.lineStyle(1.5, 0xffffff, 0.5);
  const netTop = rimY + 4;
  const netBottom = rimY + 40;
  for (let i = 0; i <= 4; i++) {
    const x = rimX + i * (rimW / 4);
    const sway = (Math.random() - 0.5) * 4;
    g.lineBetween(x, netTop, x + sway, netBottom);
  }
}
```

- [ ] **Step 2: Add graffiti wall decorations**

```javascript
drawGraffiti(g) {
  // "BALL IS LIFE" text
  const titleText = this.add.text(25, 20, 'BALL IS LIFE', {
    fontFamily: "'Arial Black', sans-serif",
    fontSize: '22px',
    fontStyle: 'bold',
    color: CONFIG.COLORS.red,
  });
  titleText.setAngle(-6);
  titleText.setShadow(2, 2, 'rgba(0,0,0,0.2)', 0);

  // Random paint splashes
  const splashColors = [0x44cc44, 0xffcc00, 0xff3366, 0x6666cc];
  for (let i = 0; i < 5; i++) {
    const color = Phaser.Utils.Array.GetRandom(splashColors);
    const x = Phaser.Math.Between(50, CONFIG.WIDTH - 100);
    const y = Phaser.Math.Between(30, CONFIG.GROUND_Y - 60);
    const r = Phaser.Math.Between(8, 20);
    g.fillStyle(color, Phaser.Math.FloatBetween(0.15, 0.35));
    g.fillCircle(x, y, r);
  }

  // "STREET" star text
  const streetText = this.add.text(CONFIG.WIDTH - 130, 80, '★ STREET ★', {
    fontFamily: "'Arial Black', sans-serif",
    fontSize: '13px',
    color: CONFIG.COLORS.purple,
  });
  streetText.setAngle(4);
  streetText.setAlpha(0.5);
}
```

- [ ] **Step 3: Call drawHoop and drawGraffiti in create()**

Update `create()` to call `this.drawHoop(g)` after drawing the ground, and `this.drawGraffiti(g)` after the hoop.

- [ ] **Step 4: Verify in browser**

Open in browser. Expected: the court now has a basketball hoop on the right side with pole, white backboard, red rim, and dangling net lines. Wall has "BALL IS LIFE" graffiti text rotated slightly, colored paint splashes, and "STREET" text.

- [ ] **Step 5: Commit**

```bash
git add street-basketball.html
git commit -m "feat(streetball): add hand-drawn hoop, backboard, net, and graffiti decorations"
```

---

### Task 3: Basketball Sprite + Swipe-to-Shoot Controls

Create the basketball as an Arcade Physics sprite (drawn via Canvas texture), implement swipe gesture detection, and launch the ball along the swipe vector.

**Files:**
- Modify: `street-basketball.html`

- [ ] **Step 1: Create basketball texture programmatically**

Add a `createTextures()` method called at start of `create()`. Generates a basketball texture using Canvas:

```javascript
createTextures() {
  // Basketball texture
  const ballSize = 28;
  const ballCanvas = this.textures.createCanvas('basketball', ballSize, ballSize);
  const ctx = ballCanvas.context;
  const cx = ballSize / 2, cy = ballSize / 2, r = ballSize / 2 - 2;

  // Ball body
  const grad = ctx.createRadialGradient(cx - 3, cy - 3, 2, cx, cy, r);
  grad.addColorStop(0, '#ff9933');
  grad.addColorStop(1, '#cc6600');
  ctx.fillStyle = grad;
  ctx.beginPath();
  ctx.arc(cx, cy, r, 0, Math.PI * 2);
  ctx.fill();

  // Lines on ball
  ctx.strokeStyle = '#884400';
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.moveTo(cx - r, cy);
  ctx.lineTo(cx + r, cy);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(cx, cy - r);
  ctx.lineTo(cx, cy + r);
  ctx.stroke();

  // Outline
  ctx.strokeStyle = '#333333';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(cx, cy, r, 0, Math.PI * 2);
  ctx.stroke();

  ballCanvas.refresh();
}
```

- [ ] **Step 2: Add player position and ball spawn**

```javascript
// In GameScene, add properties:
// this.playerX = 160
// this.playerY = CONFIG.GROUND_Y - 60

// In create(), after drawing court:
this.createTextures();
this.spawnBall();

// Method:
spawnBall() {
  if (this.ball) this.ball.destroy();
  this.ball = this.physics.add.sprite(this.playerX + 20, this.playerY - 20, 'basketball');
  this.ball.setCircle(14);
  this.ball.setBounce(0.6);
  this.ball.body.setAllowGravity(false); // gravity off until shot
  this.ball.setCollideWorldBounds(true);
}
```

- [ ] **Step 3: Implement swipe detection**

```javascript
setupInput() {
  this.swipeStart = null;
  this.swipeTrail = [];
  this.trajectoryGraphics = this.add.graphics();

  this.input.on('pointerdown', (pointer) => {
    if (this.isShooting) return;
    this.swipeStart = { x: pointer.x, y: pointer.y, time: pointer.downTime };
    this.swipeTrail = [];
  });

  this.input.on('pointermove', (pointer) => {
    if (!this.swipeStart || this.isShooting) return;
    this.swipeTrail.push({ x: pointer.x, y: pointer.y });
    this.drawTrajectoryPreview(pointer);
  });

  this.input.on('pointerup', (pointer) => {
    if (!this.swipeStart || this.isShooting) return;
    const dx = pointer.x - this.swipeStart.x;
    const dy = pointer.y - this.swipeStart.y;
    const dt = pointer.upTime - this.swipeStart.time;
    const dist = Math.hypot(dx, dy);

    this.trajectoryGraphics.clear();

    if (dist > 30 && dt < 1000) { // valid swipe
      this.shootBall(dx, dy, dt);
    }
    this.swipeStart = null;
    this.swipeTrail = [];
  });
}
```

- [ ] **Step 4: Implement shoot mechanics**

```javascript
shootBall(dx, dy, dt) {
  this.isShooting = true;
  const speed = Math.min(Math.hypot(dx, dy) / dt * 800, 700);
  const angle = Math.atan2(dy, dx);
  // Invert Y because swipe up = negative dy but we want upward velocity
  const vx = Math.cos(angle) * speed;
  const vy = Math.sin(angle) * speed;

  this.ball.body.setAllowGravity(true);
  this.ball.setVelocity(vx, vy);
  this.ball.setAngularVelocity(vx * 0.5);
}

drawTrajectoryPreview(pointer) {
  const g = this.trajectoryGraphics;
  g.clear();
  if (!this.swipeStart) return;
  const dx = pointer.x - this.swipeStart.x;
  const dy = pointer.y - this.swipeStart.y;
  const dist = Math.hypot(dx, dy);
  if (dist < 20) return;

  const speed = Math.min(dist * 2, 700);
  const angle = Math.atan2(dy, dx);
  const vx = Math.cos(angle) * speed;
  const vy = Math.sin(angle) * speed;

  g.lineStyle(2, 0xff6600, 0.5);
  g.beginPath();
  let px = this.ball.x, py = this.ball.y;
  g.moveTo(px, py);
  const dt = 1 / 60;
  for (let i = 0; i < 40; i++) {
    px += vx * dt;
    py += vy * dt;
    vy += CONFIG.GRAVITY * dt;
    if (i % 3 === 0) { // dashed effect
      g.lineTo(px, py);
    } else {
      g.moveTo(px, py);
    }
  }
  g.strokePath();
}
```

- [ ] **Step 5: Call setupInput() in create(), add isShooting flag**

Add `this.isShooting = false;` and `this.playerX = 160; this.playerY = CONFIG.GROUND_Y - 60;` before drawing, then call `this.setupInput();` at end of `create()`.

- [ ] **Step 6: Verify in browser**

Open and test. Expected: basketball appears near the left side. Swiping shows a dashed orange trajectory preview. Releasing launches the ball along the swipe direction with gravity pulling it down. Ball bounces when hitting screen edges.

- [ ] **Step 7: Commit**

```bash
git add street-basketball.html
git commit -m "feat(streetball): add basketball sprite with swipe-to-shoot controls and trajectory preview"
```

---

### Task 4: Scoring — Rim Collision, Swish Detection, Ball Reset

Detect when the ball goes through the hoop (swish vs bank shot), display score popups, and reset ball for next shot.

**Files:**
- Modify: `street-basketball.html`

- [ ] **Step 1: Create invisible sensor zones for scoring**

```javascript
setupHoop() {
  // Rim position constants
  this.rimX = 620;
  this.rimY = 185;
  this.rimW = 50;

  // Scoring zone (invisible, below rim)
  this.scoreZone = this.add.zone(this.rimX + this.rimW / 2, this.rimY + 15, this.rimW - 10, 10);
  this.physics.add.existing(this.scoreZone, true); // static body

  // Backboard (physical, for bank shots)
  this.backboard = this.add.zone(610, this.rimY - 20, 8, 38);
  this.physics.add.existing(this.backboard, true);

  // Rim edges (physical, for bouncing)
  this.rimLeft = this.add.zone(this.rimX, this.rimY + 4, 6, 6);
  this.physics.add.existing(this.rimLeft, true);
  this.rimRight = this.add.zone(this.rimX + this.rimW, this.rimY + 4, 6, 6);
  this.physics.add.existing(this.rimRight, true);

  // Ground zone for miss detection
  this.groundZone = this.add.zone(CONFIG.WIDTH / 2, CONFIG.GROUND_Y + 20, CONFIG.WIDTH, 10);
  this.physics.add.existing(this.groundZone, true);

  // Track if ball hit backboard (for bank shot detection)
  this.hitBackboard = false;

  this.physics.add.collider(this.ball, this.backboard, () => {
    this.hitBackboard = true;
  });
  this.physics.add.collider(this.ball, this.rimLeft);
  this.physics.add.collider(this.ball, this.rimRight);

  this.physics.add.overlap(this.ball, this.scoreZone, () => {
    if (!this.isShooting || this.scored) return;
    // Ball must be moving downward to count
    if (this.ball.body.velocity.y < 0) return;
    this.scored = true;
    this.onScore();
  });

  this.physics.add.overlap(this.ball, this.groundZone, () => {
    if (!this.isShooting || this.scored) return;
    this.onMiss();
  });
}
```

- [ ] **Step 2: Implement scoring logic with distance-based points**

```javascript
onScore() {
  const distance = this.rimX - this.playerX;
  let basePoints;
  let distLabel;
  if (distance < 300) {
    basePoints = 100;
    distLabel = '';
  } else if (distance < 400) {
    basePoints = 150;
    distLabel = '中投 ';
  } else {
    basePoints = 200;
    distLabel = '远投 ';
  }

  let bonus = 0;
  let shotType = '';
  if (!this.hitBackboard) {
    bonus = 50;
    shotType = 'SWISH!';
  } else {
    bonus = 30;
    shotType = 'BANK!';
  }

  this.combo++;
  const multiplier = Math.min(this.combo, 10);
  const totalPoints = (basePoints + bonus) * multiplier;
  this.score += totalPoints;

  // Score popup
  this.showScorePopup(shotType, totalPoints, multiplier);

  // Reset ball after delay
  this.time.delayedCall(800, () => this.resetBall());
}

onMiss() {
  this.combo = 0;
  this.showMissPopup();
  this.time.delayedCall(600, () => this.resetBall());
}

resetBall() {
  this.isShooting = false;
  this.scored = false;
  this.hitBackboard = false;
  this.spawnBall();
  // Re-register colliders (ball was re-created)
  this.setupHoopColliders();
}
```

- [ ] **Step 3: Add score popup text with graffiti style**

```javascript
showScorePopup(shotType, points, multiplier) {
  const x = this.rimX + this.rimW / 2;
  const y = this.rimY - 30;

  const typeText = this.add.text(x, y, shotType, {
    fontFamily: "'Arial Black', sans-serif",
    fontSize: '28px',
    color: shotType === 'SWISH!' ? CONFIG.COLORS.red : CONFIG.COLORS.orange,
  }).setOrigin(0.5).setAngle(Phaser.Math.Between(-12, 12));
  typeText.setShadow(2, 2, CONFIG.COLORS.yellow, 0);

  const pointsText = this.add.text(x, y + 30, `+${points}`, {
    fontFamily: "'Arial Black', sans-serif",
    fontSize: '20px',
    color: CONFIG.COLORS.ink,
  }).setOrigin(0.5);

  if (multiplier > 1) {
    const comboText = this.add.text(x, y + 52, `x${multiplier} COMBO`, {
      fontFamily: "'Arial Black', sans-serif",
      fontSize: '14px',
      color: CONFIG.COLORS.red,
    }).setOrigin(0.5);
    this.tweens.add({
      targets: comboText, y: y + 32, alpha: 0, duration: 1000,
      ease: 'Power2', onComplete: () => comboText.destroy()
    });
  }

  this.tweens.add({
    targets: typeText, y: y - 40, alpha: 0, duration: 1000,
    ease: 'Power2', onComplete: () => typeText.destroy()
  });
  this.tweens.add({
    targets: pointsText, y: y - 10, alpha: 0, duration: 1000,
    ease: 'Power2', onComplete: () => pointsText.destroy()
  });
}

showMissPopup() {
  const texts = ['MISS...', 'NOPE', 'AIR BALL'];
  const text = this.add.text(CONFIG.WIDTH / 2, CONFIG.HEIGHT / 2 - 30,
    Phaser.Utils.Array.GetRandom(texts), {
      fontFamily: "'Arial Black', sans-serif",
      fontSize: '24px',
      color: '#999',
    }).setOrigin(0.5).setAngle(Phaser.Math.Between(-5, 5));
  this.tweens.add({
    targets: text, alpha: 0, y: text.y - 30, duration: 800,
    onComplete: () => text.destroy()
  });
}
```

- [ ] **Step 4: Wire it all together**

Add `this.score = 0; this.combo = 0; this.scored = false;` in `create()`. Call `this.setupHoop()` after `spawnBall()`. Extract collider setup into `setupHoopColliders()` so it can be re-called on ball respawn.

- [ ] **Step 5: Add HUD display**

```javascript
createHUD() {
  this.scoreText = this.add.text(20, 12, '⭐ 0', {
    fontFamily: "'Arial Black', sans-serif",
    fontSize: '18px',
    color: CONFIG.COLORS.ink,
  });
  // Styled HUD backgrounds (hand-drawn boxes)
  const hudBg = this.add.graphics();
  hudBg.fillStyle(0xffffff, 0.7);
  hudBg.lineStyle(3, 0x333333);
  hudBg.fillRoundedRect(10, 6, 110, 32, 10);
  hudBg.strokeRoundedRect(10, 6, 110, 32, 10);
  hudBg.setAngle(-1);

  this.comboText = this.add.text(CONFIG.WIDTH / 2, 12, '', {
    fontFamily: "'Arial Black', sans-serif",
    fontSize: '18px',
    color: CONFIG.COLORS.red,
  }).setOrigin(0.5, 0);
}

// Call in update():
updateHUD() {
  this.scoreText.setText(`⭐ ${this.score}`);
  if (this.combo > 1) {
    this.comboText.setText(`COMBO x${this.combo} 🔥`);
    this.comboText.setVisible(true);
  } else {
    this.comboText.setVisible(false);
  }
}
```

- [ ] **Step 6: Add update() method**

```javascript
update() {
  this.updateHUD();

  // Out of bounds check (ball flies off screen)
  if (this.ball && this.isShooting) {
    if (this.ball.x < -50 || this.ball.x > CONFIG.WIDTH + 50 || this.ball.y > CONFIG.HEIGHT + 50) {
      this.onMiss();
    }
  }
}
```

- [ ] **Step 7: Verify in browser**

Test: swipe up-right to shoot at the hoop. Expected: ball flies in arc, going through the score zone triggers "SWISH!" or "BANK!" popup with points. Missing shows "MISS..." text. Score accumulates in the HUD. Combo counter shows on consecutive hits.

- [ ] **Step 8: Commit**

```bash
git add street-basketball.html
git commit -m "feat(streetball): add scoring system with swish/bank detection, combo counter, and HUD"
```

---

### Task 5: Player Character Drawing

Draw a graffiti-style stick figure player character with a simple shooting animation.

**Files:**
- Modify: `street-basketball.html`

- [ ] **Step 1: Create player character drawing**

```javascript
drawPlayer() {
  if (this.playerGraphics) this.playerGraphics.destroy();
  this.playerGraphics = this.add.graphics();
  const g = this.playerGraphics;
  const px = this.playerX;
  const py = this.playerY;

  // Legs
  g.lineStyle(3, 0x333333);
  g.lineBetween(px - 6, py + 30, px - 10, py + 52);
  g.lineBetween(px + 6, py + 30, px + 10, py + 52);

  // Body (jersey)
  g.fillStyle(0x3366ff);
  g.fillRoundedRect(px - 13, py, 26, 32, 6);
  g.lineStyle(3, 0x333333);
  g.strokeRoundedRect(px - 13, py, 26, 32, 6);
  // Jersey number
  this.playerNumber = this.add.text(px, py + 14, '23', {
    fontFamily: "'Arial Black', sans-serif",
    fontSize: '10px',
    color: '#fff',
  }).setOrigin(0.5);

  // Head
  g.fillStyle(0xffddaa);
  g.fillCircle(px, py - 10, 14);
  g.lineStyle(3, 0x333333);
  g.strokeCircle(px, py - 10, 14);
  // Eyes
  g.fillStyle(0x333333);
  g.fillCircle(px - 5, py - 12, 2.5);
  g.fillCircle(px + 5, py - 12, 2.5);
  // Smile
  g.lineStyle(2, 0x333333);
  g.beginPath();
  g.arc(px, py - 6, 6, 0.1, Math.PI - 0.1, false);
  g.strokePath();
  // Headband
  g.fillStyle(0xff3366);
  g.fillRoundedRect(px - 16, py - 22, 32, 7, 3);

  // Shooting arm
  g.lineStyle(3, 0xffddaa);
  g.lineBetween(px + 13, py + 5, px + 28, py - 15);
  g.lineStyle(2, 0x333333);
  g.lineBetween(px + 13, py + 5, px + 28, py - 15);
}
```

- [ ] **Step 2: Add simple shooting animation**

```javascript
playShootAnimation() {
  // Quick arm raise tween via redrawing
  const timeline = this.tweens.createTimeline();

  // Screen shake on powerful shots
  this.cameras.main.shake(100, 0.003);

  // Player jump effect
  if (this.playerGraphics) {
    timeline.add({
      targets: this.playerGraphics,
      y: -15,
      duration: 150,
      ease: 'Power2',
      yoyo: true,
    });
    if (this.playerNumber) {
      timeline.add({
        targets: this.playerNumber,
        y: this.playerNumber.y - 15,
        duration: 150,
        ease: 'Power2',
        yoyo: true,
        offset: 0,
      });
    }
  }
  timeline.play();
}
```

- [ ] **Step 3: Call drawPlayer() in create() and playShootAnimation() in shootBall()**

- [ ] **Step 4: Verify in browser**

Expected: a graffiti stick-figure player with blue jersey #23, headband, and shooting arm stands on the left. When shooting, the player jumps slightly upward.

- [ ] **Step 5: Commit**

```bash
git add street-basketball.html
git commit -m "feat(streetball): add graffiti stick-figure player with shoot animation"
```

---

### Task 6: Timer + Endless Mode Core Loop

Implement the 60-second countdown timer, score bonus time on consecutive baskets, game over condition, and basic endless mode flow.

**Files:**
- Modify: `street-basketball.html`

- [ ] **Step 1: Add game state management**

```javascript
// Add to CONFIG:
CONFIG.ENDLESS = {
  INITIAL_TIME: 60,
  BONUS_TIME: 5,
  BONUS_EVERY: 5, // every 5 baskets
};

// In GameScene create():
this.gameMode = 'endless'; // 'endless' or 'level'
this.timeLeft = CONFIG.ENDLESS.INITIAL_TIME;
this.basketCount = 0;
this.isGameOver = false;
this.gameStarted = false;
```

- [ ] **Step 2: Add countdown timer**

```javascript
createTimer() {
  this.timerText = this.add.text(CONFIG.WIDTH - 20, 12, '', {
    fontFamily: "'Arial Black', sans-serif",
    fontSize: '18px',
    color: CONFIG.COLORS.ink,
  }).setOrigin(1, 0);

  // Timer background
  const timerBg = this.add.graphics();
  timerBg.fillStyle(0xffffff, 0.7);
  timerBg.lineStyle(3, 0x333333);
  timerBg.fillRoundedRect(CONFIG.WIDTH - 120, 6, 110, 32, 10);
  timerBg.strokeRoundedRect(CONFIG.WIDTH - 120, 6, 110, 32, 10);
  timerBg.setAngle(0.5);

  this.timerEvent = this.time.addEvent({
    delay: 1000,
    callback: () => {
      if (this.isGameOver || !this.gameStarted) return;
      this.timeLeft--;
      if (this.timeLeft <= 0) {
        this.timeLeft = 0;
        this.gameOver();
      }
    },
    loop: true,
  });
}

updateTimer() {
  const mins = Math.floor(this.timeLeft / 60);
  const secs = this.timeLeft % 60;
  this.timerText.setText(`⏱ ${mins}:${secs.toString().padStart(2, '0')}`);

  // Flash red when low
  if (this.timeLeft <= 10 && this.timeLeft > 0) {
    this.timerText.setColor(this.timeLeft % 2 === 0 ? CONFIG.COLORS.red : CONFIG.COLORS.ink);
  }
}
```

- [ ] **Step 3: Add time bonus on basket streaks**

Update `onScore()` to include:

```javascript
this.basketCount++;
if (this.basketCount % CONFIG.ENDLESS.BONUS_EVERY === 0 && this.gameMode === 'endless') {
  this.timeLeft += CONFIG.ENDLESS.BONUS_TIME;
  // Bonus time popup
  const bonusText = this.add.text(CONFIG.WIDTH - 60, 45, `+${CONFIG.ENDLESS.BONUS_TIME}s!`, {
    fontFamily: "'Arial Black', sans-serif",
    fontSize: '16px',
    color: CONFIG.COLORS.green,
  }).setOrigin(0.5);
  this.tweens.add({
    targets: bonusText, y: 25, alpha: 0, duration: 1000,
    onComplete: () => bonusText.destroy()
  });
}
```

- [ ] **Step 4: Implement game over**

```javascript
gameOver() {
  this.isGameOver = true;
  if (this.ball) this.ball.body.setAllowGravity(false);
  if (this.ball) this.ball.setVelocity(0, 0);

  // Save high score
  this.saveHighScore();

  // Transition to ResultScene
  this.time.delayedCall(500, () => {
    this.scene.start('ResultScene', {
      score: this.score,
      combo: this.maxCombo || 0,
      baskets: this.basketCount,
      mode: this.gameMode,
      level: this.currentLevel || 0,
    });
  });
}

saveHighScore() {
  const data = JSON.parse(localStorage.getItem('streetball') || '{}');
  if (!data.highScore || this.score > data.highScore) {
    data.highScore = this.score;
  }
  localStorage.setItem('streetball', JSON.stringify(data));
}
```

- [ ] **Step 5: Start game on first swipe**

Modify `pointerdown` handler: if `!this.gameStarted`, set `this.gameStarted = true`.

- [ ] **Step 6: Track maxCombo**

In `onScore()`, add: `this.maxCombo = Math.max(this.maxCombo || 0, this.combo);`

- [ ] **Step 7: Call createTimer() in create() and updateTimer() in update()**

- [ ] **Step 8: Verify in browser**

Expected: timer shows "⏱ 1:00" at top right. First swipe starts countdown. Every 5 baskets adds +5s. When timer hits 0, game stops.

- [ ] **Step 9: Commit**

```bash
git add street-basketball.html
git commit -m "feat(streetball): add 60s countdown timer, time bonuses, and game over flow"
```

---

### Task 7: ResultScene — Game Over Screen

Create the results screen showing final score, stats, high score, and a replay button.

**Files:**
- Modify: `street-basketball.html`

- [ ] **Step 1: Create ResultScene class**

```javascript
class ResultScene extends Phaser.Scene {
  constructor() { super('ResultScene'); }

  init(data) {
    this.finalScore = data.score || 0;
    this.maxCombo = data.combo || 0;
    this.baskets = data.baskets || 0;
    this.gameMode = data.mode || 'endless';
    this.level = data.level || 0;
  }

  create() {
    const cx = CONFIG.WIDTH / 2;

    // Paper background
    this.add.graphics()
      .fillStyle(0xf5f0e0)
      .fillRect(0, 0, CONFIG.WIDTH, CONFIG.HEIGHT);

    // Notebook lines
    const g = this.add.graphics();
    g.lineStyle(1, 0x000000, 0.03);
    for (let y = 0; y < CONFIG.HEIGHT; y += 29) {
      g.lineBetween(0, y, CONFIG.WIDTH, y);
    }

    // Title
    this.add.text(cx, 40, 'GAME OVER', {
      fontFamily: "'Arial Black', sans-serif",
      fontSize: '42px',
      color: CONFIG.COLORS.red,
    }).setOrigin(0.5).setShadow(3, 3, CONFIG.COLORS.yellow, 0).setAngle(-2);

    // Score
    this.add.text(cx, 110, `${this.finalScore}`, {
      fontFamily: "'Arial Black', sans-serif",
      fontSize: '56px',
      color: CONFIG.COLORS.ink,
    }).setOrigin(0.5);

    this.add.text(cx, 150, 'POINTS', {
      fontFamily: "'Arial Black', sans-serif",
      fontSize: '14px',
      color: '#999',
    }).setOrigin(0.5);

    // High score
    const data = JSON.parse(localStorage.getItem('streetball') || '{}');
    const isNewHigh = this.finalScore >= (data.highScore || 0);
    if (isNewHigh) {
      const newHighText = this.add.text(cx, 175, '★ NEW HIGH SCORE! ★', {
        fontFamily: "'Arial Black', sans-serif",
        fontSize: '16px',
        color: CONFIG.COLORS.yellow,
      }).setOrigin(0.5).setAngle(Phaser.Math.Between(-3, 3));
      newHighText.setShadow(1, 1, CONFIG.COLORS.ink, 0);
      this.tweens.add({
        targets: newHighText, scaleX: 1.1, scaleY: 1.1,
        duration: 500, yoyo: true, repeat: -1,
      });
    } else {
      this.add.text(cx, 175, `BEST: ${data.highScore || 0}`, {
        fontFamily: "'Arial Black', sans-serif",
        fontSize: '14px',
        color: '#999',
      }).setOrigin(0.5);
    }

    // Stats
    const statsY = 210;
    const stats = [
      { label: '进球', value: this.baskets, icon: '🏀' },
      { label: '最高连击', value: `x${this.maxCombo}`, icon: '🔥' },
    ];
    stats.forEach((s, i) => {
      const x = cx + (i - 0.5) * 140;
      const bg = this.add.graphics();
      bg.fillStyle(0xffffff, 0.6);
      bg.lineStyle(2, 0x333333);
      bg.fillRoundedRect(x - 55, statsY, 110, 55, 8);
      bg.strokeRoundedRect(x - 55, statsY, 110, 55, 8);

      this.add.text(x, statsY + 15, `${s.icon} ${s.value}`, {
        fontFamily: "'Arial Black', sans-serif", fontSize: '20px',
        color: CONFIG.COLORS.ink,
      }).setOrigin(0.5);
      this.add.text(x, statsY + 38, s.label, {
        fontSize: '12px', color: '#999',
      }).setOrigin(0.5);
    });

    // Buttons
    this.createButton(cx, 320, '🔄 REPLAY', CONFIG.COLORS.blue, () => {
      this.scene.start('GameScene', { mode: this.gameMode, level: this.level });
    });

    this.createButton(cx, 370, '🏠 MENU', CONFIG.COLORS.purple, () => {
      this.scene.start('MenuScene');
    });
  }

  createButton(x, y, label, color, callback) {
    const bg = this.add.graphics();
    bg.fillStyle(Phaser.Display.Color.HexStringToColor(color).color, 0.15);
    bg.lineStyle(3, Phaser.Display.Color.HexStringToColor(color).color);
    bg.fillRoundedRect(x - 80, y - 18, 160, 36, 12);
    bg.strokeRoundedRect(x - 80, y - 18, 160, 36, 12);

    const text = this.add.text(x, y, label, {
      fontFamily: "'Arial Black', sans-serif",
      fontSize: '16px',
      color: color,
    }).setOrigin(0.5).setInteractive({ useHandCursor: true });

    text.on('pointerover', () => text.setScale(1.1));
    text.on('pointerout', () => text.setScale(1));
    text.on('pointerdown', callback);
  }
}
```

- [ ] **Step 2: Register ResultScene in Phaser config**

Change the scene array to: `scene: [GameScene, ResultScene]`

- [ ] **Step 3: Verify in browser**

Play until timer runs out. Expected: "GAME OVER" screen with graffiti styling, score, stats, new high score indicator if applicable, REPLAY and MENU buttons. REPLAY restarts the game.

- [ ] **Step 4: Commit**

```bash
git add street-basketball.html
git commit -m "feat(streetball): add graffiti-styled ResultScene with stats and high score"
```

---

### Task 8: MenuScene — Main Menu with Mode Selection

Create the main menu with graffiti styling, game title, mode selection (levels/endless), and a placeholder for character selection.

**Files:**
- Modify: `street-basketball.html`

- [ ] **Step 1: Create MenuScene class**

```javascript
class MenuScene extends Phaser.Scene {
  constructor() { super('MenuScene'); }

  create() {
    const cx = CONFIG.WIDTH / 2;

    // Paper background
    this.add.graphics().fillStyle(0xf5f0e0).fillRect(0, 0, CONFIG.WIDTH, CONFIG.HEIGHT);

    // Notebook lines
    const g = this.add.graphics();
    g.lineStyle(1, 0x000000, 0.03);
    for (let y = 0; y < CONFIG.HEIGHT; y += 29) {
      g.lineBetween(0, y, CONFIG.WIDTH, y);
    }

    // Graffiti splashes
    const splashColors = [0xff3366, 0x44cc44, 0xffcc00, 0x6666cc, 0x3366ff];
    for (let i = 0; i < 8; i++) {
      g.fillStyle(Phaser.Utils.Array.GetRandom(splashColors), Phaser.Math.FloatBetween(0.1, 0.25));
      g.fillCircle(Phaser.Math.Between(30, CONFIG.WIDTH - 30), Phaser.Math.Between(30, CONFIG.HEIGHT - 30), Phaser.Math.Between(10, 30));
    }

    // Title
    this.add.text(cx, 55, '🏀 街头篮球', {
      fontFamily: "'Arial Black', sans-serif",
      fontSize: '48px',
      color: CONFIG.COLORS.ink,
    }).setOrigin(0.5).setAngle(-2);

    this.add.text(cx, 100, 'STREET BASKETBALL', {
      fontFamily: "'Arial Black', sans-serif",
      fontSize: '16px',
      color: CONFIG.COLORS.red,
    }).setOrigin(0.5).setAngle(1);

    // Bouncing basketball decoration
    const ballDeco = this.add.text(cx + 160, 50, '🏀', { fontSize: '30px' }).setOrigin(0.5);
    this.tweens.add({
      targets: ballDeco, y: 40, duration: 600,
      yoyo: true, repeat: -1, ease: 'Bounce.easeOut',
    });

    // Mode buttons
    this.createModeButton(cx, 180, '🏆 关卡模式', '15关挑战 · 3大区域', CONFIG.COLORS.blue, () => {
      this.scene.start('GameScene', { mode: 'level', level: this.getNextLevel() });
    });

    this.createModeButton(cx, 260, '⏱ 无尽挑战', '60秒 · 冲击最高分', CONFIG.COLORS.red, () => {
      this.scene.start('GameScene', { mode: 'endless' });
    });

    // High score display
    const data = JSON.parse(localStorage.getItem('streetball') || '{}');
    if (data.highScore) {
      this.add.text(cx, 340, `🏅 最高分: ${data.highScore}`, {
        fontFamily: "'Arial Black', sans-serif",
        fontSize: '14px',
        color: '#999',
      }).setOrigin(0.5);
    }

    // Character select hint
    this.add.text(cx, 390, '👤 角色选择', {
      fontFamily: "'Arial Black', sans-serif",
      fontSize: '14px',
      color: CONFIG.COLORS.purple,
    }).setOrigin(0.5).setInteractive({ useHandCursor: true })
      .on('pointerdown', () => this.scene.start('CharSelectScene'));

    // Back to library
    this.add.text(20, CONFIG.HEIGHT - 25, '← 返回游戏库', {
      fontSize: '13px', color: '#999',
    }).setInteractive({ useHandCursor: true })
      .on('pointerdown', () => { window.location.href = 'index.html'; });
  }

  createModeButton(x, y, title, subtitle, color, callback) {
    const bg = this.add.graphics();
    const colorNum = Phaser.Display.Color.HexStringToColor(color).color;
    bg.fillStyle(colorNum, 0.1);
    bg.lineStyle(3, colorNum);
    bg.fillRoundedRect(x - 150, y - 25, 300, 60, 14);
    bg.strokeRoundedRect(x - 150, y - 25, 300, 60, 14);

    const titleText = this.add.text(x, y - 5, title, {
      fontFamily: "'Arial Black', sans-serif", fontSize: '20px', color: color,
    }).setOrigin(0.5);

    this.add.text(x, y + 18, subtitle, {
      fontSize: '12px', color: '#888',
    }).setOrigin(0.5);

    const hitArea = this.add.zone(x, y, 300, 60).setInteractive({ useHandCursor: true });
    hitArea.on('pointerover', () => { titleText.setScale(1.05); });
    hitArea.on('pointerout', () => { titleText.setScale(1); });
    hitArea.on('pointerdown', callback);
  }

  getNextLevel() {
    const data = JSON.parse(localStorage.getItem('streetball') || '{}');
    const levels = data.levels || {};
    // Find first uncompleted level
    for (let i = 1; i <= 15; i++) {
      if (!levels[i] || levels[i].stars === 0) return i;
    }
    return 1; // All completed, restart from 1
  }
}
```

- [ ] **Step 2: Update scene registration and make MenuScene the first scene**

Change scene array to: `scene: [MenuScene, GameScene, ResultScene]`

- [ ] **Step 3: Update GameScene.init() to accept mode parameters**

```javascript
init(data) {
  this.gameMode = data?.mode || 'endless';
  this.currentLevel = data?.level || 1;
}
```

- [ ] **Step 4: Verify in browser**

Expected: graffiti-styled menu with game title, two mode buttons (关卡模式 / 无尽挑战), high score display, character select link, and back button. Clicking 无尽挑战 starts the game.

- [ ] **Step 5: Commit**

```bash
git add street-basketball.html
git commit -m "feat(streetball): add MenuScene with mode selection and graffiti styling"
```

---

### Task 9: Level Mode — Level Config, Targets, and Star Rating

Implement the 15-level system with varying difficulty parameters, target scores, star ratings, and level-specific positions.

**Files:**
- Modify: `street-basketball.html`

- [ ] **Step 1: Define level configurations**

```javascript
// Add to CONFIG:
CONFIG.LEVELS = [
  // Area 1: Street Corner (1-5)
  { id: 1, area: 'street', name: '初试身手', target: 300, balls: 10, playerX: 200, wind: 0, weather: 'clear', rimMove: false, obstacles: false, stars: [300, 500, 800] },
  { id: 2, area: 'street', name: '左右开弓', target: 400, balls: 10, playerX: 0, wind: 0, weather: 'clear', rimMove: false, obstacles: false, stars: [400, 700, 1000], randomPos: true },
  { id: 3, area: 'street', name: '移动目标', target: 500, balls: 12, playerX: 180, wind: 0, weather: 'clear', rimMove: true, obstacles: false, stars: [500, 800, 1200] },
  { id: 4, area: 'street', name: '逆风投篮', target: 500, balls: 12, playerX: 160, wind: 2, weather: 'windy', rimMove: false, obstacles: false, stars: [500, 900, 1300] },
  { id: 5, area: 'street', name: '街角之王', target: 800, balls: 0, playerX: 180, wind: 1, weather: 'clear', rimMove: false, obstacles: false, stars: [800, 1200, 1800], timeLimit: 30 },

  // Area 2: City Park (6-10)
  { id: 6, area: 'park', name: '远距离', target: 600, balls: 10, playerX: 120, wind: 1, weather: 'clear', rimMove: false, obstacles: false, stars: [600, 1000, 1500] },
  { id: 7, area: 'park', name: '雨中作战', target: 600, balls: 12, playerX: 150, wind: 0, weather: 'rain', rimMove: false, obstacles: false, stars: [600, 1000, 1500] },
  { id: 8, area: 'park', name: '夜幕降临', target: 700, balls: 12, playerX: 160, wind: 1, weather: 'night', rimMove: false, obstacles: false, stars: [700, 1100, 1600] },
  { id: 9, area: 'park', name: '风雨交加', target: 700, balls: 12, playerX: 140, wind: 3, weather: 'rain', rimMove: true, obstacles: false, stars: [700, 1200, 1800] },
  { id: 10, area: 'park', name: '公园霸主', target: 1000, balls: 0, playerX: 130, wind: 3, weather: 'rain', rimMove: true, obstacles: false, stars: [1000, 1600, 2400], timeLimit: 30, nightOverlay: true },

  // Area 3: Rooftop (11-15)
  { id: 11, area: 'rooftop', name: '天台初探', target: 800, balls: 12, playerX: 130, wind: 2, weather: 'windy', rimMove: false, obstacles: true, stars: [800, 1300, 1900] },
  { id: 12, area: 'rooftop', name: '摇晃篮筐', target: 900, balls: 12, playerX: 140, wind: 2, weather: 'clear', rimMove: true, obstacles: true, stars: [900, 1400, 2100], rimShake: true },
  { id: 13, area: 'rooftop', name: '暴风之夜', target: 900, balls: 12, playerX: 120, wind: 4, weather: 'night', rimMove: false, obstacles: true, stars: [900, 1500, 2200] },
  { id: 14, area: 'rooftop', name: '极限挑战', target: 1000, balls: 14, playerX: 110, wind: 3, weather: 'rain', rimMove: true, obstacles: true, stars: [1000, 1600, 2400], rimShake: true },
  { id: 15, area: 'rooftop', name: '街球传奇', target: 1500, balls: 0, playerX: 110, wind: 4, weather: 'rain', rimMove: true, obstacles: true, stars: [1500, 2200, 3200], timeLimit: 35, nightOverlay: true, rimShake: true },
];
```

- [ ] **Step 2: Update GameScene to load level config**

```javascript
// In GameScene.create(), after init:
if (this.gameMode === 'level') {
  this.levelConfig = CONFIG.LEVELS[this.currentLevel - 1];
  this.ballsLeft = this.levelConfig.balls; // 0 = time-based
  this.timeLeft = this.levelConfig.timeLimit || 0;
  this.playerX = this.levelConfig.playerX || 160;
  this.isTimedLevel = this.levelConfig.timeLimit > 0;
} else {
  this.levelConfig = null;
  this.ballsLeft = Infinity;
  this.timeLeft = CONFIG.ENDLESS.INITIAL_TIME;
  this.isTimedLevel = true;
}
```

- [ ] **Step 3: Add ball counter for non-timed levels**

```javascript
// In createHUD(), add ball counter:
if (this.gameMode === 'level' && !this.isTimedLevel) {
  this.ballsText = this.add.text(CONFIG.WIDTH - 20, 12, '', {
    fontFamily: "'Arial Black', sans-serif",
    fontSize: '18px',
    color: CONFIG.COLORS.ink,
  }).setOrigin(1, 0);
}

// In updateHUD():
if (this.ballsText) {
  this.ballsText.setText(`🏀 x${this.ballsLeft}`);
}
```

- [ ] **Step 4: Add level-end check on each shot**

```javascript
// In resetBall(), add:
if (this.gameMode === 'level' && !this.isTimedLevel) {
  this.ballsLeft--;
  if (this.ballsLeft <= 0) {
    this.time.delayedCall(500, () => this.levelComplete());
    return;
  }
}

levelComplete() {
  const config = this.levelConfig;
  let stars = 0;
  if (this.score >= config.stars[2]) stars = 3;
  else if (this.score >= config.stars[1]) stars = 2;
  else if (this.score >= config.stars[0]) stars = 1;

  // Save level data
  const data = JSON.parse(localStorage.getItem('streetball') || '{}');
  if (!data.levels) data.levels = {};
  const prev = data.levels[config.id] || { stars: 0, best: 0 };
  data.levels[config.id] = {
    stars: Math.max(prev.stars, stars),
    best: Math.max(prev.best, this.score),
  };
  // Update total stars
  let totalStars = 0;
  for (const l of Object.values(data.levels)) totalStars += l.stars;
  data.totalStars = totalStars;
  localStorage.setItem('streetball', JSON.stringify(data));

  this.scene.start('ResultScene', {
    score: this.score,
    combo: this.maxCombo || 0,
    baskets: this.basketCount,
    mode: 'level',
    level: config.id,
    stars: stars,
    target: config.target,
  });
}
```

- [ ] **Step 5: Update ResultScene to show level results with stars**

In `ResultScene.init()`, add `this.stars = data.stars || 0; this.target = data.target || 0;`

Add after the score display in `ResultScene.create()`:

```javascript
if (this.gameMode === 'level') {
  // Star display
  const starY = 170;
  for (let i = 0; i < 3; i++) {
    this.add.text(cx - 40 + i * 40, starY, i < this.stars ? '⭐' : '☆', {
      fontSize: '30px',
    }).setOrigin(0.5);
  }

  // Pass/fail
  const passed = this.stars > 0;
  this.add.text(cx, starY + 35, passed ? 'PASSED!' : 'FAILED...', {
    fontFamily: "'Arial Black', sans-serif",
    fontSize: '16px',
    color: passed ? CONFIG.COLORS.green : CONFIG.COLORS.red,
  }).setOrigin(0.5);

  // Next level button if passed
  if (passed && this.level < 15) {
    this.createButton(cx, 310, '▶ 下一关', CONFIG.COLORS.green, () => {
      this.scene.start('GameScene', { mode: 'level', level: this.level + 1 });
    });
  }
}
```

- [ ] **Step 6: Add level select to MenuScene**

Replace the simple "关卡模式" button action with a transition to a level grid. Add `createLevelGrid()` method showing 15 levels in a 5x3 grid with stars and lock indicators:

```javascript
showLevelSelect() {
  // Clear menu content and show level grid
  this.scene.start('LevelSelectScene');
}
```

Create a new `LevelSelectScene`:

```javascript
class LevelSelectScene extends Phaser.Scene {
  constructor() { super('LevelSelectScene'); }

  create() {
    const cx = CONFIG.WIDTH / 2;
    this.add.graphics().fillStyle(0xf5f0e0).fillRect(0, 0, CONFIG.WIDTH, CONFIG.HEIGHT);

    this.add.text(cx, 30, '🏆 选择关卡', {
      fontFamily: "'Arial Black', sans-serif",
      fontSize: '28px',
      color: CONFIG.COLORS.ink,
    }).setOrigin(0.5).setAngle(-1);

    const data = JSON.parse(localStorage.getItem('streetball') || '{}');
    const levels = data.levels || {};

    const areaNames = { street: '街角球场', park: '城市公园', rooftop: '天台球场' };
    const areaColors = { street: CONFIG.COLORS.red, park: CONFIG.COLORS.green, rooftop: CONFIG.COLORS.purple };
    let lastArea = '';
    let areaY = 60;

    CONFIG.LEVELS.forEach((lvl, idx) => {
      if (lvl.area !== lastArea) {
        areaY += 10;
        this.add.text(cx, areaY, areaNames[lvl.area], {
          fontFamily: "'Arial Black', sans-serif",
          fontSize: '14px',
          color: areaColors[lvl.area],
        }).setOrigin(0.5);
        areaY += 20;
        lastArea = lvl.area;
      }

      const col = (idx % 5);
      const startX = cx - 180;
      const x = startX + col * 90;

      if (col === 0 && idx > 0 && CONFIG.LEVELS[idx - 1].area === lvl.area) {
        areaY += 75;
      }

      const y = areaY;
      const levelData = levels[lvl.id];
      const unlocked = lvl.id === 1 || levels[lvl.id - 1]?.stars > 0;

      const bg = this.add.graphics();
      if (unlocked) {
        bg.fillStyle(0xffffff, 0.6);
        bg.lineStyle(2, 0x333333);
      } else {
        bg.fillStyle(0xcccccc, 0.3);
        bg.lineStyle(2, 0x999999);
      }
      bg.fillRoundedRect(x - 32, y - 20, 64, 55, 8);
      bg.strokeRoundedRect(x - 32, y - 20, 64, 55, 8);

      // Level number
      this.add.text(x, y, `${lvl.id}`, {
        fontFamily: "'Arial Black', sans-serif",
        fontSize: '18px',
        color: unlocked ? CONFIG.COLORS.ink : '#999',
      }).setOrigin(0.5);

      // Stars
      const starStr = levelData ? '⭐'.repeat(levelData.stars) + '☆'.repeat(3 - levelData.stars) : '☆☆☆';
      this.add.text(x, y + 18, unlocked ? starStr : '🔒', {
        fontSize: '10px',
      }).setOrigin(0.5);

      if (unlocked) {
        const hitZone = this.add.zone(x, y + 7, 64, 55).setInteractive({ useHandCursor: true });
        hitZone.on('pointerdown', () => {
          this.scene.start('GameScene', { mode: 'level', level: lvl.id });
        });
      }
    });

    // Back button
    this.add.text(20, CONFIG.HEIGHT - 25, '← 返回菜单', {
      fontSize: '13px', color: '#999',
    }).setInteractive({ useHandCursor: true })
      .on('pointerdown', () => this.scene.start('MenuScene'));
  }
}
```

- [ ] **Step 7: Register LevelSelectScene**

Add to scene array: `scene: [MenuScene, LevelSelectScene, GameScene, ResultScene]`

- [ ] **Step 8: Verify in browser**

Expected: Menu → 关卡模式 → level grid showing 15 levels in 3 areas. Level 1 is unlocked, rest locked. Clicking level 1 starts game with level config. Completing a level shows stars and unlocks the next.

- [ ] **Step 9: Commit**

```bash
git add street-basketball.html
git commit -m "feat(streetball): add 15-level system with star ratings and level select screen"
```

---

### Task 10: Weather System — Wind, Rain, Night

Implement the weather effects that modify gameplay and visuals.

**Files:**
- Modify: `street-basketball.html`

- [ ] **Step 1: Add wind system**

```javascript
setupWeather() {
  this.windForce = 0;
  this.windDirection = 1; // 1 = right, -1 = left
  this.weatherType = 'clear';

  if (this.gameMode === 'level' && this.levelConfig) {
    this.windForce = this.levelConfig.wind || 0;
    this.weatherType = this.levelConfig.weather || 'clear';
  }

  // Wind indicator
  if (this.windForce > 0) {
    this.windText = this.add.text(20, CONFIG.HEIGHT - 25, '', {
      fontFamily: "'Arial Black', sans-serif",
      fontSize: '13px',
      color: CONFIG.COLORS.ink,
    });
    this.updateWindDisplay();

    // Change wind direction periodically
    this.time.addEvent({
      delay: 4000,
      callback: () => {
        this.windDirection = Math.random() > 0.5 ? 1 : -1;
        this.windForce = this.levelConfig ?
          this.levelConfig.wind * Phaser.Math.FloatBetween(0.5, 1.5) :
          Phaser.Math.FloatBetween(0, 3);
        this.updateWindDisplay();
      },
      loop: true,
    });
  }
}

updateWindDisplay() {
  if (!this.windText) return;
  const arrow = this.windDirection > 0 ? '→' : '←';
  const level = Math.round(this.windForce);
  this.windText.setText(`💨 ${arrow} ${level}级`);
}

// In update(), apply wind to ball in flight:
applyWind() {
  if (this.ball && this.isShooting && this.windForce > 0) {
    this.ball.body.velocity.x += this.windDirection * this.windForce * 0.5;
  }
}
```

- [ ] **Step 2: Add rain effect using Phaser particle emitter**

```javascript
setupRain() {
  if (this.weatherType !== 'rain') return;

  // Create rain drop texture
  const rainCanvas = this.textures.createCanvas('raindrop', 3, 12);
  const ctx = rainCanvas.context;
  ctx.fillStyle = 'rgba(150,180,255,0.5)';
  ctx.fillRect(0, 0, 3, 12);
  rainCanvas.refresh();

  this.rainEmitter = this.add.particles(0, -10, 'raindrop', {
    x: { min: 0, max: CONFIG.WIDTH },
    lifespan: 1000,
    speedY: { min: 300, max: 500 },
    speedX: { min: -30, max: -60 },
    scale: { min: 0.5, max: 1 },
    quantity: 3,
    frequency: 30,
  });

  // Rain affects ball trajectory with random wobble
  this.rainWobble = true;
}

// In update():
applyRainEffect() {
  if (this.rainWobble && this.ball && this.isShooting) {
    this.ball.body.velocity.x += (Math.random() - 0.5) * 2;
  }
}
```

- [ ] **Step 3: Add night overlay**

```javascript
setupNight() {
  if (this.weatherType !== 'night') return;

  // Dark overlay
  this.nightOverlay = this.add.graphics();
  this.nightOverlay.fillStyle(0x000022, 0.6);
  this.nightOverlay.fillRect(0, 0, CONFIG.WIDTH, CONFIG.HEIGHT);
  this.nightOverlay.setDepth(100);

  // Glow around rim
  const glow = this.add.graphics();
  glow.fillStyle(0xffff66, 0.15);
  glow.fillCircle(this.rimX + this.rimW / 2, this.rimY, 50);
  glow.setDepth(101);

  // Ball glow (follows ball)
  this.ballGlow = this.add.graphics();
  this.ballGlow.setDepth(101);

  // Make HUD visible above overlay
  this.scoreText?.setDepth(102);
  this.comboText?.setDepth(102);
  this.timerText?.setDepth(102);
  this.windText?.setDepth(102);
  if (this.ball) this.ball.setDepth(101);
}

// In update():
updateNightGlow() {
  if (this.ballGlow && this.ball) {
    this.ballGlow.clear();
    this.ballGlow.fillStyle(0xffaa33, 0.2);
    this.ballGlow.fillCircle(this.ball.x, this.ball.y, 25);
  }
}
```

- [ ] **Step 4: Call setupWeather(), setupRain(), setupNight() in create() and wind/rain/night updates in update()**

- [ ] **Step 5: For endless mode, add random weather switching**

```javascript
// In endless mode setup:
if (this.gameMode === 'endless') {
  this.time.addEvent({
    delay: 20000, // every 20 seconds
    callback: () => {
      const weathers = ['clear', 'windy', 'rain', 'night'];
      this.weatherType = Phaser.Utils.Array.GetRandom(weathers);
      this.windForce = this.weatherType === 'windy' ? Phaser.Math.Between(1, 4) : 0;
      this.cleanupWeatherEffects();
      this.setupRain();
      this.setupNight();
      this.updateWindDisplay();
    },
    loop: true,
  });
}
```

- [ ] **Step 6: Verify in browser**

Start level 4 (wind) — should show wind indicator and ball drifts. Start level 7 (rain) — should see rain particles and ball wobble. Start level 8 (night) — should see dark overlay with glowing rim and ball. Endless mode should cycle weather.

- [ ] **Step 7: Commit**

```bash
git add street-basketball.html
git commit -m "feat(streetball): add weather system with wind, rain, and night effects"
```

---

### Task 11: Combo Visual Effects — Fire, Lightning, BEAST MODE

Implement escalating combo visual effects.

**Files:**
- Modify: `street-basketball.html`

- [ ] **Step 1: Create fire/lightning particle textures**

```javascript
// Add to createTextures():
// Fire particle
const fireCanvas = this.textures.createCanvas('fireparticle', 8, 8);
const fctx = fireCanvas.context;
const fGrad = fctx.createRadialGradient(4, 4, 0, 4, 4, 4);
fGrad.addColorStop(0, '#ffcc00');
fGrad.addColorStop(0.5, '#ff6600');
fGrad.addColorStop(1, 'rgba(255,0,0,0)');
fctx.fillStyle = fGrad;
fctx.fillRect(0, 0, 8, 8);
fireCanvas.refresh();

// Spark particle
const sparkCanvas = this.textures.createCanvas('spark', 4, 4);
const sctx = sparkCanvas.context;
sctx.fillStyle = '#ffff88';
sctx.fillRect(1, 0, 2, 4);
sctx.fillRect(0, 1, 4, 2);
sparkCanvas.refresh();

// Ink splat particle
const inkCanvas = this.textures.createCanvas('inksplat', 10, 10);
const ictx = inkCanvas.context;
ictx.fillStyle = '#ff3366';
ictx.beginPath();
ictx.arc(5, 5, 4, 0, Math.PI * 2);
ictx.fill();
inkCanvas.refresh();
```

- [ ] **Step 2: Add combo effect manager**

```javascript
updateComboEffects() {
  // Clean up previous effects
  if (this.comboEmitter) { this.comboEmitter.destroy(); this.comboEmitter = null; }

  if (this.combo >= 2 && this.ball) {
    if (this.combo >= 7) {
      // Lightning ball
      this.comboEmitter = this.add.particles(0, 0, 'spark', {
        follow: this.ball,
        lifespan: 200,
        speed: { min: 50, max: 100 },
        scale: { start: 1, end: 0 },
        quantity: 2,
        frequency: 30,
        blendMode: 'ADD',
      });
      this.ball.setTint(0x88ccff);
    } else if (this.combo >= 4) {
      // Fire trail
      this.comboEmitter = this.add.particles(0, 0, 'fireparticle', {
        follow: this.ball,
        lifespan: 300,
        speed: { min: 20, max: 60 },
        scale: { start: 1.5, end: 0 },
        quantity: 2,
        frequency: 40,
        blendMode: 'ADD',
      });
      this.ball.setTint(0xff8800);
    } else {
      // Orange trail
      this.comboEmitter = this.add.particles(0, 0, 'fireparticle', {
        follow: this.ball,
        lifespan: 200,
        speed: { min: 10, max: 30 },
        scale: { start: 1, end: 0 },
        quantity: 1,
        frequency: 60,
      });
      this.ball.clearTint();
    }
  } else if (this.ball) {
    this.ball.clearTint();
  }
}
```

- [ ] **Step 3: Add BEAST MODE at x10 combo**

```javascript
activateBeastMode() {
  if (this.beastModeActive) return;
  this.beastModeActive = true;

  // "BEAST MODE" text
  const beastText = this.add.text(CONFIG.WIDTH / 2, CONFIG.HEIGHT / 2 - 40, 'BEAST MODE!!', {
    fontFamily: "'Arial Black', sans-serif",
    fontSize: '40px',
    color: CONFIG.COLORS.red,
  }).setOrigin(0.5).setAngle(-5).setDepth(200);
  beastText.setShadow(3, 3, CONFIG.COLORS.yellow, 0);

  this.tweens.add({
    targets: beastText, scaleX: 1.3, scaleY: 1.3, alpha: 0,
    duration: 1500, ease: 'Power2',
    onComplete: () => beastText.destroy(),
  });

  // Screen flash
  const flash = this.add.graphics().setDepth(199);
  flash.fillStyle(0xffcc00, 0.3);
  flash.fillRect(0, 0, CONFIG.WIDTH, CONFIG.HEIGHT);
  this.tweens.add({
    targets: flash, alpha: 0, duration: 500,
    onComplete: () => flash.destroy(),
  });

  // Enlarge rim for 3 seconds (visual: move rim edges outward)
  this.cameras.main.shake(300, 0.01);

  // Graffiti splashes fly across screen
  for (let i = 0; i < 10; i++) {
    const colors = [0xff3366, 0x44cc44, 0xffcc00, 0x3366ff, 0x6666cc];
    const splat = this.add.graphics().setDepth(198);
    const startX = Phaser.Math.Between(-50, CONFIG.WIDTH + 50);
    const startY = Phaser.Math.Between(-50, CONFIG.HEIGHT + 50);
    splat.fillStyle(Phaser.Utils.Array.GetRandom(colors), 0.5);
    splat.fillCircle(0, 0, Phaser.Math.Between(15, 40));
    splat.setPosition(startX, startY);
    this.tweens.add({
      targets: splat, alpha: 0, scale: 1.5,
      duration: Phaser.Math.Between(800, 1500),
      delay: i * 100,
      onComplete: () => splat.destroy(),
    });
  }
}
```

- [ ] **Step 4: Add graffiti splash effect on scoring**

```javascript
showScoreSplash() {
  // Ink splatters around the hoop on score
  const colors = [0xff3366, 0xffcc00, 0x44cc44, 0x3366ff];
  for (let i = 0; i < 6; i++) {
    const g = this.add.graphics();
    g.fillStyle(Phaser.Utils.Array.GetRandom(colors), Phaser.Math.FloatBetween(0.3, 0.6));
    const r = Phaser.Math.Between(5, 15);
    g.fillCircle(0, 0, r);
    g.setPosition(
      this.rimX + this.rimW / 2 + Phaser.Math.Between(-40, 40),
      this.rimY + Phaser.Math.Between(-30, 20)
    );
    this.tweens.add({
      targets: g, alpha: 0, scale: 1.5,
      duration: Phaser.Math.Between(400, 800),
      onComplete: () => g.destroy(),
    });
  }
}
```

- [ ] **Step 5: Wire in — call updateComboEffects() in onScore(), activateBeastMode() when combo hits 10, showScoreSplash() on every score, camera shake on combo >= 4**

- [ ] **Step 6: Verify in browser**

Score consecutive baskets. Expected: x2 = orange trail, x4 = fire + screen shake, x7 = lightning sparks + blue tint, x10 = BEAST MODE text + flash + graffiti explosion.

- [ ] **Step 7: Commit**

```bash
git add street-basketball.html
git commit -m "feat(streetball): add combo visual effects — fire trail, lightning, BEAST MODE"
```

---

### Task 12: Power-Up System

Implement the 5 power-ups that spawn and can be collected by the ball's trajectory.

**Files:**
- Modify: `street-basketball.html`

- [ ] **Step 1: Define power-up types and create textures**

```javascript
CONFIG.POWERUPS = {
  bigRim:    { name: '大篮筐', icon: '🎯', duration: 3, color: 0xff6600, desc: '篮筐 x1.5' },
  magnet:    { name: '磁铁球', icon: '🧲', duration: 2, color: 0x3366ff, desc: '自动微调' },
  freeze:    { name: '冻结', icon: '❄️', duration: 5, color: 0x00ccff, desc: '时间暂停5秒', isTime: true },
  doubleScore: { name: '双倍分', icon: '✨', duration: 3, color: 0xffcc00, desc: '得分x2' },
  graffitiBomb: { name: '涂鸦炸弹', icon: '💥', duration: 1, color: 0xff3366, desc: '自动进球' },
};
```

- [ ] **Step 2: Implement power-up spawning**

```javascript
setupPowerUps() {
  this.activePowerUps = {}; // { type: remainingShots }
  this.powerUpSprite = null;

  if (this.gameMode === 'level') {
    // Fixed spawn at specific basket counts (every 4 baskets)
    this.nextPowerUpAt = 4;
  } else {
    // Random spawn
    this.nextPowerUpAt = Phaser.Math.Between(3, 6);
  }
}

trySpawnPowerUp() {
  if (this.powerUpSprite) return; // one at a time
  if (this.basketCount < this.nextPowerUpAt) return;

  const types = Object.keys(CONFIG.POWERUPS);
  const type = Phaser.Utils.Array.GetRandom(types);
  const cfg = CONFIG.POWERUPS[type];

  const x = Phaser.Math.Between(200, 550);
  const y = Phaser.Math.Between(80, CONFIG.GROUND_Y - 80);

  // Draw power-up as floating icon with glow
  this.powerUpSprite = this.add.text(x, y, cfg.icon, {
    fontSize: '28px',
  }).setOrigin(0.5).setDepth(50);

  this.powerUpSprite.powerType = type;

  // Glow circle behind it
  this.powerUpGlow = this.add.graphics().setDepth(49);
  this.powerUpGlow.fillStyle(cfg.color, 0.2);
  this.powerUpGlow.fillCircle(x, y, 22);

  // Bob animation
  this.tweens.add({
    targets: [this.powerUpSprite, this.powerUpGlow],
    y: y - 8, duration: 800,
    yoyo: true, repeat: -1, ease: 'Sine.easeInOut',
  });

  // Physics zone for collection
  this.powerUpZone = this.add.zone(x, y, 44, 44);
  this.physics.add.existing(this.powerUpZone, true);
  this.physics.add.overlap(this.ball, this.powerUpZone, () => {
    this.collectPowerUp(type);
  });

  this.nextPowerUpAt = this.basketCount + Phaser.Math.Between(3, 6);
}
```

- [ ] **Step 3: Implement power-up collection and effects**

```javascript
collectPowerUp(type) {
  if (!this.powerUpSprite) return;
  const cfg = CONFIG.POWERUPS[type];

  // Collection animation
  this.tweens.add({
    targets: this.powerUpSprite, scale: 2, alpha: 0, duration: 300,
    onComplete: () => { this.powerUpSprite?.destroy(); this.powerUpSprite = null; }
  });
  if (this.powerUpGlow) { this.powerUpGlow.destroy(); this.powerUpGlow = null; }
  if (this.powerUpZone) { this.powerUpZone.destroy(); this.powerUpZone = null; }

  // Pickup text
  const pickText = this.add.text(CONFIG.WIDTH / 2, 60, `${cfg.icon} ${cfg.name}!`, {
    fontFamily: "'Arial Black', sans-serif",
    fontSize: '20px',
    color: `#${cfg.color.toString(16).padStart(6, '0')}`,
  }).setOrigin(0.5).setDepth(200);
  this.tweens.add({
    targets: pickText, y: 40, alpha: 0, duration: 1000,
    onComplete: () => pickText.destroy(),
  });

  // Apply effect
  if (type === 'freeze' && this.isTimedLevel) {
    // Pause timer for 5 seconds
    this.timerFrozen = true;
    this.time.delayedCall(5000, () => { this.timerFrozen = false; });
  } else if (type === 'graffitiBomb') {
    // Auto-score on next shot
    this.autoScore = true;
  } else {
    this.activePowerUps[type] = cfg.duration; // shots remaining
  }

  // Update powerup HUD
  this.updatePowerUpHUD();
}

// In timer callback, check freeze:
// if (this.timerFrozen) return; (add before decrement)

// In onScore(), consume shot-based powerups:
consumePowerUpShots() {
  for (const [type, shots] of Object.entries(this.activePowerUps)) {
    this.activePowerUps[type]--;
    if (this.activePowerUps[type] <= 0) {
      delete this.activePowerUps[type];
    }
  }
  this.updatePowerUpHUD();
}
```

- [ ] **Step 4: Implement gameplay effects of active power-ups**

```javascript
// In scoring calculation (onScore):
// bigRim: temporarily widen score zone (handled in setupHoop after collection)
// doubleScore: multiply final points by 2
// magnet: in update(), adjust ball velocity toward rim

applyMagnetEffect() {
  if (!this.activePowerUps.magnet || !this.ball || !this.isShooting) return;
  const targetX = this.rimX + this.rimW / 2;
  const targetY = this.rimY + 10;
  const dx = targetX - this.ball.x;
  const dy = targetY - this.ball.y;
  const dist = Math.hypot(dx, dy);
  if (dist < 150 && dist > 10) {
    this.ball.body.velocity.x += (dx / dist) * 3;
    this.ball.body.velocity.y += (dy / dist) * 2;
  }
}

applyBigRimEffect() {
  // Widen the score zone
  if (this.activePowerUps.bigRim && this.scoreZone) {
    this.scoreZone.body.setSize(this.rimW * 1.5 - 10, 14);
  } else if (this.scoreZone) {
    this.scoreZone.body.setSize(this.rimW - 10, 10);
  }
}
```

- [ ] **Step 5: Add power-up HUD indicator**

```javascript
updatePowerUpHUD() {
  if (this.powerUpHudText) this.powerUpHudText.destroy();
  const active = Object.entries(this.activePowerUps);
  if (active.length === 0) return;

  const text = active.map(([type, shots]) => {
    const cfg = CONFIG.POWERUPS[type];
    return `${cfg.icon} x${shots}`;
  }).join('  ');

  this.powerUpHudText = this.add.text(CONFIG.WIDTH - 20, CONFIG.HEIGHT - 25, text, {
    fontFamily: "'Arial Black', sans-serif",
    fontSize: '13px',
    color: CONFIG.COLORS.ink,
  }).setOrigin(1, 0.5);
}
```

- [ ] **Step 6: Wire in — call setupPowerUps() in create(), trySpawnPowerUp() in onScore(), applyMagnetEffect() and applyBigRimEffect() in update(), consume shots in onScore()**

- [ ] **Step 7: Verify in browser**

Play and score several baskets. Expected: power-ups appear floating on the court, ball passing through them collects them, effects visible (bigger rim, magnet pull, etc.), HUD shows active power-ups.

- [ ] **Step 8: Commit**

```bash
git add street-basketball.html
git commit -m "feat(streetball): add 5 power-ups with collection, effects, and HUD display"
```

---

### Task 13: Character System — Selection and Passive Skills

Implement 6 characters with unique visuals and passive abilities.

**Files:**
- Modify: `street-basketball.html`

- [ ] **Step 1: Define character data**

```javascript
CONFIG.CHARACTERS = [
  { id: 'default', name: '小涂鸦', color: '#3366ff', headband: '#ff3366', unlock: null, skill: null, desc: '默认角色' },
  { id: 'fire', name: '火焰哥', color: '#ff4400', headband: '#ffcc00', unlock: { type: 'level', value: 5 }, skill: 'fireBoost', desc: 'combo火焰更猛' },
  { id: 'spring', name: '弹簧妹', color: '#44cc44', headband: '#88ff88', unlock: { type: 'level', value: 10 }, skill: 'bankBoost', desc: '篮板反弹区更大' },
  { id: 'wind', name: '风之子', color: '#00aaff', headband: '#88ddff', unlock: { type: 'level', value: 15 }, skill: 'windResist', desc: '风力影响减半' },
  { id: 'lucky', name: '幸运星', color: '#ffaa00', headband: '#ffdd44', unlock: { type: 'stars', value: 50 }, skill: 'luckyDrop', desc: '道具+30%' },
  { id: 'king', name: '涂鸦王', color: '#cc33ff', headband: '#ff66ff', unlock: { type: 'score', value: 5000 }, skill: 'scoreBoost', desc: '得分+10%' },
];
```

- [ ] **Step 2: Create CharSelectScene**

```javascript
class CharSelectScene extends Phaser.Scene {
  constructor() { super('CharSelectScene'); }

  create() {
    const cx = CONFIG.WIDTH / 2;
    this.add.graphics().fillStyle(0xf5f0e0).fillRect(0, 0, CONFIG.WIDTH, CONFIG.HEIGHT);

    this.add.text(cx, 30, '👤 角色选择', {
      fontFamily: "'Arial Black', sans-serif",
      fontSize: '28px',
      color: CONFIG.COLORS.ink,
    }).setOrigin(0.5);

    const data = JSON.parse(localStorage.getItem('streetball') || '{}');
    const unlockedChars = data.unlockedChars || ['default'];
    const selectedChar = data.selectedChar || 'default';

    CONFIG.CHARACTERS.forEach((char, i) => {
      const col = i % 3;
      const row = Math.floor(i / 3);
      const x = cx - 160 + col * 160;
      const y = 100 + row * 170;
      const unlocked = unlockedChars.includes(char.id);
      const selected = char.id === selectedChar;

      // Card background
      const bg = this.add.graphics();
      if (selected) {
        bg.fillStyle(0xffcc00, 0.2);
        bg.lineStyle(3, 0xffcc00);
      } else if (unlocked) {
        bg.fillStyle(0xffffff, 0.6);
        bg.lineStyle(2, 0x333333);
      } else {
        bg.fillStyle(0xcccccc, 0.2);
        bg.lineStyle(2, 0x999999);
      }
      bg.fillRoundedRect(x - 60, y - 10, 120, 150, 10);
      bg.strokeRoundedRect(x - 60, y - 10, 120, 150, 10);

      // Mini character drawing
      this.drawMiniChar(x, y + 30, char, unlocked);

      // Name
      this.add.text(x, y + 75, unlocked ? char.name : '🔒', {
        fontFamily: "'Arial Black', sans-serif",
        fontSize: '14px',
        color: unlocked ? CONFIG.COLORS.ink : '#999',
      }).setOrigin(0.5);

      // Skill desc
      this.add.text(x, y + 95, unlocked ? char.desc : this.getUnlockHint(char), {
        fontSize: '10px',
        color: '#888',
        wordWrap: { width: 110 },
        align: 'center',
      }).setOrigin(0.5);

      // Selection
      if (unlocked) {
        const hitZone = this.add.zone(x, y + 60, 120, 150).setInteractive({ useHandCursor: true });
        hitZone.on('pointerdown', () => {
          data.selectedChar = char.id;
          localStorage.setItem('streetball', JSON.stringify(data));
          this.scene.restart(); // refresh to show selection
        });
      }
    });

    // Back button
    this.add.text(20, CONFIG.HEIGHT - 25, '← 返回菜单', {
      fontSize: '13px', color: '#999',
    }).setInteractive({ useHandCursor: true })
      .on('pointerdown', () => this.scene.start('MenuScene'));
  }

  drawMiniChar(x, y, char, unlocked) {
    const g = this.add.graphics();
    const alpha = unlocked ? 1 : 0.3;

    // Head
    g.fillStyle(unlocked ? 0xffddaa : 0xcccccc, alpha);
    g.fillCircle(x, y - 18, 12);
    g.lineStyle(2, 0x333333, alpha);
    g.strokeCircle(x, y - 18, 12);

    // Headband
    const hColor = Phaser.Display.Color.HexStringToColor(char.headband).color;
    g.fillStyle(hColor, alpha);
    g.fillRoundedRect(x - 14, y - 27, 28, 6, 3);

    // Body
    const bColor = Phaser.Display.Color.HexStringToColor(char.color).color;
    g.fillStyle(bColor, alpha);
    g.fillRoundedRect(x - 11, y - 5, 22, 28, 5);
    g.lineStyle(2, 0x333333, alpha);
    g.strokeRoundedRect(x - 11, y - 5, 22, 28, 5);
  }

  getUnlockHint(char) {
    if (!char.unlock) return '';
    switch (char.unlock.type) {
      case 'level': return `通关第${char.unlock.value}关`;
      case 'stars': return `收集${char.unlock.value}颗星`;
      case 'score': return `无尽模式${char.unlock.value}分`;
      default: return '';
    }
  }
}
```

- [ ] **Step 3: Apply character passive skills in GameScene**

```javascript
// In GameScene.create():
loadCharacter() {
  const data = JSON.parse(localStorage.getItem('streetball') || '{}');
  this.selectedChar = data.selectedChar || 'default';
  this.charConfig = CONFIG.CHARACTERS.find(c => c.id === this.selectedChar);
}

// Apply skills in relevant places:
// 'windResist': in applyWind(), halve the wind force
// 'bankBoost': in setupHoop(), widen backboard collider
// 'luckyDrop': in trySpawnPowerUp(), reduce nextPowerUpAt gap
// 'scoreBoost': in onScore(), multiply total by 1.1
// 'fireBoost': purely visual — extra particles when combo active
```

- [ ] **Step 4: Check and grant character unlocks after each game**

```javascript
checkUnlocks() {
  const data = JSON.parse(localStorage.getItem('streetball') || '{}');
  if (!data.unlockedChars) data.unlockedChars = ['default'];

  for (const char of CONFIG.CHARACTERS) {
    if (data.unlockedChars.includes(char.id) || !char.unlock) continue;
    let unlocked = false;
    switch (char.unlock.type) {
      case 'level':
        unlocked = data.levels?.[char.unlock.value]?.stars > 0;
        break;
      case 'stars':
        unlocked = (data.totalStars || 0) >= char.unlock.value;
        break;
      case 'score':
        unlocked = (data.highScore || 0) >= char.unlock.value;
        break;
    }
    if (unlocked) {
      data.unlockedChars.push(char.id);
    }
  }
  localStorage.setItem('streetball', JSON.stringify(data));
}
```

Call `this.checkUnlocks()` in `gameOver()` and `levelComplete()`.

- [ ] **Step 5: Update drawPlayer() to use character colors**

Replace hardcoded jersey color with `this.charConfig.color` and headband color with `this.charConfig.headband`.

- [ ] **Step 6: Register CharSelectScene**

Add to scene array: `scene: [MenuScene, LevelSelectScene, CharSelectScene, GameScene, ResultScene]`

- [ ] **Step 7: Verify in browser**

Menu → 角色选择 → shows 6 characters, only default unlocked. Select default, play a game. Complete level 5 → fire character unlocks. Character colors appear in game.

- [ ] **Step 8: Commit**

```bash
git add street-basketball.html
git commit -m "feat(streetball): add 6-character system with selection, unlocks, and passive skills"
```

---

### Task 14: Sound Effects — Web Audio API

Add programmatically generated sound effects.

**Files:**
- Modify: `street-basketball.html`

- [ ] **Step 1: Create SoundManager**

```javascript
class SoundManager {
  constructor() {
    this.ctx = null;
    this.enabled = true;
    this.init();
  }

  init() {
    try { this.ctx = new (window.AudioContext || window.webkitAudioContext)(); }
    catch (e) { this.enabled = false; }
  }

  resume() {
    if (this.ctx?.state === 'suspended') this.ctx.resume();
  }

  play(type) {
    if (!this.enabled || !this.ctx) return;
    this.resume();
    switch (type) {
      case 'shoot': this.playShoot(); break;
      case 'swish': this.playSwish(); break;
      case 'bank': this.playBank(); break;
      case 'miss': this.playMiss(); break;
      case 'combo': this.playCombo(); break;
      case 'pickup': this.playPickup(); break;
      case 'beast': this.playBeast(); break;
    }
  }

  playTone(freq, duration, type = 'sine', volume = 0.3) {
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = type;
    osc.frequency.value = freq;
    gain.gain.setValueAtTime(volume, this.ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + duration);
    osc.connect(gain);
    gain.connect(this.ctx.destination);
    osc.start();
    osc.stop(this.ctx.currentTime + duration);
  }

  playNoise(duration, volume = 0.15) {
    const bufferSize = this.ctx.sampleRate * duration;
    const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const data = buffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) data[i] = (Math.random() * 2 - 1) * volume;
    const source = this.ctx.createBufferSource();
    const gain = this.ctx.createGain();
    source.buffer = buffer;
    gain.gain.setValueAtTime(volume, this.ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + duration);
    source.connect(gain);
    gain.connect(this.ctx.destination);
    source.start();
  }

  playShoot() {
    this.playTone(800, 0.1, 'sine', 0.2);
    this.playTone(1200, 0.08, 'sine', 0.15);
  }

  playSwish() {
    this.playNoise(0.15, 0.2);
    this.playTone(1000, 0.2, 'sine', 0.25);
    setTimeout(() => this.playTone(1200, 0.15, 'sine', 0.2), 50);
  }

  playBank() {
    this.playTone(300, 0.15, 'square', 0.3);
    setTimeout(() => this.playSwish(), 100);
  }

  playMiss() {
    this.playTone(200, 0.2, 'triangle', 0.2);
  }

  playCombo() {
    this.playTone(600, 0.1, 'square', 0.2);
    setTimeout(() => this.playTone(800, 0.1, 'square', 0.2), 80);
    setTimeout(() => this.playTone(1000, 0.15, 'square', 0.2), 160);
  }

  playPickup() {
    this.playTone(1200, 0.08, 'sine', 0.2);
    setTimeout(() => this.playTone(1600, 0.1, 'sine', 0.2), 60);
  }

  playBeast() {
    this.playTone(80, 0.5, 'sawtooth', 0.3);
    this.playTone(100, 0.5, 'square', 0.2);
    this.playNoise(0.6, 0.15);
  }
}

// Create global instance
const soundManager = new SoundManager();
```

- [ ] **Step 2: Wire sound triggers into game events**

Add `soundManager.play('shoot')` in `shootBall()`, `soundManager.play('swish')` / `soundManager.play('bank')` in `onScore()`, `soundManager.play('miss')` in `onMiss()`, `soundManager.play('combo')` when combo increments past 2, `soundManager.play('pickup')` in `collectPowerUp()`, `soundManager.play('beast')` in `activateBeastMode()`.

- [ ] **Step 3: Add sound toggle to MenuScene**

```javascript
// In MenuScene.create(), add a sound toggle button:
const data = JSON.parse(localStorage.getItem('streetball') || '{}');
soundManager.enabled = data.soundOn !== false;

const soundBtn = this.add.text(CONFIG.WIDTH - 20, CONFIG.HEIGHT - 25,
  soundManager.enabled ? '🔊' : '🔇', {
  fontSize: '20px',
}).setOrigin(1, 1).setInteractive({ useHandCursor: true });

soundBtn.on('pointerdown', () => {
  soundManager.enabled = !soundManager.enabled;
  soundBtn.setText(soundManager.enabled ? '🔊' : '🔇');
  const d = JSON.parse(localStorage.getItem('streetball') || '{}');
  d.soundOn = soundManager.enabled;
  localStorage.setItem('streetball', JSON.stringify(d));
});
```

- [ ] **Step 4: Verify in browser**

Play the game. Expected: swoosh sound on shoot, satisfying swish/bank sounds on scoring, dull thud on miss, ascending tones on combo, ding on power-up pickup, deep bass on BEAST MODE. Sound toggle works.

- [ ] **Step 5: Commit**

```bash
git add street-basketball.html
git commit -m "feat(streetball): add programmatic sound effects via Web Audio API"
```

---

### Task 15: Moving Rim and Obstacles

Implement moving rim (for certain levels) and flying obstacles.

**Files:**
- Modify: `street-basketball.html`

- [ ] **Step 1: Add moving rim logic**

```javascript
setupMovingRim() {
  if (!(this.levelConfig?.rimMove || (this.gameMode === 'endless' && this.basketCount > 15))) return;

  this.rimMoving = true;
  this.rimBaseX = this.rimX;
  this.rimMoveRange = 40;
  this.rimMoveSpeed = 0.02;
  this.rimMovePhase = 0;
}

updateMovingRim() {
  if (!this.rimMoving) return;
  this.rimMovePhase += this.rimMoveSpeed;
  const offset = Math.sin(this.rimMovePhase) * this.rimMoveRange;
  const newX = this.rimBaseX + offset;

  // Update physics bodies' positions
  if (this.scoreZone) this.scoreZone.setPosition(newX + this.rimW / 2, this.rimY + 15);
  if (this.backboard) this.backboard.setPosition(newX - 10, this.rimY - 20);
  if (this.rimLeft) this.rimLeft.setPosition(newX, this.rimY + 4);
  if (this.rimRight) this.rimRight.setPosition(newX + this.rimW, this.rimY + 4);

  // Redraw hoop visuals at new position
  this.redrawHoop(newX);
}

redrawHoop(x) {
  if (this.hoopGraphics) this.hoopGraphics.clear();
  else this.hoopGraphics = this.add.graphics().setDepth(10);
  const g = this.hoopGraphics;

  // Pole (stretches to new position)
  g.fillStyle(0x666666);
  g.fillRect(x - 4, this.rimY - 5, 8, CONFIG.GROUND_Y - this.rimY + 5);
  // Backboard
  g.fillStyle(0xffffff, 0.85);
  g.fillRect(x - 28, this.rimY - 40, 55, 38);
  g.lineStyle(3, 0x333333);
  g.strokeRect(x - 28, this.rimY - 40, 55, 38);
  // Rim
  g.lineStyle(4, 0xff3300);
  g.beginPath();
  g.arc(x + this.rimW / 2, this.rimY + 4, this.rimW / 2, 0, Math.PI, false);
  g.strokePath();
  // Net
  g.lineStyle(1.5, 0xffffff, 0.5);
  for (let i = 0; i <= 4; i++) {
    const nx = x + i * (this.rimW / 4);
    g.lineBetween(nx, this.rimY + 4, nx + (Math.random() - 0.5) * 4, this.rimY + 40);
  }
}
```

- [ ] **Step 2: Add rim shake effect**

```javascript
updateRimShake() {
  if (!this.levelConfig?.rimShake) return;
  // Add micro-vibration to rim Y
  if (this.scoreZone) {
    const shakeY = this.rimY + 15 + Math.sin(Date.now() * 0.01) * 3;
    this.scoreZone.setPosition(this.scoreZone.x, shakeY);
  }
}
```

- [ ] **Step 3: Add flying obstacles**

```javascript
setupObstacles() {
  if (!this.levelConfig?.obstacles && !(this.gameMode === 'endless' && this.basketCount > 25)) return;

  this.obstacles = [];

  // Bird that flies across
  this.time.addEvent({
    delay: Phaser.Math.Between(5000, 8000),
    callback: () => this.spawnObstacle(),
    loop: true,
  });
}

spawnObstacle() {
  const types = ['bird', 'clothesline'];
  const type = Phaser.Utils.Array.GetRandom(types);

  if (type === 'bird') {
    const y = Phaser.Math.Between(100, 250);
    const bird = this.add.text(-30, y, '🐦', { fontSize: '24px' });
    this.physics.add.existing(bird);
    bird.body.setAllowGravity(false);
    bird.body.setVelocityX(Phaser.Math.Between(80, 150));

    // Collide with ball
    this.physics.add.collider(this.ball, bird, () => {
      // Deflect ball
      this.ball.body.velocity.y += 50;
    });

    // Destroy when off screen
    this.time.delayedCall(8000, () => bird.destroy());
  }
}
```

- [ ] **Step 4: Call setupMovingRim(), setupObstacles() in create(). Call updateMovingRim(), updateRimShake() in update()**

- [ ] **Step 5: Verify in browser**

Start level 3 (moving rim). Expected: hoop slides left/right smoothly. Level 11+ should have bird obstacles flying across. Level 12+ has shaking rim.

- [ ] **Step 6: Commit**

```bash
git add street-basketball.html
git commit -m "feat(streetball): add moving rim, rim shake, and flying obstacles"
```

---

### Task 16: Area-Specific Backgrounds

Implement the 3 different background themes for each area (street corner, city park, rooftop).

**Files:**
- Modify: `street-basketball.html`

- [ ] **Step 1: Refactor drawCourt to accept area parameter**

```javascript
drawCourt() {
  const area = this.levelConfig?.area || 'street';
  const g = this.add.graphics();

  // Paper background
  g.fillStyle(0xf5f0e0);
  g.fillRect(0, 0, CONFIG.WIDTH, CONFIG.HEIGHT);
  // Notebook lines
  g.lineStyle(1, 0x000000, 0.03);
  for (let y = 0; y < CONFIG.HEIGHT; y += 29) g.lineBetween(0, y, CONFIG.WIDTH, y);

  switch (area) {
    case 'street': this.drawStreetBg(g); break;
    case 'park': this.drawParkBg(g); break;
    case 'rooftop': this.drawRooftopBg(g); break;
    default: this.drawStreetBg(g); break;
  }

  // Ground
  g.fillStyle(0x8B7355);
  g.fillRect(0, CONFIG.GROUND_Y, CONFIG.WIDTH, CONFIG.HEIGHT - CONFIG.GROUND_Y);
  g.lineStyle(3, 0x333333, 0.6);
  g.lineBetween(0, CONFIG.GROUND_Y, CONFIG.WIDTH, CONFIG.GROUND_Y);
}

drawStreetBg(g) {
  this.drawBrickWall(g);
  // Red brick graffiti
  this.drawGraffiti(g, ['BALL IS LIFE', 'STREET', 'SWISH']);
}

drawParkBg(g) {
  // Concrete wall with cracks
  g.fillStyle(0xbbbbaa, 0.25);
  g.fillRect(0, 0, CONFIG.WIDTH, CONFIG.GROUND_Y);
  // Green bushes at bottom of wall
  for (let x = 0; x < CONFIG.WIDTH; x += 60) {
    g.fillStyle(0x338833, 0.3);
    g.fillCircle(x + 30, CONFIG.GROUND_Y - 10, Phaser.Math.Between(15, 25));
  }
  this.drawGraffiti(g, ['PARK LIFE', 'HOOPS', 'DUNK']);
}

drawRooftopBg(g) {
  // Sky gradient
  g.fillGradientStyle(0x334466, 0x334466, 0x667799, 0x667799);
  g.fillRect(0, 0, CONFIG.WIDTH, CONFIG.GROUND_Y * 0.4);
  // City skyline silhouette
  const skylineY = CONFIG.GROUND_Y * 0.4;
  g.fillStyle(0x222233, 0.5);
  for (let x = 0; x < CONFIG.WIDTH; x += Phaser.Math.Between(40, 80)) {
    const h = Phaser.Math.Between(30, 90);
    const w = Phaser.Math.Between(30, 60);
    g.fillRect(x, skylineY - h, w, h);
    // Windows
    g.fillStyle(0xffcc66, 0.3);
    for (let wy = skylineY - h + 8; wy < skylineY - 5; wy += 12) {
      for (let wx = x + 5; wx < x + w - 5; wx += 10) {
        if (Math.random() > 0.4) g.fillRect(wx, wy, 5, 6);
      }
    }
    g.fillStyle(0x222233, 0.5);
  }
  // Chain link fence pattern
  g.lineStyle(1, 0x666666, 0.3);
  for (let x = 0; x < CONFIG.WIDTH; x += 12) {
    g.lineBetween(x, skylineY, x + 6, skylineY + 20);
    g.lineBetween(x + 6, skylineY, x, skylineY + 20);
  }
  this.drawGraffiti(g, ['ROOFTOP', 'SKY HIGH', 'LEGEND']);
}
```

- [ ] **Step 2: Update drawGraffiti to accept custom text array**

```javascript
drawGraffiti(g, texts) {
  const text1 = this.add.text(25, 20, texts[0], {
    fontFamily: "'Arial Black', sans-serif",
    fontSize: '22px',
    fontStyle: 'bold',
    color: CONFIG.COLORS.red,
  }).setAngle(-6).setShadow(2, 2, 'rgba(0,0,0,0.2)', 0);

  // Random paint splashes
  const splashColors = [0x44cc44, 0xffcc00, 0xff3366, 0x6666cc];
  for (let i = 0; i < 5; i++) {
    const color = Phaser.Utils.Array.GetRandom(splashColors);
    g.fillStyle(color, Phaser.Math.FloatBetween(0.15, 0.35));
    g.fillCircle(
      Phaser.Math.Between(50, CONFIG.WIDTH - 100),
      Phaser.Math.Between(30, CONFIG.GROUND_Y - 60),
      Phaser.Math.Between(8, 20)
    );
  }

  if (texts[1]) {
    this.add.text(CONFIG.WIDTH - 130, 80, `★ ${texts[1]} ★`, {
      fontFamily: "'Arial Black', sans-serif",
      fontSize: '13px',
      color: CONFIG.COLORS.purple,
    }).setAngle(4).setAlpha(0.5);
  }
}
```

- [ ] **Step 3: For endless mode, randomize background area**

In endless mode setup: `this.currentArea = Phaser.Utils.Array.GetRandom(['street', 'park', 'rooftop']);` and use it for `drawCourt()`.

- [ ] **Step 4: Verify in browser**

Play levels from different areas. Expected: levels 1-5 show brick wall, 6-10 show concrete+bushes, 11-15 show city skyline+fence.

- [ ] **Step 5: Commit**

```bash
git add street-basketball.html
git commit -m "feat(streetball): add 3 area-specific backgrounds — street, park, rooftop"
```

---

### Task 17: Player Position Variation and Difficulty Scaling

Implement randomized player positions for certain levels and endless mode difficulty scaling.

**Files:**
- Modify: `street-basketball.html`

- [ ] **Step 1: Add player position randomization**

```javascript
// In resetBall(), for levels with randomPos:
if (this.levelConfig?.randomPos) {
  this.playerX = Phaser.Math.Between(100, 250);
  this.redrawPlayer();
}

// In endless mode, gradually move player further:
if (this.gameMode === 'endless') {
  // Every 10 baskets, shift range slightly further
  const minX = Math.max(80, 160 - this.basketCount * 2);
  const maxX = Math.min(250, 200);
  this.playerX = Phaser.Math.Between(minX, maxX);
  this.redrawPlayer();
}

redrawPlayer() {
  this.drawPlayer();
}
```

- [ ] **Step 2: Add endless mode difficulty scaling**

```javascript
// In endless mode, update difficulty each shot:
updateEndlessDifficulty() {
  if (this.gameMode !== 'endless') return;

  // Shrink rim slightly over time
  const shrink = Math.max(0.7, 1 - this.basketCount * 0.005);
  if (this.scoreZone) {
    this.scoreZone.body.setSize((this.rimW - 10) * shrink, 10);
  }

  // Increase wind
  if (this.basketCount > 10 && !this.windForce) {
    this.windForce = 1;
    this.windDirection = Math.random() > 0.5 ? 1 : -1;
  }
  if (this.basketCount > 10) {
    this.windForce = Math.min(1 + (this.basketCount - 10) * 0.15, 5);
  }

  // Enable moving rim after 15 baskets
  if (this.basketCount >= 15 && !this.rimMoving) {
    this.setupMovingRim();
  }

  // Enable obstacles after 25 baskets
  if (this.basketCount >= 25 && !this.obstaclesEnabled) {
    this.obstaclesEnabled = true;
    this.setupObstacles();
  }
}
```

- [ ] **Step 3: Call updateEndlessDifficulty() in resetBall()**

- [ ] **Step 4: Verify in browser**

Play endless mode for 20+ baskets. Expected: player position shifts, wind increases, rim starts moving, eventually obstacles appear.

- [ ] **Step 5: Commit**

```bash
git add street-basketball.html
git commit -m "feat(streetball): add position variation and endless mode difficulty scaling"
```

---

### Task 18: Add to Game Library

Add the street basketball game to the game library (index.html).

**Files:**
- Modify: `index.html`

- [ ] **Step 1: Add game entry to the games array**

In `index.html`, add to the `games` array:

```javascript
{
  icon: '🏀', title: '街头篮球',
  desc: '涂鸦风投篮挑战，解锁角色，征服15关',
  tags: ['🏀 投篮', '✏️ 涂鸦风', '🏆 关卡'],
  glow: '#ff6600', url: 'street-basketball.html'
}
```

- [ ] **Step 2: Add the game thumbnail to the selector bar HTML**

```html
<div class="game-thumb" data-game="2" onclick="selectGame(2)" style="background: linear-gradient(135deg, #2a1a0a, #352010);">
  <span class="thumb-emoji">🏀</span>
  <span class="thumb-name">街头篮球</span>
</div>
```

- [ ] **Step 3: Verify in browser**

Open `index.html`. Expected: 3 games in the selector bar. Street basketball has orange glow and correct info. Clicking PLAY navigates to `street-basketball.html`.

- [ ] **Step 4: Commit**

```bash
git add index.html street-basketball.html
git commit -m "feat: add street basketball to game library"
```

---

### Task 19: Final Polish and Bug Testing

Final integration testing, edge case fixes, and visual polish.

**Files:**
- Modify: `street-basketball.html`

- [ ] **Step 1: Test all 15 levels play through correctly**

Open browser, play through levels 1-5 (at minimum). Verify:
- Level configs load correctly (player position, wind, weather)
- Star ratings calculate correctly
- Level unlocks work
- Character unlocks trigger at correct levels

- [ ] **Step 2: Test endless mode edge cases**

- Play until 30+ baskets: verify difficulty scaling works
- Let timer expire: verify game over → result screen → replay works
- Verify high score saves and displays correctly
- Verify weather changes in endless mode

- [ ] **Step 3: Test all power-ups function correctly**

- Big rim: visually wider, easier to score
- Magnet: ball curves toward rim
- Freeze: timer pauses
- Double score: points doubled
- Graffiti bomb: auto-score

- [ ] **Step 4: Test mobile responsiveness**

Open in Chrome DevTools mobile view (iPhone SE, iPhone 14). Verify:
- Canvas scales correctly
- Swipe gesture works with touch
- UI is readable at small sizes

- [ ] **Step 5: Fix any discovered issues**

Address any bugs found during testing.

- [ ] **Step 6: Final commit**

```bash
git add street-basketball.html
git commit -m "fix(streetball): polish and edge case fixes from integration testing"
```
