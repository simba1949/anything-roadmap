# domain-map.json 契约

`domain-map.json` 是公共知识地图唯一机器正本。下游只能依赖本契约，不得从 HTML 反向解析数据。

## 顶层

```json
{
  "schema_version": "1.0",
  "domain_map_id": "dm-distributed-systems",
  "version": "1.0.0",
  "generated_at": "2026-09-03",
  "domain": {
    "name": "分布式系统",
    "definition": "研究多个独立计算节点如何协同提供统一能力的领域。",
    "core_questions": ["如何在故障和并发下维持正确性？"],
    "scope": {
      "includes": ["一致性", "复制", "分区", "容错"],
      "excludes": ["单机操作系统实现细节"],
      "interfaces": ["数据库", "网络", "操作系统"]
    }
  },
  "modules": [],
  "relationships": [],
  "typical_traversal": [],
  "sources": [],
  "research_ref": {
    "research_id": "research-distributed-systems-20260903",
    "path": "../distributed-systems-research-20260903/research.md"
  }
}
```

必填：`schema_version`、`domain_map_id`、`version`、`generated_at`、`domain`、`modules`、`relationships`、`typical_traversal`、`sources`。ID 使用稳定、小写 ASCII slug；版本使用语义版本。

## 递归节点

模块是顶层节点；后代可以跳过主题或章节，但必须按顺序向下，最终到知识点。

```json
{
  "id": "m-foundations",
  "type": "module",
  "title": "理论基础",
  "summary": "建立讨论正确性与故障所需的共同语言。",
  "why": "后续所有工程权衡都依赖这些定义。",
  "stage": "foundation",
  "children": [
    {
      "id": "t-models",
      "type": "topic",
      "title": "系统模型",
      "summary": "描述节点、通信与故障假设。",
      "children": [
        {
          "id": "kp-failure-model",
          "type": "knowledge_point",
          "title": "故障模型",
          "definition": "对系统中允许发生的故障类型作出的明确假设。",
          "importance": "算法正确性只在声明的故障模型下成立。",
          "problems": ["区分崩溃故障与拜占庭故障"],
          "prerequisites": [],
          "leads_to": ["kp-consensus"],
          "applications": ["共识协议选型"],
          "difficulty": "foundation",
          "source_ids": ["src-01"]
        },
        {
          "id": "kp-time-model",
          "type": "knowledge_point",
          "title": "时间模型",
          "definition": "系统对消息延迟和处理时间所作的假设。",
          "importance": "它决定哪些失败检测与一致性保证可能实现。",
          "problems": ["理解同步、异步与部分同步模型"],
          "prerequisites": [],
          "leads_to": ["kp-consensus"],
          "applications": ["超时与故障检测"],
          "difficulty": "foundation",
          "source_ids": ["src-01"]
        }
      ]
    }
  ]
}
```

规则：

- `type` 只能是 `module`、`topic`、`chapter`、`knowledge_point`。
- 中间节点使用 `children`，知识点不得包含非空 `children`。
- `topic` 与 `chapter` 一旦出现，必须至少有两个子节点。
- 同一知识可通过关系引用，不复制为第二个知识点。
- `stage` 建议值：`foundation`、`core`、`branch`、`application`、`frontier`。
- `difficulty` 建议值：`foundation`、`intermediate`、`advanced`、`frontier`。

## 跨节点关系

```json
{
  "from": "kp-failure-model",
  "to": "kp-consensus",
  "type": "prerequisite",
  "note": "共识的可解性与保证取决于故障假设。"
}
```

`type` 可用：`prerequisite`、`supports`、`contrasts`、`interfaces`、`applies_to`。端点必须是已存在节点 ID。

## 典型遍历

`typical_traversal` 是节点 ID 数组，通常列模块或关键知识点。它表达公共地图中的一种常见浏览顺序，不代表个人学习路径。

## 来源

```json
{
  "id": "src-01",
  "title": "Designing Data-Intensive Applications",
  "url": "https://dataintensive.net/",
  "publisher": "Martin Kleppmann",
  "tier": "authoritative-book",
  "language": "en",
  "verified_at": "2026-09-03",
  "supports": ["m-foundations", "kp-failure-model"],
  "note": "用于系统模型与复制结构。"
}
```

每个 URL 必须实际打开验证。`supports` 只能引用存在的节点。

## 版本规则

- PATCH：文案、来源替换，不改变节点语义与依赖。
- MINOR：新增节点或关系，旧 ID 仍有效。
- MAJOR：节点语义、边界或依赖发生破坏性变化。

