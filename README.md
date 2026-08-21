# anything-roadmap

为任意领域生成系统化学习路线的 agent skill：先真实调研**前人的学习路线设计**作骨架，再为每个知识点搜索并**逐条打开验证**权威源（官方文档/博客/视频/网站），产出 Markdown + 自包含交互 HTML（知识星图）双格式。

Generate a systematic learning roadmap for any domain — real prior learning paths as the skeleton, every source link opened and verified one by one, delivered as Markdown + a self-contained interactive HTML "knowledge star chart".

## 安装 / Install

```bash
npx skills add <你的GitHub用户名>/anything-roadmap
```

或手动安装：把 `skills/anything-roadmap/` 整个文件夹复制到你的 agent 技能目录（如 Claude Code 的 `~/.claude/skills/`）。

## 它做什么

调用 `/anything-roadmap <领域> [一句话背景]`（背景省略即零基础），一站式生成：

1. **前人路线调研**：搜索官方学习路线、大学课表、awesome 清单、高质量个人路线文、社区共识，可信度阶梯排序；冷门领域搜不到 ≥2 条时降级为"官方文档目录结构为骨"并显式声明。
2. **四级大纲**：模块 → 主题 → 章节 → 知识点，按知识内聚拆分，含全局地图与模块间关联。
3. **逐条验证的源**：每个知识点 ≤3 个源、全份 ~40 封顶，英文权威为骨、中文教学为辅；每个入选链接都被真实打开验证（活着/对题/权威三问），死链与幻觉链零容忍，结尾附验证统计。
4. **双格式产物**：`syllabus.md` + 单文件自包含 `index.html`（暗色知识星图：模块为星、关联为连线，四级折叠下钻、按媒介筛选，零 CDN、离线可开）。
5. **方法论导出**：`references/playbook.md` 可整段复制给 ChatGPT/网页版 Claude 等无工具环境使用（含验证降级声明）。

设计原则：一站到底不中途提问；纠正意见 = 全新重跑而非修补；一次性快照不做增量刷新。

## 依赖说明

无硬依赖。搜索层优先复用环境里已安装的搜索类 skill（如 agent-reach），缺席时自动降级到内置 WebSearch/WebFetch；链接验证三通道接力（Jina Reader → web_reader → WebFetch），任一可用即可。

## License

MIT
