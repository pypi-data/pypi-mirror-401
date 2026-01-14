import originpro as op
from CV.Gamry import CVParser as GamryCVParser
from CV.Biologic import CVParser as BiologicCVParser
from pathlib import Path
import pandas as pd
import math
import scipy as sp
from typing import Any
import numpy as np


class CVMaker:
    def __init__(self, path_list: list, diameter: float | None = None, scan_rate: float | None = None):
        self.df_dict = {}
        for path in path_list:
            p = Path(path)
            self.df_dict[p.stem] = pd.read_csv(path, sep="\t")
        self.colors = [
            "#F14040",
            "#515151",
            "#1A6FDF",
            "#37AD6B",
            "#B177DE",
            "#CC9900",
            "#00CBCC",
            "#7D4E4E",
            "#8E8E00",
            "#FB6501"
        ]
        self.diameter = diameter
        self.scan_rate = scan_rate

    def auto_limit(self):
        x_df_list = []
        y_df_list = []
        for name, df in self.df_dict.items():
            x_df_list.append(df.iloc[:, 0::2])
            y_df_list.append(df.iloc[:, 1::2])
        x_df = pd.concat(x_df_list, axis=1)
        y_df = pd.concat(y_df_list, axis=1)
        xmin = math.floor(x_df.min().min())
        xmax = math.ceil(x_df.max().max())
        ymin = math.floor(y_df.min().min())
        ymax = math.ceil(y_df.max().max())
        x_d = math.ceil((xmax - xmin)/5)
        y_d = math.ceil((ymax - ymin)/5)

        return xmin, xmax, ymin, ymax, x_d, y_d

    def normalized_by_area(self, area: float):
        for name, df in self.df_dict.items():
            # all y values are divided by area
            df.iloc[:, 1::2] = df.iloc[:, 1::2] / area
            self.df_dict[name] = df

    def calculate_red_ox_area(self, data: pd.DataFrame, scan_rate: float | None = None) -> pd.DataFrame:
        # 2列ずつ処理
        reduction_area_list = []
        oxidation_area_list = []
        for col in range(0, len(data.columns), 2):
            # devide reduction and oxidation: y value of reduction is negative, that of oxidation is positive
            df = data.iloc[:, col:col+2]
            reduction = df[df.iloc[:, 1] < 0]
            oxidation = df[df.iloc[:, 1] > 0]
            # devide the dataframes into two parts based on the scan direction and sort_values by x
            reduction_negatives = reduction[reduction.iloc[:, 0].diff() < 0].sort_values(
                reduction.columns[0])
            reduction_positives = reduction[reduction.iloc[:, 0].diff() > 0].sort_values(
                reduction.columns[0])
            oxidation_negatives = oxidation[oxidation.iloc[:, 0].diff() < 0].sort_values(
                reduction.columns[0])
            oxidation_positives = oxidation[oxidation.iloc[:, 0].diff() > 0].sort_values(
                reduction.columns[0])

            # calculate area
            try:
                reduction_area = abs(sp.integrate.simpson(
                    reduction_negatives.iloc[:, 1], reduction_negatives.iloc[:, 0])) + abs(sp.integrate.simpson(
                        reduction_positives.iloc[:, 1], reduction_positives.iloc[:, 0]))
                oxidation_area = abs(sp.integrate.simpson(
                    oxidation_negatives.iloc[:, 1], oxidation_negatives.iloc[:, 0])) + abs(sp.integrate.simpson(
                        oxidation_positives.iloc[:, 1], oxidation_positives.iloc[:, 0]))
            except Exception as e:
                print(e)
                reduction_area = np.nan
                oxidation_area = np.nan
            reduction_area_list.append(reduction_area)
            oxidation_area_list.append(oxidation_area)
        red_ox_df = pd.DataFrame([reduction_area_list, oxidation_area_list]).T
        red_ox_df.columns = ['reduction', 'oxidation']
        if scan_rate is not None:
            red_ox_df['reduction'] = red_ox_df['reduction'] / (scan_rate * 3.6)
            red_ox_df['oxidation'] = red_ox_df['oxidation'] / (scan_rate * 3.6)
        red_ox_df['Efficiency / %'] = red_ox_df['oxidation'] / \
            red_ox_df['reduction'] * 100
        red_ox_df.dropna(subset=['reduction', 'oxidation'])
        red_ox_df.index = np.arange(1, len(red_ox_df)+1)
        red_ox_df.reset_index(inplace=True)
        return red_ox_df

    def plot(
        self,
        xmin=None,
        xmax=None,
        ymin=None,
        ymax=None,
        x_d=1.0,
        y_d=1.0,
    ):
        # wks_1st = op.new_sheet("w", lname="1st cycle")
        gp_all = op.new_graph(
            lname="all sample", template=op.path("u") + "CV.otpu"
        )
        gl_all = gp_all[0]
        # gl_all.rescale()
        if self.diameter is not None:
            area = math.pi * (float(self.diameter) / 20) ** 2
            self.normalized_by_area(area)
        if xmin is None and xmax is None and ymin is None and ymax is None:
            xmin, xmax, ymin, ymax, x_d, y_d = self.auto_limit()
        gl_all.set_xlim(xmin, xmax, x_d)
        gl_all.set_ylim(ymin, ymax, y_d)

        for sample_n, (name, df) in enumerate(self.df_dict.items()):
            cv_wks = op.new_sheet("w", lname=f"{name}_cv")
            cv_wks.from_df(df)
            area_df = self.calculate_red_ox_area(df)
            area_wks = op.new_sheet("w", lname=f"{name}_area")
            area_wks.from_df(area_df)

            # グラフを作成
            gp = op.new_graph(
                lname=f"{name}", template=op.path("u") + "CV.otpu"
            )
            gl = gp[0]
            last_col = len(df.columns)
            for i in range(0, last_col, 2):
                p1 = gl.add_plot(cv_wks, colx=i, coly=i + 1, type="l")
                p_all = gl_all.add_plot(
                    cv_wks, colx=i, coly=i + 1, type="l")
                try:
                    p1.color = self.colors[int(i/2) % 10]
                except Exception as e:
                    print(e)
                try:
                    p_all.color = self.colors[int(sample_n) % 10]
                    p_all.name = name
                except Exception as e:
                    print(e)
            # gl.rescale()
            gl.set_xlim(xmin, xmax, x_d)
            gl.set_ylim(ymin, ymax, y_d)

            gp_area = op.new_graph(
                lname=f"{name}_area", template=op.path("u") + "cycle_efficiency.otpu"
            )
            gl_area = gp_area[0]
            gl_eff = gp_area[1]
            p_area = gl_area.add_plot(area_wks, colx=0, coly=2, type="y")
            p_eff = gl_eff.add_plot(area_wks, colx=0, coly=3, type="y")
            gl_area.rescale()
            gl_eff.rescale()
            # gl_area.set_ylim(ymin, ymax, y_d)
            gl_eff.set_ylim(0, 100, 10)


