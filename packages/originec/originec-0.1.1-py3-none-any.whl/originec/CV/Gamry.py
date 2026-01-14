# %%
import pandas as pd
import numpy as np
from io import StringIO


class CVParser:
    def __init__(self, file_path):
        self.file_path = file_path
        # if file is .txt, read it as a dataframe
        if file_path.endswith(".txt"):
            # Read the text file as dataframe
            self.data = pd.read_csv(
                file_path, sep="\t", header=None, skiprows=2)

        if file_path.endswith(".DTA"):
            self.data = self.read_raw_dta(file_path)
        # Rename columns
        col_name = [
            f"{int(i/2)+1}{['x', 'y'][i%2]}"
            for i in range(len(self.data.columns))
        ]
        self.data.columns = col_name

    def read_raw_dta(self, file_path):
        with open(file_path, "r") as f:
            lines = f.readlines()

        curves = []
        start_index = 0
        for i, line in enumerate(lines):
            if start_index and (line.startswith("CURVE") or i == len(lines) - 2):
                # 次の"CURVE"行またはファイルの終わりまでを曲線データとする
                end_index = i
                curve_data = lines[start_index:end_index]
                # データフレームに変換
                df = pd.read_csv(StringIO("".join(curve_data)), sep="\t")
                try:
                    curves.append(df[['V vs. Ref.', 'A']])
                except KeyError:
                    pass
                start_index = i + 2
            elif "CURVE" in line:
                # "CURVE"行の2行後からデータが始まる
                start_index = i + 2
        # 曲線データを結合
        df = pd.concat(curves, axis=1)

        return df

    def clean_data(self, split_val=None):
        # First, let's create two empty dataframes for 'x' and 'y'
        df_x = pd.DataFrame()
        df_y = pd.DataFrame()

        # Then, fill the 'x' dataframe with all 'x' columns from the original one
        for col in self.data.columns:
            if "x" in col:
                df_x = pd.concat([df_x, self.data[col]]).reset_index(drop=True)

        # And same with 'y'
        for col in self.data.columns:
            if "y" in col:
                df_y = pd.concat([df_y, self.data[col]]).reset_index(drop=True)

        # Finally, concatenate x and y dataframes along columns (axis=1)
        xy_df = pd.concat([df_x, df_y], axis=1)
        xy_df = xy_df.dropna()
        xy_df.columns = ["x", "y"]
        xy_df["x"] = xy_df["x"].str.replace(",", ".").astype(float)
        xy_df["y"] = xy_df["y"].str.replace(",", ".").astype(float)
        xy_df["y"] = xy_df["y"] * 1000  # Convert to mA

        if split_val is None:
            # Get first value
            first_val = xy_df.iloc[0, 0]
        else:
            first_val = split_val

        # Find the indices where the x value crosses first_val
        crosses_first_val = np.where(
            np.diff(np.sign(xy_df["x"] - first_val)))[0]
        # if diff < 2, then the first value is not crossed
        crosses_first_val = crosses_first_val[1:][np.diff(
            crosses_first_val) > 2]

        # Split dataframe at these indices
        clean_df = pd.DataFrame()
        prev_index = 0

        if len(crosses_first_val) < 2:
            clean_df = xy_df

        for i, index in enumerate(crosses_first_val, start=1):
            if i % 2 == 0:
                df_temp = xy_df.iloc[prev_index: index + 1]
                clean_df[f"{int(i/2)}x"] = df_temp["x"].reset_index(drop=True)
                clean_df[f"{int(i/2)}y"] = df_temp["y"].reset_index(drop=True)
                prev_index = index + 1
            elif i == len(crosses_first_val):
                df_temp = xy_df.iloc[prev_index:]
                clean_df[f"{int(i/2)+1}x"] = df_temp["x"].reset_index(drop=True)
                clean_df[f"{int(i/2)+1}y"] = df_temp["y"].reset_index(drop=True)

        return clean_df


def main():
    # Initialize the parser with the path to the file
    parser = CVParser(
        r"mychem\data\03mAlTFSIH2O_BIm_Pt_-23_-13_2.DTA")

    # Clean the data
    clean_data = parser.clean_data()

    # Print the cleaned data
    print(clean_data)


if __name__ == "__main__":
    main()
