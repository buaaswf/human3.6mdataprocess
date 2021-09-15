# -*- coding: utf-8 -*-

import json
import os
import  numpy as np
from bvh_skeleton import  h36m_skeleton,smartbody_skeleton

def write_smartbody_bvh(outbvhfilepath,prediction3dpoint):
    # '''
    #     :param outbvhfilepath: 输出bvh动作文件路径
    #     :param prediction3dpoint: 预测的三维关节点
    #     :return:
    # '''
    # 将预测的点放大100倍
    for frame in prediction3dpoint:
        for point3d in frame:
            # point3d[0] *= 100
            # point3d[1] *= 100
            # point3d[2] *= 100

            # my add
            point3d[0] = point3d[0] / 100
            point3d[1] = point3d[1] / 100
            point3d[2] = point3d[2] / 100

            # 交换Y和Z的坐标
            X = point3d[0]
            Y = point3d[1]
            Z = point3d[2]

            # point3d[0] = -X  # original
            point3d[0] = X
            point3d[1] = Z
            point3d[2] = -Y

    dir_name = os.path.dirname(outbvhfilepath)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    # dir_name = os.path.dirname(outbvhfilepath)
    # basename = os.path.basename(outbvhfilepath)
    # video_name = basename[:basename.rfind('.')]
    # bvhfileDirectory = os.path.join(dir_name, video_name, "bvh")
    # if not os.path.exists(bvhfileDirectory):
    #     os.makedirs(bvhfileDirectory)
    # bvhfileName = os.path.join(dir_name, video_name, "bvh", "{}.bvh".format(video_name))

    SmartBody_skeleton = smartbody_skeleton.SmartBodySkeleton()
    SmartBody_skeleton.poses2bvh(prediction3dpoint, output_file=outbvhfilepath)


def write_standard_bvh(outbvhfilepath,prediction3dpoint):
    # '''
    # :param outbvhfilepath: 输出bvh动作文件路径
    # :param prediction3dpoint: 预测的三维关节点
    # :return:
    # '''
    # 将预测的点放大100倍
    for frame in prediction3dpoint:
        for point3d in frame:
            # my add
            point3d[0] = point3d[0] / 100
            point3d[1] = point3d[1] / 100
            point3d[2] = point3d[2] / 100

            # 交换Y和Z的坐标
            X = point3d[0]
            Y = point3d[1]
            Z = point3d[2]

            point3d[0] = -X
            point3d[1] = Z
            point3d[2] = Y
    dir_name = os.path.dirname(outbvhfilepath)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    # dir_name = os.path.dirname(outbvhfilepath)
    # basename = os.path.basename(outbvhfilepath)
    # video_name = basename[:basename.rfind('.')]
    # bvhfileDirectory = os.path.join(dir_name, video_name, "bvh")
    # if not os.path.exists(bvhfileDirectory):
    #     os.makedirs(bvhfileDirectory)
    # bvhfileName = os.path.join(dir_name, video_name, "bvh", "{}.bvh".format(video_name))
    human36m_skeleton = h36m_skeleton.H36mSkeleton()
    human36m_skeleton.poses2bvh(prediction3dpoint, output_file=outbvhfilepath)
def read_json(file):
    with open(file, 'r') as f:
        temp = json.loads(f.read())
    return temp
def read_points_3d(content):
    flag = 0
    for value in content.values():
        if flag == 0:
            points_3d = np.array(value)[np.newaxis, :, :]
            flag = 1
        else:
            temp = np.array(value)[np.newaxis, :, :]
            points_3d = np.concatenate((points_3d, temp), axis=0)

    return points_3d
if __name__ == '__main__':
    index = [1, 5, 6, 7, 8, 9, 11]
    # index = [5]
    kind = ['camera', 'data', 'joint_3d']
    annotations_dir = '../annotations'
    filelists = os.listdir(annotations_dir)
    for i in index:
        # # camera
        # filename_camera = 'Human36M_subject{}_{}.json'.format(i,kind[0])
        # file_path = os.path.join(annotations_dir, filename_camera)
        # content_camera = read_json(file_path)
        #
        # # data
        # filename_data = 'Human36M_subject{}_{}.json'.format(i, kind[1])
        # file_path = os.path.join(annotations_dir, filename_data)
        # content_data = read_json(file_path)

        # joint_3d
        filename_joint_3d = 'Human36M_subject{}_{}.json'.format(i, kind[2])
        file_path = os.path.join(annotations_dir, filename_joint_3d)
        content_joint_3d = read_json(file_path)

        for content1_key in content_joint_3d.keys():
            for content2_key in content_joint_3d[content1_key].keys():
                content3 = content_joint_3d[content1_key][content2_key]
                points_3d = read_points_3d(content3)

                save_path = './human3.6m/{}/{}_{}.bvh'.format(i, content1_key,content2_key)
                write_smartbody_bvh(save_path, points_3d)
                # write_standard_bvh(save_path, points_3d)
                print(save_path)
                a = 0

