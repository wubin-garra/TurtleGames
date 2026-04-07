# 段位赛 + 装备品质 + 套装系统 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为乌龟赛跑游戏新增段位赛模式、装备品质分级和套装系统

**Architecture:** 在现有单文件HTML游戏中扩展：(1) 给COSMETIC_ITEMS增加quality字段 (2) 新增套装定义和套装加成计算 (3) 新增段位赛scene和完整比赛流程。所有数据结构、CSS、HTML、JS都在turtle-race.html中。

**Tech Stack:** 纯HTML/CSS/JavaScript，localStorage持久化

---

### Task 1: 装备品质分级 — 数据层

**Files:**
- Modify: `turtle-race.html` (COSMETIC_ITEMS数组, ~lines 2902-2961)

- [ ] **Step 1: 在COSMETIC_ITEMS数组前添加品质等级常量**

在COSMETIC_ITEMS定义之前（约line 2900）添加：

```javascript
const QUALITY_TIERS = [
  { id: 'common',    name: '普通', icon: '⚪', color: '#9CA3AF', border: '#6B7280', glow: 'none' },
  { id: 'fine',      name: '优秀', icon: '🟢', color: '#22C55E', border: '#16A34A', glow: '0 0 8px rgba(34,197,94,0.4)' },
  { id: 'rare',      name: '稀有', icon: '🔵', color: '#3B82F6', border: '#2563EB', glow: '0 0 8px rgba(59,130,246,0.4)' },
  { id: 'epic',      name: '史诗', icon: '🟣', color: '#A855F7', border: '#9333EA', glow: '0 0 10px rgba(168,85,247,0.5)' },
  { id: 'legendary', name: '传说', icon: '🟠', color: '#F97316', border: '#EA580C', glow: '0 0 12px rgba(249,115,22,0.5)' },
  { id: 'mythic',    name: '神话', icon: '🔴', color: '#EF4444', border: '#DC2626', glow: '0 0 14px rgba(239,68,68,0.6)' },
];

function getQualityTier(qualityId) {
  return QUALITY_TIERS.find(q => q.id === qualityId) || QUALITY_TIERS[0];
}
```

- [ ] **Step 2: 给现有COSMETIC_ITEMS每个item添加quality字段**

根据每个item的bonus值分配品质：
- bonus <= 0.08: `quality: 'common'`
- bonus <= 0.12: `quality: 'fine'`
- bonus <= 0.15: `quality: 'rare'`
- bonus <= 0.18: `quality: 'epic'`
- 有extraStats的: `quality: 'legendary'`

逐个检查并添加。例如：
```javascript
// 原来：{ id:'straw_hat', emoji:'🌾', name:'草帽', cost:200, ... bonus:0.08 }
// 改为：{ id:'straw_hat', emoji:'🌾', name:'草帽', cost:200, ... bonus:0.08, quality:'common' }
```

对所有43个item执行此操作。

- [ ] **Step 3: 新增传说品质装备（3套 × 4件 = 12件）**

在COSMETIC_ITEMS数组末尾添加3套传说装备：

```javascript
// ❄️ 冰霜领主套装 (传说)
{ id:'frost_crown', emoji:'❄️', name:'冰霜王冠', cost:15000, effect:'frost_crown', stat:'speed', bonus:0.20, desc:'寒冰之力加持', slot:'head', terrain:'snow', terrainBonus:0.15, quality:'legendary', setId:'frost_lord' },
{ id:'frost_mask', emoji:'🥶', name:'冰霜面罩', cost:12000, effect:'frost_mask', stat:'stamina', bonus:0.18, desc:'极寒耐力', slot:'face', terrain:'snow', terrainBonus:0.15, quality:'legendary', setId:'frost_lord' },
{ id:'frost_cape', emoji:'🧊', name:'冰霜披风', cost:14000, effect:'frost_cape', stat:'sprint', bonus:0.20, desc:'寒风助力', slot:'back', terrain:'snow', terrainBonus:0.15, quality:'legendary', setId:'frost_lord' },
{ id:'frost_sled', emoji:'🛷', name:'冰霜雪橇', cost:16000, effect:'frost_sled', stat:'speed', bonus:0.22, desc:'冰面疾驰', slot:'mount', terrain:'snow', terrainBonus:0.18, quality:'legendary', setId:'frost_lord' },

// 🔥 烈焰君王套装 (传说)
{ id:'flame_helm', emoji:'🔥', name:'烈焰头盔', cost:15000, effect:'flame_helm', stat:'sprint', bonus:0.20, desc:'烈火冲刺', slot:'head', terrain:'volcano', terrainBonus:0.15, quality:'legendary', setId:'flame_king' },
{ id:'flame_visor', emoji:'😈', name:'烈焰面甲', cost:12000, effect:'flame_visor', stat:'speed', bonus:0.18, desc:'火焰之眼', slot:'face', terrain:'volcano', terrainBonus:0.15, quality:'legendary', setId:'flame_king' },
{ id:'flame_wings', emoji:'🦅', name:'烈焰之翼', cost:14000, effect:'flame_wings', stat:'burst', bonus:0.20, desc:'火翼爆发', slot:'back', terrain:'volcano', terrainBonus:0.15, quality:'legendary', setId:'flame_king' },
{ id:'flame_chariot', emoji:'🐎', name:'烈焰战车', cost:16000, effect:'flame_chariot', stat:'sprint', bonus:0.22, desc:'烈焰驱动', slot:'mount', terrain:'volcano', terrainBonus:0.18, quality:'legendary', setId:'flame_king' },

// 🌙 暗夜刺客套装 (传说)
{ id:'night_hood', emoji:'🌙', name:'暗夜兜帽', cost:15000, effect:'night_hood', stat:'dodge', bonus:0.20, desc:'暗影潜行', slot:'head', terrain:'night', terrainBonus:0.15, quality:'legendary', setId:'night_assassin' },
{ id:'night_mask', emoji:'🎭', name:'暗夜面具', cost:12000, effect:'night_mask', stat:'sprint', bonus:0.18, desc:'暗杀冲刺', slot:'face', terrain:'night', terrainBonus:0.15, quality:'legendary', setId:'night_assassin' },
{ id:'night_cloak', emoji:'🦇', name:'暗夜斗篷', cost:14000, effect:'night_cloak', stat:'dodge', bonus:0.20, desc:'蝙蝠闪避', slot:'back', terrain:'night', terrainBonus:0.15, quality:'legendary', setId:'night_assassin' },
{ id:'night_shadow', emoji:'👻', name:'暗影坐骑', cost:16000, effect:'night_shadow', stat:'speed', bonus:0.22, desc:'暗影飞驰', slot:'mount', terrain:'night', terrainBonus:0.18, quality:'legendary', setId:'night_assassin' },
```

