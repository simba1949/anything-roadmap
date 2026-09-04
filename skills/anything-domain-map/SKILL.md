---
name: anything-domain-map
description: 为任意领域生成面向所有人的全链路知识地图，覆盖模块、可选主题/章节和知识点，以及客观依赖、应用、边界与来源。产出 domain-map.json、domain-map.md、domain-map.html、validation.md。当用户要领域全貌、完整知识体系、全链路大纲、知识地图、domain map，而不是个人学习路线时使用。
---

# anything-domain-map

生成与具体学习者无关的公共领域地图。核心目标是让人先看见全局，再决定自己的路线。

## 不可违背

1. **公共地图不是个人课程**：不根据某位学习者删减领域，不生成个人能力或进度。
2. **完整等于边界清楚**：覆盖基础、核心、主要分支、典型应用、相邻接口和前沿；不追求无限细节。
3. **结构有证据**：优先消费 `anything-research` 的领域制图卷宗；所有进入正式产物的 URL 必须实际打开验证。
4. **层级服从知识内聚**：结构固定为 `模块 →〔主题〕→〔章节〕→ 知识点`。模块和知识点必有，主题/章节仅在能聚合至少两个有意义子项时出现。
5. **一个机器正本**：先完成并验证 `domain-map.json`，再由它生成 Markdown 与 HTML，禁止三份内容分别编造。
6. **典型顺序不是个人路线**：可给客观依赖和典型遍历顺序，但必须显式声明不针对任何学习者。

## 输入

调用：`/anything-domain-map <领域> [范围说明]`

领域有实质歧义时问一个范围问题。若范围仍宽，采用主流定义，并把包含/排除项写入地图；不要向用户索取学习背景，因为本 skill 与个人背景无关。

## 工作流

### 1. 获取证据

- 优先寻找同领域、仍在有效期内的领域制图 `research.md`。
- 没有时，若 `anything-research` 可用，以“领域制图模式”调用它：领域边界与核心问题、知识结构与依赖、主要分支、应用与前沿、权威结构来源、分歧与缺口。
- 联网工具（例如 `agent-reach`）只是被 research 层使用的资料访问路由，不是领域地图的研究入口，也不应直接替代 research dossier。
- research 不可用时自行完成同等调研，并在 `validation.md` 声明降级。
- 结构来源优先级：官方知识体系/标准 → 大学培养方案与课程群 → 权威教材目录 → 专业组织知识体 → 多条高质量课程路线的共识。

### 2. 划定边界

写清领域定义、包含项、排除项、相邻接口和时效截止日。若同名异义未解决，不进入制图。

### 3. 建模

阅读 [references/domain-map-schema.md](references/domain-map-schema.md)，先构建 `domain-map.json`：

- 模块按领域结构而非学习周次划分；
- 知识点是展示叶子；
- 跨模块关系放 `relationships`，不靠重复节点表达；
- 每个知识点记录为何重要、解决什么问题、应用和来源；
- 使用稳定 ID；显示名变化不应改变 ID；
- `typical_traversal` 只表达一种常见浏览顺序。

### 4. 验证结构化正本

运行：

```bash
python scripts/validate_domain_map.py <输出目录>/domain-map.json
```

修复所有 error 后再渲染。warning 必须在 `validation.md` 解释或修复。

### 5. 生成四个产物

输出目录：`./<domain>-domain-map-<version>/`

- `domain-map.json`：机器正本。
- `domain-map.md`：按 [references/domain-map-template.md](references/domain-map-template.md) 生成的人类可审阅全链路大纲。
- `domain-map.html`：复制 `references/template.html`，用脚本嵌入 JSON：

```bash
python scripts/render_domain_map.py <输出目录>/domain-map.json <输出目录>/domain-map.html
```

- `validation.md`：按 [references/validation-template.md](references/validation-template.md) 记录事实、来源、结构、覆盖、渲染检查和缺口。

### 6. 验收

- JSON 校验通过；
- Markdown 与 HTML 的模块数、知识点数、ID 和来源数与 JSON 一致；
- 所有中间层至少有两个子项；
- 所有关系端点和来源引用存在；
- HTML 单文件、零 CDN、键盘可操作、支持窄屏/打印/`prefers-reduced-motion`；
- 用户能从总览逐层下钻到知识点，并可单独查看跨模块关系；
- `validation.md` 坦白覆盖边界、低置信结构和信息缺口。

交付时列出四个文件的绝对路径。不要替用户生成个人路线；那属于 `anything-roadmap`。
