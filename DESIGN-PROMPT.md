# 知识观测台模板设计提示词

> 本提示词约束 `anything-domain-map` 与 `anything-roadmap` 的离线 HTML 阅读器。决策正本为 `CONSENSUS.md`；数据契约变化必须先更新 schema 与迁移说明。

## Design Read

这是面向学习者的高密度知识可视化产品界面，视觉语言是克制的科技观测台，不是营销落地页，也不是学习进度仪表盘。

- `DESIGN_VARIANCE: 4`：结构稳定，允许少量非对称信息布局。
- `MOTION_INTENSITY: 4`：动效只表达下钻、定位、高亮和视图切换。
- `VISUAL_DENSITY: 7`：能够承载大纲，但用渐进披露控制认知负荷。
- 实现：原生 HTML/CSS/JS，单文件、零 CDN、离线可打开。

## 两个模板

### domain-map template

位置：`skills/anything-domain-map/references/template.html`

只替换脚本中的数据块：

```js
/* DOMAIN_MAP_DATA_START */
const DOMAIN_MAP = {...};
/* DOMAIN_MAP_DATA_END */
```

职责：展示面向所有人的完整知识地图，支持模块总览、主题/章节下钻、知识点搜索和关系层。

### roadmap template

位置：`skills/anything-roadmap/references/template.html`

只替换两段数据：

```js
/* DOMAIN_MAP_DATA_START */
const DOMAIN_MAP = {...};
/* DOMAIN_MAP_DATA_END */

/* LEARNING_PATH_DATA_START */
const LEARNING_PATH = {...};
/* LEARNING_PATH_DATA_END */
```

职责：在完整公共地图上叠加个人能力路径，支持“全局 + 我的路线 / 只看全局 / 只看路线”切换，并从能力定位到相关知识点。

## 立宪要求

1. 先整体后局部，打开页面即可理解领域模块和个人位置。
2. 被延后的内容仍存在于全图，路径取舍和理由可见。
3. HTML 只是大纲阅读器，不做教学、答题、判分、进度存储或复习调度。
4. 公共知识层级与个人能力图在视觉上有明确区别。
5. 科技感来自信息结构、状态反馈和空间关系，不来自无意义霓虹、扫描线堆叠或持续动画。

## 硬约束

- 所有 CSS 和 JS 内联，不加载外部脚本、样式、字体或图片。
- 同一模板的数据 marker 各自只出现一次；不得从 HTML 反向解析正本。
- 不使用随机布局；相同数据始终产生相同页面。
- 所有按钮、折叠和定位可用键盘操作，焦点清晰。
- 支持窄屏、打印和 `prefers-reduced-motion`。
- 空模块、空关系、长名称、缺少可选字段时不出现 `undefined` 或崩溃。
- 动画只使用 transform/opacity，且每个动画必须能说明它传达的状态变化。
- 采用一个暗色主题、一套圆角规则和一个主强调色；正文对比达到 WCAG AA。

## domain-map 信息结构

```text
领域定义与地图统计
→ 搜索、展开深度、关系层工具
→ 边界与核心问题
→ 模块总览
→ 主题/章节/知识点递归下钻
→ 跨节点关系
→ 地图 ID、版本与“非个人路线”声明
```

主题和章节是可选中间层。模块和知识点必须始终可访问。

## roadmap 信息结构

```text
目标情境与毕业任务
→ 全局/个人视图切换
→ 完整领域地图
→ 按顺序排列的个人能力路径
→ 点击能力，高亮其多对多知识点映射
→ 路线 ID 与“学习者保留选择权”声明
```

路径角色使用稳定语义色：核心、必要支撑、按需分支、明确延后。颜色不是唯一编码，同时显示文字标签和边框差异。

## 验收

每次改模板后必须：

1. 用 `tests/fixtures/domain-map.json` 渲染 domain-map；
2. 用 domain-map + `tests/fixtures/learning-path.json` 渲染 roadmap；
3. 对提取的内联 JavaScript 执行 `node --check`；
4. 确认没有外部 `script src` 或 `link href`；
5. 在浏览器检查搜索、折叠、视图切换、能力定位、键盘、窄屏和打印；
6. 对照 JSON 核验模块数、知识点数、能力数和关系数。

交付时说明设计改动、数据契约是否变化、自动检查结果和未完成的浏览器检查。
