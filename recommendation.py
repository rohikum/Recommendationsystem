import pandas as pd

follows = pd.read_csv('follows.csv', names = ['Follower ID', 'Followee ID'], header = 0)

temp_f = []
for i in range(len(follows)):
    temp_f.append(1)        

follows['Temp'] = temp_f
rating_count_f = follows.groupby(by = ['Followee ID'])['Temp'].count().reset_index()
rating_count_f = rating_count_f.sort_values('Temp', ascending = False).reset_index(drop = True)
rating_count_f = rating_count_f.rename(index=str, columns={"Temp": "Number of Followers"})

id_input = int(input('Enter a User ID to follow: '))

if id_input in rating_count_f['Followee ID'].tolist():
    
    df = follows.pivot_table(index='Follower ID', columns='Followee ID', values='Temp').fillna(0)
    rating = df[id_input]
    people_like_input = df.corrwith(rating)
    corr_review_f = pd.DataFrame(people_like_input, columns=['Correlation'])  
    corr_review_f.dropna(inplace=True)  
    corr_review_f = corr_review_f.sort_values('Correlation', ascending = False).drop([id_input])
    corr_review_f = corr_review_f.merge(rating_count_f, left_on = 'Followee ID', right_on = 'Followee ID', how = 'inner')
    corr_review_f = corr_review_f[corr_review_f.Correlation >= 0.5]

    print '\n\n'
    print 'If a user is following ID ' + str(id_input) +' then he might follow the following people as well:'
    print '\n'
    print(corr_review_f.head())
    
else:
    print '\n'
    print 'Sorry! No Such Person Exists.'

