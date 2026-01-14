import numpy as np


def marker_schedule(marker_schedule=None):

    if marker_schedule == "SPBM":
        based_marker = {
            "ADAM": "v",                # square
            "ALR-SMAG": "^",            # pixel marker
            "Bundle": "h",              # circle
            "SGD": "x",                 # pentagon
            "SPSmax": "s",              # tri-right
            "SPBM-PF": "*",             # star
            "SPBM-TR": "*",             # star
            "SPBM-PF-NoneCut": "s",     # circle
            "SPBM-TR-NoneCut": "s",     # circle
        }
        
    else:
        based_marker = {
            "point": ".",                # point marker
            "pixel": ",",                # pixel marker
            "circle": "o",               # circle
            "triangle_down": "v",        # down triangle
            "triangle_up": "^",          # up triangle
            "triangle_left": "<",        # left triangle
            "triangle_right": ">",       # right triangle
            "tri_down": "1",             # tri-down
            "tri_up": "2",               # tri-up
            "tri_left": "3",             # tri-left
            "tri_right": "4",            # tri-right
            "square": "s",               # square
            "pentagon": "p",             # pentagon
            "star": "*",                 # star
            "hexagon1": "h",             # hexagon 1
            "hexagon2": "H",             # hexagon 2
            "plus": "+",                 # plus
            "x": "x",                    # x
            "diamond": "D",              # diamond
            "thin_diamond": "d",         # thin diamond
            "vline": "|",                # vertical line
            "hline": "_",                # horizontal line
        }

    return based_marker


def colors_schedule(colors_schedule=None):

    if colors_schedule == "SPBM":
        based_color = {
            "ADAM":      "#7f7f7f",  
            "ALR-SMAG":  "#796378",  
            "Bundle":    "#17becf",  
            "SGD":       "#2ca02c",  
            "SPSmax":    "#BA6262",  
            "SPBM-PF":   "#1f77b4",  
            "SPBM-TR":   "#d62728",  
            "SPBM-PF-NoneCut": "#8c564b",
            "SPBM-TR-NoneCut": "#e377c2",
        }

    else:
        based_color = {
            "ADAM":     "#1f77b4",
            "ALR-SMAG": "#ff7f0e",
            "Bundle":   "#2ca02c",
            "SGD":      "#d62728",
            "SPSmax":   "#9467bd",
            "SPBM-PF":  "#8c564b",
            "SPBM-TR":  "#e377c2",
            "dddd":     "#7f7f7f",
            "xxx":      "#bcbd22",
            "ED":       "#17becf",
        }
    return based_color

def linestyle_schedule(style_schedule=None):

    if style_schedule == "SPBM":
        based_style = {
            "ADAM":      "--",         
            "ALR-SMAG":  "--",          
            "Bundle":    "--",           
            "SGD":       "--",           
            "SPSmax":    "--",   
            "SPBM-PF":   "-",           
            "SPBM-TR":   "-",          
            "SPBM-PF-NoneCut": (0, (5, 2)),
            "SPBM-TR-NoneCut": (0, (1, 1)),
        }

    else:
        based_style = {
            "ADAM":     "--",
            "ALR-SMAG": "-.",
            "Bundle":   ":",
            "SGD":      "-",
            "SPSmax":   (0, (3, 1)),
            "SPBM-PF":  "-",
            "SPBM-TR":  "--",
            "dddd":     (0, (5, 5)),
            "xxx":      (0, (1, 1)),
            "ED":       "-.",
        }

    return based_style


def set_marker_point(epoch_num: int) -> list:
    marker_point = {
        1: [0],
        3: [0, 2],
        4: [0, 2, 4],
        6: [0, 2, 4, 6],
        8: [0, 2, 4, 6, 8],
        10: [0, 2, 4, 6, 8, 10],
        50: [0, 10, 20, 30, 40, 50],
        100: [0, 20, 40, 60, 80, 100],
        200: [0, 40, 80, 120, 160, 200],
    }
    if epoch_num not in marker_point:
        raise ValueError(f"No marker defined for epoch {epoch_num}")
    
    return marker_point[epoch_num]


def set_fig_info(user_line_style,
        label_mapping,
        color_scheme,
        opt_name,
        makers,
        y_mean,
        ax,
        data_name,
        opt_paras,
    ):
    # line style
    if user_line_style is not None:
        line_style = linestyle_schedule(user_line_style)[opt_name]
    else:
        line_style = None

    # label name mapping
    if label_mapping is not None:
        label_name = label_mapping[opt_name]
    else:
        label_name = opt_name

    # color
    if color_scheme is not None:
        color = colors_schedule(color_scheme)[opt_name]
    else:
        color = None

    # with opt paras
    if opt_paras is not None:
        label_name = f'{label_name}_{opt_paras[data_name][opt_name]["para_str"]}'
    
    # makers
    if makers:
        x = np.array(set_marker_point(len(y_mean)-1))
        ax.scatter(x, y_mean[x], 
            color = colors_schedule(color_scheme)[opt_name]
        )

    return line_style, label_name, color, ax