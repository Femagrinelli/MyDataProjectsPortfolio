#---------------------
# >>> Imports
#---------------------
import pandas    as pd
import numpy     as np
import matplotlib.pyplot as plt

from pandas_profiling import ProfileReport
import cufflinks as cf

import plotly.express as px
#from plotly.offline import init_notebook_mode

#init_notebook_mode(connected= True)
cf.go_offline()

#---------------------
# >>> Functions
#---------------------

def readingDataFrame(path):
    dataframe = pd.read_csv(path)
    return dataframe

def displayDataFrame(dataframe):
    return print(dataframe)


def displayDataFrameSamples(dataframe, samples):
    return print(dataframe.sample(samples))


def displayDataFrameHead(dataframe, lines= None):
    return print(dataframe.head(lines))

    
def dimensionDataFrame(dataframe):
    dimensionData = dataframe.shape
    return print(f'The requested dataset has {dimensionData[0]} properties and {dimensionData[1]} available attributes.')


def listDataFrameColumns(dataframe):
    print('The dataset columns is: [', end= '')
    dataFrameColumns = list(dataframe.columns)
    for index, columns in enumerate(dataFrameColumns):
        print(f'{columns}', end= '')
        if index == (len(dataFrameColumns) - 1):
            print(end= '.')
            print(']')
        else:
            print(end= ', ')

def dataInfo(dataframe):
    return dataframe.info()

            
def uniqueColumnData(dataframe, column):
    print(f'{column} = {dataframe[column].unique()}')


def dropDataFrame(dataframe, atributos, eixo):
    dataframe = dataframe.drop(atributos, axis = eixo)
    return dataframe


def checkDuplicatesValues(dataframe, column):
    dataframe = dataframe[dataframe[column].duplicated(keep= False)]
    return dataframe


def deletingDuplicatesValues(dataframe, column):
    dataframe = dataframe.drop_duplicates(subset= [column], keep= 'first')
    return dataframe


def resetIndex(dataframe):
    dataframe.reset_index(drop= True, inplace= True)


def intNewColumnOfDate(dataframe, newColumn, formato):
    dataframe[newColumn] = dataframe['date'].dt.strftime(formato)
    dataframe[newColumn] = dataframe[newColumn].astype(int)
    return dataframe


def selectColumnsInDataFrame(dataframe, columns):
    dataframe = dataframe[columns]
    return dataframe


def printCompilanceDateData(dataframe, column):
    print(f'> {column.upper()}')
    print(f'The maximum {column} of property registration is {data[column].max()}')
    print(f'The minimum {column} of property registration is {data[column].min()}')
    return None


def dataFrameTypes(dataframe):
    dataframe = dataframe.dtypes
    return dataframe


def boxplot(dataframe, columns):
    plt.boxplot(dataframe[columns])
    plt.title(columns + ' boxplot')
    plt.show()
    return None


def calculateFences(dataframe, column, sit= None):
    quartile1, quartile3 = np.percentile(dataframe[column], [25, 75])
    interquartile = quartile3 - quartile1
    lowerInnerFence = quartile1 - (interquartile * 1.5) 
    upperInnerFence = quartile3 + (interquartile * 1.5)
    lowerOuterFence = lowerInnerFence - (interquartile * 1.5) 
    upperOuterFence = upperInnerFence + (interquartile * 1.5)
    if lowerInnerFence < 0:
        lowerInnerFence = 0
    if lowerOuterFence < 0:
        lowerOuterFence = 0
    
    print(f'The upper inner fence is {upperInnerFence} and lower inner fence is {lowerInnerFence} of {column} column') 
    print(f'The upper outer fence is {upperOuterFence} and lower outer fence is {lowerOuterFence} of {column} column') 
    
    if sit == 'outer':
        dfOutliers = dataframe.loc[(dataframe[column] > upperOuterFence) | (dataframe[column] < lowerOuterFence)]
        return dfOutliers
    elif sit == 'inner':
        dfOutliers = dataframe.loc[(dataframe[column] > upperInnerFence) | (dataframe[column] < lowerInnerFence)]
        return dfOutliers
    else:
        sit


