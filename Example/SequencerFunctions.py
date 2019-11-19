#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SequencerFunctions.py
# @Author :  ()
# @Link   : 
# @Date   : 2019/11/19 下午6:40:43

# unreal.MovieSceneSequence
#   https://api.unrealengine.com/INT/PythonAPI/class/MovieSceneSequence.html

# unreal.LevelSequence
#   https://api.unrealengine.com/INT/PythonAPI/class/LevelSequence.html

# unreal.SequencerBindingProxy
#   https://api.unrealengine.com/INT/PythonAPI/class/SequencerBindingProxy.html

import unreal



# 创建LevelSequence资源。
'''
	Summary:
		在指定目录下创建具有给定名称的 level sequence 。这是一个如何创建 level sequence 资源的示例，
		如何将当前映射中的对象添加到序列中，以及如何创建一些示例绑定/etc。
		Creates a level sequence with the given name under the specified directory. This is an example of how to create Level Sequence assets,
		how to add objects from the current map into the sequence and how to create some example bindings/etc.
	Params:
		asset_name - Name of the resulting asset, ie: "MyLevelSequence" 所得资产的名称，即："MyLevelSequence"
		package_path - Name of the package path to put the asest into, ie: "/Game/LevelSequences/" 要将asest放入的包路径的名称
	Returns:
		The created LevelSequence asset. 创建LevelSequence资源。
'''
def create_level_sequence(asset_name, package_path = '/Game/Sequences/'):
    # 创建LevelSequence资源
    sequence = unreal.AssetToolsHelpers.get_asset_tools().create_asset(asset_name, package_path, unreal.LevelSequence, unreal.LevelSequenceFactoryNew())



# 获取定序器，并添加 actor ，返回 actor 绑定的代理
# sequence_path: str : The level sequence asset path 关卡定序器资产路径
# actor: obj unreal.Actor : The actor you want to add into (or get from) the sequence asset 要添加到序列资源中（或从序列资源中获取）的 actor
# return: obj unreal.SequencerBindingProxy : The actor binding 绑定的 actor
def getOrAddPossessableInSequenceAsset(sequence_path='', actor=None):
    sequence_asset = unreal.LevelSequence.cast(unreal.load_asset(sequence_path)) # 绑定 sequence 资产
    possessable = sequence_asset.add_possessable(object_to_possess=actor) # 添加 actor 资产到 sequence
    return possessable


# 向 actor 绑定的代理，添加动画 
# animation_path: str : The animation asset path 动画资源路径
# possessable: obj unreal.SequencerBindingProxy : The actor binding you want to add the animation on 要添加动画的 actor 绑定
# return: obj unreal.SequencerBindingProxy : The actor binding 绑定的 actor
def addSkeletalAnimationTrackOnPossessable(animation_path='', possessable=None):
    # Get Animation 获取动画
    animation_asset = unreal.AnimSequence.cast(unreal.load_asset(animation_path))
    params = unreal.MovieSceneSkeletalAnimationParams() # 电影场景骨骼动画参数
    params.set_editor_property('Animation', animation_asset)
    # Add track 添加轨道
    animation_track = possessable.add_track(track_type=unreal.MovieSceneSkeletalAnimationTrack) # 添加轨道，类型为动画类型
    # Add section 添加动画片段
    animation_section = animation_track.add_section()
    animation_section.set_editor_property('Params', params)
    animation_section.set_range(0, animation_asset.get_editor_property('sequence_length'))


def addSkeletalAnimationTrackOnActor_EXAMPLE():
    sequence_path = '/Game/Mannequin/Animations/ThirdPersonRun'
    actor_path = '/Game/Mannequin/Character/Mesh/SK_Mannequin'
    animation_path = '/Game/Mannequin/Animations/ThirdPersonRun'
    actor_in_world = unreal.GameplayStatics.get_all_actors_of_class(unreal.EditorLevelLibrary.get_editor_world(), unreal.SkeletalMeshActor)()[0]
    possessable_in_sequence = getOrAddPossessableInSequenceAsset(sequence_path, actor_path)
    addSkeletalAnimationTrackOnPossessable(animation_path, possessable_in_sequence)


if __name__ == "__main__":
    create_level_sequence('MyLevelSequence')