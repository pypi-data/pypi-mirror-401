# aggregate_analysis.py
import argparse
import json
import os
import subprocess  # 添加导入
from pathlib import Path
import glob

def aggregate_stack_data(input_dir, output_dir):
    """聚合所有节点的堆栈数据"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 收集所有节点的数据
    all_stack_files = []
    for node_dir in input_path.iterdir():
        if node_dir.is_dir() and node_dir.name.startswith('node_'):
            stack_files = list(node_dir.glob("*.json"))
            all_stack_files.extend(stack_files)
    
    print(f"找到 {len(all_stack_files)} 个堆栈数据文件")
    
    # 合并所有数据
    aggregated_data = []
    for stack_file in all_stack_files:
        try:
            with open(stack_file, 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    aggregated_data.extend(data)
                else:
                    aggregated_data.append(data)
        except Exception as e:
            print(f"读取文件 {stack_file} 失败: {e}")
    
    # 保存聚合数据
    aggregated_file = output_path / "aggregated_stack_data.json"
    with open(aggregated_file, 'w') as f:
        json.dump(aggregated_data, f, indent=2)
    
    print(f"聚合数据已保存到: {aggregated_file}")
    
    # 转换为原有格式以便分析
    convert_to_original_format(aggregated_data, output_path)
    
def convert_to_original_format(aggregated_data, output_path):
    """转换为原有.stackdata格式"""
    for i, data in enumerate(aggregated_data):
        if isinstance(data, list):
            # 如果是列表，处理每个元素
            for j, item in enumerate(data):
                filename = f"{i:05d}_{j:05d}.stackdata"
                filepath = output_path / filename
                with open(filepath, 'w') as f:
                    json.dump(item, f, indent=2)
        else:
            # 单个对象
            filename = f"{i:05d}.stackdata"
            filepath = output_path / filename
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
    
    print(f"已转换 {len(aggregated_data)} 个文件为原始格式")

def aggregate_gxdata(input_dir, output_dir):
    """聚合所有 .gxdata 文件，按 rank 顺序写入单个文件"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 收集所有 .gxdata 文件（包括子目录）
    gxdata_files = []
    for path in input_path.rglob("*.gxdata"):
        if path.is_file():
            gxdata_files.append(path)

    if not gxdata_files:
        print("未找到任何 .gxdata 文件")
        return

    # 按文件名前缀（rank）排序
    def get_rank_from_filename(filepath):
        name = filepath.name
        if '-' in name and name.endswith('.gxdata'):
            try:
                rank_str = name.split('-')[0]
                return int(rank_str)
            except ValueError:
                pass
        return float('inf')  # 无法解析的放最后

    gxdata_files.sort(key=get_rank_from_filename)

    # 合并内容
    aggregated_gxdata_file = output_path / "aggregated_gxdata.txt"
    with open(aggregated_gxdata_file, 'w') as out_f:
        for i, gx_file in enumerate(gxdata_files):
            if i > 0:
                out_f.write("\n" + "="*80 + "\n\n")  # 分隔不同 rank
            out_f.write(f"# Source: {gx_file}\n")
            try:
                with open(gx_file, 'r') as f:
                    out_f.write(f.read())
            except Exception as e:
                out_f.write(f"# ERROR: Failed to read {gx_file}: {e}\n")

    print(f"已聚合 {len(gxdata_files)} 个 .gxdata 文件到: {aggregated_gxdata_file}")
def main():
    parser = argparse.ArgumentParser(description="聚合分布式堆栈数据")
    parser.add_argument("--input-dir", default="/tmp/stack_data_all", help="输入目录（协调器的dump路径）")
    parser.add_argument("--output-dir", default="/tmp/stack_analysis", help="输出目录")
    
    args = parser.parse_args()
    
    # 确保输出目录存在
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 调用聚合函数
    # aggregate_stack_data(args.input_dir, args.output_dir)
    
    # 运行原有分析脚本    
    cmd = [
        "python3", "-m", "cluster.stack_processor",
        "--path", args.input_dir,
        "--output-dir", args.output_dir,
    ]
    
    print("运行堆栈分析...")
    result = subprocess.run(cmd)
    if result.returncode == 0:
        print("分析完成")
    else:
        print("分析失败")
        
    cmd = [
        "python3", "-m", "cluster.process_processor",
        "--dump-path", args.input_dir,
        "--output-dir", args.output_dir,
    ]
    
    print("运行堆栈分析...")
    result = subprocess.run(cmd)
    if result.returncode == 0:
        print("分析完成")
    else:
        print("分析失败")
    
    # 👇 新增：聚合 .gxdata 文件
    aggregate_gxdata(args.input_dir, args.output_dir)

if __name__ == "__main__":
    main()