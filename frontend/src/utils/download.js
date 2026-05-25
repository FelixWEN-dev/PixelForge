import JSZip from "jszip";

let isDownloading = false;

/**
 * 清洗文件名
 */
function sanitizeFilename(filename) {
  return filename.replace(/[<>:"/\\|?*]/g, "_");
}

/**
 * 下载单张图片
 * @param {string} url
 * @param {string} filename
 */
export async function downloadImage(url, filename = "image.png") {
  try {
    const response = await fetch(url, {
      method: "GET",
      cache: "no-store",
    });

    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }

    const blob = await response.blob();

    const blobUrl = window.URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = blobUrl;
    link.download = sanitizeFilename(filename);

    document.body.appendChild(link);

    requestAnimationFrame(() => {
      link.click();

      setTimeout(() => {
        document.body.removeChild(link);
        window.URL.revokeObjectURL(blobUrl);
      }, 5000);
    });
  } catch (error) {
    console.error("下载图片失败:", error);

    // 降级方案
    window.open(url, "_blank");
  }
}

/**
 * 批量下载图片（ZIP）
 * @param {Array} images
 */
export async function downloadImages(images) {
  if (!images?.length) return;

  // 防止重复点击
  if (isDownloading) {
    console.warn("已有下载任务正在进行");
    return;
  }

  isDownloading = true;

  try {
    // 单张直接下载
    if (images.length === 1) {
      const img = images[0];

      await downloadImage(
        img.url,
        img.name || "image_1.png"
      );

      return;
    }

    console.log("开始批量下载:", images.length);

    const zip = new JSZip();

    // 限制并发
    const concurrency = 3;

    for (let i = 0; i < images.length; i += concurrency) {
      const batch = images.slice(i, i + concurrency);

      await Promise.all(
        batch.map(async (img, index) => {
          const realIndex = i + index;

          try {
            console.log(`下载第 ${realIndex + 1} 张`);

            const response = await fetch(img.url, {
              method: "GET",
              cache: "no-store",
            });

            if (!response.ok) {
              throw new Error(`HTTP ${response.status}`);
            }

            // 使用 arrayBuffer 替代 blob
            const arrayBuffer =
              await response.arrayBuffer();

            const filename = sanitizeFilename(
              img.name || `image_${realIndex + 1}.png`
            );

            zip.file(filename, arrayBuffer);

            console.log(`完成: ${filename}`);
          } catch (error) {
            console.error(
              `第 ${realIndex + 1} 张失败`,
              error
            );
          }
        })
      );
    }

    console.log("开始生成 ZIP");

    const zipBlob = await zip.generateAsync({
      type: "blob",
      compression: "DEFLATE",
      compressionOptions: {
        level: 6,
      },
    });

    console.log("ZIP 生成完成");

    const zipUrl = window.URL.createObjectURL(zipBlob);

    const link = document.createElement("a");

    link.href = zipUrl;
    link.download = `pixelforge_${Date.now()}.zip`;

    document.body.appendChild(link);

    requestAnimationFrame(() => {
      link.click();

      setTimeout(() => {
        document.body.removeChild(link);

        window.URL.revokeObjectURL(zipUrl);

        // 主动释放 JSZip 引用
        zip.files = {};

        console.log("资源已释放");
      }, 5000);
    });

    console.log("ZIP 下载已触发");
  } catch (error) {
    console.error("批量下载失败:", error);

    // 降级方案
    images.forEach((img) => {
      window.open(img.url, "_blank");
    });
  } finally {
    isDownloading = false;
  }
}