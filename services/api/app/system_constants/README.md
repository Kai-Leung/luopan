# services/api/app/system_constants

## 目录职责

本目录只允许存放系统级、非业务、跨模块通用的常量。

## 允许放入

- `DEFAULT_PAGE_SIZE`
- `TIME_FORMAT`
- `MAX_UPLOAD_SIZE`
- `SYSTEM_NAME`
- 请求超时配置
- 编码格式
- 与业务语义无关的系统运行常量

## 禁止放入

- 业务枚举
- 事实类型
- 字段规则
- 风险等级
- 业务关键词
- 治理规则
- 反问规则
- `standard_governance` 中已经归口的任何规则

## 归位原则

如果一个常量会影响 L0-L7 主链路业务判断、S2 治理、字段缺失、事实类型分类或人工确认边界，它不属于本目录，应归入对应业务模块或 `standard_governance`。
