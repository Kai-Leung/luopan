# input_flow

现有 H5 主交互的兼容实现目录。

本次落位保留该目录，避免破坏已完成页面。后续新开发应优先使用标准适配目录：

- `l0_input/`
- `l1_candidate/`
- `s2_governance_gate/`
- `confirmation/`
- `l2_fact/`
- `l3_query_view/`

边界：`input_flow` 只作为前端交互编排和接口调用兼容层，不承担事实裁决；L2 入链必须由后端复核 S2、确认记录和来源链。