- [ ] **Step 4: 新增神话品质装备（2套 × 4件 = 8件）**

```javascript
// 🐉 龙皇套装 (神话)
{ id:'dragon_crown', emoji:'🐉', name:'龙皇冠冕', cost:25000, effect:'dragon_crown', stat:'speed', bonus:0.24, desc:'龙之威压', slot:'head', terrain:'all', terrainBonus:0.10, quality:'mythic', setId:'dragon_emperor' },
{ id:'dragon_mask', emoji:'🐲', name:'龙皇面甲', cost:22000, effect:'dragon_mask', stat:'sprint', bonus:0.22, desc:'龙息冲刺', slot:'face', terrain:'all', terrainBonus:0.10, quality:'mythic', setId:'dragon_emperor' },
{ id:'dragon_wings', emoji:'🪽', name:'龙皇双翼', cost:24000, effect:'dragon_wings', stat:'burst', bonus:0.24, desc:'龙翼爆发', slot:'back', terrain:'all', terrainBonus:0.10, quality:'mythic', setId:'dragon_emperor' },
{ id:'dragon_mount', emoji:'🐲', name:'神龙坐骑', cost:28000, effect:'dragon_mount', stat:'speed', bonus:0.25, desc:'御龙飞驰', slot:'mount', terrain:'all', terrainBonus:0.12, quality:'mythic', setId:'dragon_emperor' },

// 🌈 彩虹套装 (神话)
{ id:'rainbow_crown', emoji:'🌈', name:'彩虹王冠', cost:25000, effect:'rainbow_crown', stat:'luck', bonus:0.22, desc:'七彩好运', slot:'head', quality:'mythic', setId:'rainbow_set' },
{ id:'rainbow_glasses', emoji:'🤩', name:'彩虹眼镜', cost:22000, effect:'rainbow_glasses', stat:'speed', bonus:0.22, desc:'七彩视界', slot:'face', quality:'mythic', setId:'rainbow_set' },
{ id:'rainbow_wings', emoji:'🦋', name:'彩虹蝶翼', cost:24000, effect:'rainbow_wings', stat:'sprint', bonus:0.24, desc:'蝶舞冲刺', slot:'back', quality:'mythic', setId:'rainbow_set' },
{ id:'rainbow_unicorn', emoji:'🦄', name:'彩虹独角兽', cost:28000, effect:'rainbow_unicorn', stat:'speed', bonus:0.25, desc:'独角飞驰', slot:'mount', quality:'mythic', setId:'rainbow_set' },
```

- [ ] **Step 5: 添加套装定义常量**

在QUALITY_TIERS之后添加：

```javascript
const SET_BONUSES = {
  frost_lord: {
    name: '❄️ 冰霜领主', quality: 'legendary', theme: 'snow',
    auraColor: 'rgba(147,197,253,0.3)',
    bonuses: {
      2: { speed: 0.10, label: '速度+10%' },
      3: { speed: 0.18, stamina: 0.12, label: '速度+18%, 耐力+12%' },
      4: { speed: 0.25, terrainBonus: { snow: 0.30 }, specialEffect: 'freeze', label: '速度+25%, 雪地+30%, 冰冻特效' },
    }
  },
  flame_king: {
    name: '🔥 烈焰君王', quality: 'legendary', theme: 'volcano',
    auraColor: 'rgba(249,115,22,0.3)',
    bonuses: {
      2: { sprint: 0.10, label: '冲刺+10%' },
      3: { sprint: 0.18, speed: 0.12, label: '冲刺+18%, 速度+12%' },
      4: { sprint: 0.25, terrainBonus: { volcano: 0.30 }, specialEffect: 'blaze', label: '冲刺+25%, 火山+30%, 烈焰特效' },
    }
  },
  night_assassin: {
    name: '🌙 暗夜刺客', quality: 'legendary', theme: 'night',
    auraColor: 'rgba(139,92,246,0.3)',
    bonuses: {
      2: { dodge: 0.10, label: '闪避+10%' },
      3: { dodge: 0.18, sprint: 0.12, label: '闪避+18%, 冲刺+12%' },
      4: { dodge: 0.25, terrainBonus: { night: 0.30 }, specialEffect: 'stealth', label: '闪避+25%, 夜间+30%, 隐身特效' },
    }
  },
  dragon_emperor: {
    name: '🐉 龙皇套装', quality: 'mythic', theme: 'all',
    auraColor: 'rgba(234,179,8,0.4)',
    bonuses: {
      2: { speed: 0.08, sprint: 0.08, dodge: 0.08, stamina: 0.08, burst: 0.08, label: '全属性+8%' },
      3: { speed: 0.15, sprint: 0.15, dodge: 0.15, stamina: 0.15, burst: 0.15, label: '全属性+15%' },
      4: { speed: 0.22, sprint: 0.22, dodge: 0.22, stamina: 0.22, burst: 0.22, terrainBonus: { all: 0.20 }, specialEffect: 'dragonfire', label: '全属性+22%, 全地形+20%, 龙焰特效' },
    }
  },
  rainbow_set: {
    name: '🌈 彩虹套装', quality: 'mythic', theme: 'rainbow',
    auraColor: 'rgba(168,85,247,0.4)',
    bonuses: {
      2: { luck: 0.10, speed: 0.08, label: '幸运+10%, 速度+8%' },
      3: { luck: 0.18, speed: 0.15, label: '幸运+18%, 速度+15%' },
      4: { luck: 0.25, speed: 0.20, terrainBonus: { rainbow: 0.30 }, specialEffect: 'rainbow_burst', label: '幸运+25%, 速度+20%, 彩虹赛道+30%, 七彩特效' },
    }
  },
};
```

