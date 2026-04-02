# 装备槽位约束 + 新装备外观 + 套装光环 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 修复装备槽位唯一性、为20件传说/神话装备添加SVG图案、比赛中套装激活显示持续光环

**Architecture:** 单文件HTML游戏，所有修改在 `turtle-race.html`。三个独立模块：(1) toggleCosmetic/buyCosmetic加槽位检查 (2) ACCESSORY_SVG新增20条目 (3) 新增aura CSS类+JS计算函数+render()应用

**Tech Stack:** 纯HTML/CSS/JavaScript，SVG坐标系 viewBox="0 0 64 48"

---

### Task 1: 装备槽位唯一性

**Files:**
- Modify: `turtle-race.html` (toggleCosmetic line 3811, buyCosmetic line 2935)

- [ ] **Step 1: 修改 toggleCosmetic() 添加槽位检查**

找到 `toggleCosmetic` 函数（line ~3811），将整个函数替换为：

```javascript
function toggleCosmetic(itemId) {
  if (!state.equippedCosmetics) state.equippedCosmetics = [];
  const idx = state.equippedCosmetics.indexOf(itemId);
  if (idx >= 0) {
    // 卸下
    state.equippedCosmetics.splice(idx, 1);
  } else {
    // 穿戴：先移除同槽位已装备的装备
    const item = COSMETIC_ITEMS.find(c => c.id === itemId);
    if (item && item.slot) {
      const conflictIdx = state.equippedCosmetics.findIndex(id => {
        const equipped = COSMETIC_ITEMS.find(c => c.id === id);
        return equipped && equipped.slot === item.slot;
      });
      if (conflictIdx >= 0) {
        state.equippedCosmetics.splice(conflictIdx, 1);
      }
    }
    state.equippedCosmetics.push(itemId);
  }
  playSound('select');
  saveGame();
  const cmEl = document.getElementById('cosmeticModal');
  if (cmEl) renderCosmeticModal(cmEl, false);
  render();
}
```

- [ ] **Step 2: 修改 buyCosmetic() 自动穿戴时检查槽位**

找到 `buyCosmetic` 函数（line ~2935），将自动穿戴部分修改为：

```javascript
function buyCosmetic(itemId) {
  const item = COSMETIC_ITEMS.find(c => c.id === itemId);
  if (!item || state.coins < item.cost) return;
  if (!state.ownedCosmetics) state.ownedCosmetics = [];
  if (state.ownedCosmetics.includes(itemId)) return;
  state.coins -= item.cost;
  state.ownedCosmetics.push(itemId);
  if (!state.equippedCosmetics) state.equippedCosmetics = [];
  // 自动穿戴：先移除同槽位冲突
  if (item.slot) {
    const conflictIdx = state.equippedCosmetics.findIndex(id => {
      const equipped = COSMETIC_ITEMS.find(c => c.id === id);
      return equipped && equipped.slot === item.slot;
    });
    if (conflictIdx >= 0) {
      state.equippedCosmetics.splice(conflictIdx, 1);
    }
  }
  state.equippedCosmetics.push(itemId);
  playSound('coin');
  saveGame();
  renderShop();
}
```

- [ ] **Step 3: 提交**

```bash
git add turtle-race.html
git commit -m "fix: enforce one item per equipment slot (head/face/back/mount)"
```

---

### Task 2: 20件新装备 SVG 图案

**Files:**
- Modify: `turtle-race.html` (ACCESSORY_SVG 对象，在现有条目之后追加20个新条目)

坐标参考（viewBox 0 0 64 48）：
- **head** (头顶)：cx≈48~53, cy≈5~14
- **face** (脸部)：cx≈51~61, cy≈17~27
- **back** (背部)：cx≈18~22, cy≈14~28（向左展开）
- **mount** (底部)：cy≈36~46（从底部延伸）

- [ ] **Step 1: 在 ACCESSORY_SVG 对象末尾追加冰霜领主套装（4件）**

在 `ACCESSORY_SVG` 对象的最后一个条目之后（闭合 `}` 之前）添加：

