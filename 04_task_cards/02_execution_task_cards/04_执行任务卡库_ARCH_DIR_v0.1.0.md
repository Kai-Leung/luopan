# 04_执行任务卡库_ARCH_DIR_v0.1.0

文件名：04_执行任务卡库_ARCH_DIR_v0.1.0.md  
文件类型：Codex 执行任务卡库  
任务卡库版本：EXEC-TASK-v0.1.4  
目录架构版本：ARCH_DIR_v0.1.0  
用途：把一级任务卡拆分为适合 Codex 云任务逐张执行的执行卡。  

---

## 1. 使用原则

- 本库用于 Codex 云任务逐张执行，不用于一次性全量执行。
- 每张执行卡控制在 1 个明确目标、1-3 个主要目录、1 个可验证结果。
- 执行前必须读取 `AGENTS.md`、`03_control/01_开发依据与目录映射总表.md`、`03_control/02_任务卡索引与读取规则.md`。
- 如需修改任务卡外目录，必须停止并回传 `NEEDS_USER_DECISION`。

## 2. 执行顺序索引

| 顺序 | 批次 | 任务编号 | 任务名称 | 状态 |
|---:|---|---|---|---|
| 1 | `00_BASELINE` | `TASK-BASELINE-001` | 当前工程基线体检 | 待执行 |
| 2 | `01_DIR` | `TASK-DIR-001A` | 目录骨架缺口补齐 | 待执行 |
| 3 | `01_DIR` | `TASK-DIR-001B` | 现有代码到目标目录迁移建议 | 待执行 |
| 4 | `02_CONTRACTS` | `TASK-CONTRACT-001A` | 处理方向与错误结构 contracts | 待执行 |
| 5 | `02_CONTRACTS` | `TASK-CONTRACT-001B` | L0/L1/S2 最小 schema | 待执行 |
| 6 | `02_CONTRACTS` | `TASK-CONTRACT-001C` | L2/L3 最小 schema | 待执行 |
| 7 | `03_DATA` | `TASK-DATA-001A` | 数据模型映射文档 | 待执行 |
| 8 | `03_DATA` | `TASK-DATA-001B` | 对象资产最小 models | 待执行 |
| 9 | `03_DATA` | `TASK-DATA-001C` | L0/L1/S2/L2 最小 models | 待执行 |
| 10 | `04_S1` | `TASK-S1-001A` | 后端运行上下文接口 | 待执行 |
| 11 | `04_S1` | `TASK-S1-001B` | H5 运行上下文展示 | 待执行 |
| 12 | `05_L0L1` | `TASK-L0L1-001A` | 后端 L0 原始输入 | 待执行 |
| 13 | `05_L0L1` | `TASK-L0L1-001B` | 后端 L1 候选生成 | 待执行 |
| 14 | `05_L0L1` | `TASK-L0L1-001C` | H5 输入与候选展示 | 待执行 |
| 15 | `06_S2` | `TASK-S2-001A` | S2 校验与处理方向 | 待执行 |
| 16 | `06_S2` | `TASK-S2-001B` | 待补 supplement | 待执行 |
| 17 | `06_S2` | `TASK-S2-001C` | 确认 confirmation | 待执行 |
| 18 | `06_S2` | `TASK-S2-001D` | H5 S2 状态展示 | 待执行 |
| 19 | `07_L2L3` | `TASK-L2L3-001A` | L2 正式事实入链 | 待执行 |
| 20 | `07_L2L3` | `TASK-L2L3-001B` | L3 查询视图 | 待执行 |
| 21 | `07_L2L3` | `TASK-L2L3-001C` | H5 正式事实与查询展示 | 待执行 |
| 22 | `08_TRACE` | `TASK-TRACE-001` | 最小来源追溯 | 待执行 |
| 23 | `09_H5` | `TASK-H5-001A` | H5 首页输入与分流 | 待执行 |
| 24 | `09_H5` | `TASK-H5-001B` | H5 候选/S2/待补/确认状态 | 待执行 |
| 25 | `09_H5` | `TASK-H5-001C` | H5 正式事实/查询/来源摘要 | 待执行 |
| 26 | `10_RESERVED_CAPABILITIES` | `TASK-UPLOAD-001` | 上传资料进入候选链路 | 待执行 |
| 27 | `10_RESERVED_CAPABILITIES` | `TASK-EXTERNAL-001` | 外部协同输入边界 | 待执行 |
| 28 | `10_RESERVED_CAPABILITIES` | `TASK-AI-001` | AI 辅助预处理边界 | 待执行 |
| 29 | `11_TEST` | `TASK-TEST-001A` | 后端单元与接口测试 | 待执行 |
| 30 | `11_TEST` | `TASK-TEST-001B` | 前端状态展示测试 | 待执行 |
| 31 | `11_TEST` | `TASK-TEST-001C` | 边界负向验收测试 | 待执行 |
| 32 | `12_VERIFY` | `TASK-VERIFY-001` | 构建、禁止项、回传检查 | 待执行 |
| 33 | `13_DEPLOY_RESERVED` | `TASK-DEPLOY-PREP-001` | 部署前准备占位 | 后置 |

