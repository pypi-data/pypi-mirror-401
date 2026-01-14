import matplotlib.pyplot as plt

# define A4 size
A4_W, A4_H = 8.27, 11.69  # portrait

fig3 = plt.figure(figsize=(A4_W, A4_H), constrained_layout=True)
gs = fig3.add_gridspec(3, 3)
f3_ax1 = fig3.add_subplot(gs[0, :])
f3_ax1.set_title("gs[0, :]")
f3_ax2 = fig3.add_subplot(gs[1, :-1])
f3_ax2.set_title("gs[1, :-1]")
f3_ax3 = fig3.add_subplot(gs[1:, -1])
f3_ax3.set_title("gs[1:, -1]")
f3_ax4 = fig3.add_subplot(gs[-1, 0])
f3_ax4.set_title("gs[-1, 0]")
f3_ax5 = fig3.add_subplot(gs[-1, -2])
f3_ax5.set_title("gs[-1, -2]")


if __name__ == "__main__":
    from pathlib import Path

    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages

    from eta_incerto.plotting.performance import PerformancePlot
    from eta_incerto.plotting.scenario import ScenarioPlot
    from eta_incerto.plotting.table import TablePlot
    from eta_incerto.plotting.topology import TopologyPlot

    # --- adjust these paths to your machine ---
    h5_path_w_invest = Path(
        r"C:/Git/eta-incerto/examples/hp_comparison/results/stochastic_expected_with_invest_opex.h5"
    )
    h5_path_wo_invest = Path(r"C:/Git/eta-incerto/examples/hp_comparison/results/stochastic_expected.h5")
    out_dir = Path(r"C:/Git/eta-incerto/examples/hp_comparison/plots")
    out_dir.mkdir(parents=True, exist_ok=True)

    topo = TopologyPlot(h5_path=h5_path_w_invest)
    scenario = ScenarioPlot(h5_path=h5_path_w_invest)
    performance = PerformancePlot(h5_without_invest=h5_path_wo_invest, h5_with_invest=h5_path_w_invest)
    table = TablePlot(h5_path=h5_path_w_invest)

    # Figure 1/ pdf page 1
    fig = plt.figure(figsize=(8.27, 11.69), constrained_layout=True)  # A4 portrait
    gs = fig.add_gridspec(3, 1)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[1, 0])  # middle
    ax3 = fig.add_subplot(gs[2, 0])

    ax1.set_title("Top subplot", pad=10)
    ax2.set_title("Middle subplot", pad=10)
    ax3.set_title("Bottom subplot", pad=10)

    topo.plot_into(ax1, use_graphviz=True)
    scenario.plot_into(ax2, ylabel_suffix="\nEUR/kWh")
    performance.plot_into(ax3, title="performance")
    # global spacing first
    fig.subplots_adjust(top=0.97, bottom=0.05, hspace=0.30)

    # Figure 2 / pdf page 2
    fig_table = plt.figure(figsize=(8.27, 11.69), constrained_layout=True)  # A4 portrait
    ax_table = fig_table.add_subplot(111)
    table.plot_into(ax_table)

    out_pdf = out_dir / "comparison_A4_two_pages.pdf"
    with PdfPages(out_pdf) as pdf:
        pdf.savefig(fig, bbox_inches="tight", pad_inches=0.1)  # your page 1 (topology/scenario/performance)
        pdf.savefig(fig_table, bbox_inches="tight", pad_inches=0.1)  # page 2 (the KPI table)