```javascript
  // ===== 冰霜领主套装 =====
  frost_crown: `<polygon points="47,14 49,7 51,12 53,6 55,12 57,7 59,14" fill="#93C5FD" stroke="#BFDBFE" stroke-width="0.5"/>
    <rect x="47" y="13" width="12" height="2" rx="1" fill="#1E40AF"/>
    <circle cx="53" cy="7" r="1" fill="#BFDBFE"/>`,
  frost_mask: `<rect x="51" y="17" width="9" height="4" rx="1.5" fill="#93C5FD" opacity="0.7"/>
    <polygon points="52,21 50,27 54,25" fill="#BFDBFE" stroke="#93C5FD" stroke-width="0.4"/>
    <polygon points="56,21 54,27 58,25" fill="#BFDBFE" stroke="#93C5FD" stroke-width="0.4"/>
    <polygon points="59,21 57,26 61,25" fill="#BFDBFE" stroke="#93C5FD" stroke-width="0.4"/>`,
  frost_cape: `<path d="M20,16 L10,28 L18,26 L14,38 L22,28 L20,34 L26,24 Z" fill="#BFDBFE" stroke="#93C5FD" stroke-width="0.5" opacity="0.85"/>
    <line x1="20" y1="16" x2="14" y2="30" stroke="#93C5FD" stroke-width="0.5" opacity="0.6"/>
    <line x1="20" y1="16" x2="22" y2="30" stroke="#93C5FD" stroke-width="0.5" opacity="0.6"/>`,
  frost_sled: `<path d="M10,40 Q28,44 46,40" stroke="#1E40AF" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <path d="M13,39 Q28,43 43,39" stroke="#93C5FD" stroke-width="1.2" fill="none" stroke-linecap="round"/>
    <line x1="22" y1="38" x2="20" y2="43" stroke="#BFDBFE" stroke-width="1"/>
    <line x1="34" y1="38" x2="36" y2="43" stroke="#BFDBFE" stroke-width="1"/>`,
```

- [ ] **Step 2: 追加烈焰君王套装（4件）**

```javascript
  // ===== 烈焰君王套装 =====
  flame_helm: `<ellipse cx="53" cy="12" rx="7" ry="5" fill="#EF4444" stroke="#F97316" stroke-width="0.8"/>
    <polygon points="50,7 53,1 56,7" fill="#F97316"/>
    <polygon points="47,8 50,3 52,8" fill="#FCD34D"/>
    <polygon points="54,8 56,3 59,8" fill="#FCD34D"/>
    <rect x="47" y="14" width="12" height="2" rx="1" fill="#B91C1C"/>`,
  flame_visor: `<rect x="50" y="18" width="11" height="5" rx="2" fill="#F97316" opacity="0.95"/>
    <rect x="51" y="19" width="9" height="3" rx="1.5" fill="#FCD34D" opacity="0.5"/>
    <line x1="50" y1="20.5" x2="61" y2="20.5" stroke="#EF4444" stroke-width="0.6"/>`,
  flame_wings: `<path d="M18,18 L6,8 L12,20 L4,14 L14,26 L18,22 Z" fill="#F97316" opacity="0.9"/>
    <path d="M18,18 L6,8 L12,20 L4,14 L14,26 L18,22 Z" fill="#FCD34D" opacity="0.35"/>
    <path d="M22,18 L34,8 L28,20 L36,14 L26,26 L22,22 Z" fill="#EF4444" opacity="0.9"/>
    <path d="M22,18 L34,8 L28,20 L36,14 L26,26 L22,22 Z" fill="#FCD34D" opacity="0.35"/>`,
  flame_chariot: `<circle cx="16" cy="40" r="4" fill="none" stroke="#F97316" stroke-width="2"/>
    <circle cx="40" cy="40" r="4" fill="none" stroke="#F97316" stroke-width="2"/>
    <line x1="16" y1="36" x2="16" y2="44" stroke="#EF4444" stroke-width="1"/>
    <line x1="12" y1="40" x2="20" y2="40" stroke="#EF4444" stroke-width="1"/>
    <line x1="36" y1="36" x2="44" y2="44" stroke="#EF4444" stroke-width="1"/>
    <line x1="36" y1="44" x2="44" y2="36" stroke="#EF4444" stroke-width="1"/>
    <line x1="16" y1="40" x2="40" y2="40" stroke="#B91C1C" stroke-width="1.5"/>
    <circle cx="16" cy="40" r="1.5" fill="#FCD34D"/>
    <circle cx="40" cy="40" r="1.5" fill="#FCD34D"/>`,
```

- [ ] **Step 3: 追加暗夜刺客套装（4件）**