---

## 3. 执行卡正文


---

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



---

# TASK-DIR-001A｜目录骨架缺口补齐

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：按 ARCH_DIR_v0.1.0 补齐缺失目录和占位文件，不迁移现有代码，不写业务逻辑。  
任务状态：待执行  
任务批次：01_DIR

## 依据来源

- 01_arch_dir/Compass_目录树说明_ARCH_DIR_v0.1.0.md
- 03_control/01_开发依据与目录映射总表.md

## 允许修改目录

- apps/
- services/
- packages/
- docs/
- tests/
- scripts/
- ops/
- data/.gitkeep
- storage/.gitkeep
- README.md
- AGENTS.md
- .gitignore
- .env.example

## 禁止修改目录

- 业务逻辑文件大规模改写
- 真实数据
- 真实上传文件
- .env
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

- 根据目录说明补齐缺失目录。
- 只创建 README、.gitkeep、占位文件。
- 不得删除或迁移现有代码。
- 如发现迁移需求，写入报告，不直接迁移。

## 验收重点

- 目录结构具备开发落位点。
- 新增文件均为占位或说明。
- 未修改业务逻辑。

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



---

# TASK-DIR-001B｜现有代码到目标目录迁移建议

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：只读分析现有代码与 ARCH_DIR_v0.1.0 的差异，输出迁移建议，不实际迁移代码。  
任务状态：待执行  
任务批次：01_DIR

## 依据来源

- 03_control/01_开发依据与目录映射总表.md
- 01_arch_dir/Compass_目录树说明_ARCH_DIR_v0.1.0.md

## 允许修改目录

- 05_reports/TASK-DIR-001B_report.md
- docs/development/current_to_target_path_map.md

## 禁止修改目录

- 实际移动代码
- 删除文件
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

- 扫描现有代码目录。
- 对照目标目录输出 current_to_target_path_map。
- 标记保留、迁移、废弃、需用户裁决。

## 验收重点

- 输出当前目录到目标目录映射。
- 未实际移动代码。
- 迁移风险清楚。

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



---

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



---

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



---

# TASK-CONTRACT-001C｜L2/L3 最小 schema

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：建立 L2 正式事实和 L3 查询视图的最小 contracts 基线。  
任务状态：待执行  
任务批次：02_CONTRACTS

## 依据来源

- 40_业务数据体系/02_事实记录/
- 40_业务数据体系/03_汇总视图/
- 50_系统业务运行规则/05_正式事实入链与查询运行规则.md

## 允许修改目录

- packages/contracts/schemas/l2_fact.schema.json
- packages/contracts/schemas/l3_query_view.schema.json

