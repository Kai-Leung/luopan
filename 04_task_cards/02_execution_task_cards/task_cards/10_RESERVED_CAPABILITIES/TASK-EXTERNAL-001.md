# TASK-EXTERNAL-001｜外部协同输入边界

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：建立外部协同输入边界，使外部提交先进入 L0/L1/S2。  
任务状态：待执行  
任务批次：10_RESERVED_CAPABILITIES

## 依据来源

- 50_系统业务运行规则/07_AI辅助与外部协同运行规则.md
- 60_接口边界与集成约束/05_外部系统接入与回执规则.md

## 允许修改目录

- services/api/app/modules/external_collaboration/
- services/api/app/modules/l0_input/
- services/api/app/modules/l1_candidate/
- services/api/app/modules/s2_validation/
- apps/h5/src/modules/external_collaboration/
- packages/contracts/schemas/

## 禁止修改目录

- L2 直写
- 新增 webhook 顶级服务
- 完整客户门户
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

- 外部输入记录来源。
- 转入 L0/L1/S2。
- 不做完整门户。

## 验收重点

- 外部输入不直写 L2。
- 来源可记录。

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


