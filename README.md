# Garra's Game Library

PS5 风格的游戏合集，为女儿打造的趣味小游戏。

**在线游玩：https://wubin-garra.github.io/TurtleGames/**

## 游戏列表

| 游戏 | 简介 |
|------|------|
| **乌龟赛跑** | 竞速 RPG，装备系统 + 排位赛，成为赛道之王 |
| **合成大乌龟** | 合成收集类，解锁稀有乌龟品种，探索海洋世界 |
| **街头篮球** | 滑动投篮街机游戏，物理引擎 + 灌篮高手 BGM |

## 技术栈

- 纯 HTML / CSS / JavaScript，无框架依赖
- 游戏引擎：Phaser 3（街头篮球）
- 部署：GitHub Pages + GitHub Actions 自动部署

## 项目结构

```
projects/           # 游戏源文件
  turtle-race/
  merge-turtle/
  street-basketball/
  portfolio/        # 游戏库首页
deploy-game-library/  # 部署目录（自动同步）
```

## 部署

推送 `projects/` 下的 HTML 文件到 `main` 分支，GitHub Actions 自动同步到部署目录并发布到 GitHub Pages。

## License

MIT
