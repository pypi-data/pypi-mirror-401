import time
import cv2
import base64
import numpy as np

from policelibrary import ChatRobot, ImageChatRobot

def resize_image(image_path: str, output_path: str, target_size: int = 1024) -> None:
    image = cv2.imread(image_path)
    # 保持比例resize，边缘填充128
    h, w = image.shape[:2]
    scale = min(target_size / w, target_size / h)
    new_w = int(w * scale)
    new_h = int(h * scale)
    resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
    # 创建1024x1024的画布，填充128
    canvas = np.full((target_size, target_size, 3), 128, dtype=image.dtype)
    # 计算居中位置
    top = (target_size - new_h) // 2
    left = (target_size - new_w) // 2
    # 将resize后的图像放到画布中央
    canvas[top:top+new_h, left:left+new_w] = resized
    cv2.imwrite(output_path, canvas)

if __name__ == "__main__":

    # =============================== 测试1：简单对话 ===============================
    print("=============================== 测试1: 简单对话 ===============================")
    chat_robot = ChatRobot()
    # 组织messages, 包括对话历史和当前用户输入
    messages = [
        {"role": "user", "content": "今天天气怎么样?"},
        {"role": "assistant", "content": "今天天气晴朗, 温度适宜, 适合出行。"},
        {"role": "user", "content": "介绍一下你自己?"},
    ]

    start_time = time.time()
    for text in chat_robot.chat(messages):
        print(text, end="", flush=True)
    end_time = time.time()
    print("\n")
    print(f"对话时间: {end_time - start_time}秒")
    


    # =============================== 测试2：图像理解 ===============================
    image_chat_robot = ImageChatRobot()

    # 测试本地图片(有人物)
    print("=============================== 测试2: 图像理解(有人物) ===============================")
    resize_image("./assets/laugh.jpg", "./assets/laugh_resized.jpg") # 先resize图片
    start_time = time.time()
    for text in image_chat_robot.chat("./assets/laugh_resized.jpg"):
        print(text, end="", flush=True)
    print("\n")
    end_time = time.time()
    print(f"图像理解时间: {end_time - start_time}秒")

    # 测试本地图片(无笑脸)
    print("=============================== 测试2: 图像理解(无笑脸) ===============================")
    resize_image("./assets/tree.jpg", "./assets/tree_resized.jpg") # 先resize图片
    start_time = time.time()
    for text in image_chat_robot.chat("./assets/tree_resized.jpg"):
        print(text, end="", flush=True)
    print("\n")
    end_time = time.time()
    print(f"图像理解时间: {end_time - start_time}秒")

    # 测试网络图片(有人物)
    print("=============================== 测试2: 图像理解(网络图片)(图片尺寸是1024*1024, 如果不是bbox不准) ===============================")
    start_time = time.time()
    for text in image_chat_robot.chat("https://ark-project.tos-cn-beijing.ivolces.com/images/view.jpeg"):
        print(text, end="", flush=True)
    print("\n")
    end_time = time.time()
    print(f"图像理解时间: {end_time - start_time}秒")

    # 测试网络图片(无笑脸)
    print("=============================== 测试2: 图像理解(网络图片)(图片尺寸是1024*1024, 如果不是bbox不准) ===============================")
    start_time = time.time()
    for text in image_chat_robot.chat("https://ark-project.tos-cn-beijing.ivolces.com/images/view.jpeg"):
        print(text, end="", flush=True)
    print("\n")
    end_time = time.time()
    print(f"图像理解时间: {end_time - start_time}秒")