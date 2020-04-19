#!/usr/bin/env python3
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from Anno import AnnoDataset


class AnnoCalculator(tk.Tk):
    """docstring for AnnoCalculator"""
    def __init__(self, dataset):
        super().__init__()
        self.dataset = dataset
        self.title("Anno productivity calculator")
        self.geometry("900x600")
        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(size=16)
        self.notebook = ttk.Notebook(self)
        self.notebook.option_add("*Font", default_font)

        self.selection_tab = tk.Frame(self.notebook)
        self.result_tab = tk.Frame(self.notebook)

        self.notebook.add(self.selection_tab, text="Buildings")
        self.notebook.add(self.result_tab, text="Results")
        self.notebook.pack(fill=tk.BOTH, expand=1)
        padding = 15
        self.create_dropdown()
        #self.create_radiobuttons(20)
        tk.Label(self.selection_tab, text="Number of buildings").grid(row=2,
                                                                      column=2,
                                                                      padx=padding)
        tk.Label(self.selection_tab, text="Productivity").grid(row=2, column=3, padx=padding)

        tk.Label(self.result_tab, text="Product").grid(row=1,
                                                       column=1,
                                                       padx=padding)
        tk.Label(self.result_tab, text="Productivity").grid(row=1,
                                                            column=2,
                                                            padx=padding)
        tk.Label(self.result_tab,
                 text="Number of Buildings").grid(row=1,
                                                  column=3,
                                                  padx=padding)
        tk.Button(self.selection_tab, text="Exit",
                  command=self.destroy).grid(row=1, column=3)

        self.box = []
        self.radio = []
        self.entry = []
        self.labels = []

    def create_dropdown(self):
        # Create a Tkinter variable
        tkvar = tk.StringVar()

        # Dictionary with options
        choices = self.dataset.get_names()
        tkvar.set(choices[0])  # set the default option

        popupMenu = ttk.Combobox(self.selection_tab,
                                 textvariable=tkvar,
                                 values=choices)
        tk.Label(self.selection_tab,
                 text="Choose an endproduct").grid(row=1, column=1)

        popupMenu.grid(row=2, column=1)

        # on change dropdown value
        def change_dropdown(*args):
            self.reset()
            target = tkvar.get()
            self.chain = self.dataset.get_chain(product=target)
            self.add_chain()

        # link function to change dropdown
        tkvar.trace('w', change_dropdown)

    def add_chain(self):
        k = 4
        self.selected = tk.IntVar()
        self.selected.set(0)
        prods = self.dataset.get_chain_productivity(self.chain)

        for s in self.chain:
            self.radio.append(
                tk.Radiobutton(self.selection_tab,
                               text=s,
                               padx=20,
                               variable=self.selected,
                               value=k - 4))
            self.radio[-1].grid(row=k, column=1, sticky=tk.W)

            self.box.append(tk.Spinbox(self.selection_tab, from_=1, to=100))
            self.box[-1].grid(row=k, column=2, sticky=tk.W)

            dv = tk.DoubleVar(self.selection_tab, value=prods[k - 4])
            self.entry.append(tk.Entry(self.selection_tab, text=dv))
            self.entry[-1].grid(row=k, column=3, sticky=tk.W)
            k += 1
        self.start = tk.Button(self.selection_tab,
                               text="Calculate!",
                               command=self.calc_callback)
        self.start.grid(column=1, row=k)

        self.save = tk.Button(self.selection_tab,
                              text="Save",
                              command=self.save_callback)
        self.save.grid(column=2, row=k)

    def calc_callback(self):
        selected = self.selected.get()
        number = int(self.box[selected].get())
        self.update_productivity()
        result = d.scaleChain(chain=self.chain,
                              number=number,
                              scale_product=self.chain[selected])
        self.write_result(result)

    def save_callback(self):
        self.update_productivity()
        self.dataset.write_data()

    def update_productivity(self):
        for k in range(len(self.chain)):
            product = self.chain[k]
            self.dataset.productivity[product] = float(self.entry[k].get())

    def reset(self):
        try:
            for b in self.box:
                b.destroy()
            for r in self.radio:
                r.destroy()
            for e in self.entry:
                e.destroy()
            for l in self.labels:
                l.destroy()
            self.labels = []
            self.box = []
            self.entry = []
            self.radio = []
            self.start.destroy()
            self.save.destroy()
        except Exception as e:
            pass

    def write_result(self, result):
        self.labels = []
        k = 2
        for c in self.chain:
            self.labels.append(tk.Label(self.result_tab, text=c))
            self.labels[-1].grid(row=k, column=1, sticky=tk.W)
            self.labels.append(
                tk.Label(self.result_tab,
                         text="{:1.2f}".format(result[c, "productivity"])))
            self.labels[-1].grid(row=k, column=2)
            self.labels.append(
                tk.Label(self.result_tab,
                         text="{:1.2f}".format(result[c, "number"])))
            self.labels[-1].grid(row=k, column=3)
            k += 1


if __name__ == '__main__':
    d = AnnoDataset()
    gui = AnnoCalculator(d)
    #chain = d.get_chain(product="naehmaschinen")
    #d.scaleChain(chain=chain, number=3)
    gui.mainloop()