#!/usr/bin/python3 sudo reboot Q

import time
import math
import smbus

class PCA9685:
    # 定义PCA9685芯片的寄存器地址常量
    __MODE1              = 0x00   # 模式控制寄存器1，用于设置基本操作模式
    __PRESCALE           = 0xFE   # 预分频寄存器，用于设置PWM频率
    __LED0_ON_L          = 0x06   # LED0_ON低字节寄存器，控制PWM开启时间的低位
    __LED0_ON_H          = 0x07   # LED0_ON高字节寄存器，控制PWM开启时间的高位
    __LED0_OFF_L         = 0x08   # LED0_OFF低字节寄存器，控制PWM关闭时间的低位
    __LED0_OFF_H         = 0x09   # LED0_OFF高字节寄存器，控制PWM关闭时间的高位
    
    
    def __init__(self, address=0x40, debug=False):
        """
        初始化类的构造函数。
        
        参数:
        - address: I2C通信地址，默认值为0x40。
        - debug: 是否开启调试模式，默认为False。
        
        该方法会初始化I2C通信，并设置设备的通信地址和调试模式。
        """
        # 初始化I2C通信总线
        self.bus = smbus.SMBus(1)
        # 设置设备的I2C通信地址
        self.address = address
        # 设置调试模式
        self.debug = debug
        # 向设备发送初始化设置，这里假设__MODE1是设备的一个配置寄存器，0x00是配置的数据
        self.write(self.__MODE1, 0x00)

    def write(self, reg, value):
        """
        向I2C设备上的指定寄存器写入特定值。

        此方法主要用于向I2C设备的特定寄存器写入数据，以设置或更新设备的配置或状态。

        参数:
        - reg: 要写入的寄存器地址。用于指定值应写入的配置或数据寄存器。
        - value: 要写入寄存器的值。用于设置或更新设备的配置或状态。

        返回:
        - None: 此方法不返回任何值；其目的是向I2C设备发送数据。
        """
        # 向I2C总线上的指定寄存器地址写入一个字节的数据
        self.bus.write_byte_data(self.address, reg, value)

    def read(self, reg):
        """
        从I2C设备的指定寄存器读取一个字节的数据。

        此方法用于从设备的特定寄存器中获取当前的配置值或状态信息。

        参数:
        - reg: 寄存器地址，指定要读取数据的寄存器位置。

        返回:
        - int: 从寄存器读取的一个字节数据（0~255）。
        """ 
        return self.bus.read_byte_data(self.address, reg)

    def setPWMFreq(self, freq):
        """
        设置PWM的频率
    
        参数:
        freq: 想要设置的PWM频率，单位为赫兹。
    
        返回值:
        无
        """
        # 计算预分频值，基于25MHz的时钟频率
        prescaleval = 25000000.0
        prescaleval /= 4096.0
        prescaleval /= float(freq)
        prescaleval -= 1.0
        # 四舍五入得到最终的预分频值
        prescale = math.floor(prescaleval + 0.5)
    
        # 读取当前的模式寄存器值
        oldmode = self.read(self.__MODE1)
        # 设置预分频模式
        newmode = (oldmode & 0x7F) | 0x10
        self.write(self.__MODE1, newmode)
        # 写入计算得到的预分频值
        self.write(self.__PRESCALE, int(prescale))
        # 恢复之前的模式
        self.write(self.__MODE1, oldmode)
        # 等待一段时间以确保设置生效
        time.sleep(0.005)
        # 重新启动设备以应用新的预分频值
        self.write(self.__MODE1, oldmode | 0x80)

    def setPWM(self, channel, on, off):
        """
        设置指定通道的PWM信号的开启和关闭时间。
    
        该方法通过向PWM控制器的相应寄存器写入数据来控制PWM信号的开启和关闭时间，
        从而控制与该通道相连的设备的运行状态。
    
        参数:
        - channel: PWM通道号，决定向哪个通道的LED控制器写入数据。
        - on: PWM信号的开启时间，表示PWM信号在一个周期内开始导通的时间点。
        - off: PWM信号的关闭时间，表示PWM信号在一个周期内停止导通的时间点。
    
        返回值:
        无
        """
        # 写入通道的开启时间低8位
        self.write(self.__LED0_ON_L + 4 * channel, on & 0xFF)
        # 写入通道的开启时间高8位
        self.write(self.__LED0_ON_H + 4 * channel, on >> 8)
        # 写入通道的关闭时间低8位
        self.write(self.__LED0_OFF_L + 4 * channel, off & 0xFF)
        # 写入通道的关闭时间高8位
        self.write(self.__LED0_OFF_H + 4 * channel, off >> 8)

    def setServoPulse(self, channel, pulse):
        """
        设置指定通道的伺服脉冲。
    
        该方法根据输入的脉冲值计算相应的PWM信号，并设置到指定的通道。
    
        参数:
        - channel: 通道号，指定哪个通道的伺服脉冲。
        - pulse: 伺服脉冲宽度（单位：微秒）。
    
        返回值:
        无
        """
        # 将脉冲宽度转换为50Hz的PWM信号所需的脉冲数
        pulse = pulse * 4096 / 20000  # 20ms -> 50Hz
        # 设置指定通道的PWM信号，其中0表示脉冲开始时的占空比，int(pulse)表示脉冲结束时的占空比
        self.setPWM(channel, 0, int(pulse))
    def angle_to_pulse(self, angle):
        """
        将角度转换为脉冲宽度。
    
        该方法接受一个角度值作为输入，并将其转换为相应的脉冲宽度值。
        脉冲宽度值用于控制伺服马达等设备的位置。
    
        参数:
        angle (int): 输入的角度值，应为 0 到 270 度之间的整数。
    
        返回:
        int: 转换后的脉冲宽度值，范围为 500 到 2500 微秒。
        """
        # 限制角度在 0 到 270 度之间，以确保在有效范围内
        angle = max(0, min(270, angle))
        # 计算脉冲宽度，将角度线性映射到脉冲宽度范围
        return 500 + (angle / 270.0) * 2000

    def set_servo_angle(self, channel, angle):
        """
        设置指定通道的舵机角度。
    
        将角度转换为脉冲宽度，然后使用转换后的脉冲宽度值设置舵机的转动角度。
    
        参数:
        channel (int): 舵机的通道号，用于指定要控制的舵机。
        angle (float): 想要设置的舵机角度，单位为度。
    
        返回:
        无
        """
        # 将角度转换为对应的脉冲宽度
        pulse = self.angle_to_pulse(angle)
        
        # 使用转换后的脉冲宽度设置舵机角度
        self.setServoPulse(channel, pulse)
