import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import math
import numpy as np
from matplotlib.ticker import StrMethodFormatter

from io import StringIO
import mlxtend
from mlxtend.plotting import category_scatter
#função para definição de distância física
#ACHAR QUEM FEZ ESSA FUNÇÃO
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
#reviews = pd.read_csv("Breviews.csv")
#calendar = pd.read_csv("Bcalendar.csv")
Slistings = pd.read_csv("Slistings.csv")
#Sreviews = pd.read_csv("Sreviews.csv")
#Scalendar = pd.read_csv("Scalendar.csv")

pd.set_option("display.max.columns", None)


#juntar dados de Boston com Seattle
listings = listings[listings.city == 'Boston']
Slistings = Slistings[Slistings.city == 'Seattle']
listings = pd.concat([listings, Slistings])
listings = pd.DataFrame(listings).reset_index()
#print(listings.shape[1]) #7403 linhas, 95 colunas


'''#########################################################################
Escolher as variáveis para o modelo final de previsão de preços.'''
'''

listings = listings[['price','host_verifications', 'host_has_profile_pic', 'host_identity_verified',
              'is_location_exact','host_is_superhost', 'property_type','room_type','bathrooms',
              'bedrooms','beds','bed_type','amenities','cleaning_fee','minimum_nights',
              'cancellation_policy','market']]
'''


listings = listings[['id','price','host_is_superhost', 'room_type','property_type',
                     'beds','bathrooms', 'cleaning_fee','neighbourhood_cleansed',
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

'''###########################################################################
Criação da variável de distância para o centro da cidade'''
listings["distance"] = ""
listings = listings[listings['market'].isin(['Boston','Seattle'])]
listings = listings.dropna(axis = 0)
#listings = listings[listings.room_type=="Entire home/apt"]

latB = 42.36
logB = -71.05
latS = 47.622451 
logS = -122.352033

for i in range(0, listings.shape[0]):
    if listings["market"].values[i] == "Boston":
        listings["distance"].values[i] = distance((listings['latitude'].values[i],
                                                   listings['longitude'].values[i]),
                                 (latB, logB))
    elif listings["market"].values[i] == "Seattle":
        listings["distance"].values[i] = distance((listings['latitude'].values[i],
                                                   listings['longitude'].values[i]),
                                 (latS, logS))


listings.distance = listings.distance.astype('float64')
listings = listings.drop(['latitude', 'longitude'], axis = 1)


''' ##########################################################################
Retirada de sinais para as colunas de type object.'''
for i in listings.select_dtypes('object').columns:
    listings[i] = listings[i].str.replace('\{|\}|\$|\%|\"|\[|\]' ,'')
    listings[i]= listings[i].str.replace("'" ,"")
    listings[i]= listings[i].str.replace('f', '0')
    listings[i]= listings[i].str.replace('t', '1')
    

''' ##########################################################################
Definição de type para variáveis numéricas'''
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


'''###########################################################################
Criação de dummies para variáveis categóricas'''
for i in  listings.select_dtypes('object').columns:
    try:
        #primeiro retira qualquer símbolo que possa causar duplicação ou outro problema
        listings = pd.concat([listings.drop([i], axis =1),
               listings[i].str.get_dummies(',')], axis = 1)
        #agora cria dummy para as categorias, cria uma dummy para valores NA
    except:
        print("não retirou símbolos")



y = listings['price']

#listings = listings.drop(['Sea11le'], axis = 1)

#y = y.str.replace('\$|\,','')
#y = pd.to_numeric(y)




X = listings.drop(['price'], axis = 1)


### GRÁFICOS DE ANÁLISE DESCRITIVA



# Heat Map
corrMatrilistings = listings.corr() 
sn.heatmap (corrMatrilistings, annot = True)
plt.show()


## Preços e review scores
plt.bar(listings.review_scores_rating, listings.price)
#parece haver alguma relação entre o score e o preço dos imóveis.

# Gráfico de preços por cidade

listings.hist(column = 'price', bins = 40, grid = True, by = 'Sea11le')

listings.boxplot(column = ['price'], by='Sea11le')
listings.boxplot(column = ['price'], by= 'host_is_superhost',
                 showmeans = True)
listings.boxplot(column = ['price'], by ='bathrooms',
                 showmeans = True)
listings.boxplot(column = ['price'], by ='beds',
                 showmeans = True)
listings[listings.market == 'Sea11le'].bar(column = ['price'],
                                 by = 'neighbourhood_cleansed')

plt.scatter(listings.beds, listings.price)
np.corrcoef(listings.bathrooms, listings.price)

# Histograma de preços
a = listings.hist(column = 'price', bins = 20, grid = False, by = "host_is_superhost")
for i,x in enumerate(a):
    
    x.spines['right'].set_visible(False)
    x.spines['top'].set_visible(False)
    x.spines['left'].set_visible(False)
    # Switch off ticks
    x.tick_params(axis="both", which="both", bottom="off", top="off", 
                  labelbottom="on", left="off", right="off", labelleft="on")
     # Draw horizontal axis lines
    vals = x.get_yticks()
    for tick in vals:
        x.axhline(y=tick, linestyle='dashed', alpha=0.4, color='#eeeeee', zorder=1)

    # Set x-axis label
    x.set_xlabel("Session Duration (Seconds)", labelpad=20, weight='bold', size=12)

    # Set y-axis label
    if i == 1:
        x.set_ylabel("Sessions", labelpad=50, weight='bold', size=12)

    # Format y-axis label
    x.yaxis.set_major_formatter(StrMethodFormatter('{x:,g}'))

    x.tick_params(axis='x', rotation=0)
''' Dá pra notar que existe uma cauda mais pesada para superhosts, ou seja
 uma distribuição de preços mais alta para quem é superhost.
 isso não nos indica mais nada, somente que superhosts tendem a ter um valor
 melhor pelos seus imóveis.
'''

    

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












































