# -*- coding: UTF-8 -*-
import subprocess
import json
import yaml
import sys
import os
import io

def addDependency(podfileDic,itemKey,itemVaule):
  dependencyDic = podfileDic['dependency'].update({itemKey,itemVaule})
  return dependencyDic

def deleteDependency(podfileDic,itemKey):
  del podfileDic['dependency'][itemKey]
  dependencyDic = podfileDic['dependency']
  return dependencyDic

def addSource(podfileDic,addSourceStr):
  sourceList = podfileDic['source'] 
  if addSourceStr not in sourceList:
    sourceList.append(addSourceStr)    
  return sourceList

def deleteSource(podfileDic,delSourceStr):
  sourceList = podfileDic['source'] 
  if delSourceStr in sourceList:
    sourceList.remove(delSourceStr)
  return sourceList

def modifyTargetName(podfileDic):
  return 1
def analysisPodfile(podfilePath):
  # 创建yaml文件 
  cwd = os.getcwd()
  podfile_yaml_path = cwd + "/podfile-yaml.yaml"
  podfile_yaml = open(podfile_yaml_path,'w+')  
  print (podfile_yaml_path)
  cmd = "pod ipc podfile %s" % podfilePath

  output = subprocess.check_output(cmd.split()).decode()

  podfile_yaml.write(output)
  podfile_yaml.close()
  # 解析yaml文件
  podfile_yaml = open(podfile_yaml_path)
  yamldir = yaml.load(podfile_yaml)

  yaml_sources = yamldir['sources']

  yaml_dependencies = yamldir['target_definitions'][0]['children'][0]['dependencies']

  yaml_targetName = yamldir['target_definitions'][0]['children'][0]['name']
  # 解析dependencies 方便调用
  yaml_dependencies_dic = dict() 

  for items in yaml_dependencies:
    key =  list(items.keys())[0]
    value = list(items[key])[0]
    yaml_dependencies_dic.update({key:value})
  podfileDic = {'source':yaml_sources,'dependency':yaml_dependencies_dic,'targetName':yaml_targetName}

  return podfileDic

def operationPodfile(podfileDic,modifyDic):
  modifySourceDic = modifyDic['source']
  modifyTargetName = modifyDic['targetName']
  modifyDependencyDic = modifyDic['dependency']

  for itemKey in modifySourceDic.keys():
    if modifySourceDic[itemKey] == 1 :
      podfileDic['source'] = addSource(podfileDic,itemKey)
    else:
      podfileDic['source'] = deleteSource(podfileDic,itemKey)
  
  for dependencyItemKey in modifyDependencyDic.keys():
    if modifyDependencyDic[dependencyItemKey]:
      podfileDic['dependency'] = addDependency(podfileDic,dependencyItemKey,modifyDependencyDic[dependencyItemKey])
    else:
      podfileDic['dependency'] = deleteDependency(podfileDic,dependencyItemKey)

  

      
      
      

  return newPodfileDic
if __name__ == '__main__':
  # add delete modify
  # operation = sys.argv[1]
  operation = 'add'

  # dependency source tergetName
  # operationType = sys.argv[2]
  operationType = 'dependency'

  # Podfile Path
  # podfilePath = sys.argv[3]
  podfilePath= "/Users/sdk-dev/Documents/GITLAB/GFSDKMainland_Main/GFSDKMainLand/Podfile"
  # modify JSON
  jsonPath = "/Users/sdk-dev/Desktop/scripts/podfilePython/PodfileTool/modify.json"
  # 解析Podfile文件 转换为dic
  podfileDic = analysisPodfile(podfilePath)
  # 解析modify.json 转换为dic
  jsonFile = open(jsonPath)
  jsonDic = json.load(jsonFile)
  # 调用通过字符串拼接
  print (jsonDic)
  # defStr = operation+operationType.capitalize()
  # mod    = sys.modules['__main__']  
  # defAttribute=getattr(mod,defStr)
  # defReturn   = defAttribute(podfileDic,modifyDic)

  # newPodfileDic = operationPodfile(podfileDic,modifyDic)

    
    