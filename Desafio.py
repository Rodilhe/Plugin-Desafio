import wx
from plugins import DefaultPlugin
from classes.om import ObjectManager
from plugins.Desafio.db.database import Database
from plugins.Desafio.ui.desafio_ui import DesafioFrame

class DesafioPlugin(DefaultPlugin):
    def run(self):
        OM = ObjectManager()
        #wells = OM.list('well')
        app = wx.App()
        frame = DesafioFrame(None, title="Desafio Plugin", OM=OM)
        frame.Show()
        app.MainLoop()

if __name__ == "__main__":
    DesafioPlugin().run()
