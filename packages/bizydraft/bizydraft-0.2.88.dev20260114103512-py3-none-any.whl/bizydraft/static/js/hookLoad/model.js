import { hideWidget } from "../tool.js";
import { fetchNodeConfig } from "./configLoader.js";

// 动态配置缓存
let nodeConfigCache = null;
let configLoadPromise = null;
let storageClearedOnce = false;

const HAZY_WHITELIST_NODES = {};

export const possibleWidgetNames = [
  "clip_name",
  "clip_name1",
  "clip_name2",
  "clip_name3",
  "clip_name4",
  "ckpt_name",
  "lora_name",
  "name",
  "lora",
  "lora_01",
  "lora_02",
  "lora_03",
  "lora_04",
  "lora_1_name",
  "lora_2_name",
  "lora_3_name",
  "lora_4_name",
  "lora_5_name",
  "lora_6_name",
  "lora_7_name",
  "lora_8_name",
  "lora_9_name",
  "lora_10_name",
  "lora_11_name",
  "lora_12_name",
  "model_name",
  "control_net_name",
  "ipadapter_file",
  "unet_name",
  "vae_name",
  "model",
  "model_name",
  "instantid_file",
  "pulid_file",
  "style_model_name",
  "yolo_model",
  "face_model",
  "bbox_model_name",
  "sam_model_name",
  "model_path",
  "upscale_model",
  "supir_model",
  "sdxl_model",
  "upscale_model_1",
  "upscale_model_2",
  "upscale_model_3",
  "sam_model",
  "sam2_model",
  "grounding_dino_model",
];

// 获取节点配置的API函数（使用共享配置加载器）
async function fetchNodeConfigWithCache() {
  if (nodeConfigCache) {
    return nodeConfigCache;
  }

  if (configLoadPromise) {
    return configLoadPromise;
  }

  configLoadPromise = (async () => {
    const config = await fetchNodeConfig();
    if (config) {
      nodeConfigCache = config;
      console.log(
        "节点配置加载成功:",
        Object.keys(nodeConfigCache).length,
        "个节点"
      );
    }
    return config;
  })();

  return configLoadPromise;
}

// 读取 mode_type（不再兼容旧的 modelType）
export function getModelTypeFromInput(inputConfig) {
  console.log("inputConfig", inputConfig);
  if (!inputConfig) return undefined;
  console.log("inputConfig", inputConfig);
  return inputConfig.mode_type;
}

// 根据节点名称获取节点配置信息（名单优先，正则补充；不阻塞返回）
export async function getNodeConfig(nodeName) {
  const excluded =
    /bizyair/i.test(nodeName) &&
    ![
      "BizyAir_LoraLoader",
      "BizyAir_NunchakuFluxLoraLoader",
      "BizyAir_Wan_LoraLoader",
      "BizyAir_ControlNetLoader",
      "BizyAir_CheckpointLoaderSimple",
    ].includes(nodeName);
  if (excluded) {
    return null;
  }

  // 1) 名单（API）优先（仅用缓存，不等待网络）
  if (nodeConfigCache && nodeConfigCache[nodeName]) {
    return { nodeName, config: nodeConfigCache[nodeName] };
  }

  // 若尚未发起请求，后台发起一次
  if (!configLoadPromise) {
    try {
      void fetchNodeConfigWithCache();
    } catch (e) {}
  }

  // 2) 正则补充：如 XxxLoader => Xxx（立即返回，不等待API）
  const regex = /^(\w+).*Loader.*/i;
  const match = nodeName.match(regex);
  if (match) {
    const inferredType = match[1];
    return {
      nodeName,
      config: {
        inputs: { [nodeName]: { mode_type: inferredType, required: true } },
      },
    };
  }
  return null;
}

export function createSetWidgetCallback(nodeConfig, selectedBaseModels = []) {
  return function setWidgetCallback() {
    if (!nodeConfig || !nodeConfig.config || !nodeConfig.config.inputs) {
      console.warn("节点配置无效:", nodeConfig);
      return;
    }

    const inputs = nodeConfig.config.inputs;
    const inputKeys = Object.keys(inputs);

    // 根据API配置找到对应的widget
    const targetWidgets = [];
    inputKeys.forEach((inputKey) => {
      const widget = this.widgets.find((w) => w.name === inputKey);
      if (widget) {
        targetWidgets.push({
          widget: widget,
          inputKey: inputKey,
          inputConfig: inputs[inputKey],
        });
      }
    });

    // 如果没有找到匹配的widget，使用原来的逻辑作为备选
    if (targetWidgets.length === 0) {
      const fallbackWidgets = this.widgets.filter((widget) =>
        possibleWidgetNames.includes(widget.name)
      );
      fallbackWidgets.forEach((wdt, index) => {
        const firstInput = Object.values(inputs)[0];
        if (firstInput) {
          targetWidgets.push({
            widget: wdt,
            inputKey: wdt.name,
            inputConfig: firstInput,
            index: index,
          });
        }
      });
    }

    targetWidgets.forEach(({ widget, inputKey, inputConfig, index }) => {
      // 检查是否禁用comfyagent
      if (inputConfig.disable_comfyagent) {
        console.log(`跳过禁用的widget: ${inputKey}`);
        return;
      }

      widget.value = widget.value || "to choose";
      widget.mouse = function (e, pos, canvas) {
        try {
          if (
            e.type === "pointerdown" ||
            e.type === "mousedown" ||
            e.type === "click" ||
            e.type === "pointerup"
          ) {
            e.preventDefault();
            e.stopPropagation();
            e.widgetClick = true;
            window.parent.postMessage(
              {
                type: "collapsePublishWorkflowDialog",
                method: "collapsePublishWorkflowDialog",
                result: true,
              },
              "*"
            );
            const currentNode = this.node;

            if (!currentNode || !currentNode.widgets) {
              console.warn("Node or widgets not available");
              return false;
            }

            // 使用 parentPostMessage 发送 openWidgetSelect 消息
            const modelType = getModelTypeFromInput(inputConfig);
            if (modelType) {
              // 存储当前上下文，用于处理返回结果
              const widgetContext = {
                node: currentNode,
                widget: widget,
                inputKey: inputKey,
                targetWidgets: targetWidgets,
                twIndex: targetWidgets.findIndex((tw) => tw.widget === widget),
              };

              // 存储到节点的临时属性中，以便消息处理时使用
              if (!currentNode._pendingWidgetSelect) {
                currentNode._pendingWidgetSelect = new Map();
              }
              currentNode._pendingWidgetSelect.set(widget.name, widgetContext);

              // 发送消息给父窗口
              window.parent.postMessage(
                {
                  type: "openWidgetSelect",
                  widgetType: "model",
                  payload: {
                    config: {
                      modelType: [modelType],
                      selectedBaseModels: selectedBaseModels,
                    },
                    nodeId: currentNode.id,
                    widgetName: widget.name,
                  },
                },
                "*"
              );
            } else {
              console.warn("无法获取 modelType，跳过打开模型选择对话框");
            }
            return false;
          }
        } catch (error) {
          console.error("Error handling mouse event:", error);
        }
      };

      widget.options = widget.options || {};
      widget.options.values = () => [];
      widget.options.editable = false;
      widget.clickable = true;
      widget.processMouse = true;
    });
  };
}

