#!/bin/bash

# 检查是否已安装 conda
if ! [ -x "$(command -v conda)" ]; then
  echo "Error: conda 未安装，请先运行 Miniforge 安装脚本。"
  exit 1
fi

# 设置环境名称和项目路径
ENV_NAME="ai_robot_env"
PROJECT_DIR="/home/michael/ai_robot"

# 创建或更新环境
echo "正在创建或更新 conda 环境: $ENV_NAME"
conda create -n "$ENV_NAME" python=3.11 -y
conda init bash
source ~/.bashrc

# 安装基础依赖
echo "正在安装项目依赖..."
conda activate "$ENV_NAME"
pip3 install numpy pandas opencv-python torch

# 可选：进入项目目录并执行启动脚本
if [ -d "$PROJECT_DIR" ]; then
  cd "$PROJECT_DIR"
  echo "当前目录切换到项目根目录: $PROJECT_DIR"
  # 如果有 requirements.txt，可使用以下命令安装
  # pip install -r requirements.txt
fi

echo "✅ 环境 '$ENV_NAME' 已成功创建或更新！"