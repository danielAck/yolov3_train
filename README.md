# yolov3_train #

### Introduction

----------
借鉴了yolov3的Keras实现，源repo：https://github.com/qqwweee/keras-yolo3，[感谢qqwweee](https://github.com/qqwweee)

### How to Start ###

1. 准备自己的训练集，保存到 `img` 文件夹中，**注意：图片以ID命名** ，可参考 `img` 文件夹中的样例文件
2. 使用图片标注工具标注训练集，将生成的 **xml** 文件 保存到 `Annotations`文件夹中，同样可以参考文件夹中的样例文件，推荐使用 [labelImg](https://github.com/tzutalin/labelImg "labelImg")
3. 运行 `python label_convert.py`，将标注文件转换为生成anchors需要的文件，将会生成 `labels` 文件夹
4. 运行 `ptyhon gen_train.py` 生成训练需要的训练标注文件
5. 运行 `python my_gen_anchors.py` 生成anchors文件，保存在 `model_data` 文件夹中，其中包括 9 个anchor，参考文件夹中的 `yolo_anchors.txt`
6. 准备类别文件, 存放到 `model_data` 下，参考 `voc_classes.txt`，使用 **空格** 隔开
7. 运行 `python my_trian.py` 进行模型训练，最终生成权重文件，存放在生成的 `log` 文件夹下

### Detection ###

- **将**训练好的权重文件移动到 `model_data` 文件夹下，修改文件名为 **yolo_demo.h5**
- 运行 `python run_yolo.py` 启动图片检测模式
- 输入要检测的图片名

**HAVE FUN ！！！**