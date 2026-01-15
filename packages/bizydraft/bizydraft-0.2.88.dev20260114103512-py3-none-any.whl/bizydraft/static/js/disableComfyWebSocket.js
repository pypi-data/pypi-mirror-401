// 保存原始的 WebSocket 构造函数
const OriginalWebSocket = window.WebSocket;

// 保存原始的 fetch 函数
const OriginalFetch = window.fetch;

// 保存原始的 XMLHttpRequest
const OriginalXHR = window.XMLHttpRequest;

// 需要跳过的 URL 数组
const skipFetchUrls = ["manager/badge_mode", "pysssss/autocomplete"];

// 需要拦截并上传到 OSS 的路由
const uploadRoutes = [
  "/upload/image",
  "/upload/mask",
  "/api/upload/image",
  "/api/upload/mask",
];

/**
 * 统一处理上传请求的核心逻辑
 */
async function handleUploadRequest(url, formData) {
  const { fileToOss } = await import("./uploadFile.js");

  const file = formData.get("image");
  const type = formData.get("type");

  if (!file || !(file instanceof File)) {
    throw new Error("未找到文件或文件格式错误");
  }

  const isMaskUpload = url.includes("/mask");
  let ossUrl;

  if (isMaskUpload) {
    const originalRef = formData.get("original_ref");
    const maskResult = await handleMaskUpload(
      file,
      type,
      originalRef,
      fileToOss
    );
    ossUrl = maskResult.url;
  } else {
    const result = await fileToOss(file);
    ossUrl = result.url;
  }

  return {
    name: ossUrl,
    subfolder: "",
    type: type || "input",
  };
}

/**
 * 检查 URL 是否需要拦截
 */
function shouldInterceptUrl(url, urlList) {
  const urlString = typeof url === "string" ? url : url.toString();
  return urlList.some((item) => urlString.includes(item));
}

/**
 * 模拟 XHR 成功响应
 */
function mockXHRResponse(xhr, data) {
  const responseText = typeof data === "string" ? data : JSON.stringify(data);
  Object.defineProperty(xhr, "status", { value: 200, writable: false });
  Object.defineProperty(xhr, "statusText", { value: "OK", writable: false });
  Object.defineProperty(xhr, "readyState", { value: 4, writable: false });
  Object.defineProperty(xhr, "responseText", {
    value: responseText,
    writable: false,
  });
  Object.defineProperty(xhr, "response", {
    value: responseText,
    writable: false,
  });

  if (xhr.onreadystatechange) xhr.onreadystatechange();
  if (xhr.onload) xhr.onload();
}

class FakeWebSocket {
  constructor(url) {
    this.url = url;
    this.readyState = WebSocket.CONNECTING; // 核心：保持 CONNECTING 状态
    console.warn("[BizyDraft] 已阻止 WebSocket 连接:", url);
  }
  send() {}
  close() {}
  addEventListener() {}
  removeEventListener() {}
}

window.WebSocket = function (url, protocols) {
  //精确拦截/ws请求
  if (typeof url === "string" && /^wss?:\/\/[^/]+\/ws(\?.*)?$/.test(url)) {
    return new FakeWebSocket(url);
  }
  // 其他连接正常创建，不影响
  return new OriginalWebSocket(url, protocols);
};

// 保留 WebSocket 的静态属性和原型
Object.setPrototypeOf(window.WebSocket, OriginalWebSocket);
window.WebSocket.prototype = OriginalWebSocket.prototype;

// 复制静态常量（使用 defineProperty 避免只读属性错误）
["CONNECTING", "OPEN", "CLOSING", "CLOSED"].forEach((prop) => {
  Object.defineProperty(window.WebSocket, prop, {
    value: OriginalWebSocket[prop],
    writable: false,
    enumerable: true,
    configurable: true,
  });
});

// 拦截 fetch 请求
window.fetch = async function (url, options) {
  const urlString = typeof url === "string" ? url : url.toString();

  // 检查 URL 是否在跳过列表中
  if (shouldInterceptUrl(urlString, skipFetchUrls)) {
    console.warn("[BizyDraft] 已阻止 fetch 请求:", urlString);
    return Promise.resolve(
      new Response(null, {
        status: 200,
        statusText: "OK",
        headers: new Headers({ "Content-Type": "application/json" }),
      })
    );
  }

  // 检查是否是上传路由
  if (
    shouldInterceptUrl(urlString, uploadRoutes) &&
    options?.method === "POST" &&
    options.body instanceof FormData
  ) {
    console.log("[BizyDraft] 拦截上传请求，转发到 OSS:", urlString);

    try {
      const result = await handleUploadRequest(urlString, options.body);
      return new Response(JSON.stringify(result), {
        status: 200,
        headers: new Headers({ "Content-Type": "application/json" }),
      });
    } catch (error) {
      console.error("[BizyDraft] OSS 上传失败:", error);
      return OriginalFetch.apply(this, arguments);
    }
  }

  // 其他请求正常发送
  return OriginalFetch.apply(this, arguments);
};

/**
 * 处理 mask 上传
 */
