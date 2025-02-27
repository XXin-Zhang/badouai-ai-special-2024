import numpy as np
import cv2


def warp_perspective_matrix(src, dst):
    assert src.shape[0] == dst.shape[0] and src.shape[0] >= 4 # assert断言语句

    nums = src.shape[0]
    A = np.zeros((2 * nums, 8))  # A*warp_matrix=B
    B = np.zeros((2 * nums, 1))
    for i in range(0, nums):
        A_i = src[i, :]
        B_i = dst[i, :]
        A[2 * i, :] = [A_i[0], A_i[1], 1, 0, 0, 0,
                       -A_i[0] * B_i[0], -A_i[1] * B_i[0]]
        B[2 * i] = B_i[0]

        A[2 * i + 1, :] = [0, 0, 0, A_i[0], A_i[1], 1,
                           -A_i[0] * B_i[1], -A_i[1] * B_i[1]]
        B[2 * i + 1] = B_i[1]

    A = np.mat(A) # 将A矩阵转换为NumPy的矩阵类型

    # 用A.I求出A的逆矩阵，然后与B相乘，求出warp_matrix
    warp_matrix = A.I * B  # 求出a_11, a_12, a_13, a_21, a_22, a_23, a_31, a_32

    # 之后为结果的后处理
    warp_matrix = np.array(warp_matrix).T[0]
    warp_matrix = np.insert(warp_matrix, warp_matrix.shape[0], values=1.0, axis=0)  # 插入a_33 = 1
    warp_matrix = warp_matrix.reshape((3, 3))
    return warp_matrix


# if __name__ == '__main__':
#     print('warp_matrix')
#     src = [[10.0, 457.0], [395.0, 291.0], [624.0, 291.0], [1000.0, 457.0]]
#     src = np.array(src)
#
#     dst = [[46.0, 920.0], [46.0, 100.0], [600.0, 100.0], [600.0, 920.0]]
#     dst = np.array(dst)
#
#     warp_matrix = warp_perspective_matrix(src, dst)
#     print(warp_matrix)


img = cv2.imread('photo1.jpg')

result3 = img.copy()
src = np.float32([[207, 151], [517, 285], [17, 601], [343, 731]])
dst = np.float32([[0, 0], [337, 0], [0, 488], [337, 488]])
print(img.shape)
# 生成透视变换矩阵；进行透视变换
m = cv2.getPerspectiveTransform(src, dst)
print("warpMatrix:")
print(m)
result = cv2.warpPerspective(result3, m, (337, 488))
cv2.imshow("src", img)
cv2.imshow("result", result)
cv2.waitKey(0)