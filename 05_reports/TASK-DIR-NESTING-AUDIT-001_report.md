# TASK-DIR-NESTING-AUDIT-001 Report｜目录嵌套层级审计

## 1. 当前目录树（深度 ≤ 4 层）

```
.
├── .gitignore
├── AGENTS.md
├── FIRST_CLOUD_TASK_PROMPT.md
├── README.md
├── manifest.json
├── 01_arch_dir/
│   └── compass/
│       ├── .env.example
│       ├── .gitignore
│       ├── AGENTS.md            ⚠️ 与根目录文件重复
│       ├── README.md            ⚠️ 与根目录文件重复
│       ├── package.json
│       ├── pyproject.toml
│       ├── package-lock.json
│       ├── apps/
│       │   ├── h5/              ← 真实前端目录
│       │   ├── mobile-shell/    ← 空壳（3 文件）
│       │   └── pc/              ← 空壳（2 文件）
│       ├── data/
│       │   ├── .gitkeep
│       │   ├── dev/
│       │   └── test/
│       ├── docs/
│       ├── node_modules/
│       ├── ops/
│       ├── packages/
│       │   ├── contracts/       ← 真实契约目录
│       │   ├── native-bridge/
│       │   ├── shared-types/
│       │   └── shared-utils/
│       ├── scripts/
│       ├── services/
│       │   └── api/             ← 真实后端目录
│       ├── storage/
│       │   ├── .gitkeep
│       │   ├── dev/
│       │   └── test/
│       └── tests/               ← 空壳目录
│           ├── acceptance/ (empty)
│           ├── e2e/ (empty)
│           └── integration/ (empty)
├── 02_development_basis/
│   └── COMMON_罗盘系统正式开发依据包/
│       └── 罗盘系统正式开发依据包_v1.0.1/
│           ├── 00_manifest.md
│           ├── 00_tree.md
│           ├── 00_开发依据包总览与阅读顺序.md
│           ├── 10_顶层定义/
│           ├── 20_系统架构/
│           ├── 30_标准治理/
│           ├── 40_业务数据体系/
│           ├── 50_系统业务运行规则/
│           ├── 60_接口边界与集成约束/
│           ├── 70_前后端协同边界与页面承接/
│           └── 80_验证与验收规则/
├── 03_control/
│   ├── 01_开发依据与目录映射总表.md
│   ├── 02_任务卡索引与读取规则.md
│   ├── 03_技术选型摘要.md
│   └── 04_环境基线摘要.md
├── 04_task_cards/
│   └── 02_execution_task_cards/
│       ├── 04_执行任务卡库_ARCH_DIR_v0.1.0.md
│       ├── README.md
│       └── task_cards/ (14 个子目录)
└── 05_reports/
    ├── TASK-DB-SQLITE-FILE-001_report.md
    ├── TASK-FE-BE-INTEGRATION-001_report.md
    ├── TASK-H5-MC-PENDING-ID-FIX-001_report.md
    └── TASK-H5-PROXY-001_report.md
```

## 2. 过度嵌套目录清单

最大嵌套深度为 **10 层**（不含 `.git`/`node_modules`/`__pycache__`）：

```
10: 01_arch_dir/compass/services/api/app/modules/standard_governance/rules/...
10: 01_arch_dir/compass/services/api/app/modules/standard_governance/enums/...
10: 01_arch_dir/compass/services/api/app/modules/standard_governance/display/...
10: 01_arch_dir/compass/services/api/app/modules/s2_governance_gate/confirmation/...
```

但这是 **ARCH_DIR 参考架构本身的模块化设计**（app/core/db/api 分层 + modules 内 policy/tests/adapters 分层），并非无意嵌套。属于"有意为之的架构分层"，无需扁平化。

**总计：** 工作区 ≈ 350 个目录，H5 src ≈ 112 个，后端 app ≈ 110 个。

## 3. 补丁包残留目录清单

**无残留。** ✅

之前解压的 `Compass_combined_code_patches_v0.1.0/` 目录已在上一轮删除。`/tmp/compass_pack/` 存在但不在工作区内，不影响。

## 4. 重复代码目录清单

### 4.1 AGENTS.md / README.md 重复

| 位置 | 文件 | 状态 |
|---|---|---|
| 根目录 | AGENTS.md | ✅ 根工作区 AGENTS.md |
| `01_arch_dir/compass/AGENTS.md` | AGENTS.md | ⚠️ 重复嵌套 |
| 根目录 | README.md | ✅ 根工作区 README.md |
| `01_arch_dir/compass/README.md` | README.md | ⚠️ 重复嵌套 |

`01_arch_dir/compass/` 下的 AGENTS.md 和 README.md 是 Codex 原始 monorepo 遗留下来的，与根目录文件内容不同，指向不同的受众（基于参考架构的开发者 vs 基于执行开发包的执行器）。