- [ ] **Step 6: 添加套装加成计算函数**

在getCosmeticBonuses()函数附近（约line 3055后）添加：

```javascript
function getEquippedSetInfo(equippedCosmetics) {
  // Count equipped pieces per set
  const setCounts = {};
  equippedCosmetics.forEach(id => {
    const item = COSMETIC_ITEMS.find(c => c.id === id);
    if (item && item.setId) {
      setCounts[item.setId] = (setCounts[item.setId] || 0) + 1;
    }
  });
  return setCounts;
}

function getSetBonuses(equippedCosmetics) {
  const setCounts = getEquippedSetInfo(equippedCosmetics);
  const totalBonuses = {};
  const activeEffects = [];

  Object.entries(setCounts).forEach(([setId, count]) => {
    const setDef = SET_BONUSES[setId];
    if (!setDef) return;
    // Apply highest qualifying tier
    const tier = count >= 4 ? 4 : count >= 3 ? 3 : count >= 2 ? 2 : 0;
    if (tier === 0) return;
    const bonus = setDef.bonuses[tier];
    Object.entries(bonus).forEach(([key, val]) => {
      if (key === 'label' || key === 'terrainBonus' || key === 'specialEffect') return;
      totalBonuses[key] = (totalBonuses[key] || 0) + val;
    });
    if (bonus.terrainBonus) {
      totalBonuses._terrainBonus = bonus.terrainBonus;
    }
    if (bonus.specialEffect) {
      activeEffects.push(bonus.specialEffect);
    }
  });
  totalBonuses._activeEffects = activeEffects;
  return totalBonuses;
}
```

- [ ] **Step 7: 将套装加成集成到getCosmeticBonuses()**

修改现有的getCosmeticBonuses()函数，在返回前合并套装加成：

```javascript
// 在getCosmeticBonuses()函数末尾，return之前添加：
const setBonuses = getSetBonuses(state.equippedCosmetics);
Object.entries(setBonuses).forEach(([key, val]) => {
  if (key.startsWith('_')) return; // skip meta keys
  bonuses[key] = (bonuses[key] || 0) + val;
});
if (setBonuses._terrainBonus) {
  bonuses._setTerrainBonus = setBonuses._terrainBonus;
}
if (setBonuses._activeEffects) {
  bonuses._activeEffects = setBonuses._activeEffects;
}
```

- [ ] **Step 8: 提交**

```bash
git add turtle-race.html
git commit -m "feat: add equipment quality tiers, set definitions, and set bonus calculation"
```

---

### Task 2: 套装特效在比赛中的实现

**Files:**
- Modify: `turtle-race.html` (tick()函数 ~lines 4636-5159, beginRaceAnimation() ~lines 4565-4627)

- [ ] **Step 1: 在beginRaceAnimation()中初始化套装特效状态**

在turtleState初始化中（约line 4590）为玩家龟添加套装特效信息：

```javascript
// 在 const turtleStates = raceTurtles.map((t, i) => { ... }) 内部添加：
activeSetEffects: i === state.selected ? (getCosmeticBonuses()._activeEffects || []) : (t._aiSetEffects || []),
freezeCooldown: 0,    // 冰冻特效冷却
stealthCharge: 0,     // 隐身特效充能
dragonFireReady: true, // 龙焰反弹就绪
rainbowLastZone: -1,  // 彩虹上次区域
```

- [ ] **Step 2: 在tick()函数中添加套装特效逻辑**

在tick()的速度计算之后、进度更新之前（约line 4820附近）添加：

```javascript
// === 套装特效处理 ===
const ts = turtleStates[i];
if (ts.activeSetEffects && ts.activeSetEffects.length > 0) {
  // ❄️ 冰冻特效：每圈冻结1名对手0.5秒
  if (ts.activeSetEffects.includes('freeze') && ts.freezeCooldown <= 0) {
    if (progress[i] > 0 && Math.floor(progress[i]) > Math.floor(progress[i] - effectiveSpeed * dt)) {
      // 刚跨过整圈
      const opponents = [0,1,2,3].filter(j => j !== i && !state.finished.includes(j));
      if (opponents.length > 0) {
        const target = opponents[Math.floor(Math.random() * opponents.length)];
        turtleStates[target].slowTimer = Math.max(turtleStates[target].slowTimer, 30); // 0.5秒
        ts.freezeCooldown = 60; // 1秒冷却
        showSetEffect(target, '❄️');
      }
    }
  }
  if (ts.freezeCooldown > 0) ts.freezeCooldown--;

  // 🔥 烈焰特效：冲刺阶段额外+15%
  if (ts.activeSetEffects.includes('blaze')) {
    const lapProgress = progress[i] % 1;
    if (lapProgress > 0.80) {
      effectiveSpeed *= 1.15;
    }
  }

  // 🌙 隐身特效：被障碍物命中时50%闪避
  // (集成在障碍物命中逻辑中，见下方)

  // 🐉 龙焰特效：被减速时反弹给最近对手
  if (ts.activeSetEffects.includes('dragonfire') && ts.dragonFireReady && ts.slowTimer > 0) {
    const opponents = [0,1,2,3].filter(j => j !== i && !state.finished.includes(j));
    if (opponents.length > 0) {
      // 找最近对手
      let closest = opponents[0];
      let minDist = Math.abs(progress[opponents[0]] - progress[i]);
      opponents.forEach(j => {
        const d = Math.abs(progress[j] - progress[i]);
        if (d < minDist) { minDist = d; closest = j; }
      });
      turtleStates[closest].slowTimer = Math.max(turtleStates[closest].slowTimer, ts.slowTimer);
      ts.slowTimer = 0;
      ts.dragonFireReady = false;
      setTimeout(() => { ts.dragonFireReady = true; }, 3000);
      showSetEffect(closest, '🐉');
    }
  }

  // 🌈 彩虹特效：换区域时+20%加速1秒
  if (ts.activeSetEffects.includes('rainbow_burst')) {
    const currentZone = Math.floor((progress[i] % 1) * 7);
    if (ts.rainbowLastZone !== -1 && currentZone !== ts.rainbowLastZone) {
      ts.momentum *= 1.20;
      setTimeout(() => { if (ts.momentum > 1.0) ts.momentum /= 1.20; }, 1000);
      showSetEffect(i, '🌈');
    }
    ts.rainbowLastZone = currentZone;
  }
}
```