async function handleMaskUpload(file, type, originalRefStr, fileToOss) {
  // 上传文件的辅助函数
  const uploadFile = async (fileToUpload) => {
    const result = await fileToOss(fileToUpload);
    return { url: result.url, type: type || "input" };
  };

  // 如果没有 original_ref，直接上传 mask
  if (!originalRefStr) {
    return uploadFile(file);
  }

  try {
    const originalRef = JSON.parse(originalRefStr);
    const originalFilename = originalRef.filename;
    const originalSubfolder = originalRef.subfolder || "";

    if (!originalFilename) {
      throw new Error("No filename in original_ref");
    }

    // 构建原始图片的 URL
    let originalUrl;
    if (originalSubfolder.includes("http")) {
      originalUrl = `${decodeURIComponent(
        originalSubfolder
      )}/${originalFilename}`;
    } else if (
      originalFilename.startsWith("http://") ||
      originalFilename.startsWith("https://")
    ) {
      originalUrl = originalFilename;
    } else {
      // 本地文件，直接上传 mask
      return uploadFile(file);
    }

    // 下载原始图片
    const originalResponse = await OriginalFetch(originalUrl);
    if (!originalResponse.ok) {
      throw new Error(
        `Failed to download original image: ${originalResponse.status}`
      );
    }
    const originalBlob = await originalResponse.blob();

    // 使用 Canvas 处理图片：应用 alpha 通道
    const processedBlob = await applyMaskToImage(originalBlob, file);

    // 上传处理后的图片
    const processedFile = new File(
      [processedBlob],
      `clipspace-mask-${Date.now()}.png`,
      { type: "image/png" }
    );
    return uploadFile(processedFile);
  } catch (error) {
    console.error("[BizyDraft] Mask 处理失败:", error);
    // 失败时直接上传原始 mask
    return uploadFile(file);
  }
}

/**
 * 使用 Canvas 将 mask 的 alpha 通道应用到原始图片
 */
async function applyMaskToImage(originalBlob, maskFile) {
  return new Promise((resolve, reject) => {
    const originalImg = new Image();
    const maskImg = new Image();

    let originalLoaded = false;
    let maskLoaded = false;

    const checkBothLoaded = () => {
      if (originalLoaded && maskLoaded) {
        try {
          const canvas = document.createElement("canvas");
          canvas.width = originalImg.width;
          canvas.height = originalImg.height;
          const ctx = canvas.getContext("2d");

          // 绘制原始图片
          ctx.drawImage(originalImg, 0, 0);

          // 获取原始图片的像素数据
          const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
          const pixels = imageData.data;

          // 绘制 mask 到临时 canvas
          const maskCanvas = document.createElement("canvas");
          maskCanvas.width = maskImg.width;
          maskCanvas.height = maskImg.height;
          const maskCtx = maskCanvas.getContext("2d");
          maskCtx.drawImage(maskImg, 0, 0);
          const maskData = maskCtx.getImageData(
            0,
            0,
            maskCanvas.width,
            maskCanvas.height
          );
          const maskPixels = maskData.data;

          // 应用 mask 的 alpha 通道
          for (let i = 0; i < pixels.length; i += 4) {
            if (i < maskPixels.length) {
              pixels[i + 3] = maskPixels[i + 3]; // 复制 alpha 通道
            }
          }

          ctx.putImageData(imageData, 0, 0);

          // 转换为 Blob
          canvas.toBlob((blob) => {
            if (blob) {
              resolve(blob);
            } else {
              reject(new Error("Failed to convert canvas to blob"));
            }
          }, "image/png");
        } catch (error) {
          reject(error);
        }
      }
    };

    originalImg.onload = () => {
      originalLoaded = true;
      checkBothLoaded();
    };
    originalImg.onerror = () =>
      reject(new Error("Failed to load original image"));
    originalImg.src = URL.createObjectURL(originalBlob);

    maskImg.onload = () => {
      maskLoaded = true;
      checkBothLoaded();
    };
    maskImg.onerror = () => reject(new Error("Failed to load mask image"));
    maskImg.src = URL.createObjectURL(maskFile);
  });
}

// 拦截 XMLHttpRequest
window.XMLHttpRequest = function () {
  const xhr = new OriginalXHR();
  const originalOpen = xhr.open;
  const originalSend = xhr.send;
  let requestUrl = "";
  let requestMethod = "";

  xhr.open = function (method, url, ...args) {
    requestUrl = typeof url === "string" ? url : url.toString();
    requestMethod = method.toUpperCase();
    return originalOpen.apply(xhr, [method, url, ...args]);
  };

  xhr.send = function (body) {
    // 检查是否在跳过列表中
    if (shouldInterceptUrl(requestUrl, skipFetchUrls)) {
      console.warn("[BizyDraft] 已阻止 XHR 请求:", requestUrl);
      setTimeout(() => mockXHRResponse(xhr, ""), 0);
      return;
    }

    // 检查是否是上传路由
    if (
      shouldInterceptUrl(requestUrl, uploadRoutes) &&
      requestMethod === "POST" &&
      body instanceof FormData
    ) {
      console.log("[BizyDraft] 拦截 XHR 上传请求，转发到 OSS:", requestUrl);

      (async () => {
        try {
          const result = await handleUploadRequest(requestUrl, body);
          mockXHRResponse(xhr, result);
        } catch (error) {
          console.error("[BizyDraft] OSS 上传失败 (XHR):", error);
          originalSend.call(xhr, body);
        }
      })();

      return;
    }

    // 其他请求正常发送
    return originalSend.apply(xhr, arguments);
  };

  return xhr;
};

// 保留 XMLHttpRequest 的静态属性和原型
Object.setPrototypeOf(window.XMLHttpRequest, OriginalXHR);
window.XMLHttpRequest.prototype = OriginalXHR.prototype;
