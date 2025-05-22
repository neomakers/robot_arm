#!/bin/bash

# 检查 conda 是否已经安装
if command -v conda &>/dev/null; then
  echo "✅ Conda 已安装，跳过安装步骤。"
else
  echo "🔄 开始安装 Miniforge..."

  # 创建并进入 config 目录
  cd ~/Desktop/
  mkdir -p config
  cd config

  # 下载并安装 Miniforge
  wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-aarch64.sh
  bash Miniforge3-Linux-aarch64.sh

  # 加载环境变量
  source ~/.bashrc

  # 清理临时目录
  rm -rf ~/Desktop/config

  echo "✅ Miniforge 安装完成。"
fi

# 安装系统依赖（始终执行）
sudo apt update
sudo apt install -y libcap-dev

echo "✅ 环境准备完成。"