## 禁止修改目录

- AI schema 直写 L2
- 外部协同直写 L2
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

- 定义 fact_id、fact_type、source、created_by、created_at、status 等最小字段。
- 定义 query view 的只读响应结构。
- 明确 L3 不反写。

## 验收重点

- L2 包含来源字段。
- L3 schema 为只读查询视图。

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



---

# TASK-DATA-001A｜数据模型映射文档

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：建立数据模型映射文档，说明对象资产、L0、L1、S2、L2、L3、pools 与表/模型的关系。  
任务状态：待执行  
任务批次：03_DATA

## 依据来源

- 40_业务数据体系/
- 03_control/01_开发依据与目录映射总表.md

## 允许修改目录

- docs/architecture/data_model_map.md

## 禁止修改目录

- 写业务代码
- 创建数据库文件
- data/
- storage/
- .env

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

- 按四层业务数据体系列出数据模型归口。
- 列明最小表/模型建议。
- 标明哪些暂不建表。

## 验收重点

- 文档能指导后续 models 落位。
- 没有新增第五层数据体系。

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



---

# TASK-DATA-001B｜对象资产最小 models

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：在 assets 模块建立组织、项目、主体、资料等最小对象资产模型或模型占位。  
任务状态：待执行  
任务批次：03_DATA

## 依据来源

- 40_业务数据体系/01_对象资产/
- 30_标准治理/01_字段规范总表.md

## 允许修改目录

- services/api/app/modules/assets/
- packages/contracts/schemas/

## 禁止修改目录

- 正式数据库操作
- data/ 真实数据库
- storage/ 真实文件
- L2 facts 写入

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

- 按模块归口建立 models/schemas/repository 占位或实现。
- 不得把临时线索直接变正式资产。
- 保留别名/映射扩展位置但不做复杂治理。

## 验收重点

- 资产模型归口清楚。
- 不绕过确认直接形成正式资产。

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



---

# TASK-DATA-001C｜L0/L1/S2/L2 最小 models

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：为 L0 原始输入、L1 候选、S2 校验结果、L2 正式事实建立最小模型。  
任务状态：待执行  
任务批次：03_DATA

## 依据来源

- 40_业务数据体系/02_事实记录/
- 50_系统业务运行规则/02_原始输入与候选生成规则.md
- 50_系统业务运行规则/03_横向治理运行规则.md
- 50_系统业务运行规则/05_正式事实入链与查询运行规则.md

## 允许修改目录

- services/api/app/modules/l0_input/
- services/api/app/modules/l1_candidate/
- services/api/app/modules/s2_validation/
- services/api/app/modules/l2_fact/

## 禁止修改目录

- data/ 真实数据库
- 正式数据库操作
- L3/L4/L5 反写 facts
- .env

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

- 建立 raw_inputs、candidates、validation_results、facts、fact_sources 的模型或占位。
- 父子依赖清楚。
- facts 必须有来源。

## 验收重点

- 模型层级符合 L0/L1/S2/L2。
- 无绕过 S2 的 facts 写入路径。

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



---

# TASK-S1-001A｜后端运行上下文接口

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：建立 pre_run_context 后端最小接口，返回身份、组织、角色、项目范围、权限动作结果。  
任务状态：待执行  
任务批次：04_S1

## 依据来源

- 50_系统业务运行规则/01_身份识别与访问范围规则.md
- 60_接口边界与集成约束/03_权限与访问范围接口规则.md

## 允许修改目录

- services/api/app/modules/pre_run_context/
- packages/contracts/schemas/pre_run_context.schema.json

## 禁止修改目录

- l2_fact/
- apps/pc/
- apps/mobile-shell/
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

- 实现或占位 current_context 接口。
- 返回 allowed_actions 和 denied_reason。
- 不得做完整多租户后台。

## 验收重点

