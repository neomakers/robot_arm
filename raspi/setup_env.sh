#!/bin/bash

# 获取当前脚本的绝对路径
SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REQUIREMENTS_FILE="$SCRIPT_PATH/requirements.txt"
ENV_NAME="robot_env"

# 检查是否已安装 conda
if ! [ -x "$(command -v conda)" ]; then
  echo "Error: conda 未安装，请先运行 Miniforge 安装脚本。"
  exit 1
fi

# 使用完整路径调用 conda 初始化
eval "$(conda shell.bash hook)"

# 检查环境是否存在
EXISTING_ENVS=$(conda env list | awk '{print $1}' | grep -v '^#')

if echo "$EXISTING_ENVS" | grep -q "^$ENV_NAME$"; then
  echo "环境 '$ENV_NAME' 已存在。正在激活..."
else
  echo "环境 '$ENV_NAME' 不存在，正在创建..."
  conda create -n "$ENV_NAME" python=3.11 -y
fi

# 激活环境
conda activate "$ENV_NAME"

# 检查是否 requirements.txt 存在
if [ ! -f "$REQUIREMENTS_FILE" ]; then
  echo "⚠️ 错误：找不到 requirements.txt 文件！"
  echo "路径为: $REQUIREMENTS_FILE"
  exit 1
fi

# 安装依赖
echo "正在安装依赖..."
pip install -r "$REQUIREMENTS_FILE"

# 验证安装结果
echo ""
echo "✅ 环境 '$ENV_NAME' 已配置完成，当前安装的包列表："
pip list

# 可选：保持环境激活状态
exec bash --login