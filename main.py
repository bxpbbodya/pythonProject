import cv2
import numpy as np
def relative_entropy(a, b, name):
    ahist = cv2.calcHist([b], [0], None, [256], [0, 256])
    bhist = cv2.calcHist([a], [0], None, [256], [0, 256])
    epsilon = 1e-10
    ahist += epsilon
    bhist += epsilon
    ahistogram_normalized = ahist / ahist.sum()
    bhistogram_normalized = bhist / bhist.sum()
    KL_distance = np.sum(ahistogram_normalized * np.log2(ahistogram_normalized / bhistogram_normalized))
    print(f'Relative Entropy {name}: {KL_distance}')
def get_entropy(img):
    histogram = cv2.calcHist([img], [0], None, [256], [0, 256])
    histogram_normalized = histogram / histogram.sum()
    return -np.sum(histogram_normalized * np.log2(histogram_normalized + np.finfo(float).eps))
def discretization(image, step):
    new_height = (image.shape[0] // step) * step
    new_width = (image.shape[1] // step) * step
    cropped_image = image[:new_height, :new_width]
    discrete_img = np.zeros_like(cropped_image)
    for i in range(0, new_height, step):
        for j in range(0, new_width, step):
            discrete_img[i:i + step, j:j + step] = cropped_image[i, j]
    return discrete_img
def uniform_quantization(image, levels):
    min_val = np.min(image)
    max_val = np.max(image)
    step = (max_val - min_val + 1) / levels
    quantized_image = (((image - min_val) / step).astype(int) * step + min_val).astype('uint8')
    return quantized_image
def print_image_entropy(img, name):
    entropy = get_entropy(img)
    print(f'Image Entropy {name}: {entropy}')
image_path = '4.jpg'
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
print_image_entropy(image, "Original Image:")
height, width = image.shape
step2 = discretization(image, 2)
print_image_entropy(step2, "Discretization Step 2:")
cv2.imwrite('step_2_discr.png', step2)
step2_re = cv2.resize(step2, (width, height), interpolation=cv2.INTER_CUBIC)
print_image_entropy(step2_re, "Restored After Discretization Step 2:")
step4 = discretization(image, 4)
print_image_entropy(step4, "Discretization Step 4:")
cv2.imwrite('step_4_discr.png', step4)
step2_re_nearest = cv2.resize(step2, (width, height), interpolation=cv2.INTER_NEAREST)
step4_re_nearest = cv2.resize(step4, (width, height), interpolation=cv2.INTER_NEAREST)
print_image_entropy(step2_re_nearest, "Restored (Nearest Neighbor) After Discretization Step 2:")
print_image_entropy(step4_re_nearest, "Restored (Nearest Neighbor) After Discretization Step 4:")
cv2.imwrite('step2_re_nearest.png', step2)
cv2.imwrite('step4_re_nearest.png', step4)
step2_re_linear = cv2.resize(step2, (width, height), interpolation=cv2.INTER_LINEAR)
step4_re_linear = cv2.resize(step4, (width, height), interpolation=cv2.INTER_LINEAR)
print_image_entropy(step2_re_linear, "Restored (Bilinear Interpolation) After Discretization Step 2:")
print_image_entropy(step4_re_linear, "Restored (Bilinear Interpolation) After Discretization Step 4:")
cv2.imwrite('step2_re_linear.png', step2)
cv2.imwrite('step4_re_linear.png', step4)
step2_re_cubic = cv2.resize(step2, (width, height), interpolation=cv2.INTER_CUBIC)
step4_re_cubic = cv2.resize(step4, (width, height), interpolation=cv2.INTER_CUBIC)
print_image_entropy(step2_re_cubic, "Restored (Bicubic Interpolation) After Discretization Step 2:")
print_image_entropy(step4_re_cubic, "Restored (Bicubic Interpolation) After Discretization Step 4:")
cv2.imwrite('step2_re_cubic.png', step2)
cv2.imwrite('step4_re_cubic.png', step4)
quantized_image_8_levels = uniform_quantization(image, 8)
quantized_image_16_levels = uniform_quantization(image, 16)
quantized_image_64_levels = uniform_quantization(image, 64)
relative_entropy(image, quantized_image_8_levels, "8 levels")
print_image_entropy(quantized_image_8_levels, "8 levels (After 8-bit Quantization):")
relative_entropy(image, quantized_image_16_levels, "16 levels")
print_image_entropy(quantized_image_16_levels, "16 levels (After 8-bit Quantization):")
relative_entropy(image, quantized_image_64_levels, "64 levels")
print_image_entropy(quantized_image_64_levels, "64 levels (After 8-bit Quantization):")
quantized_step2_8_levels = uniform_quantization(step2, 8)
quantized_step2_16_levels = uniform_quantization(step2, 16)
quantized_step2_64_levels = uniform_quantization(step2, 64)
quantized_step4_8_levels = uniform_quantization(step4, 8)
quantized_step4_16_levels = uniform_quantization(step4, 16)
quantized_step4_64_levels = uniform_quantization(step4, 64)
cv2.imwrite('quantized_image_8_levels.png', quantized_image_8_levels)
cv2.imwrite('quantized_image_16_levels.png', quantized_image_16_levels)
cv2.imwrite('quantized_image_64_levels.png', quantized_image_64_levels)
cv2.imwrite('quantized_step2_8_levels.png', quantized_step2_8_levels)
cv2.imwrite('quantized_step2_16_levels.png', quantized_step2_16_levels)
cv2.imwrite('quantized_step2_64_levels.png', quantized_step2_64_levels)
cv2.imwrite('quantized_step4_8_levels.png', quantized_step4_8_levels)
cv2.imwrite('quantized_step4_16_levels.png', quantized_step4_16_levels)
cv2.imwrite('quantized_step4_64_levels.png', quantized_step4_64_levels)
print_image_entropy(quantized_image_8_levels, "8 levels (After Quantization):")
relative_entropy(image, quantized_image_8_levels, "8 levels (After 8-bit Quantization)")
print_image_entropy(quantized_image_16_levels, "16 levels (After Quantization):")
relative_entropy(image, quantized_image_16_levels, "16 levels (After 16-bit Quantization)")
print_image_entropy(quantized_image_64_levels, "64 levels (After Quantization):")
relative_entropy(image, quantized_image_64_levels, "64 levels (After 64-bit Quantization)")
print_image_entropy(quantized_step2_8_levels, "8 levels (After 2x Discretization):")
relative_entropy(step2, quantized_step2_8_levels, "8 levels (After 8-bit Quantization)")
print_image_entropy(quantized_step2_16_levels, "16 levels (After 2x Discretization):")
relative_entropy(step2, quantized_step2_16_levels, "16 levels (After 16-bit Quantization)")
print_image_entropy(quantized_step2_64_levels, "64 levels (After 2x Discretization):")
relative_entropy(step2, quantized_step2_64_levels, "64 levels (After 64-bit Quantization)")
print_image_entropy(quantized_step4_8_levels, "8 levels (After 4x Discretization):")
relative_entropy(step4, quantized_step4_8_levels, "8 levels (After 8-bit Quantization)")
print_image_entropy(quantized_step4_16_levels, "16 levels (After 4x Discretization):")
relative_entropy(step4, quantized_step4_16_levels, "16 levels (After 16-bit Quantization)")
print_image_entropy(quantized_step4_64_levels, "64 levels (After 4x Discretization):")
relative_entropy(step4, quantized_step4_64_levels, "64 levels (After 64-bit Quantization)")
