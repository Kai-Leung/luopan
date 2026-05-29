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


