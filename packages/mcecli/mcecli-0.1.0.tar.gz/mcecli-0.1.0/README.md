# MCE CLI

MCE CLI 是一个用于管理多模态计算引擎（MCE）服务器的 Python 命令行工具。它提供了完整的项目、队列、计算配置和作业管理功能。

## 功能特性

- **项目管理**: 创建、列出、更新和删除项目
- **队列管理**: 管理 Kueue 队列配置
- **计算配置管理**: 管理 Ray 集群配置
- **作业管理**: 创建、监控和管理 Ray 作业
- **日志管理**: 查看和流式传输作业日志
- **多种输出格式**: 支持表格、JSON、YAML 格式输出
- **配置管理**: 灵活的配置文件管理

## 安装

### 从 PyPI 安装（推荐）

```bash
pip install mcecli
```

### 从源码安装

```bash
cd mcecli
pip install -e .
```

### 使用 uv 安装

```bash
# 从 PyPI
uv pip install mcecli

# 从源码
cd mcecli
uv pip install -e .
```

## 快速开始

### 1. 配置服务器地址

```bash
# 设置 MCE Server 地址
mcecli config set server.url http://your-mce-server:8080

# 设置认证信息
mcecli config set auth.owner_appid your-app-id
mcecli config set auth.owner_uin your-uin
mcecli config set auth.owner_sub_uin your-sub-uin
```

### 2. 检查服务器连接

```bash
mcecli health
```

### 3. 创建项目

```bash
mcecli project create --name "my-project" --description "My first project" --region "ap-beijing"
```

### 4. 创建队列

```bash
mcecli queue create --project-id "proj-123" --name "default-queue" --weight 1
```

### 5. 创建计算配置

```bash
# 查看配置模板
mcecli compute-config template

# 创建配置
mcecli compute-config create \
  --project-id "proj-123" \
  --name "ray-config" \
  --ray-version "2.8.0" \
  --head-config '{"resources":{"cpu":"2","memory":"4Gi"},"image":"rayproject/ray:2.8.0"}' \
  --worker-config '{"minReplicas":1,"maxReplicas":3,"resources":{"cpu":"1","memory":"2Gi"},"image":"rayproject/ray:2.8.0"}'
```

### 6. 提交作业

```bash
mcecli job create \
  --project-id "proj-123" \
  --name "training-job" \
  --entrypoint "python train.py" \
  --image "rayproject/ray:2.8.0" \
  --queue-id "queue-456" \
  --compute-config-id "config-789" \
  --pip-package torch \
  --pip-package transformers \
  --env CUDA_VISIBLE_DEVICES=0
```

### 7. 查看作业日志

```bash
# 获取日志
mcecli logs get --project-id "proj-123" job-123

# 实时流式日志
mcecli logs stream --project-id "proj-123" job-123 --follow
```

## 命令参考

### 全局选项

- `--config-file, -c`: 指定配置文件路径
- `--server-url, -s`: 指定服务器 URL
- `--output, -o`: 输出格式 (table/json/yaml)
- `--no-color`: 禁用彩色输出
- `--verbose, -v`: 详细输出

### 项目管理

```bash
# 创建项目
mcecli project create --name NAME [--description DESC] [--region REGION] [--tag key=value]

# 列出项目
mcecli project list [--page PAGE] [--page-size SIZE]

# 获取项目详情
mcecli project get PROJECT_ID

# 更新项目
mcecli project update PROJECT_ID [--name NAME] [--description DESC] [--tag key=value]

# 删除项目
mcecli project delete PROJECT_ID [--force]
```

### 队列管理

```bash
# 创建队列
mcecli queue create --project-id PROJECT_ID --name NAME [--weight WEIGHT] [--flavor-name FLAVOR]

# 列出队列
mcecli queue list --project-id PROJECT_ID [--page PAGE] [--page-size SIZE]

# 获取队列详情
mcecli queue get --project-id PROJECT_ID QUEUE_ID

# 更新队列
mcecli queue update --project-id PROJECT_ID QUEUE_ID [--name NAME] [--weight WEIGHT]

# 删除队列
mcecli queue delete --project-id PROJECT_ID QUEUE_ID [--force]

# 获取队列状态
mcecli queue status --project-id PROJECT_ID QUEUE_ID
```

### 计算配置管理