### 4.2 空壳目录（apps/mobile-shell, apps/pc, tests/）

| 目录 | 文件数 | 建议 |
|---|---|---|
| `apps/mobile-shell` | 3 | 保留（后续用途） |
| `apps/pc` | 2 | 保留（后续用途） |
| `tests/acceptance` | 0 | 空壳 |
| `tests/e2e` | 0 | 空壳 |
| `tests/integration` | 0 | 空壳 |

### 4.3 无重复的 apps / services / packages

均只有 `01_arch_dir/compass/` 下一份，无多份重复。

## 5. 必须保留的目录

| 目录 | 原因 |
|---|---|
| `AGENTS.md` | 执行器工作规则 |
| `FIRST_CLOUD_TASK_PROMPT.md` | 首次云任务提示 |
| `README.md` | 工作区说明 |
| `manifest.json` | 包清单 |
| `01_arch_dir/compass/apps/h5/` | **真实前端代码** |
| `01_arch_dir/compass/services/api/` | **真实后端代码** |
| `01_arch_dir/compass/packages/contracts/` | **契约（openapi / schemas）** |
| `01_arch_dir/compass/data/` | 开发数据 |
| `01_arch_dir/compass/storage/` | 开发存储 |
| `01_arch_dir/compass/scripts/` | 构建/检查/开发脚本 |
| `01_arch_dir/compass/ops/` | 部署/运维脚本 |
| `01_arch_dir/compass/docs/` | 文档 |
| `02_development_basis/` | 正式开发依据 |
| `03_control/` | 控制文件 |
| `04_task_cards/` | 任务卡片库 |
| `05_reports/` | 报告 |

## 6. 可删除的临时目录

| 目录 | 处理建议 |
|---|---|
| `/tmp/compass_pack` | 可清理（工作区外部） |
| `01_arch_dir/compass/apps/h5/dist` | 构建产物，非仓库文件 |
| `01_arch_dir/compass/node_modules` | 依赖，非仓库文件 |
| `01_arch_dir/compass/services/api/.venv` | 虚拟环境，非仓库文件 |

工作区内部无可立即删除的空壳临时目录。

## 7. 建议提升到根目录的目录

**不推荐。** 当前 `01_arch_dir/compass/` 是一个 monorepo，包含 apps/services/packages/data/storage/scripts/ops/docs，整体提升到根目录会打乱 ARCG_DIR 架构设计。各层之间已有明确的依赖关系和路径引用（如 `CODE_ROOT = Path(...).parents[4]`）。

## 8. 不建议移动的目录

| 目录 | 原因 |
|---|---|
| `01_arch_dir/` → 提升取消嵌套 | `app/db/session.py` 用 `Path(...).parents[4]` 定位 `data/dev/`；`vite.config.ts` 用相对路径；移动会破坏所有路径引用 |
| `02_development_basis/` | 不改正式开发依据正文内容 |
| `03_control/` `04_task_cards/` | 执行器规则依赖这些精确路径 |
| `01_arch_dir/compass/data/` → 根目录 | `session.py` 硬编码 CODE_ROOT parents[4] 路径 |
| `01_arch_dir/compass/storage/` → 根目录 | 同上 |

## 9. 推荐最终目录结构

**维持现状。** 当前结构虽然嵌套 01_arch_dir/ 一层，但这是 ARCH_DIR 参考架构的约定格式，有充分的路径引用依据。

根目录下的 `01_arch_dir/compass/` 嵌套 AGENTS.md 和 README.md 是唯一的设计瑕疵，但考虑到其面向不同受众（Codex monorepo 开发者 vs 执行包使用者），可接受。

如果需要扁平化，最现实的改动是：
- 将 `01_arch_dir/compass/` 下的 AGENTS.md / README.md 合并或删除一份
- 删除 `tests/` 下的 3 个空壳目录

## 10. 下一步是否需要执行目录扁平化

**不需要。** 当前目录结构符合 ARCH_DIR 参考架构设计：

```
执行开发包根目录
├── AGENTS.md / README.md / manifest.json     ← 执行器入口
├── 01_arch_dir/compass/                      ← 完整代码仓库
│   ├── apps/h5/                              ← 前端
│   ├── services/api/                         ← 后端
│   ├── packages/                             ← 共享包
│   ├── data/ / storage/                      ← 数据层
│   └── ...
├── 02_development_basis/                     ← 开发依据
├── 03_control/                               ← 控制文件
├── 04_task_cards/                            ← 任务卡
└── 05_reports/                               ← 报告
```

**结论：** 无过度嵌套，无补丁包残留，无重复代码目录，无错误嵌套。结构清晰，无需扁平化。
