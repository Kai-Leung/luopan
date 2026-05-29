# Codex/Kodex 第一张云任务提示词

实际代码根目录：

```text
01_arch_dir/compass
```

只执行：

```text
04_task_cards/02_execution_task_cards/task_cards/00_BASELINE/TASK-BASELINE-001.md
```

执行前必须读取：

```text
AGENTS.md
03_control/01_开发依据与目录映射总表.md
03_control/02_任务卡索引与读取规则.md
03_control/03_技术选型摘要.md
03_control/04_环境基线摘要.md
当前任务卡
```

正式开发依据只从以下目录读取：

```text
02_development_basis/COMMON_罗盘系统正式开发依据包/
```

本任务只读检查，不修改业务代码。

完成后把报告写入：

```text
05_reports/TASK-BASELINE-001_report.md
```

禁止修改：

```text
.env
data/
storage/
01_arch_dir/**/data/dev/
01_arch_dir/**/storage/dev/
正式数据库
业务代码目录
```

未经授权不得执行：

```text
git add
git commit
git push
```
