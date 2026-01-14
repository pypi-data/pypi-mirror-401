"""
----------------------------------------------------------------------
>>> Author       : Junshan Yin
>>> Last Updated : 2025-12-19
----------------------------------------------------------------------
"""
import math, os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from collections import defaultdict
from junshan_kit import kit, ParametersHub

def marker_schedule(marker_schedule=None):

    if marker_schedule == "SPBM":
        based_marker = {
            "ADAM": "v",  # square
            "ALR-SMAG": "^",  # pixel marker
            "Bundle": "h",  # circle
            "SGD": "x",  # pentagon
            "SPSmax": "s",  # tri-right
            "SPBM-PF": "*",  # star
            "SPBM-TR": "*",  # star
            "SPBM-PF-NoneCut": "s",  # circle
            "SPBM-TR-NoneCut": "s",  # circle
        }
        
    else:
        based_marker = {
            "point": ".",  # point marker
            "pixel": ",",  # pixel marker
            "circle": "o",  # circle
            "triangle_down": "v",  # down triangle
            "triangle_up": "^",  # up triangle
            "triangle_left": "<",  # left triangle
            "triangle_right": ">",  # right triangle
            "tri_down": "1",  # tri-down
            "tri_up": "2",  # tri-up
            "tri_left": "3",  # tri-left
            "tri_right": "4",  # tri-right
            "square": "s",  # square
            "pentagon": "p",  # pentagon
            "star": "*",  # star
            "hexagon1": "h",  # hexagon 1
            "hexagon2": "H",  # hexagon 2
            "plus": "+",  # plus
            "x": "x",  # x
            "diamond": "D",  # diamond
            "thin_diamond": "d",  # thin diamond
            "vline": "|",  # vertical line
            "hline": "_",  # horizontal line
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



def Search_Paras(Paras, args, model_name, data_name, 
                optimizer_name, 
                metric_key = "training_loss", 
                user_grid = True,
                set_yscale = True
            ):

    param_dict = Paras["Results_dict"][model_name][data_name][optimizer_name]
    if Paras["epochs"] is not None:
        xlabel = "epochs"
    else:
        xlabel = "iterations"

    num_polts = len(param_dict)
    cols = 3
    rows = math.ceil(num_polts / cols)

    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows))
    axes = axes.flatten()

    for idx, (param_str, info) in enumerate(param_dict.items()):
        ax = axes[idx]
        metric_list = info.get(metric_key, [])
        # duration = info.get('duration', 0)
        ax.plot(metric_list)
        # ax.set_title(f"time:{duration:.8f}s - seed: {Paras['seed']}, ID: {Paras['time_str']} \n params = {param_str}", fontsize=10)
        ax.set_title(f'time = {info["train_time"]:.2f}, seed: {Paras["seed"]}, ID: {Paras["time_str"]} \n params = {param_str}', fontsize=10)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ParametersHub.fig_ylabel(metric_key))
        ax.grid(user_grid)
        
        if set_yscale:
            ax.set_yscale("log")


    # Delete the redundant subfigures
    for i in range(len(param_dict), len(axes)):
        fig.delaxes(axes[i])
    
    if set_yscale:
        pre_str = "log"
    else:
        pre_str = ""

    plt.suptitle(f'{model_name} on {data_name} - {optimizer_name}, (training, test) = ({Paras["train_data_num"]}/{Paras["train_data_all_num"]}, {Paras["test_data_num"]}/{Paras["test_data_all_num"]}), {Paras["device"]}, batch_size: {Paras["batch_size"]}, V-{Paras["version"]}', fontsize=16)
    plt.tight_layout(rect=(0, 0, 1, 0.9))

    filename = f'{Paras["Results_folder"]}/{pre_str}_{metric_key}_{ParametersHub.model_abbr(model_name)}_{data_name}_{optimizer_name}.pdf'
    fig.savefig(filename)
    fig.savefig(filename.replace(".pdf", ".png"))
    print(f"✅ Saved: {filename}")
    plt.close('all')


def Read_Results_from_pkl(info_dict, Exp_name, model_name):
    draw_data = defaultdict(dict)
    xlabels = {}
    for data_name, info in info_dict.items():
        for optimizer_name, info_opt in info["optimizer"].items():
            
            if info.get("epochs") is not None:
                pkl_path = f'{Exp_name}/seed_{info["seed"]}/{model_name}/{data_name}/{optimizer_name}/train_{info["train_test"][0]}_test_{info["train_test"][1]}/Batch_size_{info["batch_size"]}/epoch_{info["epochs"]}/{info_opt["ID"]}/Results_{ParametersHub.model_abbr(model_name)}_{data_name}_{optimizer_name}.pkl'
                xlabels[data_name] = "epochs"

            else:
                pkl_path = f'{Exp_name}/seed_{info["seed"]}/{model_name}/{data_name}/{optimizer_name}/train_{info["train_test"][0]}_test_{info["train_test"][1]}/Batch_size_{info["batch_size"]}/iter_{info["iter"]}/{info_opt["ID"]}/Results_{ParametersHub.model_abbr(model_name)}_{data_name}_{optimizer_name}.pkl'
                xlabels[data_name] = "iterations"

            data_ = kit.read_pkl_data(pkl_path)

            param_str = ParametersHub.opt_paras_str(info["optimizer"][optimizer_name])

            draw_data[data_name][optimizer_name] = {
                "metrics": data_[param_str][info["metric_key"]],
                "param_str": param_str
            }

    return draw_data, xlabels

