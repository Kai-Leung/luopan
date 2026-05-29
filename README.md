# Compass Codex 执行开发包 ARCH_DIR_v0.1.0 v0.1.8

本版修正点：

- `01_arch_dir/` 不再放压缩包。
- `01_arch_dir/` 内放的是已经解压后的代码目录骨架。
- 后续代码落位在 `01_arch_dir/` 下的实际代码根目录中。
- `02_development_basis/` 仍只放正式开发依据包的解压目录。

## 实际代码根目录

```text
01_arch_dir/compass
```

## 包结构

```text
Compass_Codex_执行开发包_ARCH_DIR_v0.1.0_v0.1.8/
├── AGENTS.md
├── README.md
├── FIRST_CLOUD_TASK_PROMPT.md
├── manifest.json
├── .gitignore
├── 01_arch_dir/
│   └── <已解压代码目录骨架>
├── 02_development_basis/
│   └── COMMON_罗盘系统正式开发依据包/
├── 03_control/
├── 04_task_cards/
└── 05_reports/
```

## 第一张任务

先执行：

```text
04_task_cards/02_execution_task_cards/task_cards/00_BASELINE/TASK-BASELINE-001.md
```

不要一次性执行全量任务卡。


## v0.1.8 修正

- 修正任务卡引用已移除 RUN / COMMON 源文件导致的阻断。
- `02_development_basis/` 仍保持只放正式开发依据包解压目录。
- 环境检查口径改由 `03_control/04_环境基线摘要.md` 承接。
- 技术选型口径改由 `03_control/03_技术选型摘要.md` 承接。