def copyDataFrame(dataframe):
    dataframe = dataframe.copy()
    return dataframe 
    

def mergeDataFrame(dataframe1, dataframe2, on= None, how= 'inner'):
    dataframe = pd.merge(dataframe1, dataframe2, on= on, how= how)
    return dataframe


def createColunmInDataFrame(dataframe, column, contents):
    dataframe[column] = contents
    return None


def saveDataFrameInCSV(dataframe, path):
    dataframe.to_csv(path, index= False)
    return None


def fillSeasonalityColumn(dataframe):
    dataframe.loc[(dataframe['date'] >= '2014-06-21') & (dataframe['date'] < '2014-09-23'), 'seasonality'] = 'Summer'
    dataframe.loc[(dataframe['date'] >= '2014-09-23') & (dataframe['date'] < '2014-12-22'), 'seasonality'] = 'Fall'
    dataframe.loc[(dataframe['date'] >= '2014-12-22') & (dataframe['date'] < '2015-03-20'), 'seasonality'] = 'Winter'
    dataframe.loc[(dataframe['date'] < '2014-06-21') | (dataframe['date'] >= '2015-03-20'), 'seasonality'] = 'Spring'
    return None
    
    
def renameColumn(dataframe, dictionary):
    dataframe.rename(columns= dictionary, inplace= True)
    return None


def plot_and_show_bar_graph(values, columns_names= None, title= None, ylabel= None):
    groups = columns_names
    values = values
    barlist = plt.bar(groups, values)
    barlist[1].set_color('r')
    plt. title(title)
    plt.ylabel(ylabel)
    plt.show()
    plt.close()
#---------------------
# >>> Extract
#---------------------
#Data Collect
data = readingDataFrame('/home/pietro/Documents/MyProjectsPortfolio/Insight Projects/King Count Houses/Datasets/kc_house_data.csv')

#---------------------
# >>> Transform
#---------------------
#Data Collect
print('Data Collect')
displayDataFrameSamples(data, 5)

#Data Description
print('Data Description')
dimensionDataFrame(data)

listDataFrameColumns(data)

dataInfo(data)

#Data Cleaning and Transformation
print('Data Cleaning and Transformation')
uniqueColumnData(data, 'view')
data['view'] = data['view'].apply(lambda x: 'bad' if x < 2 else 
                                            'regular' if x == 2 else 
                                            'good')
uniqueColumnData(data, 'view')

uniqueColumnData(data, 'grade')
data['grade'] = data['grade'].apply (lambda x:  'high_quality_design' if x >= 11 else 
                                                'avg_quality_design' if (x > 3) & (x <= 10) else
                                                'low_quality_design')   
uniqueColumnData(data, 'grade')

data = dropDataFrame(data, ['sqft_living15', 'sqft_lot15'], 1)
dimensionDataFrame(data)

dataDuplicates = checkDuplicatesValues(data, 'id')
dimensionDataFrame(dataDuplicates)

data = deletingDuplicatesValues(data, 'id')
resetIndex(data)
dimensionDataFrame(data)

data['date'] = pd.to_datetime(data['date'], format= '%Y-%m-%d', errors= 'ignore')
intNewColumnOfDate(data, 'year', '%Y')
intNewColumnOfDate(data, 'month', '%m')
intNewColumnOfDate(data, 'days', '%d')
dimensionDataFrame(data)
listDataFrameColumns(data)
selectedData = selectColumnsInDataFrame(data,['year', 'month', 'days'])
print(selectedData.describe())
printCompilanceDateData(data, 'year')
printCompilanceDateData(data, 'month')
printCompilanceDateData(data, 'days')

