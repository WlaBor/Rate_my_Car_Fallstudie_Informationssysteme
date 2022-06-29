import tkinter as tk
from backend.prognose import Prognose


class ErgebnisFrame(tk.Frame):

    def __init__(self, parent, controller, regression_daten_dic, *args, **kwargs):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.regression_daten_dic = regression_daten_dic

        self.prognosemodel = Prognose(controller=self.controller, **self.regression_daten_dic)

        test_pred = self.prognosemodel.make_prediction()
        print('Prognostizierter Preis: ' + str(round(test_pred, 2)))

        self.layout()

    def layout(self):

        self.config(bg='#E2E2E2')

        # Überschrift

        #