- [ ] **Step 3: 修改障碍物命中逻辑，集成隐身特效**

在tick()中的障碍物命中判断处（约line 4748-4785），包裹stealth闪避检查：

```javascript
// 在障碍物命中时，原来直接设置slowTimer的地方：
// 改为：
let dodged = false;
if (ts.activeSetEffects && ts.activeSetEffects.includes('stealth')) {
  if (Math.random() < 0.5) {
    dodged = true;
    showSetEffect(i, '💨');
  }
}
if (!dodged) {
  ts.slowTimer = 30;
  // ... 原有的障碍物减速逻辑
}
```

- [ ] **Step 4: 添加showSetEffect()视觉提示函数**

```javascript
function showSetEffect(turtleIndex, emoji) {
  const turtleEl = document.querySelectorAll('.turtle-sprite')[turtleIndex];
  if (!turtleEl) return;
  const effectEl = document.createElement('div');
  effectEl.textContent = emoji;
  effectEl.style.cssText = `
    position:absolute; top:-25px; left:50%; transform:translateX(-50%);
    font-size:20px; animation:setEffectPop 0.8s ease-out forwards;
    pointer-events:none; z-index:100;
  `;
  turtleEl.style.position = 'relative';
  turtleEl.appendChild(effectEl);
  setTimeout(() => effectEl.remove(), 800);
}
```

- [ ] **Step 5: 添加套装特效CSS动画**

```css
@keyframes setEffectPop {
  0% { opacity:1; transform:translateX(-50%) translateY(0) scale(0.5); }
  50% { opacity:1; transform:translateX(-50%) translateY(-15px) scale(1.2); }
  100% { opacity:0; transform:translateX(-50%) translateY(-30px) scale(0.8); }
}

@keyframes auraGlow {
  0%, 100% { box-shadow: 0 0 8px var(--aura-color); }
  50% { box-shadow: 0 0 16px var(--aura-color); }
}
```

- [ ] **Step 6: 提交**

```bash
git add turtle-race.html
git commit -m "feat: implement set special effects in race (freeze, blaze, stealth, dragonfire, rainbow)"
```

---

### Task 3: 商店UI更新 — 品质标签和套装展示

**Files:**
- Modify: `turtle-race.html` (renderShop()函数 ~lines 2619-2716, CSS样式)

- [ ] **Step 1: 添加品质标签CSS样式**

```css
.quality-badge {
  display: inline-block; padding: 1px 6px; border-radius: 8px;
  font-size: 11px; font-weight: 700; margin-left: 4px;
  vertical-align: middle;
}
.item-card {
  border: 2px solid var(--border); border-radius: 10px;
  padding: 8px; margin: 4px 0; transition: all 0.2s;
  position: relative;
}
.item-card[data-quality="common"] { border-color: #6B7280; }
.item-card[data-quality="fine"] { border-color: #22C55E; }
.item-card[data-quality="rare"] { border-color: #3B82F6; }
.item-card[data-quality="epic"] { border-color: #A855F7; box-shadow: 0 0 8px rgba(168,85,247,0.3); }
.item-card[data-quality="legendary"] { border-color: #F97316; box-shadow: 0 0 10px rgba(249,115,22,0.4); }
.item-card[data-quality="mythic"] { border-color: #EF4444; box-shadow: 0 0 12px rgba(239,68,68,0.5); animation: mythicPulse 2s ease-in-out infinite; }

@keyframes mythicPulse {
  0%, 100% { box-shadow: 0 0 12px rgba(239,68,68,0.5); }
  50% { box-shadow: 0 0 20px rgba(239,68,68,0.8); }
}

.set-tag {
  display: inline-block; padding: 1px 5px; border-radius: 6px;
  font-size: 10px; background: rgba(255,255,255,0.1); margin-left: 4px;
}
```

- [ ] **Step 2: 修改renderShop()中装备渲染，添加品质显示**

在renderShop()中渲染每个cosmetic item时，添加品质标签和套装标记：

```javascript
// 替换原来的item渲染逻辑，在item名称后添加品质标签
const tier = getQualityTier(item.quality || 'common');
const qualityBadge = `<span class="quality-badge" style="background:${tier.color}20;color:${tier.color};border:1px solid ${tier.color}">${tier.icon} ${tier.name}</span>`;
const setTag = item.setId && SET_BONUSES[item.setId]
  ? `<span class="set-tag">${SET_BONUSES[item.setId].name}</span>`
  : '';
// 在item卡片div上添加 data-quality="${item.quality || 'common'}"
```

- [ ] **Step 3: 在商店添加套装收集进度展示**

在商店页面（renderShop()）底部添加套装区域：

