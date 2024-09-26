import json
import pandas as pd
import matplotlib.pyplot as plt

# Charger les données du fichier JSON
with open('output.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Transformer les données en DataFrame (tableau) pour faciliter la manipulation
df = pd.DataFrame(data)

# Afficher les premières lignes pour vérifier
print(df.head())

# -------- Graphique des prix des produits -------- #
plt.figure(figsize=(10, 6))
plt.barh(df['title'], df['price'], color='skyblue')
plt.xlabel('Prix (€)')
plt.ylabel('Produits')
plt.title('Prix des iPhones scrappés sur Amazon')
plt.tight_layout()
plt.show()

# -------- Graphique des ratings des produits -------- #
plt.figure(figsize=(10, 6))
plt.scatter(df['title'], df['rating'], color='green')
plt.xticks(rotation=90)  # Rotation des labels pour éviter qu'ils se chevauchent
plt.ylabel('Note (sur 5)')
plt.title('Notes des iPhones sur Amazon')
plt.tight_layout()
plt.show()

# -------- Histogramme des prix -------- #
plt.figure(figsize=(8, 5))
plt.hist(df['price'], bins=10, color='purple', edgecolor='black')
plt.xlabel('Prix (€)')
plt.ylabel('Nombre de produits')
plt.title('Répartition des prix des iPhones')
plt.tight_layout()
plt.show()