- 接口能表达身份/组织/角色/项目范围。
- 权限失败有原因。

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



---

# TASK-S1-001B｜H5 运行上下文展示

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：在 H5 展示当前身份、组织、项目范围和权限状态，不做最终权限裁决。  
任务状态：待执行  
任务批次：04_S1

## 依据来源

- 70_前后端协同边界与页面承接/05_权限与脱敏页面承接规则.md
- 60_接口边界与集成约束/03_权限与访问范围接口规则.md

## 允许修改目录

- apps/h5/src/modules/pre_run_context/
- apps/h5/src/shared/api/

## 禁止修改目录

- 后端业务规则
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

- 调用或对接 pre_run_context API。
- 展示权限状态、范围、阻断原因。
- 不在前端计算最终权限。

## 验收重点

- H5 能展示上下文。
- 前端没有伪造 allowed_actions。

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



---

# TASK-L0L1-001A｜后端 L0 原始输入

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：建立 L0 原始输入的后端最小接口和服务逻辑。  
任务状态：待执行  
任务批次：05_L0L1

## 依据来源

- 50_系统业务运行规则/02_原始输入与候选生成规则.md
- 20_系统架构/01_L0-L7_架构总览.md

## 允许修改目录

- services/api/app/modules/l0_input/
- packages/contracts/schemas/l0_input.schema.json

## 禁止修改目录

- l2_fact/
- l3_query_view/
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

- 接收 raw input。
- 记录来源、输入类型、创建者、上下文快照。
- 不得生成正式事实。

## 验收重点

- L0 可保存或模拟保存输入。
- L0 不写 L2。

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



---

# TASK-L0L1-001B｜后端 L1 候选生成

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：基于 L0 输入生成 L1 候选内容和候选状态。  
任务状态：待执行  
任务批次：05_L0L1

## 依据来源

- 50_系统业务运行规则/02_原始输入与候选生成规则.md
- 40_业务数据体系/02_事实记录/

## 允许修改目录

- services/api/app/modules/l1_candidate/
- services/api/app/modules/l0_input/
- packages/contracts/schemas/l1_candidate.schema.json

## 禁止修改目录

- l2_fact/
- 正式事实写入
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

- 读取 L0 输入。
- 生成 candidate payload。
- 标明 candidate_status 和来源。
- 不进行正式入链。

## 验收重点

- L1 候选能生成。
- 候选与正式事实边界清楚。

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



---

# TASK-L0L1-001C｜H5 输入与候选展示

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：实现 H5 输入提交和候选展示的最小页面承接。  
任务状态：待执行  
任务批次：05_L0L1

## 依据来源

- 70_前后端协同边界与页面承接/01_H5主交互页面承接规则.md
- 60_接口边界与集成约束/04_前后端联调接口规则.md

## 允许修改目录

- apps/h5/src/modules/l0_input/
- apps/h5/src/modules/l1_candidate/
- apps/h5/src/shared/api/

## 禁止修改目录

- 后端业务逻辑
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

- 输入框提交到 L0。
- 展示 L1 候选结果。
- 标明候选不是正式事实。

## 验收重点

- H5 可展示输入和候选。
- 前端不伪造正式事实。

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



---

# TASK-S2-001A｜S2 校验与处理方向

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：建立 S2 校验核心和处理方向返回，不处理待补详情和确认详情。  
任务状态：待执行  
任务批次：06_S2

## 依据来源

- 50_系统业务运行规则/03_横向治理运行规则.md
- 30_标准治理/03_状态口径总表.md

## 允许修改目录

- services/api/app/modules/s2_validation/
- packages/contracts/schemas/s2_validation.schema.json
- packages/contracts/schemas/processing_direction.schema.json

## 禁止修改目录

- l2_fact/ 直接写入
- supplement/ 复杂实现
- confirmation/ 复杂实现
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

