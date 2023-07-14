import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import seaborn as sns
import unicodedata

duomenys = pd.read_csv('statistika.csv', encoding="utf8")

duomenys_filtruoti = duomenys[duomenys['lytis'] == 'VM']

didziausias_gimstamumas = duomenys_filtruoti['gimstamumas'].max()
maziausias_gimstamumas = duomenys_filtruoti['gimstamumas'].min()

print(f'Didžiausias gimstamumas: {didziausias_gimstamumas}')
print(f'Mažiausias gimstamumas: {maziausias_gimstamumas}')


vidurkis = duomenys_filtruoti['gimstamumas']
vid_gimstamumas = np.mean(vidurkis)
print(f'Vidutinis gimstamumas per 2018-2022 metus: {vid_gimstamumas}')

gime_per_penkis_metus = duomenys_filtruoti['gimstamumas'].sum()
print(f'Gimstamumas 2018-2022 metais: {gime_per_penkis_metus}')

Vilnius = (duomenys_filtruoti['Vilniaus_apskritis'].sum() / duomenys_filtruoti['gimstamumas'].sum()) * 100
print(f'Pasiskirstymas pagal apskritis procentais: {Vilnius}')


apskritys = pd.read_csv('statistikagime.csv', encoding="utf8")

apskritys_filtruoti = apskritys[apskritys['lytis'] == 'VM']

grouped = apskritys_filtruoti.groupby(['year', 'region'])['suma'].sum().reset_index()
metinis_isviso = grouped.groupby('year')['suma'].transform('sum')
grouped['Percentage'] = (grouped['suma'] / metinis_isviso) * 100


grouped_suapvalintas = round(grouped, 2)
print(f'Gimstamumas apskrityse procentais: {grouped_suapvalintas}')


# Nuskaityti CSV failą
df = pd.read_csv('statistikagime.csv')
# Filtruoti duomenis pagal 'V' ir 'M' lytis
df_filtruoti = df[df['lytis'].isin(['V', 'M'])]
# Grupeiškite duomenis pagal 'year' ir 'lytis' ir apskaičiuokite sumą
grouped = df_filtruoti.groupby(['year', 'lytis'])['suma'].sum().reset_index()
# Pertvarkyti duomenis, kad gautumėte stulpeliniu formatu su 'V' ir 'M' stulpeliais
gimstamumas_vm = grouped.pivot(index='year', columns='lytis', values='suma')
# Vizualizuoti duomenis stulpelinėje diagramoje
gimstamumas_vm.plot(kind='bar')
plt.xlabel('Metai')
plt.ylabel('Gimstamumas')
plt.title('Vyrų ir moterų gimstamumas kiekvienais metais')
plt.legend(['V', 'M'])
plt.show()
# Atspausdinti DataFrame su gimstamumu
print(gimstamumas_vm)


# Apskaičiuojame procentinį gimstamumo pasiskirstymą pagal regionus
gimstamumas_regionais = df.groupby('region')['suma'].sum()
procentai = gimstamumas_regionais / gimstamumas_regionais.sum() * 100
# Vizualizuojame skritulinę diagramą su procentais pagal regionus
plt.figure(figsize=(10, 6))
plt.title('Gimstamumas apskrityse procentais')
plt.pie(procentai, labels=procentai.index, autopct='%1.1f%%')
plt.axis('equal')
plt.show()


duomenys = pd.read_csv('mirepagalapsk.csv', encoding="utf8")
# Apskaičiuojame didžiausią ir mažiausią mirtingumą
didziausias_mirtingumas = duomenys['mirtingumas'].max()
maziausias_mirtingumas = duomenys['mirtingumas'].min()
print(f'Didžiausias mirtingumas pagal: {didziausias_mirtingumas}')
print(f'Mažiausias mirtingumas: {maziausias_mirtingumas}')
vidurkis = duomenys['mirtingumas']
vid_mirtingumas = np.mean(vidurkis)
print(f'Vidutinis mirtingumas per 2018-2022 metus: {vid_mirtingumas}')
mire_per_penkis_metus = duomenys['mirtingumas'].sum()
print(f'Mirtingumas 2018-2022 metais: {mire_per_penkis_metus}')
# Apskaičiuojame procentinį mirtingumo pasiskirstymą tik apskrityse, kuriuose yra "_apskritis" žodis
mirtingumas_apskrityse = duomenys[duomenys['apskritis'].str.contains("_apskritis")].groupby('apskritis')['mirtingumas'].sum()
procentai = mirtingumas_apskrityse / mirtingumas_apskrityse.sum() * 100
# Vizualizuojame skritulinę diagramą su procentais pagal apskritis
plt.figure(figsize=(10, 6))
plt.title('Mirtingumas pagal apskritis')
plt.pie(procentai, labels=procentai.index, autopct='%1.1f%%')
plt.axis('equal')
plt.show()
# Šis kodas paskaičiuoja procentinį mirtingumo pasiskirstymą kiekvienai apskrities,
# tada naudoja plt.pie() funkciją, kad vizualizuotų skritulinę diagramą su procentais.
# autopct='%1.1f%%' nurodo, kad procentinė reikšmė bus rodoma su viena skaičiaus po kablelio tikslumu.
# Šiame kodui pridėtas filtravimas, naudojant .str.contains() funkciją, kuri tikrina, ar tekste yra "_apskritis" žodis.
# Taip galime atidžiau apibrėžti tik tuos įrašus, kurie atitinka jūsų reikalavimus.


# grupuokime duomenis pagal mirimo priežastis ir gaukime vidutini mirtingumą

mirtys = pd.read_csv('statistikamire.csv', encoding="utf8")

mirtys_filtruoti = mirtys[mirtys['lytis'] == 'VM']

vidutinis_mirtingumas = mirtys_filtruoti.groupby(['metai', 'mirties_priezastis'])['suma'].mean()

# Konvertuojame grupavimo rezultatus į DataFrame
vidutinis_mirtingumas = vidutinis_mirtingumas.reset_index()
# Nubraižome linijinę diagramą
plt.figure(figsize=(10, 6))
# Iteruojame per unikalių mirties priežasčių sąrašą
for priezastis in vidutinis_mirtingumas['mirties_priezastis'].unique():
    # Filtruojame duomenis pagal mirties priežastį
    duomenys = vidutinis_mirtingumas[vidutinis_mirtingumas['mirties_priezastis'] == priezastis]
    # Nubraižome linijinę diagramą pagal metus ir vidutinį mirtingumą
    plt.plot(duomenys['metai'], duomenys['suma'], marker='o', label=priezastis)
# Pridedame ašių pavadinimus ir legendą
plt.xlabel('Metai')
plt.ylabel('Vidutinis mirtingumas')
plt.legend()
# Rodyti diagramą
plt.show()