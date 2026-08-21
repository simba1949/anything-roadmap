---
name: anything-roadmap
description: 为任意领域生成系统化学习路线（模块→主题→章节→知识点四级大纲）。先真实调研前人学习路线作骨架，再为每个知识点搜索并逐条验证权威源（官方文档/博客/视频/网站，英文权威为骨、中文教学为辅），产出 Markdown + 自包含交互 HTML 双格式。当用户想为某领域制定学习大纲、学习路线、系统学习规划、入门路线、curriculum、roadmap、syllabus、learning path 时使用。不做：把已有书籍/课程蒸馏成 skill；生成人物思维 skill。
---

# anything-roadmap — 任意领域学习路线生成器

调用：`/anything-roadmap <领域> [一句话背景]`。背景省略即按零基础制定。

## 铁律（违反任何一条即失败）

1. **零幻觉链接**：进入成品的每一个 URL 都必须真实打开验证过——链接活着、内容对题、出处确实权威。验证不过就不放，宁缺毋滥。
2. **前人路线为骨**：主题树来自搜到的现成学习路线的合成，不是凭模型记忆现编。可信度阶梯：官方路线 > 大学课表/知名课程目录 > 高星 awesome-list > 高信噪比个人路线文 > 社区讨论共识。搜不到 ≥2 条可信路线 → 降级为"官方文档目录结构为骨"，并在成品的生成说明中显式声明。
3. **一站到底**：消歧之后不再向用户提问。用户事后给纠正意见 = 带纠正意见全新重跑全流程，生成新日期目录，绝不修补旧稿。
4. **预算**：每知识点 ≤3 个源、全份封顶 ~40（同一 URL 可挂多个知识点，只占 1 个名额）。超预算时收窄主题树，不是放宽上限。

## 流程

### 0. 消歧（最多两问，问完不再问）
- 领域一句话消歧，如"支付"→支付系统开发还是支付业务？用户答"都行"→ 取最主流解释，并把该假设写进成品"生成说明"。
- 若 args 未带背景，可再问一句"有相关基础吗？"；跳过或含糊 → 零基础。

### 1. 探测搜索通道（先复用已装 skill，再内置）
- 先看环境里已安装的搜索类 skill（当前为 agent-reach），跑 `agent-reach doctor --json` 确认哪些通道今天真的活着，按活着的通道路由。
- 搜索类 skill 不在或通道全死 → 内置 WebSearch/WebFetch。编程库/框架类领域且 context7 可用 → 官方文档优先走 context7（按"可用时用"处理，不硬依赖）。

| 任务 | 首选 | 降级 |
|---|---|---|
| 前人路线 / 官方文档 / 博客 / 网站 / 社区讨论（间接） | Exa：`mcporter call exa.web_search_exa query="…" numResults=5` | WebSearch |
| awesome-list / GitHub 仓库 | `gh search repos "…" --sort stars --limit 10` | WebSearch |
| YouTube 视频 | `yt-dlp --dump-json "ytsearch5:…"` | WebSearch |
| B站视频 | `bili search "…" --type video -n 5` | WebSearch |
| 打开验证链接 | Jina：`curl -s "https://r.jina.ai/<URL>"` → web_reader MCP → WebFetch | — |

### 2. 前人路线调研
中英文都发查询：`<domain> roadmap`、`how to learn <domain>`、`<domain> syllabus site:.edu`、`awesome <domain>`、`how to learn <domain> site:reddit.com`、`<领域> 学习路线`、`<领域> 入门 知乎/掘金`（经 Exa 间接捞）。每条候选打开确认真实存在且内容对口，记录 tier/标题/URL/一句话点评 → priorPaths。数量不足 2 条 → 触发铁律 2 的降级模式。

### 3. 合成主题树
- 按知识内聚拆**模块→主题→章节→知识点**四级；模块编号 M1..Mn 体现学习顺序。
- 每模块记 why（为何这么切）与 refs（支撑它的前人路线序号）；记模块间关联（from/to/note）。
- 控制规模：知识点总数要装得下"每点 ≤3 源、全份 ~40"的预算。

### 4. 搜源
每个知识点按阶梯选 ≤3 个候选：官方文档 > 权威书/课 > 深度博客 > 视频。英文权威为骨、中文教学为辅（视频与入门讲解优先 B站/知乎/掘金）。媒介混搭（doc/blog/video/site）。

### 5. 逐条验证
- 每个候选 URL 按路由表最后一行三通道接力打开，三问全过才入选：活着？对题？权威？否则剔除并计数。
- 候选量大时可用并行子代理加速。全程记 found / passed / dropped。

### 6. 成稿
输出目录 `./<领域>-roadmap-<YYYYMMDD>/`：
- **syllabus.md**：按下方骨架写全内容，正文中文、来源标题保留原文。
- **index.html**：复制本 skill 的 `references/template.html`，只替换 `/* DATA-START */` 到 `/* DATA-END */` 之间的 DATA 对象（schema 见模板内注释），其余不动。生成后自检：`grep -E 'src="http|link[^>]*href="http' index.html` 必须为空（零 CDN 禁令，data-START 内的来源链接除外——它们是 <a> 不带 src）。
- 若为纠正重跑：把用户纠正意见当作本次的硬约束，从第 0 步重新执行全部流程。

**syllabus.md 骨架**：

```
# <领域> 学习路线
> 日期 | 模式（前人路线为骨 / 官方文档回退）| 受众 | 验证：搜到 X / 通过 Y / 剔除 Z

## 0 全局地图
### 领域面貌 / 模块拆分依据 / 模块间关联（M1 ⇄ M2：…）

## M1 <模块名>（why；参考路线 [R1]）
### <主题>
#### <章节>
- **<知识点>** — [DOC·EN Title](url) · [VID·中 标题](url) …
### 练习
1. …

## 附录 A 前人路线（tier · [标题](url) · 一句话点评）
## 附录 B 生成说明（模式、假设、验证统计、纠错=整份重跑）
```

## 边界
- 蒸馏已有书籍/课程、生成人物思维 skill 属于其他工具的职责，本 skill 只做学习路线规划。
- 无工具环境（网页版 Claude、ChatGPT 等）的方法论导出版：`references/playbook.md`，可整段复制给对方 AI 使用，其开头已含验证降级声明。
