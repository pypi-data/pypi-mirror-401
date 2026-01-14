# %%
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import os
import originpro as op
import math
from pathlib import Path

# %%


class ECLabChDisMaker:
    def __init__(self):
        # read clipboard and set cell name from the first line
        self.cellname = Path(pd.read_clipboard(
            nrows=1, header=None, sep="\t").at[0, 0]).stem
        self.df = pd.read_clipboard(header=None, names=(
            "Capacity/mA.h/g", "E/V"), skiprows=2, sep="\t")
        self.chdis_df = None
        self.cap_df = None

    def split_data(self):
        new_df = self.df.copy()
        new_df["c"] = None
        c = 1  # 充電放電の区切り
        drop_row = []
        for i, cap in enumerate(self.df["Capacity/mA.h/g"]):
            try:
                next_cap = self.df.at[i+1, "Capacity/mA.h/g"]
                if cap == 0 and next_cap == 0:
                    drop_row.append(i)
                elif cap == next_cap:
                    new_df.at[i, "c"] = c
                    drop_row.append(i+1)
                elif cap > next_cap:
                    new_df.at[i, "c"] = c
                    c += 1
                else:
                    new_df.at[i, "c"] = c
            except:
                new_df.at[i, "c"] = c
        new_df.drop(drop_row, inplace=True)
        new_df.reset_index(drop=True, inplace=True)
        new_df["cycle number"] = [math.ceil(d/2) for d in new_df["c"]]
        new_df["ch/dis"] = ["dis" if e % 2 == 0 else "ch" for e in new_df["c"]]
        key = [str(m)+"-"+l for m in range(1, int(new_df["c"].max()))
               for l in ["ch", "dis"]]  # +1しないといけない気がする
        gb = new_df.groupby("c")
        chdis = [gb.get_group(x)[["Capacity/mA.h/g", "E/V"]
                                 ].reset_index(drop=True) for x in gb.groups]
        self.chdis_df = pd.concat(chdis, axis=1, keys=key)  # keys = key
        self.cap_df = pd.crosstab(new_df["cycle number"], columns=new_df["ch/dis"],
                                  values=new_df["Capacity/mA.h/g"], aggfunc="max").dropna(how='any').reset_index()
        self.cap_df["Coulombic efficiency"] = 100 * \
            self.cap_df["dis"]/self.cap_df["ch"]

    def plot(
        self,
        xmin=None,
        xmax=None,
        ymin=None,
        ymax=None,
        interval=1,
        xaxis_title="Capacity / mAh g<sup>-1</sup>",
        yaxis_title="Voltage / V",
        x_d=None,
        y_d=None
    ):
        chdis_wks = op.new_sheet("w", lname=f"{self.cellname}_chdis")
        chdis_wks.from_df(self.chdis_df)

        # グラフを作成
        gp = op.new_graph(
            lname=f"{self.cellname}", template=op.path("u") + "charge_discharge.otpu"
        )
        gl = gp[0]
        last_col = len(self.chdis_df.columns)
        for i in range(0, last_col + 1, 4 * interval):
            if interval == 1 or i == 0:
                p1 = gl.add_plot(chdis_wks, colx=i, coly=i + 1, type="l")
                p2 = gl.add_plot(chdis_wks, colx=i + 2, coly=i + 3, type="l")
            else:
                p1 = gl.add_plot(chdis_wks, colx=i - 4, coly=i - 3, type="l")
                p2 = gl.add_plot(chdis_wks, colx=i - 2, coly=i - 1, type="l")
            if i == 0 and (p1 is not None) and (p2 is not None):
                p1.color = "red"
                p2.color = "red"
            elif (p1 is not None) and (p2 is not None):
                p1.color = "black"
                p2.color = "black"
        gl.rescale()
        gl.set_xlim(xmin, xmax, x_d)
        gl.set_ylim(ymin, ymax, y_d)

        cap_wks = op.new_sheet("w", lname=f"{self.cellname}_cap")
        cap_wks.from_df(self.cap_df)
        gp_cap = op.new_graph(
            lname=f"{self.cellname}_cap", template=op.path("u") + "cycle_efficiency.otpu"
        )
        gl_cap = gp_cap[0]
        gl_eff = gp_cap[1]
        p_cap = gl_cap.add_plot(cap_wks, colx=0, coly=2, type="y")
        p_eff = gl_eff.add_plot(cap_wks, colx=0, coly=3, type="y")
        gl_cap.rescale()
        gl_eff.rescale()
        gl_cap.set_ylim(xmin, xmax, x_d)
        gl_eff.set_ylim(0, 100, 10)