export function setupNodeMouseBehavior(node, nodeConfig) {
  // 固定隐藏主版本ID字段（其余编号字段为hidden类型本身不可见）
  hideWidget(node, "model_version_id");

  // 只设置必要的状态信息，不修改onMouseDown（已在上面的扩展中处理）
  if (!node._bizyairState) {
    node._bizyairState = {
      lastClickTime: 0,
      DEBOUNCE_DELAY: 300,
      nodeConfig: nodeConfig,
    };
  }
}

export function addBadge(node) {
  const customBadge = new LGraphBadge({
    text: "!",
    fgColor: "white",
    bgColor: "#FF6B6B",
    fontSize: 12,
    padding: 8,
    height: 20,
    cornerRadius: 10,
  });
  if (!Array.isArray(node.badges)) {
    node.badges = [];
  }
  if (node.hasTips) {
    return;
  }
  node.badges.push(() => customBadge);
  node.hasTips = true;
}

// 处理来自父窗口的 widgetSelected 消息
function handleWidgetSelected(message) {
  if (message.type !== "widgetSelected" || message.widgetType !== "model") {
    return;
  }

  const { nodeId, widgetName, result } = message.payload;
  if (!result || !result.version) {
    console.warn("widgetSelected 消息缺少必要数据:", message);
    return;
  }

  // result.data 的结构：{ version: { id, file_name }, model: model.name }
  const version = result.version;
  const modelName = result.model;

  // 查找对应的节点
  const app = window.app;
  if (!app || !app.graph) {
    console.warn("无法访问 app 或 graph");
    return;
  }

  // 使用 getNodeById 方法查找节点
  const node =
    app.graph.getNodeById && app.graph.getNodeById(nodeId)
      ? app.graph.getNodeById(nodeId)
      : app.graph._nodes_by_id && app.graph._nodes_by_id[nodeId]
        ? app.graph._nodes_by_id[nodeId]
        : app.graph._nodes && app.graph._nodes.find((n) => n.id === nodeId);

  if (!node || !node.widgets) {
    console.warn(`找不到节点 ${nodeId} 或节点没有 widgets`);
    return;
  }

  // 获取存储的上下文
  const widgetContext =
    node._pendingWidgetSelect && node._pendingWidgetSelect.get(widgetName);
  if (!widgetContext) {
    console.warn(`找不到 widget ${widgetName} 的上下文`);
    return;
  }

  const { widget, targetWidgets, twIndex } = widgetContext;

  // 更新 widget 值
  if (widget) {
    widget.value = version.file_name;

    // 找到对应的隐藏字段（固定命名：model_version_id, model_version_id2...）
    const fieldName =
      twIndex === 0 ? "model_version_id" : `model_version_id${twIndex + 1}`;
    const modelVersionField = node.widgets.find((w) => w.name === fieldName);

    if (modelVersionField && version) {
      modelVersionField.value = version.id;
      node.setDirtyCanvas(true);
    }
  }

  // 删除节点上的感叹号徽章
  if (node && node.badges && Array.isArray(node.badges)) {
    // 移除 text 为 '!' 的徽章
    node.badges = node.badges.filter((badgeFn) => {
      try {
        const badge = typeof badgeFn === "function" ? badgeFn() : badgeFn;
        return badge.text !== "!";
      } catch (e) {
        return true;
      }
    });
    // 同时移除 hasTips 标记
    if (node.hasTips) {
      delete node.hasTips;
    }
  }

  // 清理临时存储的上下文
  if (node._pendingWidgetSelect) {
    node._pendingWidgetSelect.delete(widgetName);
    if (node._pendingWidgetSelect.size === 0) {
      delete node._pendingWidgetSelect;
    }
  }
}

// 监听来自父窗口的消息
if (typeof window !== "undefined") {
  window.addEventListener("message", (event) => {
    // 只处理来自父窗口的消息

    if (
      event.source === window.parent &&
      event.data &&
      event.data.type === "callMethod" &&
      event.data.method === "widgetSelected"
    ) {
      handleWidgetSelected(event.data.params);
    }
  });
}

// 启动时后台预取（不阻塞后续逻辑）
try {
  void fetchNodeConfigWithCache();
} catch (e) {
  /* noop */
}