- 定义最小 required/conditional/risk/blocking 校验。
- 返回 accepted、need_supplement、need_confirmation、blocked、failed。
- accepted 不等于 fact_created。

## 验收重点

- 处理方向清楚。
- 无 S2 结果不得进入 L2。

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



---

# TASK-S2-001B｜待补 supplement

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：建立待补项记录和补充提交的最小机制。  
任务状态：待执行  
任务批次：06_S2

## 依据来源

- 50_系统业务运行规则/03_横向治理运行规则.md
- 70_前后端协同边界与页面承接/04_状态提示与处理方向展示规则.md

## 允许修改目录

- services/api/app/modules/supplement/
- services/api/app/modules/s2_validation/
- apps/h5/src/modules/supplement/
- packages/contracts/schemas/supplement.schema.json

## 禁止修改目录

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

- 记录待补项。
- 支持补充提交进入重新校验。
- 不把补充提交等同于治理通过。

## 验收重点

- need_supplement 可被表达和展示。
- 补充后仍需 S2 判断。

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



---

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



---

# TASK-S2-001D｜H5 S2 状态展示

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：在 H5 展示 S2 处理方向，包括待补、确认、阻断、失败、通过当前步骤。  
任务状态：待执行  
任务批次：06_S2

## 依据来源

- 70_前后端协同边界与页面承接/04_状态提示与处理方向展示规则.md

## 允许修改目录

- apps/h5/src/modules/s2_validation/
- apps/h5/src/modules/supplement/
- apps/h5/src/modules/confirmation/
- apps/h5/src/shared/api/

## 禁止修改目录

- 后端业务规则
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

- 展示 accepted、need_supplement、need_confirmation、blocked、failed。
- 阻断原因不得隐藏。
- accepted 不展示为已完成。

## 验收重点

- H5 状态展示准确。
- 前端不伪造 fact_created。

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



---

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



---

# TASK-L2L3-001B｜L3 查询视图

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：建立 L3 查询视图，只读 L2 正式事实，并按权限范围过滤。  
任务状态：待执行  
任务批次：07_L2L3

## 依据来源

- 50_系统业务运行规则/05_正式事实入链与查询运行规则.md
- 40_业务数据体系/03_汇总视图/

## 允许修改目录

- services/api/app/modules/l3_query_view/
- packages/contracts/schemas/l3_query_view.schema.json

## 禁止修改目录

- L3 反写 L2
- 查询结果生成事实
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

- 查询 L2 facts。
- 按组织/项目/角色/数据范围过滤。
- 返回只读 view result。

## 验收重点

- L3 不反写。
- 无权限和无数据区分清楚。

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



---

# TASK-L2L3-001C｜H5 正式事实与查询展示

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：H5 展示正式事实详情、来源摘要和 L3 查询结果。  
任务状态：待执行  
任务批次：07_L2L3

## 依据来源

- 70_前后端协同边界与页面承接/01_H5主交互页面承接规则.md
- 70_前后端协同边界与页面承接/05_权限与脱敏页面承接规则.md

## 允许修改目录

- apps/h5/src/modules/l2_fact/
- apps/h5/src/modules/l3_query_view/
- apps/h5/src/shared/api/

## 禁止修改目录

- 后端 L2 创建逻辑
- 前端生成事实
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

- 展示正式事实详情。
- 展示来源摘要。
- 展示查询结果和权限/脱敏状态。

## 验收重点

- 前端只展示后端返回的事实和视图。
- 不伪造正式事实。

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



---

# TASK-TRACE-001｜最小来源追溯

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：建立最小来源追溯能力，使 L2 可追溯到 L0/L1/S2/确认来源。  
任务状态：待执行  
任务批次：08_TRACE

## 依据来源

- 20_系统架构/06_追溯与审计架构.md
- 30_标准治理/04_追溯与操作日志总表.md

## 允许修改目录