uniqueColumnData(data, 'condition')
data['condition'] = data['condition'].apply(lambda x: 'bad' if x <= 2 else 
                                                      'regular' if (x == 3) | (x == 4) else
                                                      'good')
uniqueColumnData(data, 'condition')

uniqueColumnData(data, 'waterfront')
data['waterfront'] = data['waterfront'].apply(lambda x: 'No' if x == 0 else
                                                        'Yes')
uniqueColumnData(data, 'waterfront')
# Exploratory Analysis
print('Exploratory Analysis')
dataInfo(data)

dataNumericTypes = data.select_dtypes(include= 'number')
dataNumericTypes = dataNumericTypes.drop(['year' ,'month', 'days', 'lat', 'long'], axis= 1)
profile = ProfileReport(dataNumericTypes)
profile.to_notebook_iframe()

#Treating Outliers
print('Treating Outliers')
boxplot(data, 'bedrooms')
dfOutliersBedrooms = calculateFences(data, 'bedrooms', 'outer')
displayDataFrameSamples(dfOutliersBedrooms, 5)
dimensionDataFrame(dfOutliersBedrooms)
print(dfOutliersBedrooms[['bedrooms', 'sqft_living']].groupby(['bedrooms']).count())
sqftLivingBedroom33 = data['sqft_living'].loc[data['bedrooms'] == 33].reset_index(drop= True)[0]
percent30 = sqftLivingBedroom33 * 0.3
dfSqftBed33Percent30 = data[['bedrooms', 'sqft_living']].loc[(data['sqft_living'] <= sqftLivingBedroom33 + percent30) & (data['sqft_living'] >= sqftLivingBedroom33 - percent30)]
print(dfSqftBed33Percent30.mean())
print(dfSqftBed33Percent30.median())
medianBedrooms = dfSqftBed33Percent30['bedrooms'].median()
medianBedrooms
data.loc[data['bedrooms'] == 33, 'bedrooms'] = medianBedrooms
boxplot(data, 'bedrooms')

boxplot(data, 'sqft_lot')
calculateFences(data, 'sqft_lot')
dfOutliersSqftLot = data.loc[data['sqft_lot'] > 1000000].sort_values(['sqft_lot'], ascending= True)
print(dfOutliersSqftLot)
dimensionDataFrame(dfOutliersSqftLot)
meanPrice = dfOutliersSqftLot['price'].mean()
print(f'The mean price the outliers the sqft_lot columns is {meanPrice}')
percent10 = meanPrice * 0.1
dfPricePercent10 = data[['price', 'sqft_lot']].loc[(data['price'] > meanPrice - percent10) & (data['price'] < meanPrice + percent10)]
displayDataFrameSamples(dfPricePercent10, 10)
meanDf = round(dfPricePercent10.mean(), 2)
print(meanDf)
data.loc[data['sqft_lot']> 1000000, 'sqft_lot'] = meanDf['sqft_lot']
boxplot(data, 'sqft_lot')

resetIndex(data)

displayDataFrameHead(data)
dimensionDataFrame(data)

saveDataFrameInCSV(data, '/home/pietro/Documents/MyProjectsPortfolio/Insight Projects/King Count Houses/Datasets/kc_house_data_updated.csv')
#Solving Business Problems
#1
print('First Business Problem')
dataRaw = copyDataFrame(data)
dfGroupZipcodeMedianPrice = dataRaw[['price', 'zipcode']].groupby(['zipcode']).median().reset_index()
renameColumn(dfGroupZipcodeMedianPrice,{'price':'average_price_per_zipcode'})
displayDataFrameHead(dfGroupZipcodeMedianPrice)
dataRaw = mergeDataFrame(dataRaw, dfGroupZipcodeMedianPrice, on= 'zipcode') 
displayDataFrameSamples(dataRaw, 10)
renameColumn(dataRaw, {'price': 'buy_price'})
dataRaw = selectColumnsInDataFrame(dataRaw, ['id','date', 'zipcode', 'condition', 'view', 'waterfront', 'buy_price', 'average_price_per_zipcode'])
dataBuy = dataRaw.loc[(dataRaw['buy_price'] < dataRaw['average_price_per_zipcode']) & 
                      (dataRaw['condition'] != 'bad') & 
                      (dataRaw['view'] != 'bad') & 
                      (dataRaw['waterfront'] == 'Yes')]
