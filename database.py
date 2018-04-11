from pyDatalog import pyDatalog

pyDatalog.create_terms('X,Y,Z')
pyDatalog.create_terms('meal,drink')  # istnieje
pyDatalog.create_terms('sweet,hot')  # smak
pyDatalog.create_terms('breakfast,dinner,dessert,appetizer')  # rodzaj
pyDatalog.create_terms('portion')  # wielkosc
pyDatalog.create_terms('price') # cena

meal['lody']=1
sweet['lody']=1
portion['lody']=0.3
price['lody']=5


meal['ciasto']=1
sweet['ciasto']=0.6
portion['ciasto']=0.3
price['ciasto']=9


meal['pizza']=1
hot['pizza']=1
portion['pizza']=1
price['pizza']=35

meal['schab']=1
portion['schab']=1
price['schab']=20

meal['jajecznica']=1
portion['jajecznica']=0.7
price['jajecznica']=12

meal['koreczki']=1
portion['koreczki']=0.2
price['koreczki']=5

drink['herbata']=1
price['herbata']=3

dessert(X) <= (meal[X]==1) & (sweet[X]>0.5) & (portion[X]==0.3)
dinner(X) <= (meal[X]==1) & (portion[X]>0.7)
appetizer(X) <= (meal[X]==1) & (portion[X]<0.3)
breakfast(X) <= (meal[X]==1) & (portion[X]<=    0.7) & (portion[X]>0.3)

print(dessert(X))
print(dinner(X))
print(appetizer(X))
print(breakfast(X))
print(price[X]==Y)
