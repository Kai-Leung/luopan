# TASK-H5-PROXY-001_report｜H5 Vite proxy 接入后端

## 1. 任务结论

本补丁将 H5 本地开发代理接入 FastAPI 后端。

当前 H5 API client 已支持：

```text
VITE_API_BASE 为空 → 使用相对路径请求
```

因此本任务只需在 `vite.config.ts` 中配置 `/api` 代理，不需要修改 API 调用代码。

## 2. 修改文件

```text
01_arch_dir/compass/apps/h5/vite.config.ts
01_arch_dir/compass/apps/h5/README.md
```

## 3. Proxy 配置

```text
/api/* → http://127.0.0.1:8000/api/*
```

## 4. 未修改范围

未修改：

```text
01_arch_dir/compass/services/api/
01_arch_dir/compass/packages/
02_development_basis/
03_control/
04_task_cards/
.env
data/
storage/
```

## 5. 验证要求

合并后执行：

```bash
cd 01_arch_dir/compass/apps/h5
npm run check
npm run build
```

如需联调：

```bash
cd 01_arch_dir/compass/services/api
source .venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

另开终端：

```bash
cd 01_arch_dir/compass/apps/h5
npm run dev
```

然后从 H5 页面发起主链路请求。

## 6. 预期结果

- `npm run check` 通过；
- `npm run build` 通过；
- H5 通过相对路径 `/api/...` 调用后端；
- 不需要修改 `.env`；
- 不在前端写死完整后端地址。
