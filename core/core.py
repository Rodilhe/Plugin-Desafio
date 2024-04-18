import wx
from plugins.Desafio.db.database import Database
from classes.om import ObjectManager

class DesafioCore:
    def __init__(self, params, db):
        self.params = params
        self.db = db

