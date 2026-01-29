# sysom_hang_analyzer.py
#!/usr/bin/env python3
# deploy_distributed_stack.py

import subprocess
import sys
import os
import argparse
import time
from pathlib import Path
import signal  # 添加 signal 模块导入

# 添加获取主机名的辅助函数
def get_hostname():
    """获取当前主机名"""
    try:
        result = subprocess.run(["hostname"], capture_output=True, text=True)
        return result.stdout.strip()
    except:
        return os.environ.get("HOSTNAME", "")

def check_logtail_process():
    """检查是否有ilogtail进程在运行"""
    try:
        # 使用更兼容的方式
        result = subprocess.run(["/usr/bin/pgrep", "ilogtail"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # print("DEBUG: pgrep ilogtail result: returncode={}, stdout={}, stderr={}".format(
        #     result.returncode, result.stdout.decode() if result.stdout else '', 
        #     result.stderr.decode() if result.stderr else ''))
        return result.returncode == 0
    except FileNotFoundError:
        # pgrep命令不存在
        print("DEBUG: pgrep command not found")
        return False
    except Exception as e:
        print("DEBUG: Error running pgrep ilogtail: {}".format(str(e)))
        return False

def get_logtail_config():
    """获取ilogtail配置参数"""
    # 从环境变量获取配置，提供默认值
    user_id = os.environ.get("LOGTAIL_USER_ID", "1616499932672407")
    user_defined_id = os.environ.get("LOGTAIL_USER_DEFINED_ID", "user-defined-1")
    return user_id, user_defined_id

def configure_logtail_user_identity():
    """配置ilogtail用户标识"""
    # 获取配置参数
    user_id, user_defined_id = get_logtail_config()
    
    # 配置用户标识目录
    user_dir = "/etc/ilogtail/users"
    os.makedirs(user_dir, exist_ok=True)
    user_file = os.path.join(user_dir, user_id)
    # 只创建空文件，不写入内容
    open(user_file, "w").close()
        
    # 配置用户自定义标识
    user_defined_file = "/etc/ilogtail/user_defined_id"
    
    try:
        # 检查文件是否存在且包含目标标识
        if os.path.exists(user_defined_file):
            with open(user_defined_file, "r") as f:
                current_content = f.read()
                
            # 检查目标标识是否已存在于文件中
            # 这里假设标识是按行存储的
            existing_ids = [line.strip() for line in current_content.splitlines() if line.strip()]
            
            if user_defined_id in existing_ids:
                # print("INFO: ilogtail user identity already configured, User ID: {}, Custom ID: {}".format(user_id, user_defined_id))
                return
                
            # 如果标识不存在，将其追加到文件中
            with open(user_defined_file, "a") as f:
                # 如果文件不为空且最后一行没有换行符，先添加换行符
                if current_content and not current_content.endswith('\n'):
                    f.write('\n')
                f.write(user_defined_id + '\n')
        else:
            # 文件不存在，创建并写入标识
            with open(user_defined_file, "w") as f:
                f.write(user_defined_id + '\n')
                
    except Exception as e:
        # 如果出现异常，尝试重新写入（保持原有行为）
        print("WARNING: Error checking or updating user defined identity: {}, rewriting configuration".format(str(e)))
        with open(user_defined_file, "w") as f:
            f.write(user_defined_id + '\n')
    
    #print("INFO: ilogtail user identity configuration completed, User ID: {}, Custom ID: {}".format(user_id, user_defined_id))

def install_and_configure_logtail(region_id, network_mode="internal"):
    """安装并配置ilogtail日志收集组件"""
    print("INFO: Starting to install ilogtail, Region: {}, Network Mode: {}".format(region_id, network_mode))
    
    # 下载logtail安装脚本
    if network_mode == "internal":
        download_url = "http://logtail-release-{}.oss-{}-internal.aliyuncs.com/linux64/logtail.sh".format(region_id, region_id)
    else:
        download_url = "http://logtail-release-{}.oss-{}.aliyuncs.com/linux64/logtail.sh".format(region_id, region_id)
    
    # 下载安装脚本
    cmd_wget = ["wget", download_url, "-O", "logtail.sh"]
    result = subprocess.run(cmd_wget)
    if result.returncode != 0:
        print("ERROR: Failed to download logtail.sh")
        return result.returncode
    
    # 添加执行权限
    os.chmod("logtail.sh", 0o755)
    
    # 安装logtail
    install_suffix = "{}-{}".format(region_id, network_mode) if network_mode != "internal" else region_id
    cmd_install = ["./logtail.sh", "install", install_suffix]
    result = subprocess.run(cmd_install)
    if result.returncode != 0:
        print("ERROR: Failed to install logtail")
        return result.returncode
    
    # 配置用户标识
    configure_logtail_user_identity()
    
    print("INFO: ilogtail installation and configuration completed")
    return 0

def setup_logtail_if_needed(region_id, network_mode):
    """检查并设置ilogtail"""
    if check_logtail_process():
        print("INFO: Detected ilogtail process is running, configuring user identity...")
        configure_logtail_user_identity()
    else:
        print("INFO: No ilogtail process detected, starting installation...")
        install_and_configure_logtail(region_id, network_mode)

def install_gx_if_needed():
    """在 Debian/Ubuntu 系统上安装 gx 的 .deb 包（如果存在）"""
    # 仅在 Debian/Ubuntu 上尝试
    if not os.path.exists('/etc/debian_version'):
        return False

    try:
        # 假设 gx deb 在 cluster/ 子目录中（与当前脚本同级）
        cluster_dir = os.path.dirname(os.path.abspath(__file__))
        deb_files = [
            f for f in os.listdir(cluster_dir)
            if f.startswith('gx_') and f.endswith('.deb')
        ]
        
        if not deb_files:
            print("INFO: 未在 cluster/ 目录下找到 gx_*.deb，跳过安装")
            return False
        
        gx_deb_path = os.path.join(cluster_dir, deb_files[0])
        print(f"INFO: 发现 gx deb 包: {gx_deb_path}")
        
        # 安装
        result = subprocess.run(['sudo', 'dpkg', '-i', gx_deb_path], 
                               capture_output=True, text=True)
        if result.returncode == 0:
            print("INFO: gx 已成功安装")
            return True
        else:
            print(f"WARNING: dpkg 安装失败，尝试修复依赖...")
            fix_result = subprocess.run(['sudo', 'apt-get', 'install', '-f', '-y'],
                                      capture_output=True, text=True)
            if fix_result.returncode == 0:
                print("INFO: 依赖修复成功，gx 可能已安装")
                return True
            else:
                print(f"ERROR: 依赖修复失败: {fix_result.stderr}")
                return False
                
    except Exception as e:
        print(f"WARNING: 安装 gx 失败: {e}")
        return False
def setup_all_nodes(region_id=None, network_mode="internet", coordinator_host=None, 
                   coordinator_port=8080, dump_path="/tmp/stack_data_all",
                   monitor_threshold_minutes=5, monitor_log_files=None):
    """在所有节点上设置完整的hang analyzer环境"""
    # 设置默认的日志文件路径
    if monitor_log_files is None:
        monitor_log_files = ["/out.log", "/err.log"]
        
    # 获取当前节点角色
    hostname = get_hostname()
    master_addr = coordinator_host or os.environ.get("MASTER_ADDR", "")
    
    if not master_addr:
        print("错误: 必须提供MASTER_ADDR或设置相应环境变量")
        return 1
    
    # 👇 新增：尝试安装 gx 工具
    install_gx_if_needed()
    
     # 检查并设置ilogtail
    setup_logtail_if_needed(region_id, network_mode)
    
    # # 在所有节点上安装ilogtail
    # if region_id:
    #     logtail_result = install_logtail(region_id, network_mode)
    #     if logtail_result != 0:
    #         print("警告: ilogtail安装失败")
    
    # 判断是否为主节点：支持多节点（hostname匹配）和单节点（localhost/127.0.0.1）
    is_master = (
        hostname == master_addr or
        master_addr in ("localhost", "127.0.0.1", "::1")
    )
    # 部署协调器（仅在master节点）
    if is_master:
        print("在master节点部署协调器...")
        deploy_coordinator(master_addr, coordinator_port, dump_path)
        # 启动日志监控
        start_log_monitor(
            log_files=monitor_log_files,
            coordinator_host=master_addr,
            coordinator_port=coordinator_port,
            daemon=True,
            threshold_minutes=monitor_threshold_minutes,
            analysis_base_path=dump_path.replace("stack_data_all", "stack_analysis"),
            input_dir=dump_path
        )
    
    # 创建后台重试脚本
    retry_script = f'''#!/bin/bash
for i in {{1..500}}; do
    sysom-hang-analyzer node-agent {master_addr} {coordinator_port}
    if [ $? -eq 0 ]; then
        echo "节点代理启动成功"
        break
    else
        echo "节点代理启动失败，${{i}}分钟后重试..."
        if [ $i -lt 500 ]; then
            sleep 60
        else
            echo "警告: 节点代理启动失败，已达最大重试次数"
        fi
    fi
done
'''
    
    # 写入临时脚本文件并后台执行
    with open("/tmp/retry_node_agent.sh", "w") as f:
        f.write(retry_script)
    
    os.chmod("/tmp/retry_node_agent.sh", 0o755)
    
    # 后台执行重试脚本
    with open("/tmp/setup_node_agent.log", "w") as log_file:
        subprocess.Popen(["/tmp/retry_node_agent.sh"], 
                        stdout=log_file, stderr=log_file, 
                        start_new_session=True)
    
    print("节点代理重试脚本已在后台启动，日志: /tmp/setup_node_agent.log")
    return 0

def deploy_coordinator(host="0.0.0.0", port=8080, dump_path="/tmp/stack_data_all"):
    """部署协调器（在主节点上运行）"""
    print(f"部署协调器: {host}:{port}")
    
    cmd = [
        "python3", "-m", "cluster.distributed_coordinator",
        "--host", str(host),
        "--port", str(port),
        "--dump-path", dump_path
    ]
    
    with open("/tmp/coordinator.log", "w") as log_file:
        process = subprocess.Popen(cmd, stdout=log_file, stderr=log_file)
    
    # 检查进程是否仍在运行
    if process.poll() is None:
        print("协调器已启动，日志: /tmp/coordinator.log")
        return 0
    else:
        print(f"协调器启动失败，退出码: {process.returncode}")
        print("请检查日志: /tmp/coordinator.log")
        return process.returncode

def deploy_node_agent(coordinator_host=None, coordinator_port=8080, node_id=None, dump_path="/tmp/stack_data"):
    """部署节点代理（在每个训练节点上运行）"""
    # 如果没有提供coordinator_host，则尝试从环境变量获取
    if not coordinator_host:
        coordinator_host = os.environ.get("MASTER_ADDR")
        
    if not coordinator_host:
        print("错误: 必须提供协调器主机地址")
        return 1
    
    print(f"部署节点代理，连接到: {coordinator_host}:{coordinator_port}")
    
    cmd = [
        "python3", "-m", "cluster.node_agent",
        "--coordinator-host", coordinator_host,
        "--coordinator-port", str(coordinator_port),
        "--dump-path", dump_path
    ]
    
    if node_id:
        cmd.extend(["--node-id", node_id])
    
    # 启动后台进程并记录日志
    with open("/tmp/node_agent.log", "w") as log_file:
        process = subprocess.Popen(cmd, stdout=log_file, stderr=log_file)
    
    # 等待一小段时间检查初始状态
    time.sleep(3)
    
    # 检查进程是否仍在运行
    if process.poll() is None:
        print("节点代理已启动，日志: /tmp/node_agent.log")
        return 0
    else:
        print(f"节点代理启动失败，退出码: {process.returncode}")
        print("请检查日志: /tmp/node_agent.log")
        return process.returncode

def trigger_collection(coordinator_host=None, coordinator_port=8080):
    """触发采集"""
     # 如果没有提供coordinator_host，则尝试从环境变量获取
    if not coordinator_host:
        coordinator_host = os.environ.get("MASTER_ADDR")
        
    if not coordinator_host:
        print("错误: 必须提供协调器主机地址")
        return 1
    
    print("触发分布式堆栈采集...")
    
    cmd = [
        "python3", "-m", "cluster.trigger_distributed_collection",
        "--coordinator-host", coordinator_host,
        "--coordinator-port", str(coordinator_port)
    ]
    
    result = subprocess.run(cmd)
    return result.returncode

# sysom_hang_analyzer.py 中的相关部分
def start_log_monitor(log_files=None, coordinator_host=None, coordinator_port=8080, 
                     check_interval=60, threshold_minutes=5, daemon=False, trigger_mode="continuous",
                     analysis_base_path="/tmp/stack_analysis",
                     input_dir="/tmp/stack_data_all"):
    """启动日志监控守护进程"""
    # 如果没有提供coordinator_host，则尝试从环境变量获取
    if not coordinator_host:
        coordinator_host = os.environ.get("MASTER_ADDR")
        
    if not coordinator_host:
        print("错误: 必须提供协调器主机地址")
        return 1
    
    print("启动日志监控守护进程...")
    
    cmd = [
        "python3", "-m", "cluster.log_monitor_daemon",
        "--coordinator-host", coordinator_host,
        "--coordinator-port", str(coordinator_port),
        "--check-interval", str(check_interval),
        "--threshold-minutes", str(threshold_minutes),
        "--trigger-mode", trigger_mode,
        "--analysis-base-path", analysis_base_path,
        "--input-dir", input_dir
    ]
    
    # 添加日志文件参数
    if log_files:
        cmd.append("--log-files")
        cmd.extend(log_files)
    else:
        cmd.extend(["--log-files", "/out.log", "/err.log"])
    
    # 添加可选参数
    if daemon:
        cmd.append("--daemon")
    
    printable_cmd = " ".join([f"'{arg}'" if " " in arg or arg == "" else arg for arg in cmd])
    print(f"执行命令: {printable_cmd}")
    
    if daemon:
        # 后台运行模式
        process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"日志监控守护进程已在后台启动 (PID: {process.pid})")
        print("日志文件: /tmp/stack_log_monitor.log")
    else:
        # 前台运行模式
        result = subprocess.run(cmd)
        return result.returncode

def find_latest_collection_dir(base_dir):
    """
    在基础目录中查找最新的 collection 目录
    
    Args:
        base_dir: 基础目录路径
        
    Returns:
        最新 collection 目录的路径，如果没有找到则返回 None
    """
    base_path = Path(base_dir)
    if not base_path.exists():
        return None
    
    # 查找所有以 collection_ 开头的目录
    collection_dirs = []
    for item in base_path.iterdir():
        if item.is_dir() and item.name.startswith("collection_"):
            try:
                # 解析新的日期时间格式: collection_YYYYMMDD_HHMMSS
                date_part = item.name.split("_")[1]  # YYYYMMDD
                time_part = item.name.split("_")[2]  # HHMMSS
                
                # 组合成可排序的字符串: YYYYMMDDHHMMSS
                sortable_timestamp = date_part + time_part
                collection_dirs.append((sortable_timestamp, item))
            except (ValueError, IndexError):
                # 忽略无法解析的目录名
                continue
    
    # 按时间戳排序，返回最新的
    if collection_dirs:
        collection_dirs.sort(key=lambda x: x[0], reverse=True)
        return collection_dirs[0][1]
    
    return None
def aggregate_analysis(input_dir="/tmp/stack_data_all", output_dir="/tmp/stack_analysis"):
    """聚合分析"""
    # 确保基础输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 总是尝试查找最新的 collection 目录（如果输入路径存在且包含collection目录）
    actual_input_dir = input_dir
    latest_dir = find_latest_collection_dir(input_dir)
    if latest_dir:
        actual_input_dir = str(latest_dir)
        print(f"使用最新的采集目录: {actual_input_dir}")
        # 创建对应采集目录名称的输出子目录
        collection_name = os.path.basename(actual_input_dir)
        actual_output_dir = os.path.join(output_dir, collection_name)
    else:
        print(f"未找到采集目录，使用指定目录: {input_dir}")
        # 如果指定了输入目录，也创建对应的子目录
        collection_name = os.path.basename(os.path.normpath(input_dir))
        actual_output_dir = os.path.join(output_dir, collection_name)
    
    # 确保实际输出目录存在
    os.makedirs(actual_output_dir, exist_ok=True)
    
    print(f"聚合分析数据: {actual_input_dir} -> {actual_output_dir}")
    
    cmd = [
        "python3", "-m", "cluster.aggregate_analysis",
        "--input-dir", actual_input_dir,
        "--output-dir", actual_output_dir
    ]
    
    result = subprocess.run(cmd)
    return result.returncode

def stop_all_services(coordinator_host=None, coordinator_port=8080):
    """停止所有 cluster 相关服务"""
    if not coordinator_host:
        coordinator_host = os.environ.get("MASTER_ADDR")
        
    if not coordinator_host:
        print("错误: 必须提供协调器主机地址")
        return 1
    
    # 获取当前主机名
    hostname = get_hostname()
    
    print("正在停止 cluster 相关服务...")
    
    # 如果当前节点是主节点，则通过协调器通知所有节点停止
    if hostname == coordinator_host:
        try:
            import urllib.request
            import json
            
            url = f"http://{coordinator_host}:{coordinator_port}/stop-all"
            data = json.dumps({}).encode()
            req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
            response = urllib.request.urlopen(req, timeout=10)
            result = json.loads(response.read().decode())
            print(f"已通知协调器停止所有节点服务: {result}")
        except Exception as e:
            print(f"通过协调器停止服务失败: {e}")
        
        # 主节点还需要停止协调器本身
        processes = [
            "cluster.distributed_coordinator",
            "cluster.log_monitor_daemon"
        ]
    else:
        # 非主节点只需要停止自己的节点代理
        processes = [
            "cluster.node_agent"
        ]
    
    # 查找并停止相关的进程
    for process_name in processes:
        try:
            # 使用 pgrep 查找进程ID
            result = subprocess.run(["pgrep", "-f", process_name], 
                                  capture_output=True, text=True)
            if result.stdout:
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    if pid:
                        os.kill(int(pid), signal.SIGTERM)
                        print(f"已发送终止信号给进程 {process_name} (PID: {pid})")
        except Exception as e:
            print(f"停止进程 {process_name} 时出错: {e}")
    
    print("cluster 相关服务停止命令已发送")
    return 0

def show_help():
    """显示帮助"""
    print("用法: sysom-hang-analyzer [选项]")
    print("选项:")
    print("  coordinator [host] [port] [dump_path]  - 部署协调器")
    print("  node-agent [coordinator_host] [port] [node_id] [dump_path] - 部署节点代理")
    print("  trigger [coordinator_host] [port]     - 触发采集")
    print("  log-monitor [coordinator_host] [port] [--log-files file1 file2] [--daemon] [--trigger-mode MODE] [--check-interval] [--threshold-minutes] [--analysis-base-path PATH] - 启动日志监控")
    print("    MODE: continuous=持续触发(默认), once=只触发一次")
    print("  aggregate [input_dir] [output_dir]     - 聚合分析 (默认从 /tmp/stack_data_all 中查找最新采集目录)")
    print("  setup-all [region_id] [network_mode] [coordinator_host] [port] [dump_path] [threshold_minutes] [log_files...] - 在所有节点上设置完整的hang analyzer环境")
    print("  stop-all [coordinator_host] [port]     - 停止所有服务")
    print("  help                                  - 显示此帮助")

def parse_log_monitor_args(args):
    """解析log-monitor命令的参数"""
    coordinator_host = None
    coordinator_port = 8080
    log_files = None
    daemon = False
    trigger_mode = "continuous"
    check_interval = 60
    threshold_minutes = 5
    analysis_base_path = "/tmp/stack_analysis"
    
    i = 0
    while i < len(args):
        arg = args[i]
        if not arg.startswith("--"):
            # 位置参数
            if coordinator_host is None:
                coordinator_host = arg
            elif coordinator_port == 8080:  # 默认值
                try:
                    coordinator_port = int(arg)
                except ValueError:
                    print(f"错误: 端口号必须是整数，得到: {arg}")
                    return None
        else:
            # 选项参数
            if arg == "--log-files":
                log_files = []
                i += 1
                while i < len(args) and not args[i].startswith("--"):
                    log_files.append(args[i])
                    i += 1
                continue
            elif arg == "--daemon":
                daemon = True
            elif arg == "--trigger-mode":
                if i + 1 < len(args):
                    if args[i + 1] in ["continuous", "once"]:
                        trigger_mode = args[i + 1]
                        i += 1
                    else:
                        print(f"错误: trigger-mode 必须是 continuous 或 once，得到: {args[i + 1]}")
                        return None
                else:
                    print("错误: --trigger-mode 需要一个值")
                    return None
            elif arg == "--check-interval":
                if i + 1 < len(args):
                    try:
                        check_interval = int(args[i + 1])
                        i += 1
                    except ValueError:
                        print(f"错误: check-interval 必须是整数，得到: {args[i + 1]}")
                        return None
                else:
                    print("错误: --check-interval 需要一个值")
                    return None
            elif arg == "--threshold-minutes":
                if i + 1 < len(args):
                    try:
                        threshold_minutes = int(args[i + 1])
                        i += 1
                    except ValueError:
                        print(f"错误: threshold-minutes 必须是整数，得到: {args[i + 1]}")
                        return None
                else:
                    print("错误: --threshold-minutes 需要一个值")
                    return None
            elif arg == "--analysis-base-path":
                if i + 1 < len(args):
                    analysis_base_path = args[i + 1]
                    i += 1
                else:
                    print("错误: --analysis-base-path 需要一个值")
                    return None
        i += 1
    
    return {
        'coordinator_host': coordinator_host,
        'coordinator_port': coordinator_port,
        'log_files': log_files,
        'daemon': daemon,
        'trigger_mode': trigger_mode,
        'check_interval': check_interval,
        'threshold_minutes': threshold_minutes,
        'analysis_base_path': analysis_base_path
    }

def main():
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1]
    result = 0
    
    if command == "coordinator":
        host = sys.argv[2] if len(sys.argv) > 2 else "0.0.0.0"
        port = int(sys.argv[3]) if len(sys.argv) > 3 else 8080
        dump_path = sys.argv[4] if len(sys.argv) > 4 else "/tmp/stack_data_all"
        result = deploy_coordinator(host, port, dump_path)
    elif command == "node-agent":
        coordinator_host = sys.argv[2] if len(sys.argv) > 2 else None
        coordinator_port = int(sys.argv[3]) if len(sys.argv) > 3 else 8080
        node_id = sys.argv[4] if len(sys.argv) > 4 else None
        dump_path = sys.argv[5] if len(sys.argv) > 5 else "/tmp/stack_data"
        result = deploy_node_agent(coordinator_host, coordinator_port, node_id, dump_path)
    elif command == "trigger":
        coordinator_host = sys.argv[2] if len(sys.argv) > 2 else None
        coordinator_port = int(sys.argv[3]) if len(sys.argv) > 3 else 8080
        result = trigger_collection(coordinator_host, coordinator_port)
    elif command == "log-monitor":
        # 解析log-monitor的参数
        log_monitor_args = parse_log_monitor_args(sys.argv[2:])
        if log_monitor_args is not None:
            result = start_log_monitor(**log_monitor_args)
        else:
            result = 1
    elif command == "aggregate":
        # input_dir 默认为 /tmp/stack_data_all
        # output_dir 默认为 /tmp/stack_analysis
        input_dir = sys.argv[2] if len(sys.argv) > 2 else "/tmp/stack_data_all"
        output_dir = sys.argv[3] if len(sys.argv) > 3 else "/tmp/stack_analysis"
        result = aggregate_analysis(input_dir, output_dir)
    elif command == "setup-all":
        region_id = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("REGION")
        network_mode = sys.argv[3] if len(sys.argv) > 3 else "internal"
        coordinator_host = sys.argv[4] if len(sys.argv) > 4 else None
        coordinator_port = int(sys.argv[5]) if len(sys.argv) > 5 else 8080
        dump_path = sys.argv[6] if len(sys.argv) > 6 else "/tmp/stack_data_all"
        monitor_threshold_minutes = int(sys.argv[7]) if len(sys.argv) > 7 else 5
        # 处理多个日志文件参数
        monitor_log_files = None
        if len(sys.argv) > 8:
            monitor_log_files = sys.argv[8:]
        result = setup_all_nodes(region_id, network_mode, coordinator_host, coordinator_port, dump_path,
                   monitor_threshold_minutes, monitor_log_files)
    elif command == "stop-all":
        coordinator_host = sys.argv[2] if len(sys.argv) > 2 else None
        coordinator_port = int(sys.argv[3]) if len(sys.argv) > 3 else 8080
        result = stop_all_services(coordinator_host, coordinator_port)
    else:
        show_help()
        
    return result

if __name__ == "__main__":
    sys.exit(main())