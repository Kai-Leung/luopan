# AGENTS

本文件定义仓库级执行边界，适用于人工执行器、Codex、CI 和其他自动化工具。

## 代码来源与 Git

- 只以当前仓库、当前分支和当前 Git 历史为代码来源。
- 业务修改必须通过非 `main` 分支和 Pull Request 进入主线。
- 禁止 force push、改写历史、创建 orphan 分支或合并无共同历史。
- 未经明确授权不得执行 `git add`、`commit`、`push`、合并或部署。

## 数据与环境

- 不得修改、提交或输出 `.env`、密钥、Token、GitHub Secrets。
- 不得操作正式数据库，不得清空 Raw Store、`data/`、`storage/` 或用户运行数据。
- 数据库、日志、构建产物、缓存、虚拟环境和执行报告不得进入版本控制。

## 业务边界

- 不得绕过 S1、S2、S3。
- 不得由前端直接裁决或写入 L2。
- 不得把目录、路由、占位模块或构建成功描述为业务验收完成。
- 仓库治理任务不得修改 L0-L7、S1-S3、contracts 或数据模型的业务含义。

## 验证与部署

- TypeScript check、build、contracts 检查和 pytest 必须分别如实报告。
- 既有失败不得隐藏；禁止为了让治理检查通过而修改业务逻辑。
- Pull Request 和开发分支只运行 CI，不得部署。
- `main` 的运行代码变更只有在全部必需 CI 检查成功后才可自动部署；docs-only 变更不得部署。
- 部署 workflow 不得直接监听 `push`，必须由 CI 门禁调用，同时保留 `workflow_dispatch`。
- 生产部署前后必须验证服务器 Git 工作区干净，并确认最终 HEAD 与指定部署 SHA 完全一致；不得自动 reset、clean 或 stash。
- 自动化执行器不得使用 `[skip ci]` 绕过 CI、部署、依赖、业务代码或测试验证。
