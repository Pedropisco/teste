
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import math


def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d









listings = pd.read_csv("Blistings.csv")
reviews = pd.read_csv("Breviews.csv")
calendar = pd.read_csv("Bcalendar.csv")
Slistings = pd.read_csv("Slistings.csv")
Sreviews = pd.read_csv("Sreviews.csv")
Scalendar = pd.read_csv("Scalendar.csv")

pd.set_option("display.max.columns", None)


#print(Blistings.shape[0])
#- base tem 95 colunas e 3585 linhas.

#print(Breviews.comments[0])
#display(Blistings.head())


#juntar dados de Boston com Seattle

listings = pd.concat([listings, Slistings])
listings = pd.DataFrame(listings)

#reviews = reviews.join(Sreviews)
#calendar = calendar.join(Scalendar)



'''Construir um modelo base para conseguir prever o preço esperado por um imóvel
dados as características fornecidas.'''
'''

listings = listings[['price','host_verifications', 'host_has_profile_pic', 'host_identity_verified',
              'is_location_exact','host_is_superhost', 'property_type','room_type','bathrooms',
              'bedrooms','beds','bed_type','amenities','cleaning_fee','minimum_nights',
              'cancellation_policy','market']]
'''


listings = listings[['price','host_is_superhost', 'room_type','beds','bathrooms', 'cleaning_fee',
             'review_scores_rating','number_of_reviews', "market",'cancellation_policy',
             'guests_included', 'extra_people',
             'minimum_nights','latitude','longitude']]


'''
LISTINGS = Blistings[[
              'property_type','room_type','bathrooms',
              'bedrooms','beds','amenities','cleaning_fee',
              'cancellation_policy']]
'''

'''
listings = listings[["price","host_response_time", "host_response_rate","host_is_superhost",
              'host_acceptance_rate', 'host_verifications', 'host_has_profile_pic',
              'host_identity_verified','is_location_exact','property_type',
              'room_type','bathrooms','bedrooms','beds','bed_type','amenities',
              'guests_included','extra_people','cleaning_fee','minimum_nights',
              'availability_90','number_of_reviews','review_scores_rating',
              'review_scores_accuracy','review_scores_cleanliness',
              'review_scores_checkin','review_scores_communication',
              'review_scores_location','review_scores_value',
              'cancellation_policy','market']]
'neighbourhood_cleansed'

'''
listings["distance"] = ""
listings = listings[listings['market'].isin(['Boston','Seattle'])]
listings = listings.dropna(axis = 0)
listings = listings[listings.room_type=="Entire home/apt"]

latB = 42.36
logB = -71.05
latS = 47.622451 
logS = -122.352033

for i in range(0, listings.shape[0]):
    if listings["market"].values[i] == "Boston":
        listings["distance"].values[i] = distance((listings['latitude'].values[i], listings['longitude'].values[i]),
                                 (latB, logB))
    elif listings["market"].values[i] == "Seattle":
        listings["distance"].values[i] = distance((listings['latitude'].values[i], listings['longitude'].values[i]),
                                 (latS, logS))


listings.distance = listings.distance.astype('float64')
listings = listings.drop(['latitude', 'longitude'], axis = 1)


for i in listings.select_dtypes('object').columns:
    listings[i] = listings[i].str.replace('\{|\}|\$|\%|\"|\[|\]' ,'')
    listings[i]= listings[i].str.replace("'" ,"")
    listings[i]= listings[i].str.replace('f', '0')
    listings[i]= listings[i].str.replace('t', '1')
    

listings.cleaning_fee = listings.cleaning_fee.astype('float64')
listings.host_is_superhost = listings.host_is_superhost.astype('float64')
#listings.host_has_profile_pic = listings.host_has_profile_pic.astype('float64')
#listingshost_identity_verified = listings.cleaning_fee.astype('float64')
#listings.is_location_exact = listings.is_location_exact.astype('float64')
#listings.host_response_rate = listings.host_response_rate.astype('float64')
#listings.host_acceptance_rate = listings.host_acceptance_rate.astype('float64')
listings.extra_people = listings.extra_people.astype('float64')
listings['price'] = listings['price'].str.replace(',','')
listings.price = listings.price.astype('float64')



for i in  listings.select_dtypes('object').columns:
    try:
        #primeiro retira qualquer símbolo que possa causar duplicação ou outro problema
        listings = pd.concat([listings.drop([i], axis =1),
               listings[i].str.get_dummies(',')], axis = 1)
        #agora cria dummy para as categorias, cria uma dummy para valores NA
    except:
        print("não retirou símbolos")

y = listings['price']

listings = listings.drop(['Sea11le'], axis = 1)

#y = y.str.replace('\$|\,','')
#y = pd.to_numeric(y)




corrMatrilistings = listings.corr() 
sn.heatmap (corrMatrilistings, annot = True)
plt.show()



listings = listings.drop(['price'], axis = 1)
X = listings


#modificar cleaning_fee para numérico

#LISTINGS.host_response_rate = LISTINGS.host_response_rate.astype('float64')/100

#cat_df = LISTINGS.select_dtypes(include=["object"])


#criação de dummies para variáveis     
#amenities = LISTINGS['amenities'].str.get_dummies(',')
#host_verifications = LISTINGS['host_verifications'].str.get_dummies(',')
#host_response_time = LISTINGS['host_response_time'].str.get_dummies()

#concatenação de dummies criadas com a base original.
#LISTINGS = pd.concat([LISTINGS.drop(['amenities','host_verifications'], alistingsis=1),
 #              amenities, host_verifications], alistingsis = 1)












