def close_gripper(pwm:PCA9685):
    pwm.set_servo_angle(5, 135)  # 通道5 = 舵机6，设置为125°
    print("夹爪已闭合")
def open_gripper(pwm:PCA9685):
    pwm.set_servo_angle(5, 90)  # 通道5 = 舵机6，设置为125°
    print("夹爪已open")
# 慢速移动单个舵机
def slow_move_servo(pwm, channel, start_angle, end_angle, step=1, delay=0.1):
    if start_angle < end_angle:
        angle_range = range(start_angle, end_angle + 1, step)
    else:
        angle_range = range(start_angle, end_angle - 1, -step)

    for angle in angle_range:
        pwm.set_servo_angle(channel, angle)
        time.sleep(delay)    
# 慢速移动多个舵机
def slow_move_to_angles(pwm, current_angles, target_angles, step=1, delay=0.1):
    for i in range(len(target_angles)):
        slow_move_servo(pwm, i, current_angles[i], target_angles[i], step, delay)
    return target_angles  
def come_home_position(pwm, current_angles):
    target_angles = [135, 135, 150, 153, 135, 90]
    slow_move_to_angles(pwm, current_angles, target_angles)
    print("机械臂已移动到起始位置")
    return target_angles   
def move_aim_position_1(pwm, current_angles):
    target_angles = [135, 135, 80, 90, 135, 90]
    slow_move_to_angles(pwm, current_angles, target_angles)
    print("机械臂已移动到 aim 1位置")
    return target_angles
def move_aim_position_2(pwm, current_angles):
    target_angles = [200, 135, 80, 90, 135, 125]
    slow_move_to_angles(pwm, current_angles, target_angles)
    print("机械臂已移动到 aim 2位置")
    return target_angles
if __name__ == '__main__':
    pwm = PCA9685()
    pwm.setPWMFreq(50)
    current_angles = [135, 135, 150, 153, 135, 90]
    print("初始化完成，等待 2 秒")
    time.sleep(2)  # 延时2秒
    current_angles = move_aim_position_1(pwm, current_angles)
    print("识别到物块，开始夹取")
    # current_angles = come_home_position(pwm, current_angles)
    time.sleep(1)
    close_gripper(pwm)
    current_angles = move_aim_position_2(pwm, current_angles)
    print("到达目标位置，开始释放物块")
    open_gripper(pwm)
    print("任务完成开始返回")
    time.sleep(1)
    current_angles = come_home_position(pwm, current_angles)

