import numpy as np
from scipy.spatial.transform import Rotation as R


def rotation_6d_to_matrix(rot_6d: np.ndarray) -> np.ndarray:
    """
    将6D旋转表示转换为3x3旋转矩阵(使用Gram-Schmidt正交化)

    参数:
        rot_6d: numpy array of shape (..., 6)

    返回:
        numpy array of shape (..., 3, 3)
    """
    assert rot_6d.shape[-1] == 6, "输入必须是6D向量"

    # 拆分为两个3D向量
    a1 = rot_6d[..., 0:5:2]
    a2 = rot_6d[..., 1:6:2]

    # 第一个向量归一化
    b1 = a1 / np.linalg.norm(a1, axis=-1, keepdims=True)

    # 第二个向量去掉在b1上的投影，然后归一化
    dot = np.sum(b1 * a2, axis=-1, keepdims=True)  # 点积
    proj = dot * b1
    b2 = a2 - proj
    b2 = b2 / np.linalg.norm(b2, axis=-1, keepdims=True)

    # 第三个向量是叉乘
    b3 = np.cross(b1, b2)

    # 拼接为旋转矩阵，列向量形式
    # 最终形状 (..., 3, 3)
    # print(b1.shape, b2.shape, b3.shape)
    matrix = np.stack([b1, b2, b3], axis=-1)

    return matrix


def abs_6d_2_abs_euler(action):
    # left
    # print(action.shape)
    left_xyz = action[0:3]
    left_6d = action[3:9]
    left_grip = action[9]

    # right
    right_xyz = action[10:13]
    right_6d = action[13:19]
    right_grip = action[19]

    # 6d to euler
    left_matrix = rotation_6d_to_matrix(left_6d)
    right_matrix = rotation_6d_to_matrix(right_6d)
    # left_matrix = np.dot(rotation_6d_to_matrix(left_6d),np.array([[0,0,1],[0,1,0],[-1,0,0]]))
    # right_matrix = np.dot(rotation_6d_to_matrix(right_6d),np.array([[0,0,1],[0,1,0],[-1,0,0]]))

    left_euler = R.from_matrix(left_matrix).as_euler("xyz", degrees=False)
    right_euler = R.from_matrix(right_matrix).as_euler("xyz", degrees=False)

    return np.concatenate(
        [left_xyz, left_euler, [left_grip], right_xyz, right_euler, [right_grip]]
    )


def rotation_matrix_to_6d(R):
    """
    将旋转矩阵 R 转换为 6D 旋转表示
    通过提取旋转矩阵的前六个元素
    """
    return np.concatenate([R[0, :2], R[1, :2], R[2, :2]])


def eef_6d_new_reg(puppet_arm_left_pose, puppet_arm_right_pose):
    position_left = np.array(puppet_arm_left_pose[0:3])
    position_right = np.array(puppet_arm_right_pose[0:3])
    orientation_quat_left = puppet_arm_left_pose[3:6]
    orientation_quat_right = puppet_arm_right_pose[3:6]
    gripper_left = np.array([puppet_arm_left_pose[6]])
    gripper_right = np.array([puppet_arm_right_pose[6]])
    matrix_left = R.from_euler("xyz", orientation_quat_left, degrees=False).as_matrix()
    matrix_right = R.from_euler(
        "xyz", orientation_quat_right, degrees=False
    ).as_matrix()
    left_6d = rotation_matrix_to_6d(matrix_left)
    right_6d = rotation_matrix_to_6d(matrix_right)
    return np.concatenate(
        (position_left, left_6d, gripper_left, position_right, right_6d, gripper_right),
        axis=0,
    )
