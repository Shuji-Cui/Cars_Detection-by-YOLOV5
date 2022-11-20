import cv2
import numpy as np
import math
import os
import pathlib

# img_path = "data/target_img/target_img.jpg"
# cut_path = "data/target_img/cut/"
# stitch_path = "data/target_img/stitched/"

def tif_to_jpg(img_path):
    """
    将tif转换为jpg
    """
    img_path = pathlib.Path(img_path)
    tif = cv2.imdecode(np.fromfile(str(img_path), dtype=np.uint8), -1)
    jpg_path = "data/target_img/jpg_process/" + str(img_path.stem) + ".jpg"
    cv2.imencode(".jpg", tif)[1].tofile(jpg_path)   # 转换为jpg格式输出
    return jpg_path

def cut(img_path, cut_path="data/target_img/cut/"):
    """
    对图像进行切割
    """

    # 删除cut目录下的之前保留内容
    priors = os.listdir(cut_path)
    if priors:
        for p in priors:
            os.remove(cut_path + p)

    # 切割大小为768*768
    cut_width = 768
    cut_length = 768

    img = cv2.imread(img_path)
    width, length, depth = img.shape  # 保存图像原有的shape

    # 初始化接受矩阵
    pic = np.zeros((cut_width, cut_length, depth))

    # 计算长宽各能裁剪多少,进一取整
    num_width = math.ceil(width / cut_width)
    num_length = math.ceil(length / cut_length)


    for i in range(0, num_width):
        for j in range(0, num_length):
            pic = img[i * cut_width:(i + 1) * cut_width, j * cut_length:(j + 1) * cut_length, :]
            save_path = cut_path + f"{i + 1}_{j + 1}.jpg"
            cv2.imwrite(save_path, pic)

    # 返回原始图片的尺寸信息
    return [width, length]


def stitch(detect_imgs_path, save_path, img0):
    """
    将切割识别后的图像合成为为一个图像
    img0:原始图片的尺寸信息
    """
    # 分割后的图片的文件夹，以及拼接后要保存的文件夹
    img_path = detect_imgs_path
    stitch_path = save_path
    # 数组保存分割后图片的列数和行数，注意分割后图片的格式为x_x.jpg，x从1开始
    num_width_list = []
    num_lenght_list = []
    # 读取文件夹下所有图片的名称
    picture_names = os.listdir(img_path)
    if len(picture_names) == 0:
        print("没有文件")

    else:
        # 获取原始图像的尺寸
        img0_width = int(img0[0])
        img0_length = int(img0[1])
        # 获取分割后图片的尺寸
        img_1_1 = cv2.imread(str(img_path / '1_1.jpg'))
        (width, length, depth) = img_1_1.shape
        # 分割名字获得行数和列数，通过数组保存分割后图片的列数和行数
        for picture_name in picture_names:
            num_width_list.append(int(picture_name.split("_")[0]))
            num_lenght_list.append(int((picture_name.split("_")[-1]).split(".")[0]))
        # 取长和宽的最大值
        num_width = max(num_width_list)
        num_length = max(num_lenght_list)
        # 预生成拼接后的图片
        splicing_pic = np.zeros((img0_width, img0_length, depth))
        # 循环复制
        for i in range(1, num_width + 1):
            for j in range(1, num_length + 1):
                img_part = cv2.imread(str(img_path / '{}_{}.jpg').format(i, j))
                splicing_pic[width * (i - 1): width * i, length * (j - 1): length * j, :] = img_part
        # 保存图片
        # cv2.imwrite(str(stitch_path / 'result.jpg'), splicing_pic)
        cv2.imencode('.jpg', splicing_pic)[1].tofile(str(stitch_path / 'result.jpg'))  # 中文路径适用
    pass


if __name__ == "__main__":
    img_path = "data/target_img/target_tif.tif"
    tif_to_jpg(img_path)
