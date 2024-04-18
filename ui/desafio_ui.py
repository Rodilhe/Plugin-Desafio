import wx
from plugins.Desafio.db.database import Database
from classes.om import ObjectManager
from plugins.Desafio.core.core import DesafioCore
from collections import defaultdict

class DesafioFrame(wx.Frame):
    def __init__(self, *args, **kw):
        #wells = kw.pop('wells', [])
        OM = kw.pop('OM', [])
        #self.wells = OM.list('well')
        self.waves = OM.list('log')
        self.params = OM._data
        om = ObjectManager
        self.params = om._data


        # Organizando os dados
        wells = defaultdict(lambda: defaultdict(list))
        well_atual = None

        for key, value in self.params.items():
            if key[0] == 'well':
                well_id = key[1]
                well_name = value.name  # Assumindo que o nome está no próprio value
                well_atual = well_id, well_name
            else:
                if key[0] == 'log':
                    wells[well_atual][key[0]].append(value)
                else:
                    wells[well_atual][key[0]] = value              

        '''
        super(DesafioFrame, self).__init__(*args, **kw)

        panel = wx.Panel(self)


        self.wells_combo = wx.ComboBox(panel, style=wx.CB_READONLY)
        self.wells_combo.AppendItems(["Poço " + str(well.uid[1]) + " : " + str(well.name) for well in self.wells])
        '''
        # Convertendo o defaultdict para um dicionário padrão
        wells = dict(wells)
        self.db = Database()

        super(DesafioFrame, self).__init__(*args, **kw)

        panel = wx.Panel(self)

        self.wells_combo = wx.ComboBox(panel, style=wx.CB_READONLY)
        # Adicionando os itens ao ComboBox com os nomes das wells
        for well in wells.items():
            self.wells_combo.Append("Poço "+ str(well[0][0]) +" : "+ str(well[0][1]))  # Adicionando o nome do poço e seu id ao ComboBox

        self.info_panel = wx.Panel(panel)
        self.info_text = wx.StaticText(self.info_panel, label='Selecione um poço para ver as informações')
        
        self.run_button = wx.Button(panel, label='Calcular End - Start')
        self.result_text = wx.StaticText(panel, label='Resultado: ')   

        self.run_button.Bind(wx.EVT_BUTTON, self.on_run)
        self.wells_combo.Bind(wx.EVT_COMBOBOX, self.on_combo_selection)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(panel, label='Selecione um poço:'), 0, wx.ALL, 5)
        sizer.Add(self.wells_combo, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.info_panel, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.run_button, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.result_text, 0, wx.EXPAND | wx.ALL, 5)        

        self.info_panel.SetMinSize((50, 80))

        panel.SetSizer(sizer)

        self.Center()

    def on_run(self, event):
        selected_well_index = self.wells_combo.GetSelection()
        if selected_well_index != wx.NOT_FOUND:
            selected_well = self.wells_combo.GetString(selected_well_index)
            well_index = int(selected_well.split()[1])  # Extrai o índice do poço selecionado            
            values_with_well_index = [value for key, value in self.params.items() if key[1] == well_index]
            end = values_with_well_index[2].end
            start = values_with_well_index[2].start
            end_start_diff = end - start
            self.result_text.SetLabel(f'Resultado: {end_start_diff}')
            self.db.save_result(well_index, end_start_diff)

    def on_combo_selection(self, event):
        selected_well_index = self.wells_combo.GetSelection()
        if selected_well_index != wx.NOT_FOUND:
            selected_well = self.wells_combo.GetString(selected_well_index)
            well_index = int(selected_well.split()[1])  # Extrai o índice do poço selecionado  
            well_info = self.get_well_info(well_index, self.params)
            self.result_text.SetLabel(f'Resultado: ')
            
            # Concatena todas as informações
            info_text = f"Data type: {well_info.datatype}\n" \
                        f"Samples: {well_info.samples}\n" \
                        f"Start: {well_info.start}\n" \
                        f"End: {well_info.end}"
                        
            # Define o rótulo do StaticText com todas as informações
            self.info_text.SetLabel(info_text)

    def get_well_info(self, well_index, params):
        # Aqui você pode acessar as informações do poço com o índice well_index na variável params
        # Por exemplo, se params for um dicionário, você pode acessar as informações assim:
        # return params[('well', well_index)].info()
        # Supondo que o método info() retorna um objeto com as informações do poço
        values_with_well_index = [value for key, value in params.items() if key[1] == well_index]
        return values_with_well_index[2]  # Retorna o objeto com as informações do poço