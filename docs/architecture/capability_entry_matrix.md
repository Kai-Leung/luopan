# 能力接入矩阵

状态口径：

- `placeholder`：只有目录、README、配置或空入口。
- `implemented`：存在真实实现，但自动化或验收尚未全绿。
- `verified`：对应自动化检查在当前基线通过。
- `accepted`：正向、负向、一致性、回归和独立验收均完成。

目录、路由、类型、build 成功或历史报告都不能单独证明业务能力已验收。

## 当前基线

| 能力域 | 状态 | 当前代码证据 | 当前限制 |
|---|---|---|---|
| Contracts | `verified` | FastAPI OpenAPI、24 个 JSON Schema、contracts consistency 脚本 | 检查通过不代表业务接口已验收 |
| S1 运行上下文 | `implemented` | 后端 runtime-context、统一 dependency、H5/PC 上下文请求 | pytest 存在 `ContextVar` 跨线程重置失败 |
| L0-L3 事实主链路 | `implemented` | 原始输入、候选、S2、人工确认、L2 持久化、L3 查询 | 后端测试套件当前非全绿 |
| L4-L7 | `implemented` | 分析、建议、执行响应、反馈持久化与 H5 操作入口 | 受 S1 测试失败影响，不能标记 verified |
| S2 治理闸门 | `implemented` | 必填、风险、阻断、补充和确认规则 | 存在候选解析相关失败 |
| S3 审计追溯 | `implemented` | trace event 持久化与摘要查询 | 测试基线未全绿 |
| 上传与文件存储 | `implemented` | 原文件 API、类型/大小校验、H5 上传入口 | 本地存储实现，不等同生产存储服务验收 |
| 语音转写 | `implemented` | 浏览器录音、后端适配入口和 H5 flow | 供应商凭据和真实协议未形成生产验收 |
| AI 辅助 | `implemented` | 后端候选 intake 与回流边界 | 测试受 S1 失败影响，不是自主裁决能力 |
| 外部协同 | `implemented` | 外部反馈 intake 与候选回流 | 测试受 S1 失败影响，脱敏与回执仍需验收 |
| H5 | `implemented` | 可构建 React/Vite 应用，接入主要 API 和状态流 | 无完整前端自动化业务测试 |
| PC | `implemented` | 可构建治理工作台，接入上下文、确认和事实查询 | 无完整前端自动化业务测试 |
| Mobile shell | `placeholder` | Capacitor 配置和依赖 | 未生成/提交原生工程，未完成签名和真机验收 |
| 对象资产 | `placeholder` | 目录和局部类型/接口边界 | 尚无完整资产闭环证据 |
| CI | `implemented` | PR/main 检查 frontend、contracts、repository policy、pytest | pytest 当前会严格暴露既有失败 |
| Deploy | `implemented` | 独立 GitHub Actions workflow | 仅允许人工触发，不代表已执行部署 |

## 当前自动化事实

- `npm ci`：通过。
- `npm run check`：治理前的 TypeScript 与 contracts 检查通过。
- H5 build：通过。
- PC build：通过。
- contracts consistency：通过。
- pytest：当前基线为 `183 passed, 50 failed, 4 warnings`。

在 pytest 恢复全绿并完成对应业务验收前，不得把 S1-S3、L0-L7 或整体系统标记为
`verified` 或 `accepted`。
