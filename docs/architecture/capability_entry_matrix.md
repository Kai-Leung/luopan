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
| S1 运行上下文 | `verified` | async dependency、正常/异常清理、连续请求、组织和跨项目隔离测试 | 当前为受控单组织基线，不是完整账号体系验收 |
| L0-L3 事实主链路 | `verified` | 原始输入、候选、S2、pending active/resolved 持久化、人工确认、L2、L3 与重启读取测试 | 未完成独立人工业务验收 |
| L4-L7 | `verified` | 分析、建议、执行响应、反馈持久化、只读/不直写 L2 测试 | 未完成业务效果与人工验收 |
| S2 治理闸门 | `verified` | 必填、风险、阻断、补充、确认和候选解析回归测试 | 规则效果仍需真实场景验收 |
| S3 审计追溯 | `verified` | trace event 持久化与 L4-L7 来源链测试 | 未完成运维审计验收 |
| 上传与文件存储 | `verified` | 原文件 API、类型/大小校验、路径验证和 H5 上传入口 | 本地存储实现，不等同生产存储服务验收 |
| 语音转写 | `implemented` | 浏览器录音、后端适配入口和 H5 flow | 供应商凭据和真实协议未形成生产验收 |
| AI 辅助 | `implemented` | 后端候选 intake 与回流边界 | 测试受 S1 失败影响，不是自主裁决能力 |
| 外部协同 | `implemented` | 外部反馈 intake 与候选回流 | 测试受 S1 失败影响，脱敏与回执仍需验收 |
| H5 | `verified` | React/Vite build；意图分流、L0-L3、项目上下文、阻断、确认与错误路径自动化 | 缺少浏览器 E2E 和独立人工验收 |
| PC | `verified` | React/Vite build；上下文、pending、facts、确认/退回/驳回和错误路径自动化 | 缺少浏览器 E2E 和独立人工验收 |
| Mobile shell | `placeholder` | Capacitor 配置和依赖 | 未生成/提交原生工程，未完成签名和真机验收 |
| 对象资产 | `placeholder` | 目录和局部类型/接口边界 | 尚无完整资产闭环证据 |
| CI | `verified` | repository-policy、frontend、contracts、backend、integration 均为强制门禁，无 `continue-on-error` | GitHub 分支保护仍需仓库管理员确认 |
| Deploy | `implemented` | CI 全绿后由 main 运行代码变更调用 reusable workflow；部署前后检查服务器工作区并校验目标 SHA | 当前只重启后端，未包含 H5/PC 静态发布；本任务未实际部署 |

## 当前自动化事实

- `npm ci`：通过。
- `npm run check`：通过。
- H5 build：通过。
- PC build：通过。
- H5 tests：6 passed。
- PC tests：5 passed。
- contracts consistency：通过。
- pytest：`253 passed, 0 failed, 5 warnings`（系统 Python 环境额外报告 httpx/httpx2 兼容弃用提示）。
- integration：8 passed。

上述 `verified` 仅表示当前自动化证据通过。未完成独立人工验收的能力不得标记为
`accepted`，也不得宣称系统已完成业务验收。
