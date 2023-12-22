from utils import load_json
from autoviz import AutoViz_Class

def plot(dataframe, target):

    AV = AutoViz_Class()

    dft = AV.AutoViz(
    "",
    sep=",",
    depVar=target,
    dfte=dataframe,
    header=0,
    verbose=2,
    lowess=False,
    chart_format="jpg",
    max_rows_analyzed=500,
    max_cols_analyzed=20,
    save_plot_dir="plots",
    )
