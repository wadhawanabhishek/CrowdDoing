from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
from yellowbrick.cluster import KElbowVisualizer
import plotly.express as px

class Clustering_data:
    
    def __init__(self,regression_df,clusters = 4):
        self.df = regression_df
        self.f_clusters = clusters
        
        
    def __cluster_number_analysis(self):
        self.df.sort_values('Slope',ignore_index=True,inplace=True)
        x1 = np.array(self.df.index.values)
        x2 = np.array(self.df['Slope'].values)
        X = np.array(list(zip(x1, x2))).reshape(len(x1), 2)
        X=np.nan_to_num(X)
        
        
        # model = KMeans()
        # visualizer = KElbowVisualizer(
        #     model, k=(2,10))

        # visualizer.fit(X)        # Fit the data to the visualizer
        # visualizer.poof() 
        
        return X
        
    def __assigning_clusters(self,X):
        km = KMeans(
        n_clusters=self.f_clusters, init='k-means++',
        n_init=10, max_iter=300, 
        tol=1e-04, random_state=0)
        y_km = km.fit_predict(X)
        self.df['Cluster']=y_km
        self.df['group'] = self.df['Cluster'].ne(self.df['Cluster'].shift()).cumsum()

        mapping = {1:'Low', 2:'Medium', 3:'Increasing',4:'Heavily Increasing'}

        self.df['Pollution Trend']= self.df['group'].apply(lambda x : mapping[x])
        self.df.drop('group',axis=1,inplace=True)
        
    def __plot_clusters(self):
        fig = px.scatter(self.df,x=self.df.index.values,y='Slope',color='Cluster',hover_name='County',labels = 
                         dict(x = "County Index", Slope = "Slope of Regression Line"))
        title = '<b>Clustering for '+ self.df['Pollutant'].unique()[0]+' data</b>'
        fig.update_layout(title=title)
        # fig.show()
        return fig
        
    def run(self):
        X = self.__cluster_number_analysis()
        self.__assigning_clusters(X)
        figure = self.__plot_clusters()
        final_df = self.df
        return final_df,figure
        
    