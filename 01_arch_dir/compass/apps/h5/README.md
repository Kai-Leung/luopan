# apps/h5

H5 当前主前端。只做交互、状态承接、页面动作发起，不做事实裁决。

## 本次集成说明

本目录已纳入现有 H5 前端界面资产，包含：

- 首页输入与分流
- 候选展示
- S2 治理状态展示
- 待补 / 人工确认展示
- 正式事实详情展示
- L3 查询视图展示
- 上传入口 UI
- 语音转写预留能力
- Mock 演示页面

## 边界

- 前端只发起动作和展示后端返回状态。
- 前端不得决定最终权限。
- 前端不得决定 S2 校验结果。
- 前端不得直接生成正式事实。
- `requestFactCreationAfterConfirmation` 只是向后端发起入链请求；后端必须复核 S2、确认记录和来源链。
- Mock 页面只能用于本地演示，不代表正式能力。
- 语音、上传、外部协同等能力保留为后续接入口，未接入后端时不得进入正式事实链路。


## 本地开发代理

H5 本地开发环境通过 Vite proxy 访问后端：

```text
/api/* → http://127.0.0.1:8000/api/*
```

使用方式：

1. 启动后端：

```bash
cd 01_arch_dir/compass/services/api
source .venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

2. 启动前端：

```bash
cd 01_arch_dir/compass/apps/h5
npm run dev
```

3. 前端 API 调用保持相对路径，例如：

```text
/api/v1/l0/raw-input
```

不需要在前端写死完整后端地址。  
默认不要求修改 `.env`。
