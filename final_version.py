import os.path


import json
import detect
import pic_process
import coord_trans


def run_detection(tif_path):

    # 输入必要参数
    config = {
        "img_path": tif_path,  # 在此处输入影像的路径
        "name": "结果输出",  # 保存的文件夹名称

    }


    # 输出要素展示
    # ##############################代码运行############################# #

    # tif to jpg
    # print("--------正在转换影像...--------")
    yield "正在转换影像...\n"
    jpg_path = pic_process.tif_to_jpg(config["img_path"])


    # 影像分割
    # print("--------正在切割影像...--------")
    yield "正在切割影像...\n"
    img0 = pic_process.cut(
        img_path=jpg_path
    )


    # yolov5检测部分
    # print("--------开始检测算法，车辆检测中...--------")
    yield "开始检测算法，车辆检测中...\n"
    opt = detect.parse_opt()
    detect_output = detect.main(opt)
    yield detect_output['output_str']

    # print("--------正在输出结果...--------")
    yield "\n正在输出结果...\n"
    # 生成保存的文件夹
    save_path = coord_trans.increment_path(
        name=config["name"]  # 保存的文件名称
    )

    # 将检测后的图像合成
    pic_process.stitch(detect_output['imgs_path'], save_path, img0)

    # 建立一个xlxs
    wb = coord_trans.creat_wb()

    # 读取json
    with open("data/coords_output/process/js.json") as f:
        coord_dic = json.load(f)
    i = 2  # 坐标开始从第二行添加
    for key, value in coord_dic.items():
        idx = key
        for coord_pixel in value:
            xgeo, ygeo = coord_trans.coord_transor(idx, coord_pixel, tif_path)
            coord_trans.coord_output(wb, xgeo, ygeo, i)
            i += 1

    # 保存xlxs
    coords_path = save_path / "坐标数据.xlsx"
    wb.save(coords_path)

    # 编写说明文档
    with open(save_path / "说明.txt", "w") as f:
        f.write("#############################\n"
                "xlsx文档：记录影像中所有车辆的投影坐标系地理坐标。\n"
                "         xge：x轴坐标\n"
                "         ygo：y轴坐标\n"
                "\n"
                "#############################\n"
                "result.jpg：车辆检测后的图像，其中识别的车辆由红色方框圈出。")

    # print(f"识别的车辆地理坐标已保存到{coords_path}，\n"
    #       f"识别后的图像已保存到{save_path}\\result.jpg。")
    output_txt = f"识别的车辆地理坐标已保存到{os.path.abspath(coords_path)}，\n" \
                 f"识别后的图像已保存到{os.path.abspath(save_path)}\\result.jpg。"

    yield output_txt
