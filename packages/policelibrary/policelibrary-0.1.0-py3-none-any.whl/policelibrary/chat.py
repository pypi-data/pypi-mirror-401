from typing import Generator
import os
import base64
from openai import OpenAI


class ChatRobot:
    def __init__(self, model: str = "doubao-seed-1-8-251228", system_prompt: str = "你是小智, 一个智能助手"):
        """
        Args:
            model: 模型名称
                - doubao-seed-1-6-251015: 豆包1.6
                - doubao-seed-1-8-251228: 豆包1.8
            system_prompt: 系统提示词
        """
        if os.environ.get("ARK_API_KEY") is None:
            raise ValueError("ARK_API_KEY is not set")
        
        self.client = OpenAI(
            api_key=os.environ.get("ARK_API_KEY"),
            base_url="https://ark.cn-beijing.volces.com/api/v3",
        )
        self.model = model
        self.system_prompt = system_prompt

    def chat(self, messages: list[dict]) -> Generator[str, None, None]:
        """
        Args:
            messages: 对话历史, 格式为: [{"role": "user", "content": "你好"}, {"role": "assistant", "content": "你好"}]

        Returns:
            response: 对话响应
        """
        # 如果有 system_prompt，将其添加到 messages 开头
        if self.system_prompt:
            # 检查 messages 中是否已有 system 消息
            if not messages or messages[0].get("role") != "system":
                messages = [{"role": "system", "content": self.system_prompt}] + messages
        
        response = self.client.chat.completions.create(
            messages=messages,
            model=self.model,
            stream=True,
            extra_body={"thinking": {"type": "disabled"}})

        for chunk in response:
            yield chunk.choices[0].delta.content


class ImageChatRobot(ChatRobot):
    def __init__(self, model: str = "doubao-seed-1-8-251228", system_prompt: str = "你是一个图像理解助手, 能够识别图像中人脸表情, 并把头部坐标返回出来"):
        super().__init__(model, system_prompt)

    def chat(self, image_url: str) -> Generator[str, None, None]:
        if not image_url.startswith("http"):
            # 转换为base64
            with open(image_url, "rb") as image_file:
                image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
                image_data_url = f"data:image/jpeg;base64,{image_base64}"
        else:
            image_data_url = image_url

        # 组织messages
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url", 
                        "image_url": {"url": image_data_url}
                    }, 
                    {
                        "type": "text", 
                        "text": f"""你是一个图像理解助手, 能够识别图像中人脸表情, 并把头部坐标返回出来。
                        返回结果格式为json格式如下:
                        {{
                            "expression": "表情(可选: 微笑, 大笑, 愤怒, 悲伤, 惊讶, 厌恶, 轻蔑, 恐惧, 困惑, 无聊, 思考, 惊讶, 怀疑, 不满, 轻蔑, 厌恶, 恐惧, 困惑, 无聊, 思考)",
                            "description": "人脸表情详细描述",
                            "bbox": [x1, y1, x2, y2]
                        }}
                        如果有多个人的情况下，只识别主要的那个人即可；
                        如果无法识别，或图中没有人脸返回None。"""
                    }
                ]
            },
        ]

        return super().chat(messages)