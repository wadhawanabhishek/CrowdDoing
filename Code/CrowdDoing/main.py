
from fileinput import filename
from Clustering_Data import Clustering_data
from functions import figures_to_html,outliers,update_fig_size
from plot_map import Plot_Map
from pollutant import Pollutant
from regression_analysis import regression_analysis
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import webbrowser
from pathlib import Path

trend_chart_dashboard = Path(r'dashboard.html')
regression_chart_dashboard = Path(r'dashboard2.html')
clustering_chart_dashboard = Path(r'dashboard3.html')
  


df1 = Pollutant("co",2010,2021).run()
df2 = Pollutant("pm2.5",2010,2021).run()
df3 = Pollutant("ozone",2010,2021).run()

fig1,f1 = Plot_Map(df1,'conc').run()
fig2,f2 = Plot_Map(df2,'conc').run()
fig3,f3 = Plot_Map(df3,'conc').run()

figures_to_html([fig1,update_fig_size(f1), fig2,update_fig_size(f2), fig3,update_fig_size(f3)],trend_chart_dashboard)

fig4,df4 = regression_analysis(df1,'conc').run()
fig5,df5 = regression_analysis(df2,'conc').run()
fig6,df6 = regression_analysis(df3,'conc').run()

figures_to_html([update_fig_size(fig4),df4,update_fig_size(fig5),df5 ,update_fig_size(fig6),df6],
                regression_chart_dashboard)


df7,fig7 = Clustering_data(df4).run()
df8,fig8 = Clustering_data(df5).run()
df9,fig9 = Clustering_data(df6).run()

outlier_fig_1 = outliers(df7)
outlier_fig_2 = outliers(df8)
outlier_fig_3 = outliers(df9)


figures_to_html([update_fig_size(fig7),update_fig_size(outlier_fig_1),df7,update_fig_size(fig8),update_fig_size(outlier_fig_2),df8,
                update_fig_size(fig9),update_fig_size(outlier_fig_3),df9],
                clustering_chart_dashboard)

webbrowser.open_new_tab('dashboard.html')
webbrowser.open_new_tab('dashboard2.html')
webbrowser.open_new_tab('dashboard3.html')