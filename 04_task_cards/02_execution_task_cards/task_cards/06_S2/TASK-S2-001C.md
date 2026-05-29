# TASK-S2-001C｜确认 confirmation

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：建立确认动作的最小机制，记录确认人、确认时间和确认结果。  
任务状态：待执行  
任务批次：06_S2

## 依据来源

- 50_系统业务运行规则/03_横向治理运行规则.md
- 30_标准治理/04_追溯与操作日志总表.md

## 允许修改目录

- services/api/app/modules/confirmation/
- services/api/app/modules/s2_validation/
- apps/h5/src/modules/confirmation/
- packages/contracts/schemas/confirmation.schema.json

## 禁止修改目录

- 前端伪造确认
- 无权限确认
- l2_fact/ 直接写入
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

- 定义确认请求和确认结果。
- 保留确认人/时间/动作来源。
- 确认结果仍需后端判断能否入 L2。

## 验收重点

- need_confirmation 可被表达和展示。
- 确认留痕可追溯。

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


