import numpy as np
from sklearn.decomposition import NMF
import matplotlib.pyplot as plt
from PIL import Image

# 加载图像
image = Image.open('girl.jpg')
# 转换为灰度图像
gray_image = image.convert('L')
# 将灰度图像转换为二维数组
image_array = np.array(gray_image)

# 数据预处理，将像素值归一化到 [0, 1] 范围
normalized_image_array = image_array / 255.0

# 定义NMF模型并进行拟合
n_components = 4  # 分解成两个非负矩阵
model = NMF(n_components=n_components, init='random', random_state=0)
W = model.fit_transform(normalized_image_array)
H = model.components_

# 重建图像
reconstructed_image = np.dot(W, H)
reconstructed_image = np.clip(reconstructed_image, 0, 1)  # 截断像素值到 [0, 1] 范围

# 显示原始图像和重建图像
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
axes[0].imshow(image_array, cmap='gray')
axes[0].set_title('Original Image')
axes[0].axis('off')
axes[1].imshow(reconstructed_image, cmap='gray')
axes[1].set_title('Reconstructed Image')
axes[1].axis('off')
plt.show()