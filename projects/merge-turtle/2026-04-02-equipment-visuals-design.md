# 装备槽位约束 + 新装备外观 + 套装光环 设计文档

## 目标

1. 每个部位槽位（head/face/back/mount）只能装备一件，静默替换
2. 为20件新传说/神话装备添加 SVG 图案（显示在龟身上）
3. 比赛中套装激活时显示持续光环特效

---

## Part 1：槽位唯一性

### 变更范围

- `toggleCosmetic(itemId)` — 穿戴前检查同槽位已装备项，有则先移除
- `buyCosmetic(itemId)` — 购买后自动穿戴时同样执行槽位检查

### 逻辑

```
function toggleCosmetic(itemId):
  item = COSMETIC_ITEMS.find(id)
  if already equipped:
    remove from equippedCosmetics  // 正常卸下
    return
  // 穿戴：先移除同槽位旧装备
  if item.slot exists:
    oldItem = equippedCosmetics中找同slot的装备
    if oldItem: remove from equippedCosmetics
  equippedCosmetics.push(itemId)
```

shoes 已有独立的 `state.equippedShoe` 机制，不受影响。

---

## Part 2：20件新装备 SVG 图案

### 坐标系

龟 SVG viewBox: `0 0 64 48`，各槽位参考坐标：
- **head**：cx≈48, cy≈10（龟头顶）
- **face**：cx≈56, cy≈22（龟脸右侧）
- **back**：cx≈28, cy≈14（龟背中部）
- **mount**：cx≈28, cy≈40（龟底部）

### 冰霜领主套装（颜色：#93C5FD冰蓝 / #BFDBFE淡蓝 / #1E3A5F深蓝）

| effect id | 槽位 | 图案描述 |
|-----------|------|---------|
| `frost_crown` | head | 三根上翘的锯齿冰晶刺（深蓝填充+白色描边），排列在头顶 |
| `frost_mask` | face | 两根斜向冰锥覆盖脸部（冰蓝色，半透明） |
| `frost_cape` | back | 下垂的不规则冰块拼接斗篷（淡蓝渐变，带白色边缘） |
| `frost_sled` | mount | 两根向两侧延伸的弧形滑雪板（深蓝，底部平直） |

### 烈焰君王套装（颜色：#F97316橙 / #EF4444红 / #FCD34D黄）

| effect id | 槽位 | 图案描述 |
|-----------|------|---------|
| `flame_helm` | head | 圆弧头盔+顶部三根火焰舌（橙红渐变） |
| `flame_visor` | face | 宽弧形护目镜，橙色镜片+红色镜框 |
| `flame_wings` | back | 左右各一片三角形火焰翼（橙→红→黄渐变） |
| `flame_chariot` | mount | 两个小圆轮+连杆底盘，轮毂有辐射状火焰纹 |

### 暗夜刺客套装（颜色：#7C3AED深紫 / #4C1D95暗紫 / #C4B5FD淡紫）

| effect id | 槽位 | 图案描述 |
|-----------|------|---------|
| `night_hood` | head | 覆盖头顶的三角兜帽（深紫，尖顶） |
| `night_mask` | face | 菱形/蝙蝠脸型面具（暗紫，两侧各一个小尖） |
| `night_cloak` | back | 展开的蝙蝠翼型斗篷（深紫，翼尖有锯齿） |
| `night_shadow` | mount | 向两侧扩散的烟雾/暗影涟漪（淡紫色椭圆，透明度渐变） |

### 龙皇套装（颜色：#EAB308金 / #CA8A04深金 / #1C1917黑）

| effect id | 槽位 | 图案描述 |
|-----------|------|---------|
| `dragon_crown` | head | 帝王冠：中央高拱+两侧小翘角，金色描边+黑色填充 |
| `dragon_mask` | face | 龙鳞面甲：菱形鳞片纹路，金色 |
| `dragon_wings` | back | 大张龙翼：主骨架+三段翼膜，金色骨架+半透明黑膜 |
| `dragon_mount` | mount | 龙爪底座：两只向外展开的三爪龙脚，金色 |

### 彩虹套装（颜色：循环七色 #FF0000→#FF7700→#FFFF00→#00FF00→#0000FF→#8B00FF）

| effect id | 槽位 | 图案描述 |
|-----------|------|---------|
| `rainbow_crown` | head | 拱形彩虹：七色条带依次排列的半圆弧 |
| `rainbow_glasses` | face | 星形眼镜：两个四角星镜片，各色边框 |
| `rainbow_wings` | back | 蝴蝶翅膀：左右对称，三段渐变七彩色块 |
| `rainbow_unicorn` | mount | 独角兽角：螺旋纹彩色锥形，向前下方延伸 |

### 实现方式

在 `ACCESSORY_SVG` 对象中，按 `effect` 字段名添加对应的 SVG 字符串片段（与现有条目格式相同）。

---

## Part 3：套装激活光环

### 光环规则

| 激活件数 | 效果 |
|---------|------|
| 0~1件 | 无光环 |
| 2件 | 淡色静态光环（box-shadow 8px） |
| 3件 | 中等静态光环（box-shadow 12px） |
| 4件 | 强脉冲光环（box-shadow 16px + auraGlow 动画） |

### 光环颜色

| 套装 | 颜色 |
|------|------|
| frost_lord | `rgba(147,197,253,0.8)` 冰蓝 |
| flame_king | `rgba(249,115,22,0.8)` 橙红 |
| night_assassin | `rgba(139,92,246,0.8)` 深紫 |
| dragon_emperor | `rgba(234,179,8,0.8)` 金色 |
| rainbow_set | `rgba(168,85,247,0.7)` 彩虹紫（基础色，加 hue-rotate 动画） |

### 实现方式

1. **计算**：在 `getCosmeticBonuses()` 中（或专用函数），返回 `_aura: { color, intensity, setId }` 信息
2. **应用**：`render()` 中，给玩家龟的 `.turtle-sprite` 元素动态设置 `box-shadow` 和 `animation`
3. **CSS**：
   - `auraGlow` 已有定义（dim/medium/strong 三级）
   - 彩虹专属：`@keyframes rainbowAura` 循环 hue-rotate
4. **范围**：仅比赛中（`scene-race`）玩家龟显示，不影响装备界面

---

## 不在范围内

- AI对手光环（视觉太乱）
- 装备界面龟预览显示光环
- 音效变化
