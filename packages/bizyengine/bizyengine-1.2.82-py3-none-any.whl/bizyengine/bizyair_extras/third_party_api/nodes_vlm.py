from bizyairsdk import tensor_to_bytesio

from .trd_nodes_base import BizyAirTrdApiBaseNode


class TRD_VLM_API(BizyAirTrdApiBaseNode):
    NODE_DISPLAY_NAME = "Third-Party VLM API"
    RETURN_TYPES = (
        "STRING",
        """{"gemini-3-pro-preview": "gemini-3-pro-preview", "gemini-3-flash-preview": "gemini-3-flash-preview"}""",  # NOTE: 需要动态获取
    )
    RETURN_NAMES = ("string", "bizyair_model_name")
    CATEGORY = "☁️BizyAir/External APIs/VLM"
    INPUT_IS_LIST = True

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": (
                    ["gemini-3-pro-preview", "gemini-3-flash-preview"],
                    {"default": "gemini-3-flash-preview"},
                ),  # NOTE: 需要动态获取
                "system_prompt": (
                    "STRING",
                    {
                        "default": "你是一个能分析图像的AI助手。请仔细观察图像，并根据用户的问题提供详细、准确的描述。",
                        "multiline": True,
                    },
                ),
                "user_prompt": (
                    "STRING",
                    {
                        "default": "请描述这张图片的内容，并指出任何有趣或不寻常的细节。",
                        "multiline": True,
                    },
                ),
                "images": ("IMAGE",),
                "max_tokens": ("INT", {"default": 32768, "min": 1, "max": 65536}),
                "temperature": (
                    "FLOAT",
                    {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.01},
                ),
                "detail": (
                    ["low", "medium", "high"],
                    {"default": "high"},
                ),
                "enable_thinking": (
                    "BOOLEAN",
                    {"default": False, "tooltip": "如果模型支持思考模式，是否开启"},
                ),
                "inputcount": (
                    "INT",
                    {
                        "default": 1,
                        "min": 1,
                        "max": 900,
                        "tooltip": "动态控制输入的参考图数量，点击Update inputs按钮刷新",
                    },
                ),
            },
        }

    def handle_inputs(self, headers, prompt_id, **kwargs):
        temperature = kwargs.get("temperature", [1.0])[0]
        max_tokens = kwargs.get("max_tokens", [32768])[0]
        detail = kwargs.get("detail", ["high"])[0]
        images = kwargs.get("images", [])
        user_prompt = kwargs.get("user_prompt", [""])[0]
        system_prompt = kwargs.get("system_prompt", [""])[0]
        enable_thinking = kwargs.get("enable_thinking", [False])[0]
        model = kwargs.get("model", ["gemini-3-flash-preview"])[0]

        # 多图的情况可以认为图片输入都是List[Image Batch]
        total_input_images = 0
        for _, img_batch in enumerate(images if images is not None else []):
            if img_batch is not None:
                total_input_images += img_batch.shape[0]
        extra_images, total_extra_images = self.get_extra_images(**kwargs)
        total_input_images += total_extra_images
        if total_input_images == 0:
            raise ValueError("At least one image is required")
        if total_input_images > 200:
            raise ValueError("Maximum number of images is 200")
        parts = []
        index = 1
        for _, img_batch in enumerate(images if images is not None else []):
            for _, img in enumerate(img_batch if img_batch is not None else []):
                if img is not None:
                    url = self.upload_file(
                        tensor_to_bytesio(image=img, total_pixels=4096 * 4096),
                        f"{prompt_id}_{index}.png",
                        headers,
                    )
                    parts.append(url)
                    index += 1
        for _, img_batch in enumerate(extra_images):
            for _, img in enumerate(img_batch if img_batch is not None else []):
                if img is not None:
                    url = self.upload_file(
                        tensor_to_bytesio(image=img, total_pixels=4096 * 4096),
                        f"{prompt_id}_{index}.png",
                        headers,
                    )
                    parts.append(url)
                    index += 1

        data = {
            "urls": parts,
            "user_prompt": user_prompt,
            "system_prompt": system_prompt,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "detail": detail,
            "enable_thinking": enable_thinking,
        }
        return data, model

    def handle_outputs(self, outputs):
        return (outputs[2][0], "")
