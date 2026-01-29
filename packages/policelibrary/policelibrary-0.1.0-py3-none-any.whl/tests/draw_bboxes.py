import cv2
import numpy as np
import argparse
import os



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--img_path", type=str, default="./assets/laugh_resized.jpg")
    parser.add_argument("--bbox", type=list, default=[260, 7, 694, 578])
    parser.add_argument("--output_path", type=str, default="./laugh_draw_bbox.jpg")
    args = parser.parse_args()

    assert args.bbox is not None, "bbox is required"
    assert args.output_path is not None, "output_path is required"
    assert args.img_path is not None, "img_path is required"

    assert os.path.exists(args.img_path), "img_path does not exist"
    img = cv2.imread(args.img_path)

    x1, y1, x2, y2 = args.bbox
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # 保存图片  
    cv2.imwrite(args.output_path, img)

    print(f"已成功在图片上绘制矩形框并保存到: {args.output_path}")
    print(f"矩形框坐标: ({x1}, {y1}) -> ({x2}, {y2})")
