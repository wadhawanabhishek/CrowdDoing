from IPython.display import HTML
import plotly.express as px
import pandas as pd


def figures_to_html(figs, filename):
    with open(filename, 'w') as dashboard:
        dashboard.write("<html><head></head><body>" + "\n")
        for fig in figs:
            if isinstance(fig,pd.DataFrame):
                inner_html = fig.to_html(classes='mystyle')
            else: 
                inner_html = fig.to_html().split('<body>')[1].split('</body>')[0]
            dashboard.write(inner_html)
        dashboard.write("</body></html>" + "\n")


def outliers(df):

    pollutant = df['Pollutant'].unique()[0]
    q1=df["Slope"].quantile(0.25)

    q3=df["Slope"].quantile(0.75)

    IQR=q3-q1

    outliers = df[((df["Slope"]<(q1-1.5*IQR)) | (df["Slope"]>(q3+1.5*IQR)))]
    fig = px.box(df, y="Slope",hover_name="County",title= "<b>"+pollutant+" Outliers </b>")
    outliers_annotations = outliers[["County","Slope"]].sort_values(by ="Slope",ascending=False)
    outliers_lst = outliers_annotations.values.tolist()

    for county, slope in outliers_lst:
        fig.add_annotation(x=0.05, y=slope, #Q1
                text=county,
                font=dict(size=10),
                showarrow=False,
                )
    # fig['layout'].update(height = 800,width =800)
    return fig

def update_fig_size(fig,h=800,w=1200):

    fig['layout'].update(height = h,width =w)
    return fig