def Mul_Plot(model_name, info_dict, Exp_name = "SPBM", 
            cols = 3, save_path = None, save_name = None, 
            fig_show = False,
            user_subtitle = None,
            user_line_style = False,
            user_grid = True,
            color_scheme = "SPBM",
            linestyle_scheme = "SPBM",
            legend_loc = "upper",
            label_mapping = None,
            ylimit = {},
            set_yscale_log = {},
            xlabel_size = 16,
            title_size = 16,
            ylabel_size = 16,
            font_size = 12,
            legend_size = 14
        ):
    # matplotlib settings
    mpl.rcParams['font.family'] = 'Times New Roman'
    mpl.rcParams["mathtext.fontset"] = "stix"
    mpl.rcParams["axes.unicode_minus"] = False
    mpl.rcParams["font.size"] = font_size
    mpl.rcParams["mathtext.rm"] = "Times New Roman"
    xlabels = {}
    
    # Read data
    draw_data = defaultdict(dict)
    for data_name, info in info_dict.items():
        for optimizer_name, info_opt in info["optimizer"].items():
            
            if info.get("epochs") is not None:
                pkl_path = f'{Exp_name}/seed_{info["seed"]}/{model_name}/{data_name}/{optimizer_name}/train_{info["train_test"][0]}_test_{info["train_test"][1]}/Batch_size_{info["batch_size"]}/epoch_{info["epochs"]}/{info_opt["ID"]}/Results_{ParametersHub.model_abbr(model_name)}_{data_name}_{optimizer_name}.pkl'
                xlabels[data_name] = "epochs"

            else:
                pkl_path = f'{Exp_name}/seed_{info["seed"]}/{model_name}/{data_name}/{optimizer_name}/train_{info["train_test"][0]}_test_{info["train_test"][1]}/Batch_size_{info["batch_size"]}/iter_{info["iter"]}/{info_opt["ID"]}/Results_{ParametersHub.model_abbr(model_name)}_{data_name}_{optimizer_name}.pkl'
                xlabels[data_name] = "iterations"

            data_ = kit.read_pkl_data(pkl_path)

            param_str = ParametersHub.opt_paras_str(info["optimizer"][optimizer_name])

            draw_data[data_name][optimizer_name] = data_[param_str][info["metric_key"]]
        
    
    # Draw figures
    num_datasets = len(draw_data)
    nrows = math.ceil(num_datasets / cols)
    fig, axes = plt.subplots(nrows, cols, figsize=(5 * cols, 4 * nrows), squeeze=False)
    axes = axes.flatten()

    for idx, (data_name, info) in enumerate(draw_data.items()):
        ax = axes[idx]
        for optimizer_name, metric_list in info.items():
            if user_line_style:
                linestyle = linestyle_schedule(linestyle_scheme)[optimizer_name]
            else:
                linestyle = None

            if label_mapping is not None:
                label_name = label_mapping[optimizer_name]
            else:
                label_name = optimizer_name

            ax.plot(metric_list, label=label_name, 
                    color = colors_schedule(color_scheme)[optimizer_name],
                    linestyle = linestyle
                )

            if idx == 0:
                ax.set_ylabel(ParametersHub.fig_ylabel(info_dict[data_name]["metric_key"]), fontsize=ylabel_size) 

            # marker
            if info_dict[data_name].get("marker") is not None:
                x = np.array(info_dict[data_name]["marker"])

                metric_list_arr = np.array(metric_list)

                ax.scatter(x, metric_list_arr[x], 
                        marker = marker_schedule(linestyle_scheme)[optimizer_name], 
                        color = colors_schedule(color_scheme)[optimizer_name]
                    )

        if user_subtitle == None:
            set_subtitle = data_name
        else:
            set_subtitle = user_subtitle[idx]

        ax.set_title(set_subtitle, fontsize=title_size)
        ax.set_xlabel(xlabels[data_name], fontsize=xlabel_size)
        # ax.set_ylabel(ParametersHub.fig_ylabel(info_dict[data_name]["metric_key"]), fontsize=12) 
        
        if set_yscale_log.get(data_name) is not None:
            ax.set_yscale("log")
        # ax.set_xticks([0, 10, 20, 30, 40])
        # ax.set_xticklabels([r"$10^2$", "10", "20", "30", "40"])
        ax.grid(user_grid)

        if ylimit.get(data_name) is not None:
            ylim = ylimit[data_name]
            ax.set_ylim(ylim[0], ylim[1])

    # Hide redundant axes
    for ax in axes[num_datasets:]:
        ax.axis('off')

    # legend
    all_handles, all_labels = [], []
    for ax in axes[:num_datasets]:
        h, l = ax.get_legend_handles_labels()
        all_handles.extend(h)
        all_labels.extend(l)
    
    # duplicate removal
    unique = dict(zip(all_labels, all_handles))
    handles = list(unique.values())
    labels = list(unique.keys())
    
    if legend_loc == "lower":
        fig.legend(
            handles,
            labels,
            loc="lower center",
            bbox_to_anchor=(0.5, -0.08),
            ncol=min(len(handles), 4),
            fontsize=legend_size,
            # frameon=False 
        )
    elif legend_loc == "upper":
        fig.legend(
            handles,
            labels,
            loc="upper center",
            bbox_to_anchor=(0.5, 1.10),
            ncol=len(handles),
            fontsize=legend_size
        )
    else:
        print(legend_loc)
        assert False

    plt.tight_layout()
    if save_path is None:
        save_path_ = f'{model_name}.pdf'
    else:
        os.makedirs(save_path, exist_ok=True)
        save_path_ = f'{save_path}/{save_name}.pdf'
    plt.savefig(save_path_, bbox_inches="tight")
    plt.savefig(save_path_.replace("pdf", "png"), bbox_inches="tight")
    if fig_show:
        plt.show()
    plt.close("all")  # Colse the fig
    


