# -*- coding: utf-8 -*-
"""Tugpro2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qk2uDw_F4o4BszfPSFltdulHY1ZxTmL6

Kelompok:
  - Mohammad Akbar Fauzy Ali
  - Ario Bagus Bramantyo
  - Kevin Daniel Hamonangan Ompusunggu


Input:

	- Services = HIGH, AVERAGE, LOW	  	 [0,100]
	- Foods = HIGH, AVERAGE, LOW	    	  [0,10]
Ouput:

	- Score = Recommended, Considered, Not Recommended

Rules:

  - if service = 'High' and Food = 'High' then score = "Recomended"
  - if service = 'High' and Food = 'Average' then score = "Recomended"
  - if service = 'High' and Food = 'Low' then score = "Considered"
  - if service = 'Average' and Food = 'High' then score = "Recomended"
  - if service = 'Average' and Food = 'Average' then score = "Considered"
  - if service = 'Average' and Food = 'Low' then score = "Not Recommended"
  - if service = 'Low' and Food = 'High' then score = "Considered"
  - if service = 'Low' and Food = 'Average' then score = "Not Recomended"
  - if service = 'Low' and Food = 'Low' then score = "Not Recommended"
"""

import pandas

TUPLE_HIGHQUALITYSERVICE = [70, 85]   # [BATAS_BAWAH, BATAS_ATAS]
TUPLE_AVERAGEQUALITYSERVICE = [65]    # [BATAS TENGAH]
TUPLE_LOWQUALITYSERVICE = [35, 50]    # [BATAS_BAWAH, BATAS_ATAS]

TUPLE_HIGHQUALITYFOOD = [8,9]         # [BATAS_BAWAH, BATAS_ATAS]
TUPLE_AVERAGEQUALITYFOOD = [7]        # [BATAS TENGAH]
TUPLE_LOWQUALITYFOOD = [3,5]          # [BATAS_BAWAH, BATAS_ATAS]

class FuzzyRestaurant:
  #constructor
  def __init__(self, _restaurant, _service, _food): #_restaurant = ID, _service = nilai qualitas pelayanan, _food = nilai qualitas makanan 
    self.restaurant = _restaurant
    self.service = _service
    self.food = _food

    #Fuzzyfication Services
    self.highQualityService = self.LinearHigh(_service, TUPLE_HIGHQUALITYSERVICE[0], TUPLE_HIGHQUALITYSERVICE[1])
    self.averageQualityService = self.Triangles(_service, TUPLE_LOWQUALITYSERVICE[0], TUPLE_AVERAGEQUALITYSERVICE[0], TUPLE_HIGHQUALITYSERVICE[1])
    self.lowQualityService = self.LinearLow(_service, TUPLE_LOWQUALITYSERVICE[0], TUPLE_LOWQUALITYSERVICE[1])
    
    #Fuzzyfication Foods
    self.highQualityFood = self.LinearHigh(_food, TUPLE_HIGHQUALITYFOOD[0], TUPLE_HIGHQUALITYFOOD[1])
    self.averageQualityFood = self.Triangles(_food, TUPLE_LOWQUALITYFOOD[0], TUPLE_AVERAGEQUALITYFOOD[0], TUPLE_HIGHQUALITYFOOD[1])
    self.lowQualityFood = self.LinearLow(_food, TUPLE_LOWQUALITYFOOD[0], TUPLE_LOWQUALITYFOOD[1])

    #Inference
    self.recommended = self.RecommendedRules();
    self.considered = self.ConsideredRules();
    self.notRecommended = self.NotRecommendedRules();

    #Deffuzzification
    self.score = self.Deffuzzication()

  # Membership Function
  def Triangles(self,x,a,b,c):
    if x <= a or x >= c:
      return 0
    if a < x and x <= b:
      return (x-a)/(b-a)
    return -(x-c)/(c-b)
  
  def LinearHigh(self,x,a,b):
    if x <= a:
      return 0
    if a < x and x <= b:
      return (x-a)/(b-a)
    return 1
  
  def LinearLow(self,x,a,b):
    if x <= a:
      return 1
    if a < x and x <= b:
      return (b-x)/(b-a)
    return 0
  
  # def Trapezoidal(self,x,a,b,c,d):
  #   if x <= a or x >= d:
  #     return 0
  #   if a < x and x < b: 
  #     return (x-a)/(b-a)
  #   if b <= x and x <= c:
  #     return 1
  #   return -(x-d)/(d-c)
  
  # Fuzzy Rules
  def RecommendedRules(self):
    temp = []

    temp.append(min(self.highQualityService, self.highQualityFood))
    temp.append(min(self.highQualityService, self.averageQualityFood))
    temp.append(min(self.averageQualityService, self.highQualityFood))
    return max(temp)

  def ConsideredRules(self):
    temp = []

    temp.append(min(self.averageQualityService, self.averageQualityFood))
    temp.append(min(self.lowQualityService, self.highQualityFood))
    temp.append(min(self.highQualityService, self.lowQualityFood))
    return max(temp)

  def NotRecommendedRules(self):
    temp = []

    temp.append(min(self.averageQualityService, self.lowQualityFood))
    temp.append(min(self.lowQualityService, self.averageQualityFood))
    temp.append(min(self.lowQualityService, self.lowQualityFood))
    return max(temp)
  
  #Deffuzication
  def Deffuzzication(self):
    i = 5
    j = 0
    maxValue = []
    mult = 0

    while i <= 100:
      tempNR = self.LinearLow(i,40,60);
      tempC = self.Triangles(i,40,60,80)
      tempR = self.LinearHigh(i,60,80)
      
      maxValue.append(max(self.Clipping(tempNR, self.notRecommended), self.Clipping(tempC, self.considered), self.Clipping(tempR, self.recommended)))
      mult += maxValue[j] * i

      i += 10
      j += 1

   
    return mult/sum(maxValue)
  
  def Clipping(self, value, clip):
    if value > clip:
      return clip
    else:
      return value