print(dataBuy)
resetIndex(dataBuy)
saveDataFrameInCSV(dataBuy, '/home/pietro/Documents/MyProjectsPortfolio/Insight Projects/King Count Houses/Datasets/properties_to_be_purchased.csv')

#2
print('Second Businesse Problem')
dataRaw2 = copyDataFrame(data)
createColunmInDataFrame(dataRaw2, 'seasonality', 'NaN')
fillSeasonalityColumn(dataRaw2)
dfMedianZipcodeSeason = dataRaw2[['price', 'zipcode', 'seasonality']].groupby(['zipcode', 'seasonality']).median().reset_index()
dfMedianZipcodeSeason.set_index('zipcode', inplace= True)
displayDataFrame(dfMedianZipcodeSeason)
dataRaw2 = selectColumnsInDataFrame(dataRaw2, ['id', 'seasonality'])
dataSale = pd.merge(dataRaw2, dataBuy, on= 'id', how= 'right')
displayDataFrame(dataSale)
createColunmInDataFrame(dataSale, 'sale_price', 'NaN')
createColunmInDataFrame(dataSale, 'average_price_per_zip_and_season', 'NaN')
zipcodes = list(dataSale['zipcode'].unique())
for i in range(len(zipcodes)):
    priceAndSeason = dataSale[['zipcode', 'buy_price', 'seasonality']].loc[dataSale['zipcode'] == zipcodes[i]]
                                                       
    for row in range(len(priceAndSeason)):
        idx = priceAndSeason.index[row]
        seasonality = priceAndSeason['seasonality'].iloc[row]
                                                        
        dfLoc = dfMedianZipcodeSeason.loc[(dfMedianZipcodeSeason.index == zipcodes[i]) &
                        (dfMedianZipcodeSeason['seasonality'] == seasonality)]
                                                        
        if priceAndSeason['buy_price'].iloc[row] > dfLoc['price'].iloc[0]:
            dataSale['sale_price'].iloc[idx] = dataSale['buy_price'].iloc[idx] * 1.1
            dataSale['average_price_per_zip_and_season'].iloc[idx] = dfLoc['price'].iloc[0]
        else:
            dataSale['sale_price'].iloc[idx] = dataSale['buy_price'].iloc[idx] * 1.3
            dataSale['average_price_per_zip_and_season'].iloc[idx] = dfLoc['price'].iloc[0]
print(dataSale)
dataSale = selectColumnsInDataFrame(dataSale, ['id', 'date', 'zipcode','condition', 
                                               'view', 'waterfront','buy_price', 'seasonality', 
                                               'average_price_per_zip_and_season', 'sale_price'])                                    
createColunmInDataFrame(dataSale, 'gain', 'NaN')
for i in range(len(dataSale)):
    dataSale.loc[i, 'gain'] = (dataSale.loc[i, 'sale_price'] - dataSale.loc[i, 'buy_price'])
print(dataSale)
saveDataFrameInCSV(dataSale, '/home/pietro/Documents/MyProjectsPortfolio/Insight Projects/King Count Houses/Datasets/gain_from_sale_of_properties.csv')

#Hypothesis Validation
viewWater = round(data['price'].loc[(data['waterfront'] == 'Yes')].mean(), 2)
notViewWater = round(data['price'].loc[data['waterfront'] == 'No'].mean(), 2)
rate = round((viewWater - notViewWater ) / notViewWater * 100, 2)
plot_and_show_bar_graph(values= [notViewWater, viewWater], 
                        columns_names= ['Not View Water', 'View Water'], 
                        title= 'Mean Price to Properties with View x Not View to Water', 
                        ylabel= 'price')
