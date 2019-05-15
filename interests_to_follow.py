import pandas as pd

interests = pd.read_csv('interests.csv', names = ['User ID', 'Interest'], header = 0)

temp_i = []
for i in range(len(interests)):
    temp_i.append(1)        

interests['Temp'] = temp_i
rating_count_i = interests.groupby(by = ['Interest'])['Temp'].count().reset_index()
rating_count_i = rating_count_i.sort_values('Temp', ascending = False).reset_index(drop = True)
rating_count_i = rating_count_i.rename(index=str, columns={"Temp": "Number of Followers"})

interest_input = raw_input('Enter an Interest to follow: ')
interest_input = interest_input.capitalize()

if interest_input in rating_count_i['Interest'].tolist():
    
    df = interests.pivot_table(index='User ID', columns='Interest', values='Temp').fillna(0)
    rating = df[interest_input]
    interest_like_input = df.corrwith(rating)
    corr_review_i = pd.DataFrame(interest_like_input, columns=['Correlation'])  
    corr_review_i.dropna(inplace=True)
    corr_review_i = corr_review_i.sort_values('Correlation', ascending = False).drop([interest_input])
    corr_review_i = corr_review_i.merge(rating_count_i, left_on = 'Interest', right_on = 'Interest', how = 'inner')

    print '\n\n'
    print 'If a user is following the interest "' + interest_input +'" then he might follow the following interests as well:'
    print '\n'
    print(corr_review_i.head())
    
else:
    print '\n'
    print 'Sorry! No Such Interest Exists.'