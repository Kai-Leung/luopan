# l2_fact

## 模块职责
将满足前置链路条件的人工确认候选写入正式事实表。

## 所属层级
L2 正式事实入链层。

## 允许做什么
允许在 `raw_input_id`、`candidate_id`、`governance_id`、`review_id` 齐备且 `review_status=confirmed_candidate` 时写入 `fact_records`。

## 禁止越过什么
不得跳过 L0、L1、S2 或人工确认；不得让 `blocked`、退回或拒绝结果入链；不得生成 L3 视图。

## 上下游关系
上游为 `s2_governance_gate/confirmation`；下游为 `l3_query_view`。

## 正式事实口径
`fact_records` 是当前主链路中的正式事实表。
