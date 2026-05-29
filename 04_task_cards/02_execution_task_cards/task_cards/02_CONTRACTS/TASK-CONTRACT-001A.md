# TASK-CONTRACT-001A｜处理方向与错误结构 contracts

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：建立 processing_direction、error_result、flow_result 的最小 contracts 基线。  
任务状态：待执行  
任务批次：02_CONTRACTS

## 依据来源

- 60_接口边界与集成约束/02_处理方向与错误结构规则.md
- 30_标准治理/03_状态口径总表.md

## 允许修改目录

- packages/contracts/schemas/processing_direction.schema.json
- packages/contracts/schemas/error_result.schema.json
- packages/contracts/schemas/flow_result.schema.json
- packages/shared-types/

## 禁止修改目录

- 后端业务逻辑
- 前端页面
- l2_fact/
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

- 定义 accepted、need_supplement、suspended、need_confirmation、blocked、failed、not_connected、fact_created。
- 定义错误结构 code、message、reason、module、action、blocking_level、required_action、trace_id。
- 不新增业务能力。

## 验收重点

- 处理方向和错误结构可被前后端共用。
- accepted 与 fact_created 明确区分。

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


