# -*- coding: UTF-8 -*-
import subprocess
import yaml
import sys
import os

# podfilePath= sys.argv[1]
podfilePath= "/Users/sdk-dev/Documents/GITLAB/GFSDKMainland_Main/GFSDKMainLand/Podfile"

# 创建yaml文件 
cwd = os.getcwd()
podfile_yaml_path = cwd + "/podfile-yaml.yaml"
podfile_yaml = open(podfile_yaml_path,'w+')  
print podfile_yaml_path
cmd = "pod ipc podfile %s" % podfilePath

output = subprocess.check_output(cmd.split())

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
  key = items.keys()[0]
  value = items[key][0]
  yaml_dependencies_dic.update({key:value})

print yaml_dependencies_dic

# 生成Podfile
podfile = open("Podfile",'w+')
# source  部分
sourceStr = ""
for source_path in yaml_sources:
  sourceStr += "source %s \n"% source_path

dependenciesStr = ""
for key in yaml_dependencies_dic.keys():
  dependenciesStr += "pod '%s' , '%s' \n" %(key,yaml_dependencies_dic[key])

podfileStr = "%starget '%s' do \n%send\n" %(sourceStr,yaml_targetName,dependenciesStr)

podfile.write(podfileStr)