```javascript
  // ===== 暗夜刺客套装 =====
  night_hood: `<path d="M46,16 L48,5 L53,3 L58,5 L60,16 L56,13 L53,15 L50,13 Z" fill="#4C1D95" opacity="0.92" stroke="#7C3AED" stroke-width="0.5"/>
    <path d="M48,5 Q53,3 58,5" fill="none" stroke="#C4B5FD" stroke-width="0.6"/>`,
  night_mask: `<path d="M50,17 L55,14 L60,17 L62,22 L60,27 L55,29 L50,27 L48,22 Z" fill="#4C1D95" opacity="0.88" stroke="#7C3AED" stroke-width="0.6"/>
    <line x1="51" y1="21" x2="53" y2="21" stroke="#C4B5FD" stroke-width="1" stroke-linecap="round"/>
    <line x1="57" y1="21" x2="59" y2="21" stroke="#C4B5FD" stroke-width="1" stroke-linecap="round"/>
    <path d="M52,25 Q55,27 58,25" fill="none" stroke="#7C3AED" stroke-width="0.6"/>`,
  night_cloak: `<path d="M20,16 L8,6 L11,18 L5,13 L9,23 L16,20 L14,32 L20,25 Z" fill="#4C1D95" opacity="0.9" stroke="#7C3AED" stroke-width="0.4"/>
    <path d="M20,16 L32,6 L29,18 L35,13 L31,23 L24,20 L26,32 L20,25 Z" fill="#4C1D95" opacity="0.9" stroke="#7C3AED" stroke-width="0.4"/>
    <line x1="20" y1="18" x2="10" y2="10" stroke="#7C3AED" stroke-width="0.5"/>
    <line x1="20" y1="18" x2="30" y2="10" stroke="#7C3AED" stroke-width="0.5"/>`,
  night_shadow: `<ellipse cx="28" cy="43" rx="18" ry="4" fill="#7C3AED" opacity="0.35"/>
    <ellipse cx="28" cy="42" rx="12" ry="2.5" fill="#4C1D95" opacity="0.5"/>
    <ellipse cx="28" cy="41" rx="6" ry="1.5" fill="#7C3AED" opacity="0.4"/>`,
```

- [ ] **Step 4: 追加龙皇套装（4件）**

```javascript
  // ===== 龙皇套装 =====
  dragon_crown: `<path d="M46,14 L48,8 L51,12 L53,4 L55,12 L58,8 L60,14 Z" fill="#1C1917" stroke="#EAB308" stroke-width="1"/>
    <rect x="46" y="13" width="14" height="3" rx="1" fill="#CA8A04"/>
    <circle cx="53" cy="6" r="2" fill="#EAB308"/>
    <circle cx="49" cy="10" r="1.2" fill="#CA8A04"/>
    <circle cx="57" cy="10" r="1.2" fill="#CA8A04"/>`,
  dragon_mask: `<rect x="50" y="16" width="12" height="11" rx="2" fill="#1C1917" stroke="#EAB308" stroke-width="0.8"/>
    <path d="M51,19 Q53,17 55,19 Q57,17 59,19 Q61,17 62,19" fill="none" stroke="#CA8A04" stroke-width="0.7"/>
    <path d="M51,22 Q53,20 55,22 Q57,20 59,22 Q61,20 62,22" fill="none" stroke="#CA8A04" stroke-width="0.7"/>
    <circle cx="53" cy="21" r="0.8" fill="#EAB308"/>
    <circle cx="58" cy="21" r="0.8" fill="#EAB308"/>`,
  dragon_wings: `<path d="M20,17 Q10,7 5,13 Q7,21 16,20 L17,28 Q20,22 20,17 Z" fill="#1C1917" stroke="#EAB308" stroke-width="0.8"/>
    <path d="M20,17 Q30,7 35,13 Q33,21 24,20 L23,28 Q20,22 20,17 Z" fill="#1C1917" stroke="#EAB308" stroke-width="0.8"/>
    <line x1="20" y1="17" x2="7" y2="11" stroke="#CA8A04" stroke-width="0.6"/>
    <line x1="20" y1="17" x2="9" y2="19" stroke="#CA8A04" stroke-width="0.6"/>
    <line x1="20" y1="17" x2="33" y2="11" stroke="#CA8A04" stroke-width="0.6"/>
    <line x1="20" y1="17" x2="31" y2="19" stroke="#CA8A04" stroke-width="0.6"/>`,
  dragon_mount: `<path d="M14,36 L10,43 L14,41 M14,36 L12,43 M14,36 L17,43 L14,41" stroke="#EAB308" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M42,36 L38,43 L42,41 M42,36 L40,43 M42,36 L45,43 L42,41" stroke="#EAB308" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    <line x1="14" y1="37" x2="42" y2="37" stroke="#CA8A04" stroke-width="1"/>`,
