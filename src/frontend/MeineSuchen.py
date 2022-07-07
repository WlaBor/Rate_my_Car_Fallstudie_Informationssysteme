import tkinter as tk
from tkinter import ttk
from frontend.ErgebnisFrame import ErgebnisFrame
from frontend.custom_widgets.CanvasLogo import LogoCanvas

UEBERSCHRIFT_DESIGN = {
    'bg': '#E2E2E2',
    'font': ('Arial', 24, 'bold')
}


class MeineSuchenFrame(tk.Frame):

    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller

        self.meine_suchen_df = self.controller.backend.Suche.load_data_from_user_as_df(
            self.controller.active_user).sort_values('zeitpunkt', ascending=False)

        self.view_df = self.meine_suchen_df[['zeitpunkt', 'eingaben_brand', 'eingaben_model', 'eingaben_vehicletype',
                                             'eingaben_erstzulassung', 'eingaben_kilometerstand', 'eingaben_leistung_ps', 'prognose_preis']].copy()

        self.view_df.columns = ['Zeitpunkt', 'Marke', 'Modell', 'Typ',
                                'Erstzulassung', 'Kilometer', 'Leistung [PS]', 'Prognose [€]']
        self.view_df['Marke'] = self.view_df['Marke'].map(lambda val: val.upper())
        self.view_df['Modell'] = self.view_df['Modell'].map(lambda val: val.upper())
        self.view_df['Typ'] = self.view_df['Typ'].map(lambda val: val.upper())
        self.view_df['Erstzulassung'] = self.view_df['Erstzulassung'].map(lambda val: int(val))
        self.view_df['Kilometer'] = self.view_df['Kilometer'].map(lambda val: int(val))
        self.view_df['Leistung [PS]'] = self.view_df['Leistung [PS]'].map(lambda val: int(val))
        self.view_df['Prognose [€]'] = self.view_df['Prognose [€]'].map(lambda val: int(val))

        self.layout()

    def layout(self):
        self.config(bg='#E2E2E2')

    ########################################
    ########################################
        header_frame = tk.Frame(self, bg='#E2E2E2', height=200)
        header_frame.pack(side=tk.TOP, fill=tk.X)
        header_frame.pack_propagate(False)
        # Logo und Überschrift oben links
        logo = LogoCanvas(header_frame, self.controller, size=(50, 50), image_name='lupe_logo', bg='#E2E2E2')
        logo.pack(side=tk.LEFT, anchor=tk.NW, padx=20, pady=20)
        self.logo = logo
        tk.Label(header_frame, text='Deine Suchen', **
                 UEBERSCHRIFT_DESIGN).pack(side=tk.LEFT, padx=(0, 20), pady=20, anchor=tk.NW)

        ########################################
        ########################################
        tree_view_frame = tk.Frame(self, bg='#E2E2E2')
        tree_view_frame.pack(side=tk.TOP, fill=tk.X, expand=False, padx=70)
        style = ttk.Style()
        # style.theme_use("clam")
        style.configure("Treeview.Heading", background="gray", foreground="black", font=('Arial', 12, 'bold'))

        style.configure("Treeview",
                        background="black",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="black",
                        )
        style.map('Treeview', background=[('selected', '#ABDB79')])

        treeview = ttk.Treeview(tree_view_frame, selectmode='browse')
        treeview.tag_configure("evenrow", background='#DEE1E4', foreground='white', font=('Arial', 9))
        treeview.tag_configure("oddrow", background='white', foreground='white', font=('Arial', 9))

        self.treeview = treeview

        treeview['column'] = list(self.view_df.columns)
        treeview["show"] = "headings"

        widhts = [100] + [100]*(len(list(self.view_df.columns))-1)
        i = 0
        for column in treeview["columns"]:
            treeview.column(column, anchor=tk.CENTER, width=widhts[i])
            treeview.heading(column, text=column)
            i += 1

        # command means update the yaxis view of the widget
        treescrolly = tk.Scrollbar(tree_view_frame, orient="vertical", command=treeview.yview)
        # command means update the xaxis view of the widget
        treescrollx = tk.Scrollbar(tree_view_frame, orient="horizontal", command=treeview.xview)
        # assign the scrollbars to the Treeview Widget
        treeview.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
        # make the scrollbar fill the x axis of the Treeview widget
        treescrollx.pack(side="bottom", fill="x")
        # make the scrollbar fill the y axis of the Treeview widget
        treescrolly.pack(side="right", fill="y")

        treeview.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        # Liste in treeview ablegen
        self.treeview.delete(*self.treeview.get_children())
        df_rows = self.view_df.to_numpy().tolist()
        i = 1
        for row in df_rows:
            if i % 2 == 0:
                self.treeview.insert("", "end", values=row, tags=('evenrow',))
            else:
                self.treeview.insert("", "end", values=row, tags=('oddrow',))
            i += 1

        self.treeview.bind('<Double-1>', self.command_ergebnis)

        ########################################
        ########################################
        bottom_frame = tk.Frame(self, bg='#E2E2E2', height=100)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        btn = tk.Button(bottom_frame, text='Suche öffnen', command=self.command_ergebnis,
                        bg='#92D050', font=('Arial', 22, 'bold'), cursor='hand2')
        btn.pack(side=tk.RIGHT, padx=80, pady=50)
        btn.bind('<Enter>', lambda *args: btn.config(bg='#C7E7A6', fg='#394240'))
        btn.bind('<Leave>', lambda *args: btn.config(bg='#92D050', fg='black'))

    def command_ergebnis(self, *args):
        curItem = self.treeview.focus()

        if len(self.treeview.item(curItem)['values']) == 0:
            tk.messagebox.showinfo('Achtung', 'Bitte wählen sie eine Datenreihe aus.')
            return
        value = self.treeview.item(curItem)['values']
        zeitpunkt = value[0]
        print(zeitpunkt)
        subdf = self.meine_suchen_df[self.meine_suchen_df['zeitpunkt'] == zeitpunkt].iloc[0]
        print(subdf.to_dict())

        dic = subdf.to_dict()

        for widgets in self.winfo_children():
            widgets.forget()
        ErgebnisFrame(self, self.controller, regression_daten_dic={
            'brand': dic['eingaben_brand'],
            'model': dic['eingaben_model'],
            'vehicletype': dic['eingaben_vehicletype'],
            'auto_alter': 2016 - int(dic['eingaben_erstzulassung']),
            'auto_leistung_ps': int(dic['eingaben_leistung_ps']),
            'auto_kilometerstand': int(dic['eingaben_kilometerstand']),
            'getriebe': dic['eingaben_getriebe'],
            'antriebsart': dic['eingaben_fueltype'],
            'schaden_vorhanden': dic['eingaben_schaden_vorhanden'],
            'erstzulassung': int(dic['eingaben_erstzulassung'])
        }, save=False).pack(fill=tk.BOTH, expand=True)
