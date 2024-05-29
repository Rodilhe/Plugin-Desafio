import wx
from plugins.Desafio.db.database import Database
from classes.om import ObjectManager
from plugins.Desafio.core.core import DesafioCore
from plugins.Desafio.ui.plotCurva import GraphFrame
from collections import defaultdict
from classes.ui import UIManager
from classes.ui import repr_line
from classes.om import well

class DesafioFrame(wx.Frame):
    def __init__(self, *args, **kw):
        #wells = kw.pop('wells', [])
        OM = kw.pop('OM', [])
        self.waves = OM.list('log')
        om = ObjectManager
        self.params = om._data
        #item = self.params[('well', 1)]
        self.curvas = None
        self.selected_well = None
        
        


        # Organizando os dados
        self.wells = defaultdict(lambda: defaultdict(list))
        well_atual = None
        validator = False

        for key, value in self.params.items():
            if key[0] == 'well':
                id = key[1]
                name = value.name  # Assumindo que o nome está no próprio value
                well_atual = id, name
                validator = True
                
            else:
                if key[0] == 'log':
                    self.wells[well_atual][key[0]].append(value)
                else:
                    self.wells[well_atual][key[0]] = value              

        # Convertendo o defaultdict para um dicionário padrão
        self.wells = dict(self.wells)
        self.db = Database()
        
        '''
        om = ObjectManager()
        self.well = om.new('well', item)        
        om.add(self.well)
        '''
        super(DesafioFrame, self).__init__(*args, **kw)

        panel = wx.Panel(self)

        self.wells_combo = wx.ComboBox(panel, style=wx.CB_READONLY)
        # Adicionando os itens ao ComboBox com os nomes das wells
        self.addItemsToWellCombo()
        
        '''
        self.info_panel = wx.Panel(panel)
        self.info_text = wx.StaticText(self.info_panel, label='Selecione um poço para ver as informações')
        '''

        self.curvas_combo = wx.ComboBox(panel, style=wx.CB_READONLY)
        

        self.run_button = wx.Button(panel, label='Exibir curva slecionada') 

        self.run_button.Bind(wx.EVT_BUTTON, self.on_run)
        self.wells_combo.Bind(wx.EVT_COMBOBOX, self.on_combo_selection)

        

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(panel, label='Selecione um poço:'), 0, wx.ALL, 5)
        sizer.Add(self.wells_combo, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.curvas_combo, 0, wx.EXPAND | wx.ALL, 5)
        #sizer.Add(self.info_panel, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.run_button, 0, wx.EXPAND | wx.ALL, 5)      

        #self.info_panel.SetMinSize((50, 80))

        panel.SetSizer(sizer)

        self.Center()

    def on_run(self, event):
        selected_curva_combo = self.curvas_combo.GetSelection()
        if selected_curva_combo != wx.NOT_FOUND:
            selected_curva_data = self.curvas[selected_curva_combo].data  # Obter os dados da curva selecionada
            datatype = self.curvas[selected_curva_combo].datatype

            # Abrir uma nova janela com o gráfico da curva selecionada
            graph_frame = GraphFrame(None, "Gráfico da Curva", selected_curva_data, self.selected_well, datatype)
            graph_frame.Show()
            
    def on_combo_selection(self, event):
        self.curvas_combo.Clear()
        selected_well_index = self.wells_combo.GetSelection()
        if selected_well_index != wx.NOT_FOUND:
            selected_well = self.wells_combo.GetString(selected_well_index)
            well_index = int(selected_well.split()[1])  # Extrai o índice do poço selecionado  
            well_info = self.get_well_info(well_index, self.params)
            

            self.selected_well = self.buscar_por_valor(selected_well)
            self.curvas = self.selected_well[1]['log']
            curvas = self.curvas
            # Substituindo info_text pelos itens da lista curvas
            info_text = ""
            for chave in curvas:
                info_text += f"Curva: " + str(chave.datatype) + "\n"

            
            for curva in self.curvas:
                self.curvas_combo.Append("Curva: "+ curva.datatype)

            # Removendo o último caractere de quebra de linha
            info_text = info_text.rstrip('\n')


            # Define o rótulo do StaticText com todas as informações
            #self.info_text.SetLabel(info_text)

    def get_well_info(self, well_index, params):
        # Aqui você pode acessar as informações do poço com o índice well_index na variável params
        # Por exemplo, se params for um dicionário, você pode acessar as informações assim:
        # return params[('well', well_index)].info()
        # Supondo que o método info() retorna um objeto com as informações do poço
        values_with_well_index = [value for key, value in params.items() if key[1] == well_index]
        return values_with_well_index[2]  # Retorna o objeto com as informações do poço
        
    def buscar_por_valor(dic, valor):
        partes = valor.split(':')
        if len(partes) >= 2:
            informacao = partes[1].strip()
            for chave in dic.wells.items():
                c = chave[0][1]
                if c== informacao:
                    return chave
            return None    
        
    def addItemsToWellCombo(self):
        for well in self.wells.items():
            self.wells_combo.Append("Poço "+ str(well[0][0]) +" : "+ str(well[0][1]))  # Adicionando o nome do poço e seu id ao ComboBox