```

- [ ] **Step 5: 追加彩虹套装（4件）**

```javascript
  // ===== 彩虹套装 =====
  rainbow_crown: `<path d="M46,14 Q47,6 53,5 Q59,6 60,14" fill="none" stroke="#EF4444" stroke-width="2.8" stroke-linecap="round"/>
    <path d="M47,14 Q48,7 53,6 Q58,7 59,14" fill="none" stroke="#F97316" stroke-width="2"/>
    <path d="M48,14 Q49,8 53,7 Q57,8 58,14" fill="none" stroke="#EAB308" stroke-width="1.6"/>
    <path d="M49,14 Q50,9 53,8 Q56,9 57,14" fill="none" stroke="#22C55E" stroke-width="1.2"/>
    <path d="M50,14 Q51,10 53,9 Q55,10 56,14" fill="none" stroke="#3B82F6" stroke-width="0.8"/>`,
  rainbow_glasses: `<polygon points="52,20 53,17 54,20 56,19 55,22 56,24 54,23 53,26 52,23 50,24 51,22 50,19" fill="#3B82F6" opacity="0.85"/>
    <polygon points="58,20 59,17 60,20 62,19 61,22 62,24 60,23 59,26 58,23 56,24 57,22 56,19" fill="#EF4444" opacity="0.85"/>
    <line x1="55" y1="21.5" x2="57" y2="21.5" stroke="#FCD34D" stroke-width="1.2"/>`,
  rainbow_wings: `<path d="M19,17 Q9,10 6,18 Q8,26 18,24 Z" fill="#EF4444" opacity="0.8"/>
    <path d="M19,24 Q9,28 11,35 Q17,37 20,29 Z" fill="#3B82F6" opacity="0.8"/>
    <path d="M21,17 Q31,10 34,18 Q32,26 22,24 Z" fill="#22C55E" opacity="0.8"/>
    <path d="M21,24 Q31,28 29,35 Q23,37 20,29 Z" fill="#A855F7" opacity="0.8"/>`,
  rainbow_unicorn: `<polygon points="28,42 25,26 31,26" fill="none" stroke="#EF4444" stroke-width="1.2"/>
    <line x1="25.5" y1="39" x2="30.5" y2="39" stroke="#F97316" stroke-width="0.9"/>
    <line x1="25.5" y1="35" x2="30.5" y2="35" stroke="#EAB308" stroke-width="0.9"/>
    <line x1="26" y1="31" x2="30" y2="31" stroke="#22C55E" stroke-width="0.9"/>
    <line x1="26.5" y1="27.5" x2="29.5" y2="27.5" stroke="#3B82F6" stroke-width="0.9"/>
    <circle cx="23" cy="38" r="1.2" fill="#A855F7"/>
    <circle cx="33" cy="35" r="1" fill="#F97316"/>
    <circle cx="22" cy="32" r="0.8" fill="#22C55E"/>`,