```javascript
// 套装展示区
let setHtml = '<div style="margin-top:16px;padding-top:12px;border-top:1px solid var(--border)">';
setHtml += '<div style="font-size:16px;font-weight:700;margin-bottom:10px;color:var(--gold)">🎯 套装收藏</div>';

Object.entries(SET_BONUSES).forEach(([setId, setDef]) => {
  const setItems = COSMETIC_ITEMS.filter(c => c.setId === setId);
  const ownedCount = setItems.filter(c => state.ownedCosmetics.includes(c.id)).length;
  const equippedCount = setItems.filter(c => state.equippedCosmetics.includes(c.id)).length;
  const tier = getQualityTier(setDef.quality);

  setHtml += `<div class="item-card" data-quality="${setDef.quality}" style="margin-bottom:8px">`;
  setHtml += `<div style="font-weight:700;font-size:14px">${setDef.name} <span class="quality-badge" style="background:${tier.color}20;color:${tier.color};border:1px solid ${tier.color}">${tier.icon} ${tier.name}</span></div>`;
  setHtml += `<div style="font-size:12px;color:var(--text-muted);margin:4px 0">收集进度: ${ownedCount}/${setItems.length} | 已装备: ${equippedCount}件</div>`;

  // 显示套装件
  setHtml += '<div style="display:flex;gap:6px;margin:6px 0;flex-wrap:wrap">';
  setItems.forEach(item => {
    const owned = state.ownedCosmetics.includes(item.id);
    const equipped = state.equippedCosmetics.includes(item.id);
    const opacity = owned ? 1 : 0.35;
    const border = equipped ? `2px solid ${tier.color}` : '2px solid transparent';
    setHtml += `<div style="opacity:${opacity};border:${border};border-radius:8px;padding:4px 8px;font-size:13px;background:rgba(255,255,255,0.05)">${item.emoji} ${item.name}</div>`;
  });
  setHtml += '</div>';

  // 显示套装效果
  [2,3,4].forEach(n => {
    const bonus = setDef.bonuses[n];
    const active = equippedCount >= n;
    setHtml += `<div style="font-size:11px;color:${active ? tier.color : 'var(--text-muted)'};margin:2px 0;${active ? 'font-weight:600' : ''}">`;
    setHtml += `${active ? '✅' : '⬜'} ${n}件: ${bonus.label}`;
    setHtml += '</div>';
  });

  setHtml += '</div>';
});
setHtml += '</div>';
```

- [ ] **Step 4: 提交**

```bash
git add turtle-race.html
git commit -m "feat: add quality badges and set collection display in shop"
```

---

### Task 4: 段位赛 — 数据层和状态管理

**Files:**
- Modify: `turtle-race.html` (state对象, saveGame(), loadGame())

- [ ] **Step 1: 添加段位常量定义**

在QUALITY_TIERS附近添加：

```javascript
const RANKS = [
  { id: 'bronze',   name: '青铜', icon: '🥉', color: '#CD7F32', fee: 50,   reward: 200,   aiQuality: null,        aiSlots: 0, aiSetId: null },
  { id: 'silver',   name: '白银', icon: '⚪', color: '#C0C0C0', fee: 100,  reward: 500,   aiQuality: 'common',    aiSlots: 1, aiSetId: null },
  { id: 'gold',     name: '黄金', icon: '🥇', color: '#FFD700', fee: 200,  reward: 1000,  aiQuality: 'fine',      aiSlots: 2, aiSetId: null },
  { id: 'platinum', name: '铂金', icon: '💎', color: '#E5E4E2', fee: 400,  reward: 2000,  aiQuality: 'rare',      aiSlots: 3, aiSetId: null },
  { id: 'diamond',  name: '钻石', icon: '💠', color: '#B9F2FF', fee: 800,  reward: 4000,  aiQuality: 'epic',      aiSlots: 4, aiSetId: null },
  { id: 'star',     name: '星耀', icon: '🌟', color: '#FFD700', fee: 1500, reward: 8000,  aiQuality: 'legendary', aiSlots: 4, aiSetId: 'random_legendary' },
  { id: 'king',     name: '王者', icon: '👑', color: '#FF4500', fee: 3000, reward: 16000, aiQuality: 'mythic',    aiSlots: 4, aiSetId: 'random_mythic' },
];
```

- [ ] **Step 2: 扩展state对象**

在state对象（line 2245）中添加：

```javascript
// 添加到state对象
rank: 0,           // 段位索引 0-6
rankWins: 0,       // 当前段位胜场
rankLosses: 0,     // 当前段位负场
isRankedMode: false, // 是否在段位赛中
```

- [ ] **Step 3: 更新saveGame()和loadGame()**

在saveGame()中添加保存字段：

```javascript
// saveGame() 中添加：
rank: state.rank,
rankWins: state.rankWins,
rankLosses: state.rankLosses,
```

在loadGame()中添加读取：

```javascript
// loadGame() 中添加：
state.rank = save.rank || 0;
state.rankWins = save.rankWins || 0;
state.rankLosses = save.rankLosses || 0;
```

- [ ] **Step 4: 添加AI装备选择函数**

```javascript
function generateAIEquipment(rankIndex) {
  const rank = RANKS[rankIndex];
  if (rank.aiSlots === 0) return { cosmetics: [], shoe: null, setEffects: [] };

  const slots = ['head', 'face', 'back', 'mount'];
  const selectedCosmetics = [];

  // 如果有套装需求，优先选套装
  if (rank.aiSetId) {
    let targetSets;
    if (rank.aiSetId === 'random_legendary') {
      targetSets = Object.keys(SET_BONUSES).filter(k => SET_BONUSES[k].quality === 'legendary');
    } else if (rank.aiSetId === 'random_mythic') {
      targetSets = Object.keys(SET_BONUSES).filter(k => SET_BONUSES[k].quality === 'mythic');
    }
    const chosenSetId = targetSets[Math.floor(Math.random() * targetSets.length)];
    const setItems = COSMETIC_ITEMS.filter(c => c.setId === chosenSetId);
    setItems.forEach(item => selectedCosmetics.push(item.id));
  } else {
    // 按品质随机选装备填满对应槽位数
    const qualityItems = COSMETIC_ITEMS.filter(c => c.quality === rank.aiQuality);
    const usedSlots = [];
    for (let i = 0; i < rank.aiSlots && i < 4; i++) {
      const available = qualityItems.filter(c => !usedSlots.includes(c.slot));
      if (available.length > 0) {
        const pick = available[Math.floor(Math.random() * available.length)];
        selectedCosmetics.push(pick.id);
        usedSlots.push(pick.slot);
      }
    }
  }

  // 钻石及以上加鞋子
  let shoe = null;
  if (rankIndex >= 4) {
    const shoeIdx = Math.floor(Math.random() * SHOE_ITEMS.length);
    shoe = SHOE_ITEMS[shoeIdx].id;
  }

  // 计算套装特效
  const setEffects = (getSetBonuses(selectedCosmetics)._activeEffects) || [];

  return { cosmetics: selectedCosmetics, shoe, setEffects };
}
```

