#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# importAsset.py
# @Author :  ()
# @Link   : 
# @Date   : 2019/11/18 下午10:14:53

# 导入资产（可以是任意类型资产）


import unreal


# 要导入资产内容的源路径 
asset_path = 'E:\Git_Res\pythonUE4\Assets\Meshes\SM_TableRound.FBX'

# 要导入资产内容的目标路径 
destination_path = '/Game/pyTest/Meshes'

def importAsset():
    asset_task = buildImportTask(asset_path, destination_path)
    executeImportTasks([asset_task])


def buildImportTask(filename,destination_path):
    # https://docs.unrealengine.com/en-US/PythonAPI/class/AssetImportTask.html?highlight=assetimporttask
    task = unreal.AssetImportTask() # 包含要导入的一组资产的数据
    task.automated = True # 避免对话框
    task.destination_name = '' # 导入为的可选自定义名称
    task.destination_path = destination_path # 项目内容目录中将要导入资产的内容路径
    task.filename = filename # 要导入的文件名
    task.replace_existing = True # 覆盖现有资产
    task.save = True # 导入后保存
    
    # task.options # （对象） – [读写]特定于资产类型的导入选项
    task.options = unreal.FbxImportUI()
    task.options.import_as_skeletal = True
    task.options.override_full_name = True
    task.options.mesh_type_to_import = unreal.FBXImportType.FBXIT_SKELETAL_MESH
    task.options.skeletal_mesh_import_data.set_editor_property('update_skeleton_reference_pose', False)
    task.options.skeletal_mesh_import_data.set_editor_property('use_t0_as_ref_pose', True) 
    task.options.skeletal_mesh_import_data.set_editor_property('preserve_smoothing_groups', 1) 
    task.options.skeletal_mesh_import_data.set_editor_property('import_meshes_in_bone_hierarchy', False)
    task.options.skeletal_mesh_import_data.set_editor_property('import_morph_targets', True)
    task.options.skeletal_mesh_import_data.set_editor_property('threshold_position', 0.0002)
    task.options.skeletal_mesh_import_data.set_editor_property('threshold_tangent_normal', 0.0002）
    task.options.skeletal_mesh_import_data.set_editor_property('threshold_uv', 0.001)
    task.options.create_physics_asset = False
    task.options.import_animations = False

    task.options.skeletal_mesh_import_data.set_editor_property('convert_scene', True) 
    task.options.skeletal_mesh_import_data.set_editor_property('force_front_x_axis', False)
    task.options.skeletal_mesh_import_data.set_editor_property('convert_scene_unit', False)

    normal_import_method = unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS_AND_TANGENTS
    normal_generation_method = unreal.FBXNormalGenerationMethod.MIKK_T_SPACE

    task.options.skeletal_mesh_import_data.set_editor_property('normal_generation_method', normal_generation_method)
    task.options.skeletal_mesh_import_data.set_editor_property('normal_import_method', normal_import_method) 
    
    # task.imported_object_paths # （Array（str））：[读写]导入后创建或更新的对象的路径
    return task

# https://api.unrealengine.com/INT/PythonAPI/class/AssetToolsHelpers.html
# https://api.unrealengine.com/INT/PythonAPI/class/AssetTools.html
def executeImportTasks(tasks):
    # 导入方法
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks) # 使用指定的任务导入资产。


if __name__ == "__main__":
    importAsset()