def Opt_Paras_Plot(model_name, info_dict, 
                Exp_name = "SPBM", save_path = None, 
                save_name = None, 
                fig_show = False,
                user_title = None,
                user_grid = True,
                color_scheme = "SPBM",
                label_mapping = None,
                ylimit = None,
                set_yscale_log = True,
                with_paras = True,
                fig_size = (6,6), 
                xlabel_size=18,
                ylabel_size=18,
                title_size=16,
                legend_size=14,
                font_size=12
            ):

    mpl.rcParams['font.family'] = 'Times New Roman'
    mpl.rcParams["mathtext.fontset"] = "stix"
    mpl.rcParams["axes.unicode_minus"] = False
    mpl.rcParams["font.size"] = font_size
    mpl.rcParams["mathtext.rm"] = "Times New Roman"

    # Read data
    draw_data, xlabels = Read_Results_from_pkl(info_dict, Exp_name, model_name)

    if len(draw_data) >1:
        print('*' * 40)
        print("Only one data can be drawn at a time.")
        print(info_dict.keys())
        print('*' * 40)
        assert False

    plt.figure(figsize=fig_size)  # Optional: set figure size
    
    data_name = None  

    for data_name, _info in draw_data.items():
        for optimizer_name, metric_dict in _info.items():
            if label_mapping is not None:
                label_name = label_mapping[optimizer_name]
            else:
                label_name = optimizer_name
            
            # set optimal paras
            if with_paras:
                label_name = f'{label_name}_{metric_dict["param_str"]}'

            plt.plot(metric_dict["metrics"], label=label_name,
                    color=colors_schedule(color_scheme)[optimizer_name],
                    )

    if data_name is not None:
        if user_title == None:
            set_title = data_name
        else:
            set_title = user_title
    
    else:
        set_title = 'None'

    plt.title(set_title, fontsize=title_size)

    if with_paras:
        plt.legend(loc='upper center', 
                bbox_to_anchor=(0.5, -0.15), ncol=1,
                fontsize=legend_size) 
    
    else:
        plt.legend(fontsize=legend_size)

    plt.grid(user_grid)

    if set_yscale_log:
        plt.yscale("log")
    
    if ylimit is not None:
        plt.ylim(ylimit[0], ylimit[1])

    plt.tight_layout()  # Adjust layout so the legend fits
    plt.xlabel(xlabels[data_name],
            fontsize=xlabel_size)  # Or whatever your x-axis represents
    
    plt.ylabel(f'{ParametersHub.fig_ylabel(info_dict[data_name]["metric_key"])}',
            fontsize=ylabel_size)  
    
    if save_path is None:
        save_path_ = f'{model_name}.pdf'
    else:
        os.makedirs(save_path, exist_ok=True)
        save_path_ = f'{save_path}/{save_name}.pdf'
    plt.savefig(save_path_, bbox_inches="tight")
    plt.savefig(save_path_.replace("pdf", "png"), bbox_inches="tight")
    if fig_show:
        plt.show()
    
    plt.close("all")



