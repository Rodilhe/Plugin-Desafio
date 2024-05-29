import wx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.widgets import Button, RectangleSelector
import numpy as np
from scipy.signal import lfilter
from scipy import signal

import wx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RectangleSelector
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import re

from scipy.signal import butter, lfilter, filtfilt

class GraphFrame(wx.Frame):
    def __init__(self, parent, title, curve_data, well, datatype):
        super(GraphFrame, self).__init__(parent, title=title, size=(800, 650))
        self.curve_data = curve_data
        self.zoom_selected = None
        self.plots = []  # Lista para armazenar os objetos de linha
        self.plot_alphas = []  # Lista para rastrear a transparência dos gráficos

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Criar um gráfico usando matplotlib
        self.figure, self.axes = plt.subplots()

        self.plot_curve(curve_data, well[0][1], datatype, None)

        # Adicionar o gráfico à janela
        self.canvas = FigureCanvas(panel, -1, self.figure)

        vbox.Add(self.canvas, proportion=1, flag=wx.EXPAND)

        # Adicionar um campo de texto para exibir as coordenadas do ponto selecionado
        self.coordinates_text = wx.TextCtrl(panel, style=wx.TE_READONLY)
        vbox.Add(self.coordinates_text, flag=wx.EXPAND)

        panel.SetSizer(vbox)
        self.Centre()

        # Adicionar botões
        self.add_buttons(curve_data)

        # Variáveis para armazenar as coordenadas do ponto marcado
        self.marked_point = None

        # Conectar evento de clique do mouse ao método on_pick
        self.canvas.mpl_connect('button_press_event', self.on_pick)

    def plot_curve(self, curve_data, well, datatype, filtro):
        # Plotar os dados da curva
        if well and datatype is not None:
            label = f'{well} - {datatype}'
        elif filtro is not None:
            label = f'{filtro}'
        
        plot, = self.axes.plot(curve_data, np.arange(0, len(curve_data)), label=label)  # Troca de coordenadas / '''range(len(curve_data))'''
        self.plots.append(plot)  # Adiciona à lista de gráficos
        self.plot_alphas.append(1)  # Define a transparência como 1 por padrão

        self.axes.set_ylabel('Índice')  # Troca do rótulo do eixo y
        self.axes.set_xlabel('Valor')  # Troca do rótulo do eixo x
        if well and datatype is not None:
            self.axes.set_title(f'Poço: {well}\nCurva Selecionada: {datatype}')
        self.axes.grid(True)
        self.axes.legend(loc='upper right')

    def toggle_plot_visibility(self, index):
        # Toggle visibility of the plot at the given index
        if 0 <= index < len(self.plots):
            self.plot_alphas[index] = 1 - self.plot_alphas[index]  # Toggle entre 0 e 1
            self.plots[index].set_alpha(self.plot_alphas[index])  # Define a transparência
            self.canvas.draw()

    def add_buttons(self, curve_data):
        # Criar botões e adicionar ao gráfico
        ax_zoom = plt.axes([0.9, 0.85, 0.09, 0.03])  # Botão para habilitar zoom
        ax_reset = plt.axes([0.9, 0.8, 0.09, 0.03])  # Botão para redefinir os graficos
        ax_filtro = plt.axes([0.9, 0.75, 0.09, 0.03])  # Botão para adicionar filtro
        ax_toggle = plt.axes([0.9, 0.7, 0.09, 0.03])  # Botão para habilitar/desabilitar um gráfico
        ax_legend = plt.axes([0.9, 0.65, 0.09, 0.03])  # Botão para mostrar/ocultar a legenda
        ax_save = plt.axes([0.9, 0.50, 0.09, 0.03])  # Botão para mostrar/ocultar a legenda


        self.zoom_button = Button(ax_zoom, 'Zoom')
        self.reset_button = Button(ax_reset, 'Reset')
        self.add_filtro = Button(ax_filtro, 'Add filter')
        self.toggle_plot_button = Button(ax_toggle, 'Toggle Plot')  # Novo botão
        self.legend_button = Button(ax_legend, 'Legend')  # Botão para a legenda
        self.save_button = Button(ax_save, 'Save pick')

        self.zoom_button.on_clicked(self.toggle_zoom)
        self.reset_button.on_clicked(self.reset_zoom)
        self.add_filtro.on_clicked(self.open_filter_dialog)
        self.toggle_plot_button.on_clicked(self.toggle_plot_visibility_dialog)  # Conectar ao novo método
        self.legend_button.on_clicked(self.toggle_legend_visibility)  # Conectar ao método para mostrar/ocultar a legenda
        self.save_button.on_clicked(self.save_pick)  # Salvar imagem

    def save_pick(self, event):
        with wx.FileDialog(self, "Salvar imagem", wildcard="PNG files (*.png)|*.png",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # O usuário cancelou o diálogo

            # Obter o caminho do arquivo
            pathname = fileDialog.GetPath()
            try:
                # Salvar a figura no caminho selecionado
                self.figure.savefig(pathname)
                wx.MessageBox(f'Imagem salva em: {pathname}', 'Info', wx.OK | wx.ICON_INFORMATION)
            except IOError:
                wx.LogError(f"Não foi possível salvar a imagem em {pathname}")

    def toggle_legend_visibility(self, event):
        # Toggle para mostrar/ocultar a legenda
        if self.axes.legend_ is None:
            self.axes.legend(loc='upper right')
        else:
            self.axes.legend_.remove()
        self.canvas.draw()

    def toggle_plot_visibility_dialog(self, event):
        # Diálogo para selecionar qual gráfico habilitar/desabilitar
        dlg = wx.SingleChoiceDialog(None, 'Selecione um gráfico:', 'Toggle Plot', [f'Gráfico {self.plots[i]._label}' for i in range(len(self.plots))])

        if dlg.ShowModal() == wx.ID_OK:
            index = dlg.GetSelection()
            self.toggle_plot_visibility(index)

        dlg.Destroy()

    def toggle_zoom(self, event):
        self.zoom_selected = 1
        if hasattr(self, 'selector') and not self.selector.active:
            self.selector.set_active(True)
        else:
            self.selector = RectangleSelector(self.axes, self.zoom_callback,
                                               drawtype='box', useblit=True,
                                               button=[1],  # Left mouse button
                                               minspanx=5, minspany=5,
                                               spancoords='pixels',
                                               interactive=True,
                                               rectprops=dict(facecolor='blue', alpha=0.5))

    def zoom_callback(self, eclick, erelease):
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        self.axes.set_xlim(min(x1, x2), max(x1, x2))
        self.axes.set_ylim(min(y1, y2), max(y1, y2))
        self.canvas.draw()
        # Desativar o seletor de zoom após a seleção
        self.selector.set_active(False)
        self.zoom_selected = None

    def reset_zoom(self, event):
        self.axes.relim()
        self.axes.autoscale()
        self.canvas.draw()

    def on_pick(self, event):
        if self.zoom_selected == None:
            if event.inaxes == self.axes:
                if self.marked_point:
                    # Remover o ponto anterior se existir
                    self.marked_point.remove()
                # Adicionar um novo ponto
                self.marked_point = self.axes.plot(event.xdata, event.ydata, 'ro')[0]
                self.canvas.draw()

                # Exibir as coordenadas do ponto selecionado no campo de texto
                self.coordinates_text.SetValue(f'Coordenadas: x={event.xdata:.2f}, y={event.ydata:.2f}')

    def open_filter_dialog(self, event):
        dlg = FilterConfigDialog(self)
        dlg.ShowModal()
        dlg.Destroy()


    def math_operation(self, formula):
        # Implementação da operação matemática nos dados do gráfico
        try:
            operator = formula[0]  # Primeiro caractere é o operador
            value = float(formula[1:])  # Restante da string é o valor

            if operator == '*':
                resultado = [x * value for x in self.curve_data]
            elif operator == '/':
                resultado = [x / value for x in self.curve_data]
            elif operator == '+':
                resultado = [x + value for x in self.curve_data]
            elif operator == '-':
                resultado = [x - value for x in self.curve_data]
            else:
                raise ValueError("Operador inválido")

            # Plotar os dados resultantes
            self.plot_curve(resultado, None, None, f"Operação Matemática (Fórmula aplicada: {formula})")
            
        except Exception as e:
            # Captura e exibe detalhes do erro
            mensagem_erro = f"Erro ao calcular a expressão '{formula}': {str(e)}"
            wx.MessageBox(mensagem_erro, "Erro", wx.OK | wx.ICON_ERROR)

    def filtro_passa_banda(self):
        # Definindo as frequências de corte (ajustar conforme necessário)
        lowcut = 5  # Frequência de corte baixa em Hz
        highcut = 100 # Frequência de corte alta em Hz
        sampling_rate = 1000  # Número de amostras coletadas por segundo
        order = 4

        processor = SignalProcessor(self.curve_data)
        filtered_data = processor.apply_filter(lowcut, highcut, sampling_rate, order)

        # Plotando os dados filtrados
        self.plot_curve(filtered_data, None, None, f"Filtro Passa-Banda")
        self.canvas.draw()  # Adiciona esta linha para atualizar o canvas


if __name__ == '__main__':
    app = wx.App()
    data = [1, 2, 3, 4, 5]
    well = [("Well1", "Data1")]
    frame = GraphFrame(None, "Graph", data, well, "Data1")
    frame.Show()
    app.MainLoop()


class FilterConfigDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        super(FilterConfigDialog, self).__init__(*args, **kw)
        self.InitUI()

    def InitUI(self):
        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        math_btn = wx.Button(pnl, label='Math')
        math_btn.Bind(wx.EVT_BUTTON, self.on_math_btn)

        filter_btn = wx.Button(pnl, label='Filtro Passa Banda')
        filter_btn.Bind(wx.EVT_BUTTON, self.on_filter_btn)

        vbox.Add(math_btn, 0, wx.ALL, 5)
        vbox.Add(filter_btn, 0, wx.ALL, 5)

        pnl.SetSizer(vbox)

        self.SetSize((250, 150))
        self.SetTitle('Configurar Filtro')

    def on_math_btn(self, event):
        formula = wx.TextEntryDialog(self, 'Digite a formula: ', '(Ex: "+ 2")', '')
        if formula.ShowModal() == wx.ID_OK:
            formula_str = formula.GetValue()
            formula.Destroy()
            try:               
                self.GetParent().math_operation(formula_str)
            except Exception as e:
                wx.MessageBox(str(e), "Erro", wx.OK | wx.ICON_ERROR)
        else:
            formula.Destroy()

    def on_filter_btn(self, event):
            try:              
                self.GetParent().filtro_passa_banda()
            except Exception as e:
                wx.MessageBox(str(e), "Erro", wx.OK | wx.ICON_ERROR)



class SignalProcessor:
    def __init__(self, curve_data):
        self.curve_data = curve_data

    def butter_bandpass(self, lowcut, highcut, sampling_rate, order=3):
        nyq = 0.5 * sampling_rate
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='bandpass')
        return b, a

    def butter_bandpass_filter(self, waveform, lowcut, highcut, sampling_rate, order=3):
        b, a = self.butter_bandpass(lowcut, highcut, sampling_rate, order)
        y = filtfilt(b, a, waveform)
        return y

    def apply_filter(self, lowcut, highcut, sampling_rate, order=4):
        filtered_data = self.butter_bandpass_filter(self.curve_data, lowcut, highcut, sampling_rate, order)
        return filtered_data