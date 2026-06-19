# apps/h5/src/types

本目录只放跨页面、跨模块共享的前端通用类型。

## 允许放入

- 多个页面共同消费的 UI 类型。
- 多个模块共同消费且不属于某个业务模块的通用类型。
- 兼容旧 UI 展示所需的轻量类型出口。

## 禁止放入

- 模块私有类型。
- 字段规则。
- 枚举标准。
- 状态口径。
- 反问规则。
- S2 决策或治理规则。

## 归位原则

模块私有类型必须留在对应模块内，例如：

- `apps/h5/src/modules/input_flow/types.ts`
- `apps/h5/src/modules/standard_governance/*`
- `apps/h5/src/modules/facts_view/*`

不得把所有类型集中搬入本目录。全局标准治理规则统一归口到 `apps/h5/src/modules/standard_governance/`，业务模块只消费规则，不重复定义。
