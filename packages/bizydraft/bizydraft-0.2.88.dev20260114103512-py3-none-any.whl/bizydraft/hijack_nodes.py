import re
from datetime import datetime

from loguru import logger

from bizydraft.env import COMFYAGENT_NODE_CONFIG

try:
    from comfy_extras.nodes_video import LoadVideo
    from nodes import NODE_CLASS_MAPPINGS, LoadImage
except ImportError:
    logger.error(
        "failed to import ComfyUI nodes modules, ensure PYTHONPATH is set correctly. (export PYTHONPATH=$PYTHONPATH:/path/to/ComfyUI)"
    )
    exit(1)


def get_data_load_classes_from_url(config_url):
    import requests

    # 获取当前时间，精确到分钟
    current_time = datetime.now().strftime("%Y%m%d%H%M")

    try:
        config_url = config_url + "?t=" + current_time
        response = requests.get(config_url)
        response.raise_for_status()
        data = response.json()
        keys_list = []
        if "weight_load_nodes" in data:
            keys_list.extend(list(data["weight_load_nodes"].keys()))
        if "media_load_nodes" in data:
            keys_list.extend(list(data["media_load_nodes"].keys()))

        return keys_list
    except Exception as e:
        logger.error(
            f"Failed to fetch or comfyagent node config from {config_url}: {e}"
        )
        return []


DATA_LOAD_CLASSES = [
    "LoadImage",
    "LoadVideo",
    "LoadImageMask",
    "LoadAudio",
    "Load3D",
    "VHS_LoadAudioUpload",
    "VHS_LoadVideo",
]

if COMFYAGENT_NODE_CONFIG.startswith("http"):
    fetched_classes = get_data_load_classes_from_url(COMFYAGENT_NODE_CONFIG)
    if fetched_classes:
        DATA_LOAD_CLASSES.extend(fetched_classes)
        logger.info(f"Fetched additional data load classes: {fetched_classes}")
    else:
        logger.warning("No additional data load classes fetched from the URL.")


def hijack_nodes():
    # 通用情况，正则匹配后，打通用patch、替换
    for node_name, base_class in NODE_CLASS_MAPPINGS.items():

        regex = r"^(?!BizyAir_)\w+.*Loader.*"
        match = re.match(regex, node_name, re.IGNORECASE)
        if match or (node_name in DATA_LOAD_CLASSES):
            logger.debug(f"Creating patched class for {node_name}")
            patched_class = create_patched_class(base_class)
            NODE_CLASS_MAPPINGS[node_name] = patched_class


def create_patched_class(base_class, validate_inputs_func=None):
    def default_validate_inputs(cls, *args, **kwargs):
        return True

    # 使用传入的函数或默认函数
    final_validate_inputs = validate_inputs_func or default_validate_inputs

    class PatchedClass(base_class):
        # V3
        @classmethod
        def validate_inputs(cls, *args, **kwargs):
            return final_validate_inputs(cls, *args, **kwargs)

        # 兼容 V1
        VALIDATE_INPUTS = validate_inputs

    return PatchedClass