def Mul_Plot_Group(
    model_name,
    info_dict,
    Exp_name="SPBM",
    cols=2,
    save_path=None,
    save_name=None,
    fig_show=False,
    user_grid = True,
    color_scheme = "SPBM",
    linestyle_scheme = "SPBM",
    ylimit = None
):
    # ================= matplotlib settings =================
    mpl.rcParams['font.family'] = 'serif'
    mpl.rcParams['font.serif'] = ['Times New Roman']
    mpl.rcParams["mathtext.fontset"] = "stix"
    mpl.rcParams["axes.unicode_minus"] = False
    mpl.rcParams["font.size"] = 12
    mpl.rcParams["mathtext.rm"] = "Times New Roman"

    # ================= Read data =================
    draw_data = defaultdict(dict)
    xlabels = {}

    for data_name, info in info_dict.items():
        for group_name, optimizers in info["groups"].items():

            for opt_name, opt_info in optimizers.items():

                if info.get("epochs") is not None:
                    xlabels[(data_name, group_name)] = "epochs"
                    pkl_path = (
                        f'{Exp_name}/seed_{info["seed"]}/{model_name}/{data_name}/{opt_name}/'
                        f'train_{info["train_test"][0]}_test_{info["train_test"][1]}/'
                        f'Batch_size_{info["batch_size"]}/epoch_{info["epochs"]}/'
                        f'{opt_info["ID"]}/'
                        f'Results_{ParametersHub.model_abbr(model_name)}_{data_name}_{opt_name}.pkl'
                    )
                else:
                    xlabels[(data_name, group_name)] = "iterations"
                    pkl_path = (
                        f'{Exp_name}/seed_{info["seed"]}/{model_name}/{data_name}/{opt_name}/'
                        f'train_{info["train_test"][0]}_test_{info["train_test"][1]}/'
                        f'Batch_size_{info["batch_size"]}/iter_{info["iter"]}/'
                        f'{opt_info["ID"]}/'
                        f'Results_{ParametersHub.model_abbr(model_name)}_{data_name}_{opt_name}.pkl'
                    )

                data_ = kit.read_pkl_data(pkl_path)
                param_str = ParametersHub.opt_paras_str(opt_info)

                draw_data[(data_name, group_name)][opt_name] = \
                    data_[param_str][info["metric_key"]]

    # ================= Draw figures =================
    num_plots = len(draw_data)
    nrows = math.ceil(num_plots / cols)

    fig, axes = plt.subplots(
        nrows, cols,
        figsize=(5 * cols, 4 * nrows),
        squeeze=False
    )
    axes = axes.flatten()

    for idx, ((data_name, group_name), opt_info) in enumerate(draw_data.items()):
        ax = axes[idx]

        for opt_name, metric in opt_info.items():
            color = colors_schedule(color_scheme).get(opt_name, None)
            marker = marker_schedule(linestyle_scheme).get(opt_name, "o")

            ax.plot(metric, label=opt_name, color=color)

        ax.set_title(f"{data_name} - {group_name}")
        ax.set_xlabel(xlabels[(data_name, group_name)])
        ax.set_ylabel(
            ParametersHub.fig_ylabel(
                info_dict[data_name]["metric_key"]
            )
        )

        if any(k in info_dict[data_name]["metric_key"] for k in ["loss", "grad"]):
            ax.set_yscale("log")

        ax.grid(user_grid)
        if ylimit is not None:
            ax.set_ylim(ylimit[0], ylimit[1])

    for ax in axes[num_plots:]:
        ax.axis("off")

    # ================= Legend =================
    handles, labels = [], []
    for ax in axes[:num_plots]:
        h, l = ax.get_legend_handles_labels()
        handles.extend(h)
        labels.extend(l)

    unique = dict(zip(labels, handles))

    fig.legend(
        unique.values(),
        unique.keys(),
        loc="lower center",
        bbox_to_anchor=(0.5, -0.08),
        ncol=len(unique),
        fontsize=12
    )

    plt.tight_layout()

    # ================= Save =================
    if save_path is None:
        save_file = f"{model_name}.pdf"
    else:
        os.makedirs(save_path, exist_ok=True)
        save_file = f"{save_path}/{save_name}.pdf"

    plt.savefig(save_file, bbox_inches="tight")
    plt.savefig(save_file.replace(".pdf", ".png"), bbox_inches="tight")

    if fig_show:
        plt.show()

    plt.close("all")
    


