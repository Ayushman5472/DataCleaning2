import csv
from sys import set_asyncgen_hooks
rows = []
with open ('data2.csv', 'r') as f:
    csvReader = csv.reader(f)
    for i in csvReader:
        rows.append(i)

headers = rows[0]
planetData = rows[1:]
print(headers)
headers[0] = "Serial N.O." 
SolarSystemPC = {}
for i in planetData:
    if SolarSystemPC.get(i[11]):
        SolarSystemPC[i[11]] += 1
    else:
        SolarSystemPC[i[11]] = 1

MaxSolarSystem = max(SolarSystemPC, key = SolarSystemPC.get)
print(MaxSolarSystem)
koi = []
for i in planetData:
    if i[11] == MaxSolarSystem:
        koi.append(i)

print(len(koi))
print(koi)

tempPlanetData = list(planetData)
for i in tempPlanetData:
    planetMass = i[3]
    if planetMass.lower() == "unknown":
        planetData.remove(i)
        continue
    else:
        planetMassValue = planetMass.split(" ")[0]
        planetMassRef = planetMass.split(" ")[1]
        if planetMassRef == "Jupiters":
            planetMassValue = float(planetMassValue)*317.8
        i[3] = planetMassValue
    planetRadius = i[7]
    if planetRadius.lower() == 'unknown':
        planetData.remove(i)
        continue
    else:
        planetRadiusValue = planetRadius.split(" ")[0]
        planetRadiusRef = planetRadius.split(' ')[1]
        if planetRadiusRef == 'Jupiters':
            planetRadiusValue = float(planetRadiusValue)*11.2
        i[7] = planetRadiusValue

import plotly.express as px
koiMass = []
koiName = []
for i in koi:
    koiMass.append(i[3])
    koiName.append(i[1])
koiMass.append(1)
koiName.append('Earth')
graph = px.bar(x = koiName, y = koiMass)
#graph.show()

tempPlanetData = list(planetData)
planetMasses = []
planetRadii = []
planetNames = []
planetGravity = []
for i in tempPlanetData:
    if i[1].lower() == "hd 100546 b":
        planetData.remove(i)
for i in planetData:
    planetMasses.append(i[3])
    planetRadii.append(i[7])
    planetNames.append(i[1])
for index,name in enumerate(planetNames):
    gravity = ((float(planetMasses[index])* 5.972e+24)/(float(planetRadii[index])*float(planetRadii[index])*6371000*6371000))*6.674e-11
    planetGravity.append(gravity)

graph2 = px.scatter(x = planetRadii, y = planetMasses, size = planetGravity, hover_data = [planetNames])
#graph2.show()

lowGravPlanets = []
lowGravPlanets2 = []
for index,gravity in enumerate(planetGravity):
    if gravity<10:
        lowGravPlanets.append(planetData[index])
print(len(lowGravPlanets))

for index, gravity in enumerate(planetGravity):
    if gravity<100:
        lowGravPlanets2.append(planetData[index])
print(len(lowGravPlanets2))

planetType = []
for i in planetData:
    planetType.append(i[6])
print(list(set(planetType)))
planetMassLG = []
planetRadiusLG = []
for i in lowGravPlanets2:
    planetMassLG.append(i[3])
    planetRadiusLG.append(i[7])
graph3 = px.scatter(x = planetRadiusLG, y = planetMassLG)
#graph3.show()
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sb
x = []
for index,planetMass in enumerate(planetMassLG):
    templist = [planetRadiusLG[index], planetMass]
    x.append(templist)

wcss = []
for i in range(1,11):
    kmeans = KMeans(n_clusters = i, init = "k-means++", random_state = 42)
    kmeans.fit(x)
    wcss.append(kmeans.inertia_)

plt.figure(figsize = (20,15))
sb.lineplot(range(1,11), wcss, marker = "o", color = 'red')
plt.title("elbowMethod")
plt.xlabel('number of clusters')
plt.ylabel('wcss')
#plt.show()

planetMass = []
planetRadius = []
planetType = []
for i in lowGravPlanets2:
    planetMass.append(i[3])
    planetRadius.append(i[7])
    planetType.append(i[6])
graph4 = px.scatter(x = planetRadius, y = planetMass, color = planetType)
#graph4.show()

suitablePlanets = []
for i in lowGravPlanets2:
    if i[6]=='Super Earth':
        suitablePlanets.append(i)
    if i[6]=='Terrestrial':
        suitablePlanets.append(i)
print(len(suitablePlanets))