import pickle
import inflection
import pandas as pd
import numpy as np
import math
import datetime

class Rossmann(object):
    def __init__(self):
        self.home_path= '/home/pietro/Documents/MyJourneyDS/ComunidadeDS/DSemProducao/my-codes/'
        self.competition_distance_scaler   = pickle.load(open(self.home_path + 'parameters/competition_distance_scaler.pkl', 'rb'))
        
        self.competition_time_month_scaler = pickle.load(open(self.home_path + 'parameters/competition_time_month_scaler.pkl', 'rb'))
        
        self.promo_time_week_scaler        = pickle.load(open(self.home_path + 'parameters/promo_time_week_scaler.pkl', 'rb'))
        
        self.year_scaler                   = pickle.load(open(self.home_path + 'parameters/year_scaler.pkl', 'rb'))
        
        self.store_type_scaler             = pickle.load(open(self.home_path + 'parameters/store_type_scaler.pkl', 'rb'))
        
    def data_cleaning(self, dataframe):

        ## Rename Columns
        old_columns = ['Store', 'DayOfWeek', 'Date', 'Open', 'Promo','StateHoliday', 'SchoolHoliday', 'StoreType', 'Assortment',
                    'CompetitionDistance', 'CompetitionOpenSinceMonth', 'CompetitionOpenSinceYear', 'Promo2', 'Promo2SinceWeek', 'Promo2SinceYear', 'PromoInterval']

        snakecase = lambda x: inflection.underscore(x)

        new_columns = list(map(snakecase, old_columns))

        dataframe.columns = new_columns

        
        ## Data Types
        dataframe['date'] = pd.to_datetime(dataframe['date'])

        
        ## Fillout NAN
        # competition_distance 
        dataframe['competition_distance'] = dataframe['competition_distance'].apply(lambda x: 200000.0 if math.isnan(x) else x)

        # competition_open_since_month (fornece o mês aproximados em que o concorrente mais próximo foi aberto)
        dataframe['competition_open_since_month'] = dataframe.apply(lambda x: x['date'].month if math.isnan(x['competition_open_since_month']) else x['competition_open_since_month'], axis= 1)

        # competition_open_since_year (fornece o ano aproximados em que o concorrente mais próximo foi aberto)
        dataframe['competition_open_since_year'] = dataframe.apply(lambda x: x['date'].year if math.isnan(x['competition_open_since_year']) else x['competition_open_since_year'], axis= 1)

        # promo2_since_week (descreve a semana em que a loja começou a participar da Promo2)
        dataframe['promo2_since_week'] = dataframe.apply(lambda x: x['date'].week if math.isnan(x['promo2_since_week']) else x['promo2_since_week'], axis= 1)

        # promo2_since_year (descreve o ano em que a loja começou a participar da Promo2)      
        dataframe['promo2_since_year'] = dataframe.apply(lambda x: x['date'].year if math.isnan(x['promo2_since_year']) else x['promo2_since_year'], axis= 1)

        #promo_interval (descreve os intervalos consecutivos em que a Promo2 é iniciada, nomeando os meses em que a promoção é reiniciada. )
        month_map = {1: 'Jan', 2: 'Fev',3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

        dataframe['promo_interval'].fillna(0, inplace= True)

        dataframe['month_map'] = dataframe['date'].dt.month.map(month_map)

        dataframe['is_promo'] = dataframe[['promo_interval', 'month_map']].apply(lambda x: 0 if x['promo_interval'] == 0 else 1 if x['month_map'] in x['promo_interval'].split(',') else 0, axis= 1)

        
        ## Change Data Types
        #competition
        dataframe['competition_open_since_month'] = dataframe['competition_open_since_month'].astype(int)
        dataframe['competition_open_since_year'] = dataframe['competition_open_since_year'].astype(int)

        #promo2
        dataframe['promo2_since_week'] = dataframe['promo2_since_week'].astype(int)
        dataframe['promo2_since_year'] = dataframe['promo2_since_year'].astype(int)
        
        
        return dataframe
        
    def feature_engineering(self, dataframe_2):
        
        ## Feature Engineering
        #year
        dataframe_2['year'] = dataframe_2['date'].dt.year

        #month
        dataframe_2['month'] = dataframe_2['date'].dt.month

        #day
        dataframe_2['day'] = dataframe_2['date'].dt.day

        #week of year
        dataframe_2['week_of_year'] = dataframe_2['date'].dt.weekofyear

        #year week
        dataframe_2['year_week'] = dataframe_2['date'].dt.strftime('%Y-%W')

        #competition since 
        dataframe_2['competition_since'] = dataframe_2.apply(lambda x: datetime.datetime(year= x['competition_open_since_year'], month= x['competition_open_since_month'], day= 1), axis= 1)
        dataframe_2['competition_time_month'] = ((dataframe_2['date'] - dataframe_2['competition_since']) / 30).apply(lambda x: x.days).astype(int)

        #promo since
        dataframe_2['promo_since'] = dataframe_2['promo2_since_year'].astype(str) + '-' + dataframe_2['promo2_since_week'].astype(str)
        dataframe_2['promo_since'] = dataframe_2['promo_since'].apply(lambda x: datetime.datetime.strptime(x + '-1', '%Y-%W-%w') - datetime.timedelta(days= 7))
        dataframe_2['promo_time_week'] = ((dataframe_2['date'] - dataframe_2['promo_since']) / 7).apply(lambda x: x.days).astype(int)

        # assortment
        dataframe_2['assortment'] = dataframe_2['assortment'].apply(lambda x: 'basic' if x == 'a' else 'extra' if x == 'b' else 'extended')

        #state holiday 
        dataframe_2['state_holiday'] = dataframe_2['state_holiday'].apply(lambda x: 'public_holiday' if x == 'a' else 'easter_holiday' if x == 'b' else 'christmas' if x == 'c' else 'regular_day')
    
        ## Filtering Variables
        ### Line Filtering
        dataframe_2 = dataframe_2[dataframe_2['open'] != 0]

        ### Column Selection
        excluded_columns = ['open', 'promo_interval', 'month_map']
        dataframe_2 = dataframe_2.drop(excluded_columns, axis= 1)
        
        
        return dataframe_2
    
    def data_preparation(self, dataframe_3):
        
        ## Rescaling
        # competition distance
        dataframe_3['competition_distance'] = self.competition_distance_scaler.transform(dataframe_3[['competition_distance']].values)

        # competition time month
        dataframe_3['competition_time_month'] = self.competition_time_month_scaler.transform(dataframe_3[['competition_time_month']].values)

        # promo time week
        dataframe_3['promo_time_week'] = self.promo_time_week_scaler.transform(dataframe_3[['promo_time_week']].values)
        #year
        dataframe_3['year'] = self.year_scaler.transform(dataframe_3[['year']].values)

        
        ## Transformation
        ### Encoding
        # state holiday >>> one hot encoding
        dataframe_3 = pd.get_dummies(dataframe_3, prefix= ['state_holiday'], columns= ['state_holiday'])

        # store type >>> label encoding
        dataframe_3['store_type'] = self.store_type_scaler.transform(dataframe_3['store_type'])

        # assortment >>> ordinal encoding
        assortment_dictionary = {'basic': 1, 'extra': 2, 'extended': 3}
        dataframe_3['assortment'] = dataframe_3['assortment'].map(assortment_dictionary)

        ### Nature Transformation
        # day of week
        dataframe_3['day_of_week_sin'] = dataframe_3['day_of_week'].apply(lambda x: np.sin( x * (2. * np.pi/7)))
        dataframe_3['day_of_week_cos'] = dataframe_3['day_of_week'].apply(lambda x: np.cos( x * (2. * np.pi/7)))

        # month
        dataframe_3['month_sin'] = dataframe_3['month'].apply(lambda x: np.sin( x * (2. * np.pi/12)))
        dataframe_3['month_cos'] = dataframe_3['month'].apply(lambda x: np.cos( x * (2. * np.pi/12)))

        # day
        dataframe_3['day_sin'] = dataframe_3['day'].apply(lambda x: np.sin( x * (2. * np.pi/30)))
        dataframe_3['day_cos'] = dataframe_3['day'].apply(lambda x: np.cos( x * (2. * np.pi/30)))

        # week of year
        dataframe_3['week_of_year_sin'] = dataframe_3['week_of_year'].apply(lambda x: np.sin( x * (2. * np.pi/52)))
        dataframe_3['week_of_year_cos'] = dataframe_3['week_of_year'].apply(lambda x: np.cos( x * (2. * np.pi/52)))
        
        columns_selected = ['store', 'promo', 'store_type', 'assortment',
                            'competition_distance', 'competition_open_since_month',
                            'competition_open_since_year', 'promo2', 'promo2_since_week',
                            'promo2_since_year', 'competition_time_month', 'promo_time_week',
                            'day_of_week_sin', 'day_of_week_cos', 'month_sin', 'month_cos',
                            'day_sin', 'day_cos', 'week_of_year_sin', 'week_of_year_cos']
        
        
        return dataframe_3[columns_selected]
    
    
    def get_prediction(self, model, original_data, test_data):
        #prediction
        pred = model.predict(test_data)
        
        #join pred into the original data
        original_data['prediction'] = np.expm1(pred)
        
        
        return original_data.to_json(orient= 'records', date_format= 'iso')
