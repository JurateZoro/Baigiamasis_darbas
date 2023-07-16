import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
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


#gimstamumas pagal lytį
df = pd.read_csv('statistikagime.csv')
# Filtruoti duomenis pagal 'V' ir 'M' lytis
df_filtruoti = df[df['lytis'].isin(['V', 'M'])]
# Gruputi duomenis pagal 'year' ir 'lytis' ir apskaičiuoti sumą
grouped = df_filtruoti.groupby(['year', 'lytis'])['suma'].sum().reset_index()
# Pertvarkyti duomenis, kad gautumėme stulpeliniu formatu su 'V' ir 'M' stulpeliais
gimstamumas_vm = grouped.pivot(index='year', columns='lytis', values='suma')
# Vizualizuoti duomenis stulpelinėje diagramoje
gimstamumas_vm.plot(kind='bar')
plt.xlabel('Metai')
plt.ylabel('Gimstamumas')
plt.title('Gimstamumas pagal lytį')
plt.legend(['Vyrai', 'Moterys'])
plt.show()

print(gimstamumas_vm)

# Apskaičiuojame procentinį gimstamumo pasiskirstymą pagal regionus
gimstamumas_regionais = df.groupby('region')['suma'].sum()
procentai = gimstamumas_regionais / gimstamumas_regionais.sum() * 100
# Vizualizuojame skritulinę diagramą su procentais pagal regionus
plt.figure(figsize=(10, 6))
plt.title('Gimstamumas pagal apskritis')
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



# Metinis gimstamumo pokytis


# gimstamumas = np.genfromtxt('gimstamumas1.csv', delimiter=',', encoding="utf8")

metai = np.array([2018, 2019, 2020, 2021, 2022])
gimstamumas = np.array([28149, 27393, 25144, 23330, 22068])


gimstamumo_pokytis = (gimstamumas[1:] - gimstamumas[:-1]) / gimstamumas[:-1] * 100
# print(gimstamumo_pokytis)

plt.plot(metai[1:], gimstamumo_pokytis, marker='o', color='pink', label='gimstamumas')

plt.xlabel(xlabel='metai')
plt.ylabel(ylabel='gimstamumo_pokytis')
plt.title('Metinis gimstamumo pokytis procentais')

tendencija = np.polyfit(metai[1:], gimstamumo_pokytis, 1)
# prognoze
prognoze = np.polyval(tendencija, metai[1:])

plt.plot(metai[1:], prognoze, color='red', label='prognoze')
plt.xlim(2018, 2023)
plt.xticks(range(2018, 2023, 1))
plt.legend()
plt.show()


# Metinis mirtingumo pokytis


# mirtingumas = np.genfromtxt('mirtingumas.csv', delimiter=',', encoding="utf8")

metai = np.array([2018, 2019, 2020, 2021, 2022])
mirtingumas = np.array([39574, 38281, 43547, 47746, 42884])


mirtingumo_pokytis = (mirtingumas[1:] - mirtingumas[:-1]) / mirtingumas[:-1] * 100
# print(mirtingumo_pokytis)

plt.plot(metai[1:], mirtingumo_pokytis, marker='o', color='pink', label='mirtingumas')

plt.xlabel(xlabel='metai')
plt.ylabel(ylabel='mirtingumo_pokytis')
plt.title('Metinis mirtingumo pokytis procentais')

tendencija = np.polyfit(metai[1:], mirtingumo_pokytis, 1)
# prognoze
prognoze = np.polyval(tendencija, metai[1:])

plt.plot(metai[1:], prognoze, color='red', label='prognoze')
plt.xlim(2018, 2023)
plt.xticks(range(2018, 2023, 1))
plt.legend()
plt.show()


# # Nuskaitome duomenis iš pirmojo CSV failo
gime = np.genfromtxt('gimstamumas.csv', delimiter=',', encoding="utf8")
x1 = gime[:, 0]
y1 = gime[:, 1]

mire = np.genfromtxt('mirtingumas.csv', delimiter=',', encoding="utf8")
x2 = mire[:, 0]
y2 = mire[:, 1]

gime = pd.read_csv('gimstamumas.csv', delimiter=',', encoding="utf8")
mire = pd.read_csv('mirtingumas.csv', delimiter=',', encoding="utf8")
mire['metai'] = pd.to_datetime(mire['metai'])
mire['Year'] = mire['metai'].dt.year
#
gime['metai'] = pd.to_datetime(gime['metai'])
gime['Year'] = gime['metai'].dt.year

# Nubraižome pirmąją kreivę
plt.plot(x1, y1, label='Gimstamumas')
plt.xlim(2017, 2023)
plt.xticks(range(2017, 2023, 1))

# Nubraižome antrąją kreivę
plt.plot(x2, y2, label='Mirtingumas')

# Rodyti reikšmių taškus ant pirmosios kreivės
plt.scatter(x1, y1, color='red')

# Rodyti reikšmių taškus ant antrosios kreivės
plt.scatter(x2, y2, color='blue')

# Pridedame skaičius virš taškų ant pirmosios kreivės
for i in range(len(x1)):
    plt.annotate(str(y1[i]), (x1[i], y1[i]), textcoords="offset points", xytext=(0,10), ha='center')

# Pridedame skaičius virš taškų ant antrosios kreivės
for i in range(len(x2)):
    plt.annotate(str(y2[i]), (x2[i], y2[i]), textcoords="offset points", xytext=(0,10), ha='center')


# Pridedame ašių pavadinimus ir grafiko pavadinimą
plt.xlabel(xlabel='metai')
plt.ylabel(ylabel='žmonių skaičius')
plt.title('Mirtingumas ir gimstamumas 2018-2022 m.')

# Pridedame legendą
plt.legend()

plt.show()


# Mirtingumas pagal priežastis
data = pd.read_csv('statistikamire.csv')
# Grupuojame duomenis pagal metus ir mirties priežastis, ir sumuojame mirusiųjų skaičių
mirties_priezastys = data.groupby(['metai', 'mirties_priezastis'])['suma'].sum().reset_index()
# Rikiuojame mirties priežastis pagal mirusiųjų skaičių mažėjimo tvarka
mirties_priezastys = mirties_priezastys.sort_values(['metai', 'suma'], ascending=[True, False])
# Braižome grafiką naudodami seaborn
plt.figure(figsize=(10, 6))
sns.barplot(x='metai', y='suma', hue='mirties_priezastis', data=mirties_priezastys)
plt.xticks(rotation=90)
plt.xlabel = ('Metai')
plt.ylabel = ('Mirusiųjų skaičius')
plt.title('Mirtingumas pagal mirties priežastis')
plt.tight_layout()
# Rodyti grafiką
plt.show()


