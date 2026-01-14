"""
----------------------------------------------------------------------
>>> Author       : Junshan Yin  
>>> Last Updated : 2026-01-10
----------------------------------------------------------------------
"""

import math, os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from junshan_kit import kit, ParametersHub, PlotUtils
from collections import defaultdict

def _get_info_from_pkl(info_dict, Exp_name, model_name, ):
    
    # Define many variable
    xlabels = {}
    _draw_data = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    opt_paras = defaultdict(lambda: defaultdict(dict))
    
    # Reading data
    for data_name, data_info in info_dict.items():
        for optimizer_name, optimizer_info in data_info["optimizer"].items():
            for seed, ID in optimizer_info.get("seed_ID", {}).items():
                
                # set xlabel name and path of pkl file
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
                    xlabels[data_name] = "iteration"
                    pkl_path = (
                        f'{Exp_name}/seed_{seed}/{model_name}/{data_name}/'
                        f'{optimizer_name}/train_{data_info["train_test"][0]}_'
                        f'test_{data_info["train_test"][1]}/'
                        f'Batch_size_{data_info["batch_size"]}/'
                        f'iter_{data_info["iteration"]}/{ID}/'
                        f'Results_{ParametersHub.model_abbr(model_name)}_'
                        f'{data_name}_{optimizer_name}.pkl'
                    )

                # there are many parameters
                data_ = kit.read_pkl_data(pkl_path)

                para_str = ParametersHub.opt_paras_str(optimizer_info,except_= "seed_ID")

                _draw_data[data_name][optimizer_name][seed] = data_[para_str][data_info["metric_key"]]
                opt_paras[data_name][optimizer_name]["para_str"] = para_str

    return _draw_data, xlabels, opt_paras

def subfigs(draw_data, info_dict, model_name,
        user_line_style = None,  # eg: "SPBM"
        label_mapping = None,
        color_scheme = None,
        fill_between = True,
        user_subtitle = None,
        save_path = None,
        save_name = None,
        set_yscale_log = {},
        ylimit = {},
        user_grid = True,
        makers = True,
        xlabel_name = None, 
        legend_loc = "upper",
        ylabel_size = 16,
        title_size = 16,
        xlabel_size = 16,
        legend_size = 14,
        cols = 3,
        font_size = 12,
        fig_show = True,
        opt_paras = None
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

    for idx, (data_name, draw_values) in enumerate(draw_data.items()):
        ax = axes[idx]

        for opt_name, metric in draw_values.items():

            # seed 
            Y = np.stack(list(metric.values()), axis=0)
            y_mean = Y.mean(axis=0)
            y_std  = Y.std(axis=0)

            # set figs
            line_style, label_name, color, ax = PlotUtils.set_fig_info(
                user_line_style,
                label_mapping,
                color_scheme,
                opt_name,
                makers,
                y_mean,
                ax,
                data_name,
                opt_paras,
            )

            ax.plot(
                y_mean,
                label=label_name,
                color=color,
                linestyle=line_style
            )

            if fill_between:
                ax.fill_between(
                    np.arange(0, len(y_mean)),
                    y_mean - y_std,
                    y_mean + y_std,
                    alpha = 0.3
                )
            if idx % cols == 0:
                ax.set_ylabel(ParametersHub.fig_ylabel(info_dict[data_name]["metric_key"]), fontsize=ylabel_size) 

        if user_subtitle == None:
            set_subtitle = data_name
        else:
            set_subtitle = user_subtitle[idx]

        if xlabel_name is None:
            xlabel = "epochs"
        else:
            xlabel = xlabel_name[data_name]
        
        ax.set_title(set_subtitle, fontsize=title_size)
        ax.set_xlabel(xlabel, fontsize=xlabel_size)

        # set log
        if set_yscale_log.get(data_name) is None:
            ax.set_yscale("log")
        # ax.set_xticks([0, 10, 20, 30, 40])
        # ax.set_xticklabels([r"$10^2$", "10", "20", "30", "40"])
        ax.grid(user_grid)
        # ax.legend()

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
            bbox_to_anchor=(0.5, 1.1),
            ncol=len(handles),
            fontsize=legend_size
        )
    else:
        print(legend_loc)
        assert False

    plt.tight_layout()
    if save_path is None:
        save_path_ = f'{model_name}_{save_name}.pdf'
    else:
        os.makedirs(save_path, exist_ok=True)
        save_path_ = f'{save_path}/{save_name}.pdf'

    plt.savefig(save_path_, bbox_inches="tight")
    plt.savefig(save_path_.replace("pdf", "png"), bbox_inches="tight")
    print(save_path_)
    if fig_show:
        plt.show()
    
    plt.close("all")  # Colse the fig


