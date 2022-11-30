from plotly.subplots import make_subplots
from math import ceil
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class Plot_Map():
    
    def __init__(self,df,calc_type:str):
        self.df = df
        self.typ = calc_type.lower()
        self.__pollutant = None
        self.units = None
        
        assert self.typ in ['conc','aqi'], "Not a valid Calculation Type!"
        
    def _transform_data(self):
        
        self.__pollutant = self.df.Pollutant.unique().tolist()[0]
        units = self.df.Units.unique().tolist()[0]
        self.units = units
        trans_df = self.df.drop(['Month','Pollutant','Units'],axis=1)
        trans_df= trans_df.groupby(['COUNTY','Year']).mean()
        trans_df.reset_index(['COUNTY','Year'],inplace=True)
        trans_df['Year'] = trans_df.Year.apply(lambda x : str(x))
        cols = trans_df.columns.tolist()
        trans_df[cols[2]] = trans_df[cols[2]].round(2)
        trans_df[cols[3]] = trans_df[cols[3]].round(2)
        pollutant_col = "Yearly Avg "+ self.__pollutant+ " Concentration"+"("+units+")"
        aqi_col = "Yearly Avg "+ self.__pollutant+" AQI VALUE"
        trans_df = trans_df.rename(columns={trans_df.columns[2]:pollutant_col,trans_df.columns[3]:aqi_col})
        
        if self.typ == 'conc':
            trans_df.drop(trans_df.columns[3],axis=1,inplace=True)
        else:
            trans_df.drop(trans_df.columns[2],axis=1,inplace=True)
        
        return trans_df
    
    def __getmap(self,trans_df):
        
        trans_df = trans_df
        
        counties = trans_df.COUNTY.unique()
        # print(len(counties))
#         cols = df_x.columns
        rows = ceil(len(counties)/4)
        colus = 4
        fig = make_subplots(rows=rows, cols=colus,subplot_titles=counties)
        fig['layout'].update(height=3400, width=1800,)
        fig['layout'].update(title = "<b>"+self.__pollutant+" Data Trend </b>")
        r = 1
        c = 1


        for county in counties:
            cdf = trans_df[trans_df['COUNTY']==county]
#             col = cdf.columns
            fig.add_trace(go.Scatter(x=cdf['Year'], y=cdf.iloc[:,2] ,name=county),row=r, col=c)
            fig.update_xaxes(title_text = "Year")
            fig.update_yaxes(title_text = "Pollutant Concentration "+"("+self.units+")")

            c+=1
            if c > 4:
                r+=1
                c=1

        return fig  

    def __getmap_analysis(self,trans_df):
        trans_df = trans_df
        cols = trans_df.columns.tolist()
        dic= dict(trans_df.groupby("COUNTY")[cols[2]].max())
        lst =[]
        for county in dic.keys():
            val = trans_df[(trans_df["COUNTY"]==county) & (trans_df[cols[2]]==dic[county])]["Year"].values
            data = {"County": county,"Concentration":dic[county],"Year":val}
            lst.append(data)

        d = pd.DataFrame(lst)
        d= d.explode('Year')
        d_n = pd.DataFrame(d['Year'].value_counts()).reset_index()
        d_n= d_n.rename(columns = {"index":"Year","Year":"Count"})
        f = px.bar(d_n, x= "Year",y ="Count",text = "Count",text_auto=True)
        f['layout'].update(title = "<b>"+self.__pollutant+" Maximum Pollution Years </b>")
        f.update_yaxes(title_text = "No. of Counties")
        return f    
        
    def run(self):
        trans_data = self._transform_data()
        figure = self.__getmap(trans_data)
        f =self.__getmap_analysis(trans_data)
        return figure,f