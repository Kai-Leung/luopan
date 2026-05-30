# TASK-DB-SQLITE-FILE-001_report｜开发文件 SQLite 落地补丁说明

## 1. 补丁目标

将后端默认开发数据库从内存 SQLite 调整为项目内文件 SQLite，避免后端服务重启后开发数据丢失。

## 2. 修改文件

- `01_arch_dir/compass/services/api/app/db/session.py`
- `01_arch_dir/compass/services/api/tests/e2e/test_l0_l3_storage_repositories.py`

## 3. 新开发库路径

默认开发库路径：

```text
01_arch_dir/compass/data/dev/compass_dev.sqlite3
```

对应 SQLAlchemy URL：

```text
sqlite:///.../01_arch_dir/compass/data/dev/compass_dev.sqlite3
```

## 4. 测试隔离

测试环境仍使用：

```text
sqlite:///:memory:
```

处理规则：

- `app_env="test"` 时使用内存库；
- pytest 运行且没有显式传入 `app_env` / `DATABASE_URL` 时使用内存库；
- 显式 `app_env="development"` 时使用文件库；
- production/prod 环境无显式数据库配置时继续阻断。

## 5. 受控边界

本补丁不修改：

- `.env`
- `apps/h5/`
- `packages/`
- `02_development_basis/`
- `03_control/`
- `04_task_cards/`
- `storage/`
- 正式数据库

本补丁不引入：

- PostgreSQL
- Redis
- Celery
- Alembic

## 6. 落位后验证

执行：

```bash
cd 01_arch_dir/compass/services/api
source .venv/bin/activate
pytest -q
```

期望：

```text
161 passed
```

如测试失败，不得自行扩大修复范围，需回传失败原文。
