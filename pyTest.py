#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pyTest.py
# @Author :  ()
# @Link   : 
# @Date   : 2019/11/18 下午9:12:34


import unreal
import os
import tkFileDialog
# Tkinter :https://www.cnblogs.com/cap-rq/p/11207251.html
# tkinter :https://www.cnblogs.com/progor/p/8506513.html

print ('aaa')

def opendir():
    pathname=tkFileDialog.askdirectory() #返回目录名
    print(pathname)

def openfile():
    pathname=tkFileDialog.askopenfilename() #返回文件名
    print(pathname)

def openfiles():
    pathname=tkFileDialog.askopenfilenames() #可以返回多个文件名
    print(pathname)

# root = Tk()
# btn1 = Button(root,text="click",command=opendir)
# btn1.pack()
# root.mainloop()

# 要导入资产内容的源路径 
asset_path = 'E:/Git_Res/pythonUE4/Assets/Meshes/SM_TableRound.FBX'

# 要导入资产内容的目标路径 
destination_path = '/Game/pyTest/Meshes'


# 生成导入任务
# filename: str : 要导入的资源的路径
# destination_path: str : 资产路径
# option: obj : 导入对象选项。对于导入时通常没有弹出窗口的资产，可以为“无”。（如声音、纹理等）
# return: obj : The import task object
def buildImportTask(filename='', destination_path='', options=None):
    # https://docs.unrealengine.com/en-US/PythonAPI/class/AssetImportTask.html?highlight=assetimporttask
    task = unreal.AssetImportTask() # 包含要导入的一组资产的数据
    task.automated = True # 避免对话框
    task.destination_name = '' # 导入为的可选自定义名称
    task.destination_path = destination_path # 项目内容目录中将要导入资产的内容路径
    task.filename = filename # 要导入的文件名
    task.replace_existing = True # 覆盖现有资产
    task.options = options # （对象） – [读写]特定于资产类型的导入选项
    task.save = True # 导入后保存
    
    # task.imported_object_paths # （Array（str））：[读写]导入后创建或更新的对象的路径
    return task


# 建立骨架网格导入选项
# return: obj : Import option object. The basic import options for importing a skeletal mesh 导入选项对象。用于导入骨架网格的基本导入选项
def buildSkeletalMeshImportOptions():
    options = unreal.FbxImportUI()
    # unreal.FbxImportUI
    options.set_editor_property('import_mesh', True)
    options.set_editor_property('import_textures', False)
    options.set_editor_property('import_materials', False)
    options.set_editor_property('import_as_skeletal', True)  # Skeletal Mesh
    # unreal.FbxMeshImportData
    options.skeletal_mesh_import_data.set_editor_property('import_translation', unreal.Vector(0.0, 0.0, 0.0))
    options.skeletal_mesh_import_data.set_editor_property('import_rotation', unreal.Rotator(0.0, 0.0, 0.0))
    options.skeletal_mesh_import_data.set_editor_property('import_uniform_scale', 1.0)
    # unreal.FbxSkeletalMeshImportData
    options.skeletal_mesh_import_data.set_editor_property('import_morph_targets', True)
    options.skeletal_mesh_import_data.set_editor_property('update_skeleton_reference_pose', False)
    return options


# https://api.unrealengine.com/INT/PythonAPI/class/AssetToolsHelpers.html
# https://api.unrealengine.com/INT/PythonAPI/class/AssetTools.html
# 执行导入任务
# tasks: obj List : The import tasks object. You can get them from buildImportTask() 导入任务对象。您可以从buildImportTask（）获取它们
# return: str List : The paths of successfully imported assets 成功导入资产的路径
def executeImportTasks(tasks):
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks) # 使用指定的任务导入资产。
    imported_asset_paths = []
    for task in tasks:
        for path in task.get_editor_property('imported_object_paths'):
            imported_asset_paths.append(path)
    return imported_asset_paths


def importAsset():
    option = buildSkeletalMeshImportOptions()
    asset_task = buildImportTask(asset_path, destination_path, option)
    executeImportTasks([asset_task])


def funtest():
    print('bb')

if __name__ == "__main__":
    funtest()
    opendir()
    openfile()
    openfiles()
