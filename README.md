# label_image_new

本项目基于 LabelImg，并对 `libs` 目录中的部分功能进行了修改与增强。
如果已经安装过此软件，把环境中的labelimg-master或者labelimg文件夹更换成本文件夹中所有文件，再运行以下命令。

本代码已经安装编译`resources.qrc`以及打包过`exe`文件，如需在不同笔记本上环境上进行重新编译，请先下载 zip 文件或者用 git 拉取仓库，再删除`dist`文件夹，重新按照以下方式在cmd中运行命令即可。


---

## 📦 使用说明（Windows）

请参考以下步骤进行安装与运行。

---

## 1️⃣ 安装依赖

请依次安装以下组件：

- **Python（Windows）**  
  https://www.python.org/downloads/windows/

- **PyQt5（推荐）**  
  https://www.riverbankcomputing.com/software/pyqt/download5

- **lxml**  
  http://lxml.de/installation.html

```
推荐下载python3.10以上版本
以及
pip install PyQt5 lxml
```

---

## 2️⃣ 进入项目目录

打开 **cmd**，切换到项目目录，例如：

```shell
cd E:\env\conda\labelimg\labelImg-master

3️⃣ 编译资源文件（必须步骤）

项目依赖 Qt 资源文件，请确保已存在 resources.qrc。

🔹 如果使用 PyQt4：
pyrcc4 -o libs/resources.py resources.qrc

🔹 如果使用 PyQt5（推荐）：
pyrcc5 -o libs/resources.py resources.qrc

```
---

4️⃣ 运行程序
```bash
基本运行：
python labelImg.py

指定图片与预定义类别文件：
python labelImg.py [IMAGE_PATH] [PRE-DEFINED CLASS FILE]
```

---

5️⃣（可选）打包为 EXE

若需要打包为独立可执行文件：
```bash
安装 pyinstaller：
pip install pyinstaller

执行打包命令：
pyinstaller --hidden-import=pyqt5 --hidden-import=lxml -F -n "labelImg" -c labelImg.py -p ./libs -p ./
```

打包完成后，会在 dist/ 目录看到生成的 labelImg.exe。

tips:
1.如果发现下拉框中选项不正确或者缺少，请直接修改\data文件中的
accident.txt（可能导致的事故类型）
risk.txt（风险隐患类型）
scene.txt（施工场景）