- [ ] **Step 5: 提交**

```bash
git add turtle-race.html
git commit -m "feat: add rank definitions, state management, and AI equipment generation"
```

---

### Task 5: 段位赛 — UI场景和主菜单入口

**Files:**
- Modify: `turtle-race.html` (HTML结构, CSS样式, showScene())

- [ ] **Step 1: 在主菜单添加段位赛按钮**

在scene-start的.start-menu中，"开始比赛"按钮之后添加：

```html
<button class="menu-btn" onclick="showScene('scene-ranked')" style="border-color:#FFD700">
  ⚔️ 段位赛
  <span id="rankBadgeMenu" style="font-size:13px;display:block;margin-top:2px;color:var(--gold)"></span>
</button>
```

- [ ] **Step 2: 添加段位赛场景HTML**

在最后一个scene div之后添加新scene：

```html
<div id="scene-ranked" class="scene">
  <div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;background:radial-gradient(ellipse at 50% 25%,#1a1a3e 0%,#0E2240 30%,#0A1628 70%);gap:12px;padding:20px;position:relative;overflow:hidden">

    <!-- 段位展示 -->
    <div id="rankDisplay" style="text-align:center"></div>

    <!-- 战绩 -->
    <div id="rankRecord" style="display:flex;gap:16px;font-size:15px"></div>

    <!-- 段位进度条 -->
    <div id="rankProgress" style="width:280px;margin:8px 0"></div>

    <!-- 入场费和奖励信息 -->
    <div id="rankInfo" style="text-align:center;font-size:14px;color:var(--text-secondary)"></div>

    <!-- 对手预览 -->
    <div id="rankOpponentPreview" style="text-align:center;margin:8px 0;font-size:13px;color:var(--text-muted)"></div>

    <!-- 按钮 -->
    <button id="rankStartBtn" class="menu-btn" onclick="startRankedGame()" style="width:260px;background:linear-gradient(135deg,#1a1a3e,#2a1a4e);border-color:#FFD700;font-size:18px;padding:14px 32px">
      ⚔️ 开始挑战
    </button>
    <button class="menu-btn" onclick="showScene('scene-start')" style="width:260px">🔙 返回主菜单</button>
  </div>
</div>
```

- [ ] **Step 3: 添加段位赛场景CSS**

```css
.rank-icon {
  font-size: 72px;
  animation: rankFloat 3s ease-in-out infinite;
  filter: drop-shadow(0 4px 12px rgba(255,215,0,0.3));
}
@keyframes rankFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
.rank-name {
  font-size: 32px; font-weight: 900; margin-top: 8px;
  text-shadow: 0 2px 8px rgba(0,0,0,0.5);
}
.rank-star { font-size: 22px; margin: 0 2px; }
.rank-star.filled { opacity: 1; }
.rank-star.empty { opacity: 0.25; }
.rank-progress-bar {
  height: 8px; border-radius: 4px;
  background: rgba(255,255,255,0.1);
  overflow: hidden; margin: 8px 0;
}
.rank-progress-fill {
  height: 100%; border-radius: 4px;
  transition: width 0.5s ease;
}

/* 晋级动画 */
.promote-overlay {
  position: fixed; inset: 0; z-index: 9999;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  background: rgba(0,0,0,0.85);
  animation: promoteIn 0.5s ease-out;
}
@keyframes promoteIn {
  0% { opacity: 0; }
  100% { opacity: 1; }
}
.promote-icon {
  font-size: 100px;
  animation: promoteBounce 1s ease-out;
}
@keyframes promoteBounce {
  0% { transform: scale(0) rotate(-180deg); opacity: 0; }
  60% { transform: scale(1.3) rotate(10deg); opacity: 1; }
  100% { transform: scale(1) rotate(0deg); opacity: 1; }
}
.promote-text {
  font-size: 36px; font-weight: 900; margin-top: 16px;
  animation: promoteSlide 0.6s ease-out 0.3s both;
}
@keyframes promoteSlide {
  0% { transform: translateY(30px); opacity: 0; }
  100% { transform: translateY(0); opacity: 1; }
}

/* 降级动画 */
.demote-text {
  font-size: 28px; font-weight: 700; color: var(--text-secondary);
  animation: demoteShake 0.5s ease-out;
}
@keyframes demoteShake {
  0%, 100% { transform: translateX(0); }
  20% { transform: translateX(-8px); }
  40% { transform: translateX(8px); }
  60% { transform: translateX(-4px); }
  80% { transform: translateX(4px); }
}
```

- [ ] **Step 4: 添加renderRankedScene()函数**