def diff_paras(
    model_name,
    label_dict,
    optimizer_name,
    info_dict,
    Exp_name="SPBM",
    cols=3,
    save_path=None,
    save_name=None,
    fig_show=False,
    user_subtitle=None,
    user_line_style=False,
    user_grid = True,
    color_scheme = "SPBM",
    linestyle_scheme = "SPBM",
    legend_loc = "upper",
    ylimit = None
):
    # ===================== matplotlib settings =====================
    mpl.rcParams['font.family'] = 'serif'
    mpl.rcParams["mathtext.fontset"] = "stix"
    mpl.rcParams["axes.unicode_minus"] = False
    mpl.rcParams["font.size"] = 12
    mpl.rcParams["mathtext.rm"] = "Times New Roman"

    # ===================== Read data =====================
    draw_data = defaultdict(dict)
    xlabels = {}

    for data_name, data_info in info_dict.items():
        optimizer_info = data_info[optimizer_name]

        for p, paras_info in optimizer_info.items():

            if data_info.get("epochs") is not None:
                xlabels[data_name] = "epochs"
                pkl_path = (
                    f'{Exp_name}/seed_{data_info["seed"]}/{model_name}/{data_name}/'
                    f'{optimizer_name}/train_{data_info["train_test"][0]}_'
                    f'test_{data_info["train_test"][1]}/'
                    f'Batch_size_{data_info["batch_size"]}/'
                    f'epoch_{data_info["epochs"]}/{paras_info["ID"]}/'
                    f'Results_{ParametersHub.model_abbr(model_name)}_'
                    f'{data_name}_{optimizer_name}.pkl'
                )
            else:
                xlabels[data_name] = "iterations"
                pkl_path = (
                    f'{Exp_name}/seed_{data_info["seed"]}/{model_name}/{data_name}/'
                    f'{optimizer_name}/train_{data_info["train_test"][0]}_'
                    f'test_{data_info["train_test"][1]}/'
                    f'Batch_size_{data_info["batch_size"]}/'
                    f'iter_{data_info["epochs"]}/{paras_info["ID"]}/'
                    f'Results_{ParametersHub.model_abbr(model_name)}_'
                    f'{data_name}_{optimizer_name}.pkl'
                )

            data_ = kit.read_pkl_data(pkl_path)
            param_str = ParametersHub.opt_paras_str(paras_info)

            draw_data[data_name][p] = data_[param_str][data_info["metric_key"]]

    # ===================== Draw figures =====================
    num_datasets = len(draw_data)
    nrows = math.ceil(num_datasets / cols)

    fig, axes = plt.subplots(
        nrows,
        cols,
        figsize=(5 * cols, 4 * nrows),
        squeeze=False
    )
    axes = axes.flatten()

    for idx, (data_name, info_) in enumerate(draw_data.items()):
        ax = axes[idx]

        for p, metric_list in info_.items():

            linestyle = (
                linestyle_schedule(linestyle_scheme)[optimizer_name]
                if user_line_style else "-"
            )
            labels_name = label_dict[data_name][f"{p}"]

            ax.plot(
                metric_list,
                label=labels_name,  
                linestyle=linestyle,
                linewidth=2,
                # marker=marker_schedule("SPBM")[optimizer_name],
                # markersize=6
            )

            # -------- marker --------
            if info_dict[data_name].get("marker") is not None:
                x = np.array(info_dict[data_name]["marker"])
                y = np.array(metric_list)

                ax.scatter(
                    x,
                    y[x],
                    marker=marker_schedule(linestyle_scheme)[optimizer_name],
                    color=colors_schedule(color_scheme)[optimizer_name],
                    zorder=3
                )

        # -------- title --------
        title = (
            data_name if user_subtitle is None
            else user_subtitle[idx]
        )
        ax.set_title(title, fontsize=12)

        ax.set_xlabel(xlabels[data_name])
        ax.set_ylabel(
            ParametersHub.fig_ylabel(
                info_dict[data_name]["metric_key"]
            )
        )

        if any(k in info_dict[data_name]["metric_key"]
                for k in ["loss", "grad"]):
            ax.set_yscale("log")

        ax.grid(user_grid)
        if ylimit is not None:
            ax.set_ylim(ylimit[0], ylimit[1])

    # ===================== Hide redundant axes =====================
    for ax in axes[num_datasets:]:
        ax.axis("off")

    # ===================== Global legend =====================
    handles, labels = [], []
    for ax in axes[:num_datasets]:
        h, l = ax.get_legend_handles_labels()
        handles.extend(h)
        labels.extend(l)

    unique = dict(zip(labels, handles))
    handles = list(unique.values())
    labels = list(unique.keys())

    fig.subplots_adjust(bottom=0.25)

    if legend_loc == "lower":
        fig.legend(
            handles,
            labels,
            loc="lower center",
            bbox_to_anchor=(0.5, -0.08),
            ncol=min(len(handles), 4),
            fontsize=12,
            # frameon=False 
        )
    elif legend_loc == "upper":
        fig.legend(
            handles,
            labels,
            loc="upper center",
            bbox_to_anchor=(0.5, 1.10),
            ncol=len(handles),
            fontsize=12
        )
    else:
        print(legend_loc)
        assert False

    plt.tight_layout()

    # ===================== Save / Show =====================
    if save_path is None:
        save_path_ = f'{model_name}.pdf'
    else:
        os.makedirs(save_path, exist_ok=True)
        save_path_ = f'{save_path}/{save_name}.pdf'
    plt.savefig(save_path_, bbox_inches="tight")
    plt.savefig(save_path_.replace("pdf", "png"), bbox_inches="tight")
    if fig_show:
        plt.show()
    print("saved:")
    print(save_path_)
    
    plt.close("all")



