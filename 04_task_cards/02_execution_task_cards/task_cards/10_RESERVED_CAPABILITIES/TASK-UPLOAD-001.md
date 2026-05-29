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