```javascript
function renderRankedScene() {
  const rank = RANKS[state.rank];
  const tier = state.rank;

  // 段位图标和名称
  document.getElementById('rankDisplay').innerHTML = `
    <div class="rank-icon">${rank.icon}</div>
    <div class="rank-name" style="color:${rank.color}">${rank.name}</div>
  `;

  // 战绩星星
  let starsHtml = '<div style="margin:8px 0">';
  // 胜利星星（绿色）
  for (let i = 0; i < 3; i++) {
    starsHtml += `<span class="rank-star ${i < state.rankWins ? 'filled' : 'empty'}" style="color:#22C55E">★</span>`;
  }
  starsHtml += ' <span style="color:var(--text-muted);margin:0 8px">|</span> ';
  // 失败星星（红色）
  for (let i = 0; i < 3; i++) {
    starsHtml += `<span class="rank-star ${i < state.rankLosses ? 'filled' : 'empty'}" style="color:#EF4444">✖</span>`;
  }
  starsHtml += '</div>';
  document.getElementById('rankRecord').innerHTML = starsHtml;

  // 进度条
  const progressPct = (state.rankWins / 3) * 100;
  document.getElementById('rankProgress').innerHTML = `
    <div class="rank-progress-bar">
      <div class="rank-progress-fill" style="width:${progressPct}%;background:linear-gradient(90deg,${rank.color},${rank.color}cc)"></div>
    </div>
  `;

  // 费用和奖励
  const canAfford = state.coins >= rank.fee;
  document.getElementById('rankInfo').innerHTML = `
    <div style="margin:4px 0">🎫 入场费: <span style="color:${canAfford ? 'var(--gold)' : 'var(--danger)'}">${rank.fee} 🪙</span></div>
    <div style="margin:4px 0">🏆 胜利奖励: <span style="color:var(--accent)">${rank.reward} 🪙</span></div>
    <div style="margin:4px 0">💰 当前余额: <span style="color:var(--gold)">${state.coins} 🪙</span></div>
  `;

  // 对手预览
  const nextRankInfo = tier < 6 ? RANKS[tier] : RANKS[6];
  let opponentDesc = '';
  if (nextRankInfo.aiSlots === 0) {
    opponentDesc = '对手无装备，轻松上分！';
  } else {
    const qt = getQualityTier(nextRankInfo.aiQuality);
    opponentDesc = `对手装备: ${nextRankInfo.aiSlots}件 ${qt.icon}${qt.name}`;
    if (nextRankInfo.aiSetId) opponentDesc += ' (含套装效果)';
  }
  document.getElementById('rankOpponentPreview').innerHTML = `⚠️ ${opponentDesc}`;

  // 按钮状态
  document.getElementById('rankStartBtn').disabled = !canAfford;
  document.getElementById('rankStartBtn').style.opacity = canAfford ? 1 : 0.5;

  // 主菜单段位标签
  const menuBadge = document.getElementById('rankBadgeMenu');
  if (menuBadge) menuBadge.textContent = `${rank.icon} ${rank.name}`;
}
```

- [ ] **Step 5: 在showScene()中集成渲染**

在showScene()函数中添加：

```javascript
if (sceneId === 'scene-ranked') renderRankedScene();
```

- [ ] **Step 6: 提交**

```bash
git add turtle-race.html
git commit -m "feat: add ranked match scene UI with rank display, progress, and opponent preview"
```

---

### Task 6: 段位赛 — 比赛流程和晋级/降级逻辑

**Files:**
- Modify: `turtle-race.html` (新增startRankedGame(), 修改finishRace())

- [ ] **Step 1: 添加startRankedGame()函数**

```javascript
function startRankedGame() {
  const rank = RANKS[state.rank];
  if (state.coins < rank.fee) return;

  state.isRankedMode = true;
  state.coins -= rank.fee;

  // 为AI对手生成装备
  state._rankedAIEquipment = [null, null, null].map(() => generateAIEquipment(state.rank));

  // 进入选龟阶段（复用现有流程）
  state.wins = 0;
  state.round = 1;
  state.maxRounds = 1;
  state.pickPhase = true;
  state.trackPickPhase = false;
  state.progress = [0,0,0,0];
  state.finished = [];
  state.usedItems = [];

  saveGame();
  showScene('scene-race');
  render();
}
```

- [ ] **Step 2: 修改beginRaceAnimation()以应用AI装备**

在beginRaceAnimation()中，创建turtleStates时，如果isRankedMode，为非玩家龟应用AI装备加成：

```javascript
// 在turtleStates map中，对非玩家龟（i !== state.selected）：
if (state.isRankedMode && state._rankedAIEquipment) {
  const aiEquip = state._rankedAIEquipment[i > state.selected ? i - 1 : i];
  if (aiEquip && aiEquip.cosmetics.length > 0) {
    // 计算AI装备加成
    let aiSpeedBonus = 0;
    let aiSprintBonus = 0;
    let aiDodgeBonus = 0;
    let aiStaminaBonus = 0;
    aiEquip.cosmetics.forEach(cosId => {
      const item = COSMETIC_ITEMS.find(c => c.id === cosId);
      if (item) {
        if (item.stat === 'speed') aiSpeedBonus += item.bonus;
        if (item.stat === 'sprint') aiSprintBonus += item.bonus;
        if (item.stat === 'dodge') aiDodgeBonus += item.bonus;
        if (item.stat === 'stamina') aiStaminaBonus += item.bonus;
      }
    });
    // Apply bonuses
    ts.baseSpeed *= (1 + aiSpeedBonus);
    ts.sprintBonus = aiSprintBonus;
    ts.dodgeBonus = aiDodgeBonus;
    ts.staminaBonus = aiStaminaBonus;
    ts._aiSetEffects = aiEquip.setEffects;
    ts.activeSetEffects = aiEquip.setEffects;
  }
  if (aiEquip && aiEquip.shoe) {
    const shoe = SHOE_ITEMS.find(s => s.id === aiEquip.shoe);
    if (shoe) ts.baseSpeed *= 1.05; // base shoe bonus
  }
}
```

- [ ] **Step 3: 在render()中显示AI装备图标**

在段位赛中，赛道上每只AI龟旁边显示其装备emoji：