def resize_search_paras_figs(Paras, model_name, data_name, 
            optimizer_name, 
            metric_key = "training_loss", 
            user_grid = True,
            set_yscale = True,
            ylimit = None
        ):

    param_dict = Paras["Results_dict"][model_name][data_name][optimizer_name]
    if Paras["epochs"] is not None:
        xlabel = "epochs"
    else:
        xlabel = "iterations"

    num_polts = len(param_dict)
    cols = 3
    rows = math.ceil(num_polts / cols)

    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows))
    axes = axes.flatten()

    for idx, (param_str, info) in enumerate(param_dict.items()):
        ax = axes[idx]
        metric_list = info.get(metric_key, [])
        # duration = info.get('duration', 0)
        ax.plot(metric_list)
        # ax.set_title(f"time:{duration:.8f}s - seed: {Paras['seed']}, ID: {Paras['time_str']} \n params = {param_str}", fontsize=10)
        ax.set_title(f'time = {info["train_time"]:.2f}, seed: {Paras["seed"]}, ID: {Paras["time_str"]} \n params = {param_str}', fontsize=10)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ParametersHub.fig_ylabel(metric_key))
        ax.grid(user_grid)
        if ylimit is not None:
            ax.set_ylim(ylimit[0], ylimit[1])

        if set_yscale:
            ax.set_yscale("log")


    # Delete the redundant subfigures
    for i in range(len(param_dict), len(axes)):
        fig.delaxes(axes[i])
    
    if set_yscale:
        pre_str = "log"
    else:
        pre_str = ""

    plt.suptitle(f'{model_name} on {data_name} - {optimizer_name}, (training, test) = ({Paras["train_data_num"]}/{Paras["train_data_all_num"]}, {Paras["test_data_num"]}/{Paras["test_data_all_num"]}), {Paras["device"]}, batch_size: {Paras["batch_size"]}, V-{Paras["version"]}', fontsize=16)
    plt.tight_layout(rect=(0, 0, 1, 0.9))

    os.makedirs(f'{Paras["Results_folder"]}/resize', exist_ok=True)

    filename = f'{Paras["Results_folder"]}/resize/{pre_str}_{metric_key}_{ParametersHub.model_abbr(model_name)}_{data_name}_{optimizer_name}.pdf'
    fig.savefig(filename)
    fig.savefig(filename.replace(".pdf", ".png"))
    print(f"✅ Saved: {filename}")
    plt.close('all')



def diif_seed_subfigs(model_name, info_dict, Exp_name,
            save_path = None, 
            save_name = None, 
            fig_show = False,
            user_subtitle = None,
            user_grid = True,
            color_scheme = "SPBM",
            label_mapping = None,
            ylimit = None,
            user_line_style = None,
            set_yscale_log = None,
            fig_size = (6,6), 
            xlabel_size=18,
            ylabel_size=18,
            title_size=16,
            legend_size=14,
            font_size=12
        ):
    
    # ===================== matplotlib settings =====================
    mpl.rcParams['font.family'] = 'serif'
    mpl.rcParams["mathtext.fontset"] = "stix"
    mpl.rcParams["axes.unicode_minus"] = False
    mpl.rcParams["font.size"] = font_size
    mpl.rcParams["mathtext.rm"] = "Times New Roman"

    xlabels = {}
    _draw_data = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    draw_data = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

    # get the path of pkl
    for data_name, data_info in info_dict.items():
        for optimizer_name, optimizer_info in data_info["optimizer"].items():
            for seed, ID in optimizer_info.get("seed_ID", {}).items():
                # print(data_name, optimizer_name, seed, ID)
                if data_info.get("epochs") is not None:
                    xlabels[data_name] = "epochs"
                    pkl_path = (
                        f'{Exp_name}/seed_{seed}/{model_name}/{data_name}/'
                        f'{optimizer_name}/train_{data_info["train_test"][0]}_'
                        f'test_{data_info["train_test"][1]}/'
                        f'Batch_size_{data_info["batch_size"]}/'
                        f'epoch_{data_info["epochs"]}/{ID}/'
                        f'Results_{ParametersHub.model_abbr(model_name)}_'
                        f'{data_name}_{optimizer_name}.pkl'
                    )
                else:
                    pkl_path = 1
                    assert ValueError 

                # there are many parameters
                data_ = kit.read_pkl_data(pkl_path)

                para_str = ParametersHub.opt_paras_str(optimizer_info,except_= "seed_ID")

                _draw_data[data_name][optimizer_name][seed] = data_[para_str][data_info["metric_key"]]

            y = []
            for seed_, seed_data in _draw_data[data_name][optimizer_name].items():
                y.append(seed_data)
            
            Y = np.vstack(y)
            y_mean = Y.mean(axis=0)
            y_std  = Y.std(axis=0)

            draw_data[data_name][optimizer_name]["y_mean"] = y_mean
            draw_data[data_name][optimizer_name]["y_std"] = y_std
            
            _subfigs(draw_data, info_dict, model_name, save_path = save_path,
                    save_name=save_name,
                    user_subtitle=user_subtitle,
                    user_line_style = user_line_style,
                    user_grid=user_grid,
                    color_scheme=color_scheme,
                    label_mapping=label_mapping,
                    ylimit=ylimit,
                    set_yscale_log=set_yscale_log,
                    fig_size = fig_size,
                    xlabel_size = xlabel_size,
                    ylabel_size=ylabel_size,
                    title_size=title_size,
                    legend_size=legend_size,
                    fig_show=fig_show,
                )