```bash
# 创建计算配置
mcecli compute-config create --project-id PROJECT_ID --name NAME --ray-version VERSION \
  --head-config JSON --worker-config JSON

# 列出计算配置
mcecli compute-config list --project-id PROJECT_ID [--page PAGE] [--page-size SIZE]

# 获取计算配置详情
mcecli compute-config get --project-id PROJECT_ID CONFIG_ID

# 更新计算配置
mcecli compute-config update --project-id PROJECT_ID CONFIG_ID [OPTIONS]

# 删除计算配置
mcecli compute-config delete --project-id PROJECT_ID CONFIG_ID [--force]

# 查看配置模板
mcecli compute-config template
```

### 作业管理

```bash
# 创建作业
mcecli job create --project-id PROJECT_ID --name NAME --entrypoint COMMAND --image IMAGE \
  [--queue-id QUEUE_ID] [--compute-config-id CONFIG_ID] [--ray-version VERSION] \
  [--pip-package PACKAGE] [--env KEY=VALUE] [--working-dir DIR] [--volume-mount JSON]

# 列出作业
mcecli job list --project-id PROJECT_ID [--page PAGE] [--page-size SIZE]

# 获取作业详情
mcecli job get --project-id PROJECT_ID JOB_ID

# 停止作业
mcecli job stop --project-id PROJECT_ID JOB_ID [--force]

# 重试作业
mcecli job retry --project-id PROJECT_ID JOB_ID

# 删除作业
mcecli job delete --project-id PROJECT_ID JOB_ID [--force]

# 获取作业事件
mcecli job events --project-id PROJECT_ID JOB_ID

# 查看作业模板
mcecli job template
```

### 日志管理

```bash
# 获取作业日志
mcecli logs get --project-id PROJECT_ID JOB_ID [--lines N] [--since TIMESTAMP]

# 实时流式日志
mcecli logs stream --project-id PROJECT_ID JOB_ID [--follow]

# 获取日志文件信息
mcecli logs info --project-id PROJECT_ID JOB_ID
```

### 配置管理

```bash
# 查看配置
mcecli config show

# 设置配置
mcecli config set KEY VALUE

# 获取配置
mcecli config get KEY

# 重置配置
mcecli config reset [--force]

# 查看配置文件路径
mcecli config path
```

## 配置文件

配置文件默认位于 `~/.mcecli/config.yaml`：

```yaml
server:
  url: http://localhost:8080
  timeout: 30

output:
  format: table  # table, json, yaml
  color: true

auth:
  owner_appid: ""
  owner_uin: ""
  owner_sub_uin: ""
```

## 存储挂载示例

### COS 存储挂载

```json
{
  "type": "COS",
  "mountPath": "/data",
  "readOnly": false,
  "remotePath": "cos://bucket-name/path/",
  "cosOptions": {
    "region": "ap-beijing",
    "secretId": "your-secret-id",
    "secretKey": "your-secret-key"
  }
}
```

### CFS 存储挂载

```json
{
  "type": "CFS",
  "mountPath": "/shared",
  "readOnly": false,
  "remotePath": "cfs://file-system-id/path/"
}
```

### HostPath 挂载

```json
{
  "type": "HostPath",
  "mountPath": "/host-data",
  "readOnly": true,
  "remotePath": "/host/path"
}
```

## 环境变量

- `MCE_SERVER_URL`: 服务器 URL
- `MCE_CONFIG_FILE`: 配置文件路径
- `MCE_OUTPUT_FORMAT`: 输出格式
- `MCE_NO_COLOR`: 禁用彩色输出

## 错误处理

CLI 工具提供详细的错误信息和建议：

- 网络连接错误
- 认证失败
- 资源不存在
- 权限不足
- 配置错误

## 开发

### 项目结构

```
mcecli/
├── mcecli/
│   ├── __init__.py
│   ├── main.py          # CLI 入口点
│   ├── config.py        # 配置管理
│   ├── client.py        # HTTP 客户端
│   ├── utils.py         # 工具函数
│   ├── exceptions.py    # 异常定义
│   └── commands/        # 命令模块
│       ├── __init__.py
│       ├── project.py
│       ├── queue.py
│       ├── compute_config.py
│       ├── job.py
│       ├── logs.py
│       └── config.py
├── pyproject.toml
├── README.md
└── main.py             # 向后兼容入口
```

### 运行测试

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 代码格式化
black mcecli/
isort mcecli/

# 类型检查
mypy mcecli/
```

## 许可证

[添加许可证信息]

## 贡献

欢迎提交 Issue 和 Pull Request！