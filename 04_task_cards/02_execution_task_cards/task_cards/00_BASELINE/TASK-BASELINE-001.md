# TASK-BASELINE-001｜当前工程基线体检

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：只读检查仓库、目录、依赖、环境、Git 状态、禁止目录和控制文件是否具备 Codex 开发准入条件。  
任务状态：待执行  
任务批次：00_BASELINE

## 依据来源

- AGENTS.md
- 03_control/01_开发依据与目录映射总表.md
- 03_control/02_任务卡索引与读取规则.md
- 03_control/03_技术选型摘要.md
- 03_control/04_环境基线摘要.md

## 允许修改目录

- 只读检查整个仓库
- 05_reports/TASK-BASELINE-001_report.md

## 禁止修改目录

- 所有业务代码修改
- .env
- data/ 真实内容
- storage/ 真实内容
- 正式数据库

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

- 检查目录是否具备 ARCH_DIR_v0.1.0 结构。
- 检查 AGENTS.md、03_control、04_task_cards 是否存在。
- 检查前端、后端、contracts、tests、scripts、ops、data、storage 是否存在。
- 记录 Node、Python、依赖文件、测试入口。
- 不得修改业务代码。

## 验收重点

- 输出基线报告。
- 列清缺失目录、异常目录、可继续项和阻断项。
- 确认未修改业务代码、.env、data、storage。

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


