# 学习者状态契约

私人状态位于共享学习项目根目录的 `anything-tutor/` 子目录。它与其他三层同属一个项目树，但权限和导出边界独立：

```text
<project-slug>-learning/
└─ anything-tutor/
   ├─ learner-state.json
   ├─ evidence.jsonl
   └─ progress.md
```

## learner-state.json

```json
{
  "schema_version": "1.0",
  "learner_id": "learner-local",
  "roadmap_ref": {
    "roadmap_id": "rm-build-reliable-api",
    "version": "1.0.0",
    "path": "/absolute/path/to/learning-path.json"
  },
  "domain_map_ref": {
    "domain_map_id": "dm-distributed-systems",
    "version": "1.0.0",
    "path": "/absolute/path/to/domain-map.json"
  },
  "created_at": "2026-09-03T10:00:00+08:00",
  "updated_at": "2026-09-03T10:00:00+08:00",
  "session": {
    "phase": "orient",
    "current_capability_id": null,
    "teaching_mode": "attempt_first"
  },
  "capability_states": {
    "cap-example": {
      "level": "unassessed",
      "confidence": "low",
      "last_evidence_at": null,
      "evidence_refs": [],
      "last_error_type": null,
      "last_hint_level": "none",
      "next_review_at": null
    }
  },
  "route_overrides": [],
  "review_queue": [],
  "last_session_summary": null
}
```

合法 phase：`orient`、`review`、`diagnose`、`attempt`、`instruct`、`practice`、`assess`、`remediate`、`close`。

合法 level：`unassessed`、`recognition`、`recall`、`near_transfer`、`far_transfer`、`retained`。

合法 confidence：`low`、`medium`、`high`。

路线偏移只记录运行时变化，不重写 `learning-path.json`：

```json
{
  "id": "override-20260903-01",
  "type": "insert_remediation",
  "capability_id": "cap-prerequisite",
  "reason": "连续两次出现同一前置概念误解",
  "created_at": "2026-09-03T11:00:00+08:00",
  "status": "active"
}
```

## evidence.jsonl

每行是独立 JSON 对象：

```json
{"event_id":"ev-20260903-001","timestamp":"2026-09-03T11:20:00+08:00","capability_id":"cap-example","task_id":"task-example-02","evidence_type":"near_transfer","result":"pass","resulting_level":"near_transfer","hint_level":"none","error_type":null,"confidence":"high","summary":"在新情境中声明条件并正确解释选择。","next_review_at":"2026-09-06T11:20:00+08:00","artifact_ref":null}
```

必填：`event_id`、`timestamp`、`capability_id`、`task_id`、`evidence_type`、`result`、`resulting_level`、`hint_level`、`confidence`、`summary`。

`result`：`pass`、`partial`、`fail`、`ungradable`。

`hint_level`：`none`、`restate`、`focus`、`principle`、`partial_step`、`full_demo`。

`error_type`：`knowledge_gap`、`misconception`、`procedure_failure`、`condition_omission`、`transfer_failure`、`ambiguous_task`、`unreliable_grading` 或 `null`。

`summary` 只概括可观察表现，不复制完整回答。长作品用 `artifact_ref` 保存用户选择保留的本地路径。

## progress.md

由状态工具生成，面向学习者展示：

- 当前地图位置与能力；
- 各证据等级数量；
- 到期与即将到期复习；
- 最近证据摘要；
- 活跃路线偏移及原因；
- 下一步选择。

它是只读视图，不是机器正本。