#------------------------------------------------
def _subfigs(draw_data, info_dict, model_name, cols = 3, save_path = None,
            save_name = None,
            user_subtitle = None,
            user_line_style = None,
            user_grid = True,
            color_scheme = "SPBM",
            linestyle_scheme = "SPBM",
            legend_loc = "upper",
            label_mapping = None,
            ylimit = {},
            set_yscale_log = {},
            xlabel_size = 16,
            fig_size = (6,6),
            title_size = 16,
            ylabel_size = 16,
            font_size = 12,
            legend_size = 14,
            xlabel_name = "epochs",
            fig_show = True
        ):
    
    # matplotlib settings
    mpl.rcParams['font.family'] = 'Times New Roman'
    mpl.rcParams["mathtext.fontset"] = "stix"
    mpl.rcParams["axes.unicode_minus"] = False
    mpl.rcParams["font.size"] = font_size
    mpl.rcParams["mathtext.rm"] = "Times New Roman"

    # Calculate the number of datasets
    num_datasets = len(draw_data)

    nrows = math.ceil(num_datasets / cols)
    fig, axes = plt.subplots(nrows, cols, figsize=(5 * cols, 4 * nrows), squeeze=False)
    axes = axes.flatten()

    for idx, (data_name, info) in enumerate(draw_data.items()):
        ax = axes[idx]
        for optimizer_name, metric_list in info.items():
            if user_line_style is not None:
                linestyle = linestyle_schedule(linestyle_scheme)[optimizer_name]
            else:
                linestyle = None

            if label_mapping is not None:
                label_name = label_mapping[optimizer_name]
            else:
                label_name = optimizer_name

            ax.plot(metric_list["y_mean"], label=label_name, 
                    color = colors_schedule(color_scheme)[optimizer_name],
                    linestyle = linestyle
                )
            
            ax.fill_between(
                np.arange(0, len(metric_list["y_mean"])),
                metric_list["y_mean"] - metric_list["y_std"],
                metric_list["y_mean"] + metric_list["y_std"],
                alpha = 0.3
            )

            if idx == 0:
                ax.set_ylabel(ParametersHub.fig_ylabel(info_dict[data_name]["metric_key"]), fontsize=ylabel_size) 

            # marker
            if info_dict[data_name].get("marker") is not None:
                x = np.array(info_dict[data_name]["marker"])

                metric_list_arr = np.array(metric_list["y_mean"])

                ax.scatter(x, metric_list_arr[x], 
                        marker = marker_schedule(linestyle_scheme)[optimizer_name], 
                        color = colors_schedule(color_scheme)[optimizer_name]
                    )

        if user_subtitle == None:
            set_subtitle = data_name
        else:
            set_subtitle = user_subtitle[idx]

        ax.set_title(set_subtitle, fontsize=title_size)
        ax.set_xlabel(xlabel_name, fontsize=xlabel_size)
        # ax.set_ylabel(ParametersHub.fig_ylabel(info_dict[data_name]["metric_key"]), fontsize=12) 
        
        if set_yscale_log.get(data_name) is not None:
            ax.set_yscale("log")
        # ax.set_xticks([0, 10, 20, 30, 40])
        # ax.set_xticklabels([r"$10^2$", "10", "20", "30", "40"])
        ax.grid(user_grid)

        if ylimit.get(data_name) is not None:
            ylim = ylimit[data_name]
            ax.set_ylim(ylim[0], ylim[1])

    # Hide redundant axes
    for ax in axes[num_datasets:]:
        ax.axis('off')

    # legend
    all_handles, all_labels = [], []
    for ax in axes[:num_datasets]:
        h, l = ax.get_legend_handles_labels()
        all_handles.extend(h)
        all_labels.extend(l)
    
    # duplicate removal
    unique = dict(zip(all_labels, all_handles))
    handles = list(unique.values())
    labels = list(unique.keys())
    
    if legend_loc == "lower":
        fig.legend(
            handles,
            labels,
            loc="lower center",
            bbox_to_anchor=(0.5, -0.08),
            ncol=min(len(handles), 4),
            fontsize=legend_size,
            # frameon=False 
        )
    elif legend_loc == "upper":
        fig.legend(
            handles,
            labels,
            loc="upper center",
            bbox_to_anchor=(0.5, 1.10),
            ncol=len(handles),
            fontsize=legend_size
        )
    else:
        print(legend_loc)
        assert False

    plt.tight_layout()
    if save_path is None:
        save_path_ = f'{model_name}.pdf'
    else:
        os.makedirs(save_path, exist_ok=True)
        save_path_ = f'{save_path}/{save_name}.pdf'
    plt.savefig(save_path_, bbox_inches="tight")
    plt.savefig(save_path_.replace("pdf", "png"), bbox_inches="tight")
    if fig_show:
        plt.show()
    plt.close("all")  # Colse the fig
    print(save_path_)