def onefig(draw_data, info_dict, model_name,
        user_line_style = None,  # eg: "SPBM"
        label_mapping = None,
        color_scheme = None,
        fill_between = True,
        user_subtitle = None,
        save_path = None,
        save_name = None,
        set_yscale_log = {},
        ylimit = {},
        user_grid = True,
        makers = True,
        xlabel_name = None, 
        legend_loc = "upper",
        ylabel_size = 16,
        title_size = 16,
        xlabel_size = 16,
        legend_size = 14,
        font_size = 12,
        fig_show = True,
        opt_paras = None,
        ncol = 1
        ):

    # matplotlib settings
    mpl.rcParams['font.family'] = 'Times New Roman'
    mpl.rcParams["mathtext.fontset"] = "stix"
    mpl.rcParams["axes.unicode_minus"] = False
    mpl.rcParams["font.size"] = font_size
    mpl.rcParams["mathtext.rm"] = "Times New Roman"
    
    fig, axes = plt.subplots(1, 1, squeeze=False)
    axes = axes.flatten()

    for idx, (data_name, draw_values) in enumerate(draw_data.items()):
        ax = axes[idx]

        for opt_name, metric in draw_values.items():

            # seed 
            Y = np.stack(list(metric.values()), axis=0)
            y_mean = Y.mean(axis=0)
            y_std  = Y.std(axis=0)

            # set figs
            line_style, label_name, color, ax = PlotUtils.set_fig_info(
                user_line_style,
                label_mapping,
                color_scheme,
                opt_name,
                makers,
                y_mean,
                ax,
                data_name,
                opt_paras,
            )

            ax.plot(
                y_mean,
                label=label_name,
                color=color,
                linestyle=line_style
            )

            if fill_between:
                ax.fill_between(
                    np.arange(0, len(y_mean)),
                    y_mean - y_std,
                    y_mean + y_std,
                    alpha = 0.3
                )

            if idx == 0:
                ax.set_ylabel(ParametersHub.fig_ylabel(info_dict[data_name]["metric_key"]), fontsize=ylabel_size) 

        if user_subtitle == None:
            set_subtitle = data_name
        else:
            set_subtitle = user_subtitle[idx]

        if xlabel_name is None:
            xlabel = "epochs"
        else:
            xlabel = xlabel_name[data_name]
        
        ax.set_title(set_subtitle, fontsize=title_size)
        ax.set_xlabel(xlabel, fontsize=xlabel_size)

        # set log
        if set_yscale_log.get(data_name) is None:
            ax.set_yscale("log")
        # ax.set_xticks([0, 10, 20, 30, 40])
        # ax.set_xticklabels([r"$10^2$", "10", "20", "30", "40"])
        ax.grid(user_grid)
        ax.legend(ncol=ncol)

        if ylimit.get(data_name) is not None:
            ylim = ylimit[data_name]
            ax.set_ylim(ylim[0], ylim[1])
            

    plt.tight_layout()
    if save_path is None:
        save_path_ = f'{model_name}_{save_name}.pdf'
    else:
        os.makedirs(save_path, exist_ok=True)
        save_path_ = f'{save_path}/{save_name}.pdf'

    plt.savefig(save_path_, bbox_inches="tight")
    plt.savefig(save_path_.replace("pdf", "png"), bbox_inches="tight")
    print(save_path_)
    if fig_show:
        plt.show()
    
    plt.close("all")  # Colse the fig


