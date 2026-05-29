# TASK-VERIFY-001｜构建、禁止项、回传检查

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：建立构建、禁止目录、技术选型、回传材料检查能力。  
任务状态：待执行  
任务批次：12_VERIFY

## 依据来源

- 80_验证与验收规则/04_构建与环境验证规则.md
- 80_验证与验收规则/05_回传材料与验收报告规则.md

## 允许修改目录

- scripts/check/
- scripts/build/
- scripts/test/
- docs/acceptance/
- 05_reports/

## 禁止修改目录

- 业务代码自由修复
- .env
- data/
- storage/
- 自动 git add/commit/push

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

- 检查 .env、data、storage、node_modules、dist/build 是否误入 Git。
- 整理构建和测试命令。
- 输出回传模板。

## 验收重点

- 检查脚本或清单存在。
- 回传模板完整。

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


