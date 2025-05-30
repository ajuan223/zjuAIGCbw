# 项目说明   
## 项目简介  
本项目是一个基于 PyQt5 的图形界面应用，支持模型参数/超参数的读取与展示，并可显示模型评估相关图片。界面通过 uit.py 生成，支持多线程操作和超时终止。  
主要功能  
- 通过下拉框选择不同模型，自动加载对应参数、超参数和评估图片
- 参数和超参数分别显示在表格和文本框中
- 支持多线程读取数据，10 秒内未完成可自动终止
- 图形界面友好，所有控件均通过 Qt Designer 设计  

## 目录结构

    ├── main.py                # 主程序入口
    ├── uit.py                 # Qt Designer 生成的 UI 文件
    ├── classify/
    │   ├── train/
    │   │   ├── para.txt
    │   │   ├── args.yaml
    │   │   └── roc_curves.png
    │   ├── train2/
    │   │   ├── para2.txt
    │   │   ├── args.yaml
    │   │   └── roc_curves.png
    │   └── train3/
    │       ├── para3.txt
    │       ├── args.yaml
    │       └── roc_curves.png

## 环境依赖
- Python 3.7+
- PyQt5
- pyyaml

## 使用方法  
运行 main.py 启动程序：  
python main.py  
在界面中选择模型，点击“锁定”按钮，自动加载并显示参数、超参数和评估图片。  
## 注意事项  
参数/超参数文件和图片需按目录结构放置，否则会读取失败。  
若需自定义 UI，请用 Qt Designer 修改 .ui 文件并用 pyuic5 生成 uit.py。  
## 联系方式  
如有问题请提交 issue 或联系开发者。
