# learning-path.json 契约

`learning-path.json` 是个人路线和课程编排的机器正本。它引用公共地图，不复制公共知识结构。

## 顶层示例

```json
{
  "schema_version": "1.0",
  "roadmap_id": "rm-build-reliable-api",
  "version": "1.0.0",
  "generated_at": "2026-09-03",
  "domain_map_ref": {
    "domain_map_id": "dm-distributed-systems",
    "version": "1.0.0",
    "path": "../distributed-systems-domain-map-1.0.0/domain-map.json"
  },
  "learner": {
    "learner_id": "learner-local",
    "background": "有后端开发经验，没有系统学习分布式理论"
  },
  "learning_contract": {
    "goal_context": "负责一个需要跨地域部署的 API",
    "graduation_task": "为陌生业务设计可解释的容错方案并为权衡辩护",
    "constraints": ["每周 5 小时", "中文讲解，英文资料可接受"],
    "completion_evidence": ["无提示解释方案", "完成陌生情境综合任务"]
  },
  "capabilities": [],
  "recommended_sequence": [],
  "projects": [],
  "sources": []
}
```

## 能力节点

```json
{
  "id": "cap-reason-about-failures",
  "title": "按故障模型分析方案",
  "statement": "面对一个陌生服务场景，能声明故障假设并判断方案保证是否成立。",
  "role": "core",
  "selection_reason": "毕业任务中的所有容错判断都依赖明确故障假设。",
  "knowledge_links": [
    {"knowledge_point_id": "kp-failure-model", "role": "judgment_basis"}
  ],
  "prerequisite_capability_ids": [],
  "strategy": "judgment",
  "verification": "rubric",
  "lesson_file": "content/cap-reason-about-failures.md",
  "mastery_requirement": {
    "minimum_level_to_advance": "near_transfer",
    "unassisted_required": true,
    "evidence_count": 2
  },
  "diagnostic": {
    "task_id": "diag-cap-reason-about-failures",
    "branching_value": "区分术语缺失与模型误解"
  },
  "assessment": {
    "seed_task_ids": ["task-failure-01"],
    "rubric_id": "rubric-failure-model"
  },
  "remediation": {
    "likely_errors": ["confuses-failure-with-slow-response"],
    "branch_capability_ids": []
  }
}
```

`role` 只能是 `core`、`support`、`branch`、`deferred`。

`strategy` 建议值：`memory`、`mental_model`、`procedure`、`quantitative`、`judgment`、`design`。

`verification` 建议值：`exact`、`executable`、`rubric`、`external_result`、`reflection`。主观评价必须携带量规和置信度，不得伪装成精确判分。

`knowledge_links[].role` 建议值：`conceptual_basis`、`procedure`、`judgment_basis`、`constraint`、`extension`。

## 项目

```json
{
  "id": "project-graduation",
  "type": "graduation",
  "title": "陌生业务容错设计",
  "capability_ids": ["cap-reason-about-failures"],
  "novelty_constraints": ["不得复用课程案例", "更换故障与成本约束"],
  "hint_policy": "limited",
  "rubric_id": "rubric-graduation"
}
```

贯穿项目可用 `type: integrative`；最终必须至少一个 `type: graduation` 项目，并改变情境、约束或冲突条件来检验迁移。

## 推荐顺序

`recommended_sequence` 是 capability ID 数组。所有前置能力必须排在依赖它的能力之前；deferred 节点通常不进入默认顺序。

## 初始证据

roadmap 阶段只允许记录真实发生的诊断结果：

```json
{
  "capability_id": "cap-reason-about-failures",
  "level": "recognition",
  "source": "entry_diagnostic",
  "confidence": "low",
  "needs_recheck": true
}
```

没有诊断证据时不填 `initial_evidence`，由 tutor 初始化为 `unassessed`。