- services/api/app/modules/governance/trace_minimal/
- services/api/app/modules/l2_fact/
- services/api/app/modules/confirmation/
- apps/h5/src/modules/l2_fact/
- packages/contracts/schemas/flow_result.schema.json

## 禁止修改目录

- 复杂 Trace 平台
- 删除日志/trace/审计
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

- 事实关联 raw_input_id/candidate_id/source_candidate_id 或等效来源。
- 确认动作留痕。
- H5 展示来源摘要。

## 验收重点

- L2 来源可查。
- 缺来源不得入链。

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



---

# TASK-H5-001A｜H5 首页输入与分流

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：实现 H5 首页输入框和录入/查询/问分流提示，查询/问未接入时只提示，不进入 L0。  
任务状态：待执行  
任务批次：09_H5

## 依据来源

- 70_前后端协同边界与页面承接/01_H5主交互页面承接规则.md

## 允许修改目录

- apps/h5/src/modules/l0_input/
- apps/h5/src/shared/api/
- apps/h5/src/shared/ui/

## 禁止修改目录

- 后端业务规则
- L2 写入
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

- 输入默认录入。
- 查询/问未接入时提示待接入。
- 录入可调用 L0。

## 验收重点

- 输入交互清楚。
- 未接入能力不进入 L0/L2。

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



---

# TASK-H5-001B｜H5 候选/S2/待补/确认状态

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：集中实现 H5 对候选、S2 状态、待补、确认、阻断的展示。  
任务状态：待执行  
任务批次：09_H5

## 依据来源

- 70_前后端协同边界与页面承接/04_状态提示与处理方向展示规则.md

## 允许修改目录

- apps/h5/src/modules/l1_candidate/
- apps/h5/src/modules/s2_validation/
- apps/h5/src/modules/supplement/
- apps/h5/src/modules/confirmation/
- apps/h5/src/shared/api/

## 禁止修改目录

- 后端业务规则
- 前端伪造 fact_created
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

- 展示候选。
- 展示处理方向。
- 待补/确认动作发起但不裁决。

## 验收重点

- 状态显示准确。
- 前端不隐藏 blocked。

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



---

# TASK-H5-001C｜H5 正式事实/查询/来源摘要

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：集中实现 H5 对正式事实、查询视图和来源摘要的展示。  
任务状态：待执行  
任务批次：09_H5

## 依据来源

- 70_前后端协同边界与页面承接/01_H5主交互页面承接规则.md
- 70_前后端协同边界与页面承接/05_权限与脱敏页面承接规则.md

## 允许修改目录

- apps/h5/src/modules/l2_fact/
- apps/h5/src/modules/l3_query_view/
- apps/h5/src/modules/governance/
- apps/h5/src/shared/api/

## 禁止修改目录

- 前端生成事实
- L3 反写
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

- 展示正式事实详情。
- 展示查询视图。
- 展示来源摘要和脱敏/权限状态。

## 验收重点

- 事实/视图展示只读。
- 来源摘要可见。

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



---

# TASK-UPLOAD-001｜上传资料进入候选链路

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：建立上传资料最小受控链路，上传成功只代表接收成功，不直接成为有效资料事实。  
任务状态：待执行  
任务批次：10_RESERVED_CAPABILITIES

## 依据来源

- 50_系统业务运行规则/04_沉淀池与资料存储规则.md
- 60_接口边界与集成约束/06_上传资料与文件接口规则.md

## 允许修改目录

- services/api/app/modules/upload/
- services/api/app/modules/storage/
- services/api/app/modules/assets/file_assets/
- apps/h5/src/modules/upload/
- packages/contracts/schemas/

## 禁止修改目录

- storage/ 真实文件提交 Git
- L2 直写
- .env
- data/

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

- 上传接口或占位。
- 上传状态与资料有效状态分离。
- 上传进入候选/资料资产候选。

## 验收重点

- 上传不直写 L2。
- storage 受 .gitignore 保护。

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



---

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



