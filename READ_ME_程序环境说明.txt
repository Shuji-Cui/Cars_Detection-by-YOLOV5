---------------注意事项---------------
1. 需要启动系统界面时，通过Python运行qt_runtime.py文件即可。
2. 不要对文件内容做修改。

---------------运行所需第三方库---------------
pytorch
pyqt5
numpy
pathlib
openpyxl
gdal
cython
matplotlib
opencv-python
pillow
pyyaml
requests
scipy
tqdm
tensorboard
pandas
seaborn
thop

---------------文件夹说明---------------
文件夹名                             内容说明
data		          存放最终的检测结果；data\target_img中放有两张示例遥感影像，可以在程序运行时作为输入。
datasets                             包含自制的训练数据集和验证数据集。
models		          包含模型训练以及模型进行汽车目标识别时调用的各种库。
runs		          包含识别过程产生的影像以及识别使用的模型。
utils		          包含模型进行汽车目标识别时调用的各种库。

---------------Python文件说明---------------
文件名                                内容说明
__init__.py                          程序运行初始化文件。
coord_trans.py                  包含像素坐标转换为地理坐标相关功能。
demo2.py	          系统界面的UI设计以及系统的底层实现。
detect.py                           调用模型进行汽车目标识别的主要功能实现。
final_version.py                  对输入遥感影像进行汽车识别的过程进行整合。
pic_process.py                   对输入的遥感影像进行处理。
qt_runtime.py                    系统界面启动文件。
train.py                              模型训练主文件。
val.py                                 模型训练相关库文件。
export.py                           模型训练相关库文件。