#baca data
data = pandas.read_excel('restoran.xlsx')
ids = data['id'].values
services = data['pelayanan'].values
foods = data['makanan'].values
fuzzy_set = []
rank = []

for i in range(len(data)):
  fuzzy_set.append(FuzzyRestaurant(ids[i], services[i], foods[i]))
print("\n\n")

#sorting berdasarkan hasil akhir descending
fuzzy_set.sort(key=lambda x:x.score, reverse=True)
print("\t\t\t\t\t\t|\t\tService\t\t\t\t|\t\tFood\t\t\t\t|\t\tScore")
print("--------------------------------------------------------------------------------------------------------------------------------------------------------------")
print("id\t\tService\t\tFood\t\t|HIGH\t\t|AVERAGE\t|LOW\t\t|HIGH\t\t|AVERAGE\t|LOW\t\t|RECOMMENDED\t|CONSIDERED\t|NOT RECOMMENDED|")
print("--------------------------------------------------------------------------------------------------------------------------------------------------------------")
for i in range(10):    #Perulangan untuk mengambil 10 besar
  print(fuzzy_set[i].restaurant ,"\t\t|",
        fuzzy_set[i].service ,"\t\t|",
        fuzzy_set[i].food ,"\t\t|",
        "%.2f" %fuzzy_set[i].highQualityService ,"\t\t|",
        "%.2f" %fuzzy_set[i].averageQualityService,"\t\t|",
        "%.2f" %fuzzy_set[i].lowQualityService,"\t\t|",
        "%.2f" %fuzzy_set[i].highQualityFood,"\t\t|",
        "%.2f" %fuzzy_set[i].averageQualityFood,"\t\t|", 
        "%.2f" %fuzzy_set[i].lowQualityFood,"\t\t|",
        "%.2f" %fuzzy_set[i].recommended,"\t\t|",
        "%.2f" %fuzzy_set[i].considered,"\t\t|",
        "%.2f" %fuzzy_set[i].notRecommended,"\t\t|",
        "%.2f" %fuzzy_set[i].score,"\t\t|",
        )
  rank.append(fuzzy_set[i].restaurant)

#Export
pandas.DataFrame(rank, columns=['ID']).to_excel('peringkat.xlsx', index=False)