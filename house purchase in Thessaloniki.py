import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier

dataset=pd.read_csv(""https://raw.githubusercontent.com/fwteinh777/project-1---2123042/main/dataset.csv"")
dataset=dataset.dropna()
dataset=dataset[["price","type","floor","area","y_build","y_rebuild"]]
dataset["floor"]=dataset["floor"].astype(int)
dataset["y_rebuild"]=dataset["y_rebuild"].astype(int)
dataset["y_build"]=dataset["y_build"].astype(int)
dataset["price"]=dataset["price"].round(2)

columns=[]#lista gia tis filtrarismenes sthles - xarakthristika tou pinaka
print("Houses for purchase in Thessaloniki!")
print("Place some filters:")
print("Available characteristics: type , area in sqm , floor , construction , renovation ")
x=input("Enter the first characteristic:")
if x.lower()=="type":
    t=input("Enter the type of the house('Διαμέρισμα' 'Studio / Γκαρσονιέρα' 'Μεζονέτα' 'Loft''Συγκρότημα διαμερισμάτων' 'Κτίριο' 'Μονοκατοικία'):")
    filtDataset = dataset[dataset['type'].str.lower() == t.lower()]
    if "type" not in columns:
        columns.append("type")
elif x.lower() in ["area","area in sqm"]:
    a1=input("At least:")
    a2=input("Not more than:")
    filtDataset = dataset[(dataset['area']>=int(a1)) & (dataset['area']<=int(a2))]
    if "area"not in columns:
        columns.append("area")
elif x.lower()=="floor":
    f=input("Enter on which floor you want your house to be(max 8):")
    filtDataset = dataset[dataset['floor']==int(f)]
    if "floor"not in columns:
        columns.append("floor")
elif  x.lower()=="construction":
  y=input("Year of construction at least:")
  filtDataset=dataset[dataset["y_build"]>=int(y)]
  if "y_build"not in columns:
      columns.append("y_build") 
elif  x.lower()=="renovation":
    y=input("Year of renovation at least:")
    filtDataset=dataset[dataset["y_rebuild"]>=int(y)]
    if "y_rebuild"not in columns:
      columns.append("y_rebuild")   
else:
    print("No such characteristic!")  
    
cont=input("Do you want to place some more filters?(type 'Y'for yes , 'N' for no)")
while cont=="y" or cont=="Y":
    x=input("Enter the next characteristic:")
    if x.lower()=="type" :
        t=input("Enter the type of the house('Διαμέρισμα' 'Studio / Γκαρσονιέρα' 'Μεζονέτα' 'Loft' 'Συγκρότημα διαμερισμάτων' 'Κτίριο' 'Μονοκατοικία'):")
        filtDataset = filtDataset[filtDataset['type'].str.lower()==t.lower()]
        if "type" not in columns:
            columns.append("type")
    elif x.lower() in ["area","area in sqm"]:
        a1=input("At least:")
        a2=input("Not more than:")
        filtDataset = filtDataset[(filtDataset['area']>=int(a1)) & (filtDataset['area']<=int(a2))]
        if "area"not in columns:
           columns.append("area")
    elif x.lower()=="floor" :
        f=input("Enter on which floor you want your house to be(max 8):")
        filtDataset = filtDataset[filtDataset['floor']==int(f)]
        if "floor"not in columns:
         columns.append("floor")
    elif  x.lower()=="construction":
        y=input("Year of construction at least:")
        filtDataset=filtDataset[dataset["y_build"]>=int(y)]
        if "y_build"not in columns:
           columns.append("y_build")  
    elif  x.lower()=="renovation":
        y=input("Year of renovation at least:")
        filtDataset=filtDataset[dataset["y_rebuild"]>=int(y)]
        if "y_rebuild"not in columns:
            columns.append("y_rebuild") 
    else:
         print("No such characteristic!")
    cont=input("Do you want to place some more filters?(type 'Y'for yes , 'N' for no)")    

    
if filtDataset.empty:
    print("No properties with these characteristics.")
else:
 print(" ")
 print(filtDataset)
 print(" ")
 array=filtDataset["price"].to_numpy()
 print("Μέση τιμή ακινήτου για τα δοθέντα χαρακτηριστικά:",round(np.mean(array),2))
 print("Απόκλιση τιμών ακινήτου για τα δοθέντα χαρακτηριστικά:",round(np.std(array,ddof=1),2))
 print("Διάμεσος τιμής ακινήτου για τα δοθέντα χαρακτηριστικά:",round(np.median(array),2))

 dataset = pd.get_dummies(dataset, columns=["type"], drop_first=True)#to linear regression dexetai mono arithmitika dedomena ara allazoume ta kathgorika
 x=dataset.drop(columns=["price"])
 y=dataset["price"]

 model=LinearRegression()
 model.fit(x,y)

 rs=filtDataset.reindex(columns=x.columns, fill_value=0)#exoume hdh kataripsei kapoies sthles ara tis janaftiaxnoume kai bazoume 0 giati den exoun shmasia sthn problepsh
 pr=model.predict(rs)
 filtDataset["predictedPrice"] = pr#kanw kainourgia sthlh sto dataset me tis problepomenes times
 filtDataset["predictedPrice"]=filtDataset["predictedPrice"].round(2)
 print(" ")
 print("New column - price predictions:")
 print(filtDataset)
 print(" ")
 cl=DecisionTreeClassifier()
 av=(filtDataset["price"]+filtDataset["price"])/2
 categories1=[(av<=60000.0),((av>60000.0) & (av<=120000.0)),(av>120000.0)]
 categories2=["economic","medium","overpriced"]
 filtDataset["category"]=np.select(categories1,categories2,default="unknown")#antistoixish ths kathgorias timhs me thn kathgoria akinhtou
 features=filtDataset[["price","predictedPrice"]]   
 label=filtDataset[["category"]]
 cl.fit(features,label)
 filtDataset["category"]=cl.predict(features)
 print("New column - classification:")
 print(filtDataset)


 