class CVMakerGamry(CVMaker):
    def __init__(self, path_list: list, diameter: float | None = None, scan_rate: float | None = None, split_val: float | None = None):
        self.df_dict = {}
        self.diameter = diameter
        self.scan_rate = scan_rate
        try:
            self.split_val = float(split_val)
        except Exception as e:
            # print(e)
            self.split_val = None
        for path in path_list:
            p = Path(path)
            self.df_dict[p.stem] = GamryCVParser(
                path).clean_data(split_val=self.split_val)
        self.colors = [
            "#F14040",
            "#515151",
            "#1A6FDF",
            "#37AD6B",
            "#B177DE",
            "#CC9900",
            "#00CBCC",
            "#7D4E4E",
            "#8E8E00",
            "#FB6501"
        ]


class CVMakerBiologic(CVMaker):
    def __init__(self, diameter: float | None = None, scan_rate: float | None = None, split_val: float | None = None, name: str | None = None):
        """
        Initialize CVMakerBiologic by reading CV data from clipboard.
        Data should be copied from EC-Lab using Alt+D.
        
        Parameters:
        -----------
        diameter : float, optional
            Electrode diameter in mm for area normalization
        scan_rate : float, optional
            Scan rate in mV/s for charge calculation
        split_val : float, optional
            Voltage value to use for splitting cycles
        name : str, optional
            Custom name for the sample. If None, uses filename from clipboard data
        """
        self.df_dict = {}
        self.diameter = diameter
        self.scan_rate = scan_rate
        try:
            self.split_val = float(split_val)
        except Exception as e:
            self.split_val = None
        
        # Create parser from clipboard
        parser = BiologicCVParser()
        sample_name = name if name is not None else parser.filename
        self.df_dict[sample_name] = parser.clean_data(split_val=self.split_val)
        
        self.colors = [
            "#F14040",
            "#515151",
            "#1A6FDF",
            "#37AD6B",
            "#B177DE",
            "#CC9900",
            "#00CBCC",
            "#7D4E4E",
            "#8E8E00",
            "#FB6501"
        ]
