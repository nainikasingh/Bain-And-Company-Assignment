#!/usr/bin/env python3
# -*- coding: utf-8 -*-

train=pd.read_csv("train.csv")
test=pd.read_csv("test.csv")
test['casual']=0
test['registered']=0
test['count']=0
#remove Outlier piont
train = train[np.abs(train["count"]-train["count"].mean())<=(3*train["count"].std())] 


union_data=pd.concat([train,test],ignore_index=True)


union_data['day']=pd.to_datetime(union_data.datetime).dt.day
union_data['year']=pd.to_datetime(union_data.datetime).dt.year
union_data['month']=pd.to_datetime(union_data.datetime).dt.month
union_data['weekday']=pd.to_datetime(union_data.datetime).dt.weekday
union_data['date']=pd.to_datetime(union_data.datetime).dt.date
union_data['hour']=pd.to_datetime(union_data.datetime).dt.hour
union_data['year_season']=union_data.apply(lambda x:'{}_{}'.format(str(x['year']),str(x['season'])),axis=1)
union_data['year_month']=union_data.apply(lambda x:'{}_{}'.format(str(x['year']),str(x['month'])),axis=1)
#missing data fill
union_data['windspeed']=union_data[['year','month','hour','windspeed']].groupby(['year','month','hour']).transform(lambda x:x.replace(0,np.median([i for i in x if i>0])))
union_data['windspeed']=pd.cut(union_data['windspeed'],bins=[0,20,60],labels=['0','1'])


union_data['day_type']=0
union_data['day_type'][(union_data['holiday']==0)& (union_data['workingday']==0)]='weekend'
union_data['day_type'][(union_data['holiday']==0)& (union_data['workingday']==1)]='workingday'
union_data['day_type'][(union_data['holiday']==1)]='holiday'


train=union_data[:10739]


plt.figure(figsize=(100,5))
g=sns.factorplot(x='windspeed',y='count',data=train,col='year',kind='bar',estimator=sum,ci=None,size=10,aspect=1)


g=sns.factorplot(x='season',y='count',data=train,col='year',kind='bar',estimator=sum,ci=None,size=10,aspect=1)


g=sns.factorplot(x='month',y='count',data=train,col='year',kind='bar',estimator=sum,ci=None,size=10,aspect=1)


g=sns.factorplot(x='day',y='count',data=train,col='year',kind='bar',estimator=sum,ci=None,size=10,aspect=1)

#weekday trend
g=sns.factorplot(x='weekday',y='count',data=train,col='year',kind='bar',estimator=sum,ci=None,size=10,aspect=1)


#hour trend
g=sns.factorplot(x='hour',y='count',data=train,col='year',kind='bar',estimator=sum,ci=None,size=10,aspect=1)

#weather analyse
g=sns.factorplot(x='weather',y='count',data=train,col='year',kind='bar',estimator=sum,ci=None,size=10,aspect=1)

#workingday analyse
g=sns.factorplot(x='workingday',y='count',data=train,col='year',kind='bar',estimator=sum,ci=None,size=10,aspect=1)


#temparature analyse
g=sns.factorplot(x='temp',y='count',data=train,col='year',kind='bar',estimator=sum,ci=None,size=10,aspect=1)

from sklearn import tree
clf = tree.tree.DecisionTreeRegressor(max_depth=4,criterion='mse',min_samples_leaf=800)
clf = clf.fit(train['hour'].reshape(-1,1),np.ravel(train['count']))
import graphviz 
dot_data = tree.export_graphviz(clf, out_file=None,feature_names=['hour'],  
                                filled=True, rounded=True,  
                                special_characters=True,) 
graph = graphviz.Source(dot_data) 
graph


from sklearn.ensemble import RandomForestRegressor
from sklearn.grid_search import GridSearchCV
from sklearn import cross_validation, metrics
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import GradientBoostingRegressor
#X=train[['season', 'holiday', 'workingday', 'weather',
#      'atemp', 'humidity', 'windspeed','day', 'year', 'month', 'weekday','year_season']]

train_y=np.log1p(train[['count']]+1)
undumm=union_data[['datetime','year_month','atemp','temp', 'humidity','windspeed']]
get_dumm=union_data[['weather','workingday','hour','day_type','weekday']]
#enc = OneHotEncoder()
#enc.fit(train[['season', 'holiday', 'workingday', 'weather','day', 'year', 'month', 'weekday']])
#enc.transform(train[['season', 'holiday', 'workingday', 'weather','day', 'year', 'month', 'weekday']]).toarray().shape
dumm=pd.get_dummies(get_dumm,columns=get_dumm.columns)
train_X=pd.concat([undumm[:10739],dumm[:10739]],axis=1)
test_X=pd.concat([undumm[10739:],dumm[10739:]],axis=1)


train_X.columns

regr = RandomForestRegressor(n_estimators=300)
regr.fit(train_X.loc[:,'year_month':], np.ravel(train_y))
reg=GradientBoostingRegressor(n_estimators=2000, learning_rate=0.01,max_depth=4)
reg.fit(train_X.loc[:,'year_month':], np.ravel(train_y))


plt.figure(figsize=(100,5))
sns.barplot(x=train_X.loc[:,'year_month':].columns,y=regr.feature_importances_)


plt.figure(figsize=(100,5))
sns.barplot(x=train_X.loc[:,'year_month':].columns,y=reg.feature_importances_)

np.exp(regr.predict(test_X.loc[:,'year_month':]))-1

np.exp(reg.predict(test_X.loc[:,'year_month':]))-1


union_data['count'][10739:]=np.exp(reg.predict(test_X.loc[:,'year_month':]))-1

union_data[['datetime','count']].to_csv('bike_predictions.csv', index=False)









