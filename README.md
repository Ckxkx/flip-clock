# 翻页时钟 (Flip Clock)

[English](#flip-clock) | [中文](#翻页时钟-flip-clock)

你还在为电脑无法显示时间而烦恼吗？你还在为新年朋友圈没有新年倒计时而烦恼吗？现在都不是问题啦！一个现代化的桌面翻页时钟应用，支持全屏显示、时区切换、日历查看等功能，它诞生了！

## 功能特点

- 全屏显示的数字时钟
- 黑色背景，优雅的白色字体
- 支持时区切换
- 内置日历功能
- 中英文界面切换
- 点击屏幕显示/隐藏控制面板
- 按ESC键退出程序

## 安装方法

### 方法1：直接下载可执行文件（推荐）

1. 从 [Releases](https://github.com/ckxkx/flip-clock/releases) 页面下载最新版本的可执行文件
2. 双击运行 `FlipClock.exe`

### 方法2：通过pip安装

```bash
pip install flip-clock-desktop
```

安装完成后，可以通过命令行运行：
```bash
flip-clock
```

### 方法3：从源码安装

1. 克隆仓库：
   ```bash
   git clone https://github.com/ckxkx/flip-clock.git
   cd flip-clock
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 运行程序：
   ```bash
   python flip_clock.py
   ```

## 使用说明

1. 基本操作：
   - 点击屏幕任意位置：显示/隐藏控制面板
   - 按ESC键：退出程序

2. 控制面板功能：
   - 时区选择：可以切换不同时区的时间显示
   - 日历查看：查看日历并选择日期
   - 语言切换：支持中英文界面切换

## 开发说明

如果您想参与开发，可以按照以下步骤进行：

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 打包说明

1. 安装PyInstaller：
   ```bash
   pip install pyinstaller
   ```

2. 运行打包脚本：
   ```bash
   python build.py
   ```

3. 打包后的文件将在 `dist` 目录中生成

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

# Flip Clock

Are you still troubled by your computer's inability to display time? Are you still worried about not having a New Year's countdown for your social media? Now these are no longer problems! A modern desktop flip clock application with support for fullscreen display, timezone switching, calendar viewing, and more has arrived!

## Features

- Fullscreen digital clock display
- Black background with elegant white font
- Timezone switching support
- Built-in calendar functionality
- Chinese/English interface switching
- Click screen to show/hide control panel
- Press ESC to exit

## Installation

### Method 1: Download Executable (Recommended)

1. Download the latest version from the [Releases](https://github.com/ckxkx/flip-clock/releases) page
2. Double-click `FlipClock.exe` to run

### Method 2: Install via pip

```bash
pip install flip-clock-desktop
```

After installation, run from command line:
```bash
flip-clock
```

### Method 3: Install from Source

1. Clone repository:
   ```bash
   git clone https://github.com/ckxkx/flip-clock.git
   cd flip-clock
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run program:
   ```bash
   python flip_clock.py
   ```

## Usage

1. Basic Operations:
   - Click anywhere on screen: Show/hide control panel
   - Press ESC: Exit program

2. Control Panel Features:
   - Timezone Selection: Switch between different timezone displays
   - Calendar View: View and select dates
   - Language Switch: Toggle between Chinese and English interfaces

## Development

If you want to contribute to development, follow these steps:

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Packaging

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Run packaging script:
   ```bash
   python build.py
   ```

3. The packaged file will be generated in the `dist` directory

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details 