```javascript
// 在render()的龟渲染部分，如果isRankedMode：
if (state.isRankedMode && state._rankedAIEquipment && i !== state.selected) {
  const aiEquipIdx = i > state.selected ? i - 1 : i;
  const aiEquip = state._rankedAIEquipment[aiEquipIdx];
  if (aiEquip) {
    let equipEmojis = '';
    aiEquip.cosmetics.forEach(cosId => {
      const item = COSMETIC_ITEMS.find(c => c.id === cosId);
      if (item) equipEmojis += item.emoji;
    });
    if (aiEquip.shoe) {
      const shoe = SHOE_ITEMS.find(s => s.id === aiEquip.shoe);
      if (shoe) equipEmojis += shoe.emoji;
    }
    // 在龟名称旁显示
    // html += `<span style="font-size:10px">${equipEmojis}</span>`;
  }
}
```

- [ ] **Step 4: 修改finishRace()添加段位赛结算**

在finishRace()函数中，增加段位赛胜负判定：

```javascript
// 在finishRace()中，reward计算之后添加：
if (state.isRankedMode) {
  const rank = RANKS[state.rank];
  if (playerWon) {
    state.rankWins++;
    state.coins += rank.reward;
    if (state.rankWins >= 3) {
      // 晋级
      setTimeout(() => showPromoteAnimation(), 1500);
    }
  } else {
    state.rankLosses++;
    if (state.rankLosses >= 3) {
      // 降级
      setTimeout(() => showDemoteAnimation(), 1500);
    }
  }
  saveGame();
}
```

- [ ] **Step 5: 添加晋级/降级动画函数**

```javascript
function showPromoteAnimation() {
  const oldRank = RANKS[state.rank];
  if (state.rank < 6) {
    state.rank++;
  }
  state.rankWins = 0;
  state.rankLosses = 0;
  const newRank = RANKS[state.rank];
  saveGame();

  const overlay = document.createElement('div');
  overlay.className = 'promote-overlay';
  overlay.innerHTML = `
    <div class="promote-icon">${newRank.icon}</div>
    <div class="promote-text" style="color:${newRank.color}">晋级成功！</div>
    <div style="font-size:20px;margin-top:8px;color:var(--text-secondary);animation:promoteSlide 0.6s ease-out 0.5s both">
      ${oldRank.icon} ${oldRank.name} → ${newRank.icon} ${newRank.name}
    </div>
    <div style="font-size:48px;margin-top:16px;animation:promoteSlide 0.6s ease-out 0.7s both">🎉🎊🎉</div>
    <button class="menu-btn" style="margin-top:24px;width:200px;border-color:${newRank.color};animation:promoteSlide 0.6s ease-out 0.9s both" onclick="this.parentElement.remove();showScene('scene-ranked')">
      继续挑战
    </button>
  `;
  document.body.appendChild(overlay);
}

function showDemoteAnimation() {
  const oldRank = RANKS[state.rank];
  if (state.rank > 0) {
    state.rank--;
  }
  state.rankWins = 0;
  state.rankLosses = 0;
  const newRank = RANKS[state.rank];
  saveGame();

  const overlay = document.createElement('div');
  overlay.className = 'promote-overlay';
  overlay.innerHTML = `
    <div style="font-size:72px">${newRank.icon}</div>
    <div class="demote-text" style="color:var(--danger)">段位下降</div>
    <div style="font-size:18px;margin-top:8px;color:var(--text-secondary)">
      ${oldRank.icon} ${oldRank.name} → ${newRank.icon} ${newRank.name}
    </div>
    <div style="font-size:15px;margin-top:12px;color:var(--text-muted)">
      ${state.rank === 0 ? '青铜保底，不会再降了，加油！💪' : '别灰心，继续努力！💪'}
    </div>
    <button class="menu-btn" style="margin-top:24px;width:200px;border-color:var(--border)" onclick="this.parentElement.remove();showScene('scene-ranked')">
      再来一次
    </button>
  `;
  document.body.appendChild(overlay);
}
```

- [ ] **Step 6: 修改比赛结束后的返回逻辑**

在showGameOver()中，如果isRankedMode，修改返回按钮：

```javascript
// 在showGameOver()中，修改底部按钮
if (state.isRankedMode) {
  // 替换"再来一局"按钮为返回段位赛
  // onclick 改为: state.isRankedMode = false; showScene('scene-ranked');
}
```

- [ ] **Step 7: 提交**

```bash
git add turtle-race.html
git commit -m "feat: implement ranked match game flow with promotion/demotion animations"
```

---

### Task 7: 集成测试和收尾

**Files:**
- Modify: `turtle-race.html`

- [ ] **Step 1: 确保loadGame()正确初始化所有新字段**

检查loadGame()确保新字段有默认值：

```javascript
state.rank = save.rank || 0;
state.rankWins = save.rankWins || 0;
state.rankLosses = save.rankLosses || 0;
state.isRankedMode = false; // 每次加载重置
```

- [ ] **Step 2: 确保场景切换不泄漏状态**

在showScene('scene-start')时重置isRankedMode：

```javascript
// showScene() 中
if (sceneId === 'scene-start') {
  state.isRankedMode = false;
  // ... 原有逻辑
}
```

- [ ] **Step 3: 主菜单显示当前段位**

在showScene('scene-start')时更新段位标签：

```javascript
const menuBadge = document.getElementById('rankBadgeMenu');
if (menuBadge) {
  const rank = RANKS[state.rank];
  menuBadge.textContent = `${rank.icon} ${rank.name}`;
}
```

- [ ] **Step 4: 在浏览器中手动测试完整流程**

验证清单：
1. 主菜单显示段位赛按钮和当前段位
2. 点击段位赛进入段位界面，显示正确的段位、费用、奖励
3. 余额不足时按钮禁用
4. 开始段位赛 → 选龟 → 比赛 → 结果正确
5. 赢3次触发晋级动画，段位正确提升
6. 输3次触发降级动画，段位正确下降
7. 青铜不降级，王者不升级
8. AI对手在高段位穿戴可见装备
9. 套装效果在比赛中正确触发
10. 商店正确显示品质标签和套装进度
11. 刷新页面后段位数据保持

- [ ] **Step 5: 最终提交**

```bash
git add turtle-race.html
git commit -m "feat: complete ranked match system with equipment quality and set bonuses"
```
