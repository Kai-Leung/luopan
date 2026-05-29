# TASK-CONTRACT-001B｜L0/L1/S2 最小 schema

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：建立 L0 输入、L1 候选、S2 校验、待补、确认的最小接口 schema。  
任务状态：待执行  
任务批次：02_CONTRACTS

## 依据来源

- 60_接口边界与集成约束/01_接口契约与字段结构规则.md
- 50_系统业务运行规则/02_原始输入与候选生成规则.md
- 50_系统业务运行规则/03_横向治理运行规则.md

## 允许修改目录

- packages/contracts/schemas/l0_input.schema.json
- packages/contracts/schemas/l1_candidate.schema.json
- packages/contracts/schemas/s2_validation.schema.json
- packages/contracts/schemas/supplement.schema.json
- packages/contracts/schemas/confirmation.schema.json

## 禁止修改目录

- L2 facts schema 扩展
- 后端业务逻辑
- 前端页面
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

- 定义 L0 raw input 最小字段。
- 定义 L1 candidate 最小字段。
- 定义 S2 validation、supplement、confirmation 最小结构。
- 所有 schema 必须引用或兼容处理方向。

## 验收重点

- L0/L1/S2 的字段和状态边界清楚。
- 候选不被命名为正式事实。

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


