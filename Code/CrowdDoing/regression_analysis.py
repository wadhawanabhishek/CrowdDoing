from plot_map import Plot_Map
from sklearn import linear_model
import plotly.graph_objects as go
import warnings
import plotly.express as px
import pandas as pd
from scipy import stats
import numpy as np
from plotly.subplots import make_subplots
warnings.filterwarnings("ignore")

class regression_analysis(Plot_Map):
    
    def __init__(self,df,calc_type):
        self.__pollutant = None
    
        super().__init__(df,calc_type)
        
    def __r_trans_df(self):
        
        df =  super()._transform_data()
        cols = df.columns
        self.__pollutant = cols[2].split()[2]
        df['Year'] = pd.to_numeric(df['Year'])
        return df
    
    def __reg_analysis(self,initial_df):
        
        df = initial_df
        cols = df.columns
        counties_list = df.COUNTY.unique().tolist()
        appended_data =[]
        
        for i,county in enumerate(counties_list):

            df2 = df[df['COUNTY']==county]

            ## Regression Analysis
            X = df2['Year'].values.tolist()
            y = df2[cols[2]].values.tolist()

            X_f = np.array(X, dtype=np.float32)
            y_f = np.array(y, dtype=np.float32)

            slope, intercept, r_value, p_value, std_err = stats.linregress(X_f,y_f)
            line = str(round(slope,4)) + ' * '+'Year '+ '+ ' + str(round(intercept,4))

            sig=lambda p_value: True if p_value <= 0.05 else False


            data = {'County':county,'Slope':slope,'R-Squared Value':r_value**2,'P-Value':p_value,
                    'P-Value less than 0.05?':sig(p_value),
                    'Line-Equation': line}

            data_df = pd.DataFrame(data,index = [i])
            appended_data.append(data_df)

            final_df = pd.concat(appended_data)
            
        self.__annotations = final_df['Line-Equation'].values.tolist()
        
        return final_df
    
    def __getmap(self,trans_df):
        
        map_df = trans_df
        map_df['Year'] = pd.to_numeric(map_df['Year'])
        cols = map_df.columns.tolist()
        
        fig = px.scatter(map_df, x="Year", y=cols[2], color="COUNTY",trendline='ols',trendline_color_override='red')

        fig.update_layout(
            title = "<b>"+self.__pollutant+" Data " + "Regression Analysis </b>",
            updatemenus=[
                {
                    "buttons": [
                        {
                            "label": m,
                            "method": "update",
                            "args": [
                                {
                                    "visible": [
                                        True if m == "All" else t.name == m for t in fig.data
                                    ]
                    
                                }
                            ],
                        }
                        for m in ["All"] + map_df["COUNTY"].unique().tolist()
                    ]
                }
            ]
        )
        
        return fig
        # fig.show()
        
    def run(self):
        initial_df = self.__r_trans_df()
        final_df = self.__reg_analysis(initial_df)
        final_df['Pollutant']  = self.__pollutant
        figure = self.__getmap(initial_df)
        return figure,final_df
          

        
        