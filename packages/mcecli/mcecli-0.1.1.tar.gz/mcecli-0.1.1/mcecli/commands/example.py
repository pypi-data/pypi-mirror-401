"""Example template generation commands."""

import os
import click
from pathlib import Path
from ..utils import print_success, print_error


JOB_TEMPLATE = """# Ray Job 配置
# 使用方式: mcecli job create -f job.yaml

type: ray
name: {name}
entrypoint: "python main.py"
image: rayproject/ray:2.46.0
rayVersion: "2.46.0"

# 资源配置
computeConfigName: {compute_config}

# 运行时配置
pipPackages:
  - requests>=2.28.0

envVars:
  APP_NAME: {name}

# 存储挂载配置 (可选)
# volumeMounts:
#   - type: HostPath
#     remotePath: /data
#     mountPath: /data
#     readOnly: true

maxRetries: 0
timeoutS: 600
idleTimeoutS: 300
"""

RAY_DEMO_CODE = '''"""Ray Demo - 分布式计算示例

这是一个简单的 Ray 分布式计算示例，演示了：
1. Ray 初始化
2. 远程函数 (@ray.remote)
3. 并行任务执行
4. 结果收集
"""

import os
import ray
import time
from typing import List


@ray.remote
def compute_task(task_id: int, data: int) -> dict:
    """远程计算任务
    
    Args:
        task_id: 任务ID
        data: 输入数据
    
    Returns:
        计算结果字典
    """
    # 模拟计算
    time.sleep(0.1)
    result = data * data
    
    return {
        "task_id": task_id,
        "input": data,
        "result": result,
        "node": ray.get_runtime_context().get_node_id()[:8]
    }


@ray.remote
class Counter:
    """分布式计数器 Actor 示例"""
    
    def __init__(self):
        self.count = 0
    
    def increment(self, n: int = 1) -> int:
        self.count += n
        return self.count
    
    def get_count(self) -> int:
        return self.count


def run_parallel_tasks(num_tasks: int = 10) -> List[dict]:
    """并行执行多个计算任务
    
    Args:
        num_tasks: 任务数量
    
    Returns:
        所有任务的结果列表
    """
    print(f"\\n>>> 启动 {num_tasks} 个并行任务...")
    
    # 提交所有任务
    futures = [compute_task.remote(i, i + 1) for i in range(num_tasks)]
    
    # 等待所有任务完成
    results = ray.get(futures)
    
    return results


def run_actor_example() -> int:
    """运行 Actor 示例
    
    Returns:
        最终计数值
    """
    print("\\n>>> 运行 Actor 示例...")
    
    # 创建 Actor
    counter = Counter.remote()
    
    # 并行调用 Actor 方法
    futures = [counter.increment.remote(i) for i in range(1, 6)]
    ray.get(futures)
    
    # 获取最终计数
    final_count = ray.get(counter.get_count.remote())
    
    return final_count


def main():
    """主函数"""
    app_name = os.environ.get("APP_NAME", "ray-demo")
    print(f"=" * 50)
    print(f"Ray Demo: {app_name}")
    print(f"=" * 50)
    
    # 初始化 Ray
    if not ray.is_initialized():
        ray.init()
    
    print(f"\\nRay 集群信息:")
    print(f"  - 节点数: {len(ray.nodes())}")
    print(f"  - 可用 CPU: {ray.available_resources().get('CPU', 0)}")
    print(f"  - 可用 GPU: {ray.available_resources().get('GPU', 0)}")
    
    # 运行并行任务
    start_time = time.time()
    results = run_parallel_tasks(10)
    elapsed = time.time() - start_time
    
    print(f"\\n并行任务结果 (耗时 {elapsed:.2f}s):")
    for r in results[:5]:
        print(f"  Task {r['task_id']}: {r['input']}^2 = {r['result']} (node: {r['node']})")
    if len(results) > 5:
        print(f"  ... 共 {len(results)} 个任务")
    
    # 运行 Actor 示例
    final_count = run_actor_example()
    print(f"\\nActor 计数结果: {final_count} (预期: 15)")
    
    print(f"\\n{'=' * 50}")
    print("Demo 完成!")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
'''


@click.group()
def example():
    """Generate example templates for jobs and Ray programs."""
    pass


@example.command()
@click.option('--name', '-n', default='my-ray-job', help='Job name')
@click.option('--compute-config', '-c', required=True, help='Compute config name to use')
@click.option('--working-dir', '-d', default='.', help='Output directory')
@click.pass_context
def init(ctx, name: str, compute_config: str, working_dir: str):
    """Initialize a new Ray job project with templates.
    
    Generates:
    - job.yaml: Job configuration file
    - main.py: Ray demo program
    
    Examples:
    \b
    # Generate templates in current directory
    mcecli example init -c my-compute-config
    
    # Generate with custom name and directory
    mcecli example init -n my-job -c gpu-config -d ./my-project
    """
    try:
        # Create working directory if not exists
        work_path = Path(working_dir)
        work_path.mkdir(parents=True, exist_ok=True)
        
        # Generate job.yaml
        job_content = JOB_TEMPLATE.format(
            name=name,
            compute_config=compute_config
        )
        job_file = work_path / "job.yaml"
        job_file.write_text(job_content, encoding='utf-8')
        print_success(f"Created: {job_file}")
        
        # Generate main.py
        demo_file = work_path / "main.py"
        demo_file.write_text(RAY_DEMO_CODE, encoding='utf-8')
        print_success(f"Created: {demo_file}")
        
        # Print usage instructions
        click.echo("")
        click.echo("使用说明:")
        click.echo(f"  1. 进入目录: cd {working_dir}")
        click.echo(f"  2. 上传代码: mcecli upload {working_dir}")
        click.echo(f"  3. 修改 job.yaml 中的 workingDir 为上传后的 COS 路径")
        click.echo(f"  4. 提交任务: mcecli job create -f job.yaml")
        click.echo("")
        
    except Exception as e:
        print_error(f"Failed to generate templates: {str(e)}")
        ctx.exit(1)


@example.command()
@click.option('--working-dir', '-d', default='.', help='Output directory')
@click.pass_context
def job(ctx, working_dir: str):
    """Generate a job.yaml template only.
    
    Examples:
    \b
    mcecli example job
    mcecli example job -d ./my-project
    """
    try:
        work_path = Path(working_dir)
        work_path.mkdir(parents=True, exist_ok=True)
        
        job_content = JOB_TEMPLATE.format(
            name='my-ray-job',
            compute_config='<your-compute-config>'
        )
        job_file = work_path / "job.yaml"
        job_file.write_text(job_content, encoding='utf-8')
        print_success(f"Created: {job_file}")
        
    except Exception as e:
        print_error(f"Failed to generate job template: {str(e)}")
        ctx.exit(1)


@example.command()
@click.option('--working-dir', '-d', default='.', help='Output directory')
@click.pass_context
def demo(ctx, working_dir: str):
    """Generate a Ray demo program only.
    
    Examples:
    \b
    mcecli example demo
    mcecli example demo -d ./my-project
    """
    try:
        work_path = Path(working_dir)
        work_path.mkdir(parents=True, exist_ok=True)
        
        demo_file = work_path / "main.py"
        demo_file.write_text(RAY_DEMO_CODE, encoding='utf-8')
        print_success(f"Created: {demo_file}")
        
    except Exception as e:
        print_error(f"Failed to generate demo: {str(e)}")
        ctx.exit(1)
