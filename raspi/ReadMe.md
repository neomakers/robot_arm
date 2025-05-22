1. ssh远程链接
    代开终端
    ```shell
    kai@192.168.1.102
    ```
2. 配置VNC虚拟桌面，端口等
    ```shell
    sudo raspi-config
    ```
    选择`3 Interface Options`
    - VNC
    - I2C
    - SPI
    - remote-GPIO
3. 首先安装anaconda,运行
    ```shell
    bash install_anaconda.sh
    ```
4. 安装运行环境
    ```shell
    bash setup_env.sh
    ```