print(f'The average price of properties with water views is US${viewWater}')
print(f'The average price for properties that do not have water views is US${notViewWater}')
print(f'Properties that have a view of the water are {rate}% more expensive, on average, than those that don´t view to water')


notGoodViewWater = round(data['price'].loc[(data['waterfront'] == 'Yes') & (data['view'] == 'bad')].mean(), 2)
goodViewWater = round(data['price'].loc[(data['waterfront'] == 'Yes') & (data['view'] != 'bad')].mean(), 2)
rate1 = round((goodViewWater - notGoodViewWater ) / notGoodViewWater * 100, 2)
plot_and_show_bar_graph(values= [notGoodViewWater, goodViewWater], 
                        columns_names= ['Not Good View Water', 'Good View Water'], 
                        title= 'Mean Price to Properties with Good View x Not Good View to Water', 
                        ylabel= 'price')
print(f'The average price of properties that do not have good water views is US${notGoodViewWater}')
print(f'The average price for properties with good water views is US${goodViewWater}')
print(f'Properties that have a good view of the water are {rate1}% more expensive, on average, than those that don´t good view to water')


after1995 = round(data['price'].loc[data['yr_built'] >= 1955].mean(), 2)
prior1955 = round(data['price'].loc[data['yr_built'] < 1955].mean(), 2)
rate2 = abs(round((prior1955 - after1995) / after1995 * 100, 2))
plot_and_show_bar_graph(values= [after1995, prior1955], 
                        columns_names= ['After to 1955', 'Prior to 1955'], 
                        title= 'Average Price to Properties with Construction Date After x Prior to 1955', 
                        ylabel= 'price')
print(f'The average price for properties with years of construction after 1955 is US${after1995}')
print(f'The average price for properties with years of contruction prior to 1955 is US${prior1955}')
print(f'Properties with years of construction prior to 1955 are {rate2}% cheaper than the total average.')

withBasement = round(data['sqft_lot'].loc[data['sqft_basement'] > 0].mean(), 2)
noBasement = round(data['sqft_lot'].loc[data['sqft_basement'] == 0].mean(), 2)
rate3 = round((noBasement - withBasement) / withBasement * 100, 2)
plot_and_show_bar_graph(values= [withBasement, noBasement], 
                        columns_names= ['With Basement', 'Without a Basement'], 
                        title= 'Average Land Area to Properties With Basement x Without Basement', 
                        ylabel= 'sqft_lot')
print(f'The land area for property that has a basement is {withBasement}ft²')
print(f'The land area for property that does not have a basement is {noBasement}ft²')
print(f'Properties without a basement have a land area {rate3}% larger than those with a basement.')

year2014 = round(data['price'].loc[data['year'] == 2014].mean(), 2)
year2015 = round(data['price'].loc[data['year'] == 2015].mean(), 2)
growthYear = round((year2015 - year2014) / year2014 * 100, 2)
plot_and_show_bar_graph(values= [year2014, year2015], 
                        columns_names= ['2014', '2015'], 
                        title= 'Average Price to Properties the 2014 x 2015', 
                        ylabel= 'price')
print(f'The mean price the properties in year 2014 is: R${year2014}')
print(f'The mean price the properties in year 2015 is: R${year2015}')
print(f'There was a growth in property prices of {growthYear}% from 2014 to 2015.')