---

# TASK-AI-001｜AI 辅助预处理边界

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：建立 AI 辅助边界，只做输入转译、候选归整和分析建议占位，不裁决事实。  
任务状态：待执行  
任务批次：10_RESERVED_CAPABILITIES

## 依据来源

- 50_系统业务运行规则/07_AI辅助与外部协同运行规则.md
- 60_接口边界与集成约束/07_AI与模型接口约束.md

## 允许修改目录

- services/api/app/modules/ai_assist/
- services/api/app/modules/l0_input/
- services/api/app/modules/l1_candidate/
- services/api/app/modules/l4_analysis/
- services/api/app/modules/l5_recommendation/
- packages/contracts/schemas/

## 禁止修改目录

- L2 直写
- 替代 S2
- 替代人工确认
- .env 真实模型密钥
- 完整 AI 平台

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

- AI 输出默认为候选。
- 模型密钥只通过环境变量引用。
- 不实现完整 AI 平台。

## 验收重点

- AI 不裁决事实。
- 无密钥泄露。

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



---

# TASK-TEST-001A｜后端单元与接口测试

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：建立后端模块和接口的最小测试基线。  
任务状态：待执行  
任务批次：11_TEST

## 依据来源

- 80_验证与验收规则/02_测试方案.md
- 80_验证与验收规则/03_边界与负向验证规则.md

## 允许修改目录

- services/api/tests/
- services/api/app/modules/*/tests/
- scripts/test/

## 禁止修改目录

- 业务代码自由修复
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

- 覆盖 pre_run_context、L0、L1、S2、L2、L3 的基础正向测试。
- 覆盖绕过 S2、无权限、缺来源等负向测试。

## 验收重点

- 测试文件存在。
- 测试命令可执行或说明原因。

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



---

# TASK-TEST-001B｜前端状态展示测试

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：建立 H5 状态展示和处理方向展示的最小测试。  
任务状态：待执行  
任务批次：11_TEST

## 依据来源

- 70_前后端协同边界与页面承接/07_页面验收与联调检查规则.md
- 80_验证与验收规则/02_测试方案.md

## 允许修改目录

- apps/h5/tests/
- tests/e2e/
- scripts/test/

## 禁止修改目录

- 后端业务代码
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

- 测试候选、待补、确认、阻断、正式事实、查询状态展示。
- 确保前端不把 accepted 当 fact_created。

## 验收重点

- 前端测试覆盖主要状态。
- 失败原因可回传。

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



---

# TASK-TEST-001C｜边界负向验收测试

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：建立关键越界行为的负向验收测试。  
任务状态：待执行  
任务批次：11_TEST

## 依据来源

- 80_验证与验收规则/03_边界与负向验证规则.md

## 允许修改目录

- tests/acceptance/
- scripts/check/

## 禁止修改目录

- 业务代码自由修复
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

- 覆盖前端直写 L2、AI 直写 L2、上传直写 L2、外部反馈直写 L2、L3 反写等负向场景。

## 验收重点

- 负向测试目标明确。
- 不把失败伪装为通过。

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



---

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



---

# TASK-DEPLOY-PREP-001｜部署前准备占位

发给谁：Codex 云任务 / 本地 Codex  
任务卡目的：为后续部署运行准备最小目录和说明，不提前部署未验收能力。  
任务状态：后置  
任务批次：13_DEPLOY_RESERVED

## 依据来源

- 03_control/03_技术选型摘要.md
- 80_验证与验收规则/06_准出规则.md

## 允许修改目录

- ops/
- docs/deployment/
- docs/operations/

## 禁止修改目录

- 生产部署
- 正式数据库
- 正式域名/证书配置
- 真实密钥
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

- 只做部署说明、healthcheck 规划、备份与监控占位。
- 不得实际部署未验收能力。

## 验收重点

- 部署准备说明存在。
- 未包含真实密钥。

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


