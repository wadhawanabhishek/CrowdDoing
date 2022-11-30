import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import plotly.express as px

# Currently we have data from 2010 - 2021

class Pollutant:

    def __init__(self,pollutant:str,start_year:int,end_year:int):
        self.__pollutant = pollutant.upper()
        self.__start_year = start_year
        self.__end_year = end_year
        self.__master_list = []
        self.__pollutant_list = ["CO","PM2.5","OZONE"]
        self.__units = None
        
        assert self.__pollutant in self.__pollutant_list ,"Not a valid Pollutant"
        assert isinstance(start_year,int),"Start Year is not Integer!"
        assert isinstance(end_year,int),"End Year is not Integer!"


    @property
    def pollutant(self):
        return self.__pollutant

    def __get_data(self):

        #

        try:
            #
            year_regex = re.compile(r'\d\d\d\d')
            github_url = 'https://github.com/wadhawanabhishek/CrowdDoing/tree/main/'+self.__pollutant+'_data'
            result = requests.get(github_url)
            soup = BeautifulSoup(result.text, 'html.parser')
            csvfiles = soup.find_all(title=re.compile("\.csv$"))
        except:
            #
            print("Resuouce not Found!")

        filename = [ ]
        for i in csvfiles:
            #
            filename.append(i.extract().get_text())

        years=[]
        for file in filename:
            year = year_regex.search(file)
            years.append(year.group())
        years =[int(i) for i in years]

        # 2011-2016  
        if (self.__start_year < min(years)) or (self.__start_year > max(years)):
            #
            print("Invalid Year Range. The Start Year Does not Exist")

        if (self.__end_year > max(years)) or (self.__end_year < self.__start_year) or (self.__end_year < min(years)):
            #
            print("Invalid Year Range. The End Year Does not Exist")

        new_lst = [i for i in range(self.__start_year,self.__end_year+1)]

        check =  all(item in years for item in new_lst)

        up_file=[]

        if check == True:
            #
            for file in filename:
                for yr in new_lst:
                    if str(yr) in file:
                        up_file.append(file)
        else: 
            raise Exception("The data for the given years not present")

        github_url = github_url.replace("github.com",'raw.githubusercontent.com')
        github_url = github_url.replace("tree/",'')

        appended_data =[]

        for f in up_file:
            url = github_url +'/'+ f
            data = pd.read_csv(url)
            appended_data.append(data)

        final_df = pd.concat(appended_data)
        self.__units = final_df['UNITS'].unique()[0]
        return final_df

    def __feature_extraction(self,data_df):
        
        df = data_df
        df = df.iloc[:, [0,17,2,4,6,15]]
        df = df[df['STATE']=='California']
        return df

    def __get_transformed_data(self,f_df):
        initial_df= f_df
        drop_cols = ['Site ID','STATE']
        for col in drop_cols:
            initial_df = initial_df.drop(col,axis = 1)
        initial_df = initial_df.groupby(['COUNTY','Date']).sum()
        initial_df=initial_df.reset_index(['Date','COUNTY'])
        initial_df['Date']= pd.to_datetime(initial_df['Date'],format='%m/%d/%Y')
        initial_df['Year']= pd.to_datetime(initial_df['Date']).dt.to_period('Y')
        initial_df['Month']= pd.to_datetime(initial_df['Date']).dt.to_period('M')
        initial_df = initial_df.drop("Date",axis = 1)
        cols = [initial_df.columns]
        final_df = initial_df.groupby(['COUNTY','Year','Month']).mean()
        final_df = final_df.reset_index(['COUNTY','Year','Month'])
        pollutant_col = "Monthly Avg "+ self.__pollutant+ " Concentration"
        final_df = final_df.rename(columns={final_df.columns[3]:pollutant_col,"DAILY_AQI_VALUE":"Monthly_Avg_AQI_VALUE"})
        final_df['Pollutant']= self.__pollutant
        final_df['Units'] = self.__units
        return final_df    

    def run(self):
        data_df = self.__get_data()
        feature_df = self.__feature_extraction(data_df)
        trans_df = self.__get_transformed_data(feature_df)
        return trans_df