```

- [ ] **Step 6: 提交**

```bash
git add turtle-race.html
git commit -m "feat: add SVG art for 20 legendary/mythic set equipment items"
```

---

### Task 3: 套装激活光环

**Files:**
- Modify: `turtle-race.html` (CSS区域, getCosmeticBonuses附近, beginRaceAnimation, render函数)

- [ ] **Step 1: 添加光环 CSS 样式**

在已有的 `@keyframes auraGlow` 定义之后，添加：

```css
/* === 套装激活光环 === */
/* 冰霜领主 */
.aura-frost-2 { filter: drop-shadow(0 0 6px rgba(147,197,253,0.7)); }
.aura-frost-3 { filter: drop-shadow(0 0 10px rgba(147,197,253,0.85)) drop-shadow(0 0 4px rgba(147,197,253,0.5)); }
.aura-frost-4 { animation: auraFrost 2s ease-in-out infinite; }
@keyframes auraFrost {
  0%,100% { filter: drop-shadow(0 0 10px rgba(147,197,253,0.7)) drop-shadow(0 0 4px rgba(147,197,253,0.4)); }
  50% { filter: drop-shadow(0 0 18px rgba(147,197,253,1)) drop-shadow(0 0 8px rgba(147,197,253,0.7)); }
}
/* 烈焰君王 */
.aura-flame-2 { filter: drop-shadow(0 0 6px rgba(249,115,22,0.7)); }
.aura-flame-3 { filter: drop-shadow(0 0 10px rgba(249,115,22,0.85)) drop-shadow(0 0 4px rgba(249,115,22,0.5)); }
.aura-flame-4 { animation: auraFlame 2s ease-in-out infinite; }
@keyframes auraFlame {
  0%,100% { filter: drop-shadow(0 0 10px rgba(249,115,22,0.7)) drop-shadow(0 0 4px rgba(239,68,68,0.4)); }
  50% { filter: drop-shadow(0 0 18px rgba(249,115,22,1)) drop-shadow(0 0 8px rgba(239,68,68,0.7)); }
}
/* 暗夜刺客 */
.aura-night-2 { filter: drop-shadow(0 0 6px rgba(139,92,246,0.7)); }
.aura-night-3 { filter: drop-shadow(0 0 10px rgba(139,92,246,0.85)) drop-shadow(0 0 4px rgba(139,92,246,0.5)); }
.aura-night-4 { animation: auraNight 2s ease-in-out infinite; }
@keyframes auraNight {
  0%,100% { filter: drop-shadow(0 0 10px rgba(139,92,246,0.7)) drop-shadow(0 0 4px rgba(139,92,246,0.4)); }
  50% { filter: drop-shadow(0 0 18px rgba(139,92,246,1)) drop-shadow(0 0 8px rgba(139,92,246,0.7)); }
}
/* 龙皇套装 */
.aura-dragon-2 { filter: drop-shadow(0 0 6px rgba(234,179,8,0.7)); }
.aura-dragon-3 { filter: drop-shadow(0 0 10px rgba(234,179,8,0.85)) drop-shadow(0 0 4px rgba(234,179,8,0.5)); }
.aura-dragon-4 { animation: auraDragon 2s ease-in-out infinite; }
@keyframes auraDragon {
  0%,100% { filter: drop-shadow(0 0 10px rgba(234,179,8,0.7)) drop-shadow(0 0 4px rgba(202,138,4,0.4)); }
  50% { filter: drop-shadow(0 0 18px rgba(234,179,8,1)) drop-shadow(0 0 8px rgba(202,138,4,0.7)); }
}
/* 彩虹套装 */
.aura-rainbow-2 { filter: drop-shadow(0 0 6px rgba(168,85,247,0.7)); }
.aura-rainbow-3 { filter: drop-shadow(0 0 10px rgba(168,85,247,0.85)) drop-shadow(0 0 4px rgba(59,130,246,0.5)); }
.aura-rainbow-4 { animation: auraRainbow 2s linear infinite; }
@keyframes auraRainbow {
  0%   { filter: drop-shadow(0 0 14px rgba(239,68,68,0.9)); }
  16%  { filter: drop-shadow(0 0 14px rgba(249,115,22,0.9)); }
  33%  { filter: drop-shadow(0 0 14px rgba(234,179,8,0.9)); }
  50%  { filter: drop-shadow(0 0 14px rgba(34,197,94,0.9)); }
  66%  { filter: drop-shadow(0 0 14px rgba(59,130,246,0.9)); }
  83%  { filter: drop-shadow(0 0 14px rgba(168,85,247,0.9)); }
  100% { filter: drop-shadow(0 0 14px rgba(239,68,68,0.9)); }
}
```

- [ ] **Step 2: 添加 getEquippedSetAura() 函数**

在 `getEquippedSetInfo()` 函数之后添加：

```javascript
// 返回玩家当前装备的套装光环信息（件数最多且>=2的套装）
function getEquippedSetAura() {
  const setCounts = getEquippedSetInfo(state.equippedCosmetics || []);
  let bestSet = null, bestCount = 0;
  Object.entries(setCounts).forEach(([setId, count]) => {
    if (count >= 2 && count > bestCount) {
      bestSet = setId;
      bestCount = count;
    }
  });
  if (!bestSet) return null;
  const setKeyMap = {
    frost_lord: 'frost',
    flame_king: 'flame',
    night_assassin: 'night',
    dragon_emperor: 'dragon',
    rainbow_set: 'rainbow',
  };
  return {
    setKey: setKeyMap[bestSet] || 'frost',
    level: Math.min(bestCount, 4),
  };
}
```

- [ ] **Step 3: 在 beginRaceAnimation() 的 turtleState 初始化中添加 _aura 字段**

在 `turtleState` 的 `map` 回调内，`rainbowLastZone: -1,` 之后添加：

```javascript
      _aura: isPlayer ? getEquippedSetAura() : null,
```

- [ ] **Step 4: 在 render() 中应用光环 class**

在 `render()` 函数中，找到 `runner.id = 'turtle' + i;` 之后，`runner.style.left = turtleX + 'px';` 之前，添加：

```javascript
    // 套装光环
    if (state.racing && raceTurtleState[i] && raceTurtleState[i]._aura) {
      const { setKey, level } = raceTurtleState[i]._aura;
      runnerClass += ` aura-${setKey}-${level}`;
    }
```

注意：`runnerClass` 字符串此时已包含所有状态类，这行追加光环类到末尾，再赋值给 `runner.className`。

- [ ] **Step 5: 提交**

```bash
git add turtle-race.html
git commit -m "feat: add set bonus aura glow during race (frost/flame/night/dragon/rainbow)"
```
