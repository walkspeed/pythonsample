import pluginsMgr
from Screens.Screen import Screen
from Components.Label import Label
from Components.ActionMap import ActionMap

INFOMSG_DLG = """<screen position="center,center" size="500,370" title="InfoMsg Dialog" >
                 <widget name="labelInfo" position="center,center" size="450,320" font="Regular;20" transparent="1" foregroundColor="#f2e000" halign="center" />
                 </screen>"""
class InfoMsg(Screen):
    def __init__(self,session):
        Screen.__init__(self,session)
        self.skin = INFOMSG_DLG

        self['labelInfo'] = Label("This is InfoMsg Dialog\nThis is a sample!")

        self["actions"] = ActionMap(["OkCancelActions"],
        {
            "cancel": self.Exit,
            "ok": self.Exit,
        }, 1)
    def Exit(self):
        self.close()

def main(session, **kwargs):
    session.open(InfoMsg)

desclist = [{'name':_("InfoMsg"), 'description':_("InfoMsg sample"), 'where':pluginsMgr.WHERE_PLUGINMENU, 'needsRestart':False, 'fnc':main}]

Plugins = pluginsMgr.createPlugins(desclist);
