# anything 系统化教学管线

[English](./README.en.md) | 中文

本项目以人为本，利用 AI 提升人的能力。它把可信研究、领域全貌、个人路线和实际教学拆成四个可独立使用、契约相连的 agent skill：

```text
/anything-research <问题>             证据、来源、争议、边界
        ↓
/anything-domain-map <领域>           面向所有人的全链路知识地图
        ↓
/anything-roadmap <学习目标>          透明的个人能力路径和自学课程
        ↓
/anything-tutor <开始|继续|复习|状态>  教学、评估、补救、迁移和复习
```

## 安装

```bash
npx skills add simba1949/anything-roadmap --global --all --agent codex
```

更新本仓库的四个 skill（不会更新其他 skill）：

```bash
npx skills update anything-research anything-domain-map anything-roadmap anything-tutor --global --yes
```

卸载本仓库的四个 skill：

```bash
npx skills remove anything-research anything-domain-map anything-roadmap anything-tutor --global --yes --agent codex
```

以上命令只针对本仓库的四个 skill，不使用通配符，也不会影响其他 skill。

## 四层分别解决什么

### anything-research

做多轮深度调研。后轮由前轮全文阅读产生的新线索驱动；关键论断交叉验证；冲突证据不抹平；正式 URL 逐条打开验证。新增“领域制图模式”，为公共知识地图提供边界、结构、依赖、应用和前沿证据。

### anything-domain-map

生成不依赖具体学习者的公共领域地图：

```text
模块 →〔主题〕→〔章节〕→ 知识点
```

模块和知识点必有，主题/章节按知识内聚动态省略。输出：

```text
domain-map.json       机器正本
domain-map.md         可审阅全链路大纲
domain-map.html       离线知识观测台
validation.md         来源、覆盖和结构质检
```

### anything-roadmap

先展示公共地图，再结合毕业任务、基础与约束反推个人能力：

```text
毕业任务 → 成功条件 → 子任务 → 可验证能力 → 所需知识点 → 前置能力
```

能力分为核心路径、必要支撑、按需分支和明确延后。昂贵生成前只确认一次学习契约；确认后生成模块化课程、`self-study.md` 和完整地图叠加个人路径的 `roadmap.html`。

### anything-tutor

执行课程并维护私人学习状态。支持“先小试再教学”和“先系统教学再尝试”。掌握按证据推进：

```text
未诊断 → 识别 → 复述 → 近迁移 → 远迁移 → 延迟保持
```

反馈区分知识缺口、心智模型、程序执行、条件遗漏、迁移失败以及题目/评分问题。提示越强，证据越弱；课程错误不能记成学习者错误。

## 数据与隐私

一次学习项目只使用一个顶层目录，四个 skill 按子目录区分产物：

```text
<project-slug>-learning/
├─ anything-research/      调研卷宗与报告
├─ anything-domain-map/    公共知识地图
├─ anything-roadmap/       个人路线与课程包
└─ anything-tutor/         私人学习状态
```

公共地图和个人路线仍是两份正本，由 `anything-roadmap/roadmap.html` 合成展示。`anything-tutor/` 与其他产物位于同一项目树，但保持独立隐私边界：顶层目录默认按私人数据处理，公开导出时不要包含该子目录。默认只保留结构化证据摘要，不保存完整对话。

## 确定性工具

每层包含可重复执行的验证或渲染脚本：

```bash
python skills/anything-domain-map/scripts/validate_domain_map.py <项目根目录>/anything-domain-map/domain-map.json
python skills/anything-domain-map/scripts/render_domain_map.py <项目根目录>/anything-domain-map/domain-map.json <项目根目录>/anything-domain-map/domain-map.html

python skills/anything-roadmap/scripts/validate_learning_path.py <项目根目录>/anything-roadmap/learning-path.json <项目根目录>/anything-domain-map/domain-map.json
python skills/anything-roadmap/scripts/render_roadmap.py <项目根目录>/anything-domain-map/domain-map.json <项目根目录>/anything-roadmap/learning-path.json <项目根目录>/anything-roadmap/roadmap.html

python skills/anything-tutor/scripts/state_tool.py init <项目根目录>/anything-roadmap/learning-path.json <项目根目录>/anything-tutor
python skills/anything-tutor/scripts/state_tool.py validate <项目根目录>/anything-tutor
```

完整设计理由、文件契约、验收和迁移记录见 [CONSENSUS.md](./CONSENSUS.md)。

## License

MIT
