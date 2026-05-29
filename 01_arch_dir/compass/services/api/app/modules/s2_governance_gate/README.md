# s2_governance_gate

## 模块职责
对 L1 候选执行最小横向治理校验。

## 所属层级
S2 横向治理校验层。

## 允许做什么
允许输出 `auto_pass`、`needs_completion`、`needs_confirmation`、`blocked` 以及待补字段和风险提示。

## 禁止越过什么
不得替代人工确认、不得写入 L2、不得生成正式事实。

## 上下游关系
上游为 `l1_candidate`；下游为 `s2_governance_gate/confirmation`。


## 人工确认归口

人工确认属于 S2 治理闸门子能力，代码落位于 `s2_governance_gate/confirmation/`，不得作为独立业务能力绕过 S2 或直接写入 L2。
