# TASK-L2L3-001A｜L2 正式事实入链

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：实现或占位 L2 正式事实入链，只允许通过 S2 且满足确认条件的数据进入。  
任务状态：待执行  
任务批次：07_L2L3

## 依据来源

- 50_系统业务运行规则/05_正式事实入链与查询运行规则.md
- 40_业务数据体系/02_事实记录/

## 允许修改目录

- services/api/app/modules/l2_fact/
- packages/contracts/schemas/l2_fact.schema.json

## 禁止修改目录

- AI 直写 L2
- external_collaboration 直写 L2
- H5 直写 L2
- .env
- data/
- storage/

## 全局禁止项

- 禁止修改 `.env`、密钥、真实数据库、Raw Store、storage 真实内容。
- 禁止清空 `data/`、`storage/`、日志、trace、审计记录。
- 禁止绕过 S2 直接写 L2。
- 禁止让前端、AI、上传资料、外部协同直接生成正式事实。
- 禁止将 L3 查询、L4 分析、L5 建议、L6 执行、L7 反馈反写为正式事实。
- 禁止新增未被开发依据和任务卡支撑的模块。
- 禁止自行引入新框架、新语言、新运行时。
- 未经用户明确授权，禁止执行 `git add / commit / push`。
- 禁止把页面可点、HTTP 200、构建通过、无报错等同于验收通过。


## 执行要求

- 定义 create_fact 的前置条件。
- 要求 validation result 和 source。
- 事实必须有来源链。

## 验收重点

- 未通过 S2 的候选不能入 L2。
- L2 facts 有来源字段。

## 回传要求

执行完成后必须回传：

- 任务编号
- 执行状态
- 实际读取的依据
- 实际修改文件清单
- 新增文件清单
- 删除文件清单
- 涉及 contracts
- 涉及数据模型
- 执行的测试命令
- 测试结果
- 未执行测试及原因
- 是否修改 `.env`
- 是否修改 `data/`
- 是否修改 `storage/`
- 是否执行 `git add / commit / push`
- 风险和阻断项