property3Bathrooms = data[['price','date','month', 'year']].loc[data['bathrooms'] == 3]
property3Bathrooms = property3Bathrooms.sort_values(['date']).reset_index(drop= True)
priceMinMonth = property3Bathrooms['price'].loc[(data['month'] == 5) & (data['year'] == 2014)].mean()
priceMaxMonth = property3Bathrooms['price'].loc[(data['month'] == 5) & (data['year'] == 2015)].mean()
growth_rate = (((priceMaxMonth / priceMinMonth) ** (1/12)) - 1) * 100
dataH5 = data.copy()
dataH5['year and month'] = pd.to_datetime(dataH5['date']).dt.strftime('%Y-%m')
groupYearAndMonth = dataH5[['price', 'year and month']].loc[dataH5['bathrooms'] == 3].groupby('year and month').mean().reset_index()
plt.plot(groupYearAndMonth['year and month'], groupYearAndMonth['price'])
plt.title('Average month-to-month growth in property prices with 3 bathrooms')
plt.xticks(rotation= 45)
plt.show()
plt.close()
print(f'There was a {abs(round(growth_rate, 2))}% monthly decrease in the average price for properties with 3 bathrooms (from 2014-05 to 2015-05)')

dataMean = round(data['price'].mean(), 2)
dfRenovated = round(data['price'].loc[data['yr_renovated'] > 0].mean(), 2)
rate4 = round((dfRenovated - dataMean) / dataMean * 100, 2)
plot_and_show_bar_graph(values= [dataMean, dfRenovated], 
                        columns_names= ['All Properties', 'Renovated Properties'], 
                        title= 'Average Price to All Properties x Renovated Properties', 
                        ylabel= 'price')
print(f'The average dataset price is US${dataMean}')
print(f'The average price of renovates property is US${dfRenovated}')
print(f'Renovated properties are {rate4}% more expensive compared to the total average.')

dataMean = round(data['price'].mean(), 2)
more3Bedrooms = round(data['price'].loc[data['bedrooms'] > 3].mean(), 2)
rate5 = round((more3Bedrooms - dataMean) / dataMean * 100, 2)
plot_and_show_bar_graph(values= [dataMean, more3Bedrooms], 
                        columns_names= ['All Properties', 'Properties With More 3 Bedrooms'], 
                        title = 'Average Price to All Properties x Properties With More 3 Bedrooms', 
                        ylabel= 'price')
print(f'The average dataset price is US${dataMean}')
print(f'The average price for properties with more than 3 bedrooms is US${more3Bedrooms}')
print(f'Properties with more than 3 bedrooms are {rate5}% more expensive compared to the total average.')

dataMean = round(data['price'].mean(), 2)
goodCondition = round(data['price'].loc[data['condition'] == 'good'].mean(), 2)
rate6 = round(((goodCondition - dataMean) / dataMean * 100), 2)
plot_and_show_bar_graph(values= [dataMean, goodCondition], 
                        columns_names= ['All Properties', 'Renovated Properties'], 
                        title= 'Average Price to All Properties x Properties With Good Condition', 
                        ylabel= 'price')
print(f'The total price of dataset is US${dataMean}')
print(f'The total price for properties with good condition is US${goodCondition}')
print(f'Properties in good condition correspond to {rate6}% of the total property price')

lessTwoFloors = round(data['price'].loc[data['floors'] < 2].mean(), 2)
twoFloorsOrMore = round(data['price'].loc[data['floors'] >= 2].mean(), 2)
rate7 = round((twoFloorsOrMore - lessTwoFloors) / lessTwoFloors * 100, 2)
plot_and_show_bar_graph(values= [lessTwoFloors, twoFloorsOrMore], 
                        columns_names= ['Properties with less than 2 floors', 'Properties with 2 or more floors'], 
                        title= 'Average Price to Properties With Less Than 2 Floors x Properties With 2 Floors', 
                        ylabel= 'price')
print(f'The mean price the properties with less than 2 floors is US${lessTwoFloors}')
print(f'The mean price the properties with 2 floors or more is US${twoFloorsOrMore}')
print(f'Properties with 2 or more floors are {rate7}% most expensive tha properties with less than 2 floors')