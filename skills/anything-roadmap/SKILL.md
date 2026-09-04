---
name: anything-roadmap
description: 基于公共 domain-map、学习目标、基础与约束，为具体学习者生成透明的个人能力路径和可独立学习的课程包。产出学习契约、learning-path.json、模块化内容、self-study.md、roadmap.md/html 与验证报告。当用户要为自己制定学习路线、课程、入门或进阶计划时使用；面向所有人的完整领域大纲改用 anything-domain-map。
---

# anything-roadmap

为具体学习者把公共知识地图编译成个人能力路径和自学课程。AI 可以优化路径，但必须让学习者看见全局、取舍和调整理由。

## 边界

- 要领域全貌、全链路大纲、知识体系，不涉及个人目标：使用 `anything-domain-map`。
- 要实际上课、复习、评估或继续上次学习：使用 `anything-tutor`。
- 本 skill 负责确认学习契约、生成个人路线与课程包，不把阅读进度当成掌握。

## 不可违背

1. **毕业任务驱动**：从真实任务的成功条件反推能力，不把知识点标题机械改写成“理解”。
2. **全局始终可见**：所有个人路线必须引用完整 `domain-map`；被延后内容留在地图中并说明原因。
3. **能力可观察**：能力节点写成“学习者能在什么条件下完成什么行为”。
4. **二八有依据**：先判断目标必要性，再按依赖杠杆、使用频率和犯错代价排序，记录每个选择理由。
5. **一个高价值确认点**：生成昂贵课程前让用户确认学习契约；确认后不中途逐模块审批。
6. **教学闭环完整**：每项核心能力都有诊断、教学、练习、评分、错误和补救契约。
7. **来源不是教学**：综合验证过的来源形成直接可学的内容；链接只承担证据和拓展作用。
8. **路线正本不可被 tutor 静默改写**：运行时偏移写入 learner state，重大目标变化才重生成 roadmap。

## 1. 获取公共地图

接受显式 `domain-map.json` 路径；否则在当前工作区寻找同领域最新兼容版本。若不存在且 `anything-domain-map` 可用，调用它生成。无法获得正式地图时可以生成“待验证草案”，但必须显式降级，不能假装存在公共正本。

若生成地图或课程需要联网研究，调用 `anything-research` 负责问题拆解和证据验证；其底层联网访问工具（例如 `agent-reach`）只是取得原始资料的路由，不是面向学习者的研究入口。不要把“搜索到网页”当成研究完成，也不要在用户可见的教学流程中要求用户理解或调用底层路由工具。

开始个性化前，先向学习者展示领域模块、主要关系和当前地图边界。

## 2. 建立学习契约

渐进获得：

- 目标情境和希望解决的真实问题；
- 可观察的毕业任务；
- 基础自述；
- 时间、工具、语言、环境等约束；
- 完成证据与不可接受的失败。

用少量有分叉价值的题目探测起点。不会改变路线的问题不要问。基础自述和一次答对只能作为弱证据。

按 [references/learning-contract-template.md](references/learning-contract-template.md) 生成 `learning-contract.md` 草案，展示：毕业任务、核心路径摘要、延后项、假设、约束和完成证据。等待用户确认一次；修改后再次确认。确认前不批量生成教学内容。

## 3. 从任务反推能力

```text
毕业任务 → 成功条件 → 子任务 → 可验证能力 → 所需知识点 → 前置能力
```

阅读 [references/learning-path-schema.md](references/learning-path-schema.md) 创建 `learning-path.json`。

- 能力与知识点允许多对多；
- 记录知识点在能力中的作用：理解基础、操作方法、判断依据、约束条件或拓展背景；
- `prerequisite_capability_ids` 组成无环图；
- 诊断通过的能力仍保留，标记初始证据并安排低频复测，不从地图消失；
- 每项能力标注教学策略和验证方式。

## 4. 选择透明路径

把能力分为：

- `core`：直接贡献毕业任务；
- `support`：缺失会阻断核心；
- `branch`：特定错误、兴趣或情境下进入；
- `deferred`：属于完整地图，但当前回报较低。

时间不足时缩小目标或推迟分支，不降低核心能力的证据标准。为每个能力写 `selection_reason`；deferred 也必须写延后理由。

## 5. 生成课程内容

核心路径和高概率补救支线提前生成，长尾内容按需扩展。只为入选能力搜索教学型材料，所有 URL 实际打开验证；不要重复 domain-map 的全领域结构调研。

阅读 [references/course-unit-template.md](references/course-unit-template.md)。每个核心能力至少包含：能力陈述、前置诊断、心智模型、正例/反例、首次尝试、主动回忆、近迁移任务、答案或量规、错误分类、补救支线、来源。

允许两种学习顺序：默认建议小型尝试后精准教学；用户可以先系统讲授再尝试。任何讲授、观看或跟做结果都不能直接标记为掌握。

课程保存种子任务和变式约束。变式必须保持被测能力与判定条件不变，不能只换数字后声称完成远迁移。

## 6. 产物

输出目录：`./<goal>-roadmap-<version>/`

```text
learning-contract.md
learning-path.json
content/
self-study.md
roadmap.md
roadmap.html
validation.md
```

- `content/` 是模块化教学内容正本；
- `self-study.md` 是按 [references/self-study-template.md](references/self-study-template.md) 生成、可脱离 tutor 的合订版；
- `roadmap.md` 是按 [references/roadmap-template.md](references/roadmap-template.md) 生成的个人路线与取舍文字视图；
- `roadmap.html` 只负责观看大纲、定位、关系和下钻，不负责教学、判分、进度或复习；
- `validation.md` 使用 [references/validation-template.md](references/validation-template.md)。

用公共地图和个人路径渲染单文件 HTML：

```bash
python scripts/render_roadmap.py path/to/domain-map.json <输出目录>/learning-path.json <输出目录>/roadmap.html
```

## 7. 验证

```bash
python scripts/validate_learning_path.py <输出目录>/learning-path.json path/to/domain-map.json
```

修复所有 error；解释或修复 warning。再执行独立评价轮，用初学、部分掌握和高水平三种模拟学习者攻击题目歧义、泄题、条件不足、错误答案、量规失真和伪迁移，把结果写入 `validation.md`。

最终确认：

- 每项 core 能力可回溯到毕业任务和知识点；
- 能力依赖无环且推荐顺序尊重依赖；
- core/support/branch/deferred 均有理由；
- 每项 core 有完整教学闭环和可执行评价；
- 静态课程无需 tutor 才能理解；
- HTML 同时显示完整地图和个人路线，零 CDN、离线可用；
- 初始 learner state 只标记 `unassessed` 或真实诊断证据，不虚构掌握。

若 `anything-tutor` 可用，用其状态工具在独立学习者工作区初始化状态；不要把私人状态写进可共享课程目录。

交付时列出所有产物和引用的 domain-map 绝对路径。
