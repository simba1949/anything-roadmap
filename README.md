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
npx skills add simba1949/anything-roadmap
```

仓库包含四个 skill；上面的命令会发现它们并进入选择流程。安装全部四个 skill 到 Codex：

```bash
npx skills add simba1949/anything-roadmap --agent codex --global --all
```

只安装个人路线 skill 到 Codex：

```bash
npx skills add simba1949/anything-roadmap --skill anything-roadmap --agent codex --global --yes
```

安装本地检出的仓库（用于开发或验证）：

```bash
npx skills add . --skill anything-roadmap --agent codex --global --copy --yes
```

`--global` 写入用户级 skill 目录；省略它则安装到当前项目。手动安装时，将 `skills/` 下需要的目录复制到 agent 的 skill 目录。

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

公共地图和个人路线是两份正本，在一个界面中呈现：

```text
domain-map.json + learning-path.json → roadmap.html
```

私人学习状态保存在独立工作区：

```text
learner-state.json
evidence.jsonl
progress.md
```

默认只保留结构化证据摘要，不保存完整对话。

## 确定性工具

每层包含可重复执行的验证或渲染脚本：

```bash
python skills/anything-domain-map/scripts/validate_domain_map.py domain-map.json
python skills/anything-domain-map/scripts/render_domain_map.py domain-map.json domain-map.html

python skills/anything-roadmap/scripts/validate_learning_path.py learning-path.json domain-map.json
python skills/anything-roadmap/scripts/render_roadmap.py domain-map.json learning-path.json roadmap.html

python skills/anything-tutor/scripts/state_tool.py init learning-path.json learner-workspace
python skills/anything-tutor/scripts/state_tool.py validate learner-workspace
```

完整设计理由、文件契约、验收和迁移记录见 [CONSENSUS.md](./CONSENSUS.md)。

## License

MIT
