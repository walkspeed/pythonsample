# -*- coding:utf-8 -*-

"""
背景知识
***************************************************************************************************************************************************************************************************
e2的每个插件必须有一个plugin.py文件
plugin.py中必须有一个函数Plugins,完成将PluginDescriptor对象列表导出

def Plugins(**kwargs):
	return [
		PluginDescriptor(name = _("Media player"), description = _("Play back media files"), where = PluginDescriptor.WHERE_PLUGINMENU, icon="MediaPlayer.png", needsRestart = False, fnc = main),
		PluginDescriptor(name = _("Media player"), where = PluginDescriptor.WHERE_MENU, needsRestart = False, fnc = audiocdscan),
		PluginDescriptor(name = _("Media player"), description = _("Play back media files"), where = PluginDescriptor.WHERE_MENU, needsRestart = False, fnc = menu)
	]

PluginDescriptor类的构造函数声明
def __init__(self, name="Plugin", where=None, description="", icon=None, fnc=None, wakeupfnc=None, needsRestart=None, internal=False, weight=0)
****************************************************************************************************************************************************************************************************
使用
createPlugins是入口函数。
参数是一个列表，列表的项是一个字典，字典内容是PluginDescriptor类的构造函数参数的命名输入的键值对。如下

[{'name':_("Media player"), 'description':_("Play back media files"), 'where':PluginDescriptor.WHERE_PLUGINMENU, 'icon':"MediaPlayer.png", 'needsRestart':False, 'fnc':main},
 'name':_("Media player"), 'where':PluginDescriptor.WHERE_MENU, 'needsRestart':False, 'fnc':audiocdscan]

将如上列表作为参数给createPlugins

使用的文件必须有如下的一句话
Plugins = createPlugins();
必须有一个名为Plugins的全局对象
"""
from Plugins.Plugin import PluginDescriptor

WHERE_PLUGINMENU = PluginDescriptor.WHERE_PLUGINMENU

class PluginsMate:
    def __init__(self,descriptions=[]):
        self.pdlist = []
        for i in range(len(descriptions)):
            param = descriptions[i]
            item = PluginDescriptor(**param)
            self.pdlist.append(item)
        return
    def __call__(self,**kwargs):
        return self.pdlist

def createPlugins( descriptions ):
    return PluginsMate( descriptions )
