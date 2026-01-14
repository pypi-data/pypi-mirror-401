from openai import OpenAI
from .common import image_to_base64


class ChatSession:
    def __init__(
        self,
        base_url,
        api_key,
        model,
        lang=None,  # 可选 "zh", "en"，"auto", None 表示不检测
    ):
        """
        # 初始化：lang=None (自动检测)
        session = CPMChatSession()

        # 加载图片
        img1 = cv2.imread()
        img2 = cv2.imread()

        # 第一轮: 中文任务，自动检测为 zh
        session.send("描述图片1的内容", images=img1)

        # 第二轮: 英文任务，自动检测为 en
        session.send("Describe the transition from image1 to image2", images=img2)

        # 第三轮: 多图，中文任务
        session.send("描述图片1和图片2的关系", images=[img1, img2])

        # 第四轮: 新会话，英文任务
        session.start_new()
        session.send("Describe the content of image2", images=img2)
        """
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.conversation_id = None
        self.lang = lang

    def _encode_img(self, img_bgr):
        return "data:image/jpeg;base64," + image_to_base64(img_bgr)

    def start_new(self):
        """开启新会话"""
        self.conversation_id = None
        # print("\n[会话管理器] 已开启新会话\n")

    def send(self, text, images=None):
        """
        通用发送方法:
          - 纯文本: send("内容")
          - 单图+文本: send("内容", images=img)
          - 多图+文本: send("内容", images=[img1, img2])
        """

        # 构造消息内容
        contents = [{"type": "text", "text": text}]
        if images is not None:
            if isinstance(images, list):
                for img in images:
                    contents.append(
                        {
                            "type": "image_url",
                            "image_url": {"url": self._encode_img(img)},
                        }
                    )
            else:
                contents.append(
                    {
                        "type": "image_url",
                        "image_url": {"url": self._encode_img(images)},
                    }
                )

        # 请求体
        extra = {}
        if self.conversation_id:
            extra["conversation_id"] = self.conversation_id
        if self.lang:
            extra["lang"] = self.lang  # 传给服务端

        # 发起请求
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": contents}],
            extra_body=extra,
        )

        # 首次会话更新 ID
        if self.conversation_id is None:
            self.conversation_id = resp.conversation_id

        # 输出结果
        answer = resp.choices[0].message.content
        # print(f"[模型回答]: {answer}\n")
        return answer