def diff_seed_onefig(model_name, info_dict, Exp_name,
            save_path = None, 
            save_name = None, 
            fig_show = False,
            user_title = None,
            user_grid = True,
            color_scheme = "SPBM",
            label_mapping = None,
            ylimit = None,
            user_line_style = None,
            set_yscale_log = None,
            fig_size = (6,6), 
            xlabel_size=18,
            ylabel_size=18,
            title_size=16,
            legend_size=14,
            font_size=12,
            with_paras = True
        ):
    xlabels = {}
    _draw_data = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    draw_data = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

    # get the path of pkl
    for data_name, data_info in info_dict.items():
        for optimizer_name, optimizer_info in data_info["optimizer"].items():
            for seed, ID in optimizer_info.get("seed_ID", {}).items():
                # print(data_name, optimizer_name, seed, ID)
                if data_info.get("epochs") is not None:
                    xlabels[data_name] = "epochs"
                    pkl_path = (
                        f'{Exp_name}/seed_{seed}/{model_name}/{data_name}/'
                        f'{optimizer_name}/train_{data_info["train_test"][0]}_'
                        f'test_{data_info["train_test"][1]}/'
                        f'Batch_size_{data_info["batch_size"]}/'
                        f'epoch_{data_info["epochs"]}/{ID}/'
                        f'Results_{ParametersHub.model_abbr(model_name)}_'
                        f'{data_name}_{optimizer_name}.pkl'
                    )
                else:
                    pkl_path = 1
                    assert ValueError 

                # there are many parameters
                data_ = kit.read_pkl_data(pkl_path)

                para_str = ParametersHub.opt_paras_str(optimizer_info,except_= "seed_ID")

                _draw_data[data_name][optimizer_name][seed] = data_[para_str][data_info["metric_key"]]

            y = []
            for seed_, seed_data in _draw_data[data_name][optimizer_name].items():
                y.append(seed_data)
            
            Y = np.vstack(y)
            y_mean = Y.mean(axis=0)
            y_std  = Y.std(axis=0)

            draw_data[data_name][optimizer_name]["y_mean"] = y_mean
            draw_data[data_name][optimizer_name]["y_std"] = y_std

    _onefig(draw_data, model_name, info_dict, save_path = save_path, 
            save_name = save_name,
            font_size=font_size, 
            fig_size = fig_size, 
            label_mapping = label_mapping,
            with_paras = with_paras,
            fig_show = fig_show,
            xlabels = xlabels,
            user_title = user_title,
            user_line_style = user_line_style,
            color_scheme = color_scheme,
            user_grid = user_grid,
            ylimit = ylimit,
            set_yscale_log = set_yscale_log,
            xlabel_size=xlabel_size,
            ylabel_size=ylabel_size,
            title_size=title_size,
            legend_size=legend_size,
        )


#------------------------------------------------
def _onefig(draw_data, model_name, info_dict, save_path = None, save_name = None,
        font_size=12, 
        fig_size = (6,6), 
        label_mapping = None,
        with_paras = True,
        fig_show = False,
        xlabels = None,
        user_title = None,
        user_line_style = None,
        color_scheme = "SPBM",
        user_grid = True,
        ylimit = None,
        set_yscale_log = None,
        xlabel_size=18,
        ylabel_size=18,
        title_size=16,
        legend_size=14,
    ):

    mpl.rcParams['font.family'] = 'Times New Roman'
    mpl.rcParams["mathtext.fontset"] = "stix"
    mpl.rcParams["axes.unicode_minus"] = False
    mpl.rcParams["font.size"] = font_size
    mpl.rcParams["mathtext.rm"] = "Times New Roman"

    plt.figure(figsize=fig_size)  # Optional: set figure size
    
    if len(draw_data) == 0:
        raise ValueError("draw_data is empty")
    else:
        data_name = next(iter(draw_data))

    for data_name, _info in draw_data.items():
        for optimizer_name, metric_dict in _info.items():
            if label_mapping is not None:
                label_name = label_mapping[optimizer_name]
            else:
                label_name = optimizer_name
            
            # set optimal paras
            if with_paras:
                label_name = f'{label_name}_{metric_dict["param_str"]}'

            plt.plot(metric_dict["y_mean"], label=label_name,
                    color=colors_schedule(color_scheme)[optimizer_name],
                    )

    if data_name is not None:
        if user_title == None:
            set_title = data_name
        else:
            set_title = user_title
    
    else:
        set_title = 'None'

    plt.title(set_title, fontsize=title_size)

    if with_paras:
        plt.legend(loc='upper center', 
                bbox_to_anchor=(0.5, -0.15), ncol=1,
                fontsize=legend_size) 
    
    else:
        plt.legend(fontsize=legend_size)

    plt.grid(user_grid)

    if set_yscale_log:
        plt.yscale("log")
    
    if ylimit is not None:
        plt.ylim(ylimit[0], ylimit[1])

    plt.tight_layout()  # Adjust layout so the legend fits
    
    plt.xlabel(data_name,
            fontsize=xlabel_size)  # Or whatever your x-axis represents
    
    plt.ylabel(f'{ParametersHub.fig_ylabel(info_dict[data_name]["metric_key"])}',
            fontsize=ylabel_size)  
    
    if save_path is None:
        save_path_ = f'{model_name}.pdf'
    else:
        os.makedirs(save_path, exist_ok=True)
        save_path_ = f'{save_path}/{save_name}.pdf'
    plt.savefig(save_path_, bbox_inches="tight")
    plt.savefig(save_path_.replace("pdf", "png"), bbox_inches="tight")
    if fig_show:
        plt.show()
    
    plt.close("all")
    print(save_path_)