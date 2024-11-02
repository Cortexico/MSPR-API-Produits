### API Produits - Documentation

#### Contexte
L'API Produits gère les informations relatives aux produits et permet leur création, modification, et suppression. Elle est conçue pour interagir avec les API Clients et Commandes pour obtenir ou transmettre des informations produit et utilise RabbitMQ pour une communication asynchrone entre services.

#### Prérequis
- **Python 3.9+**
- **Docker** et **Docker Compose** installés
- **RabbitMQ** en cours d'exécution avec le réseau Docker partagé `backend` (se référer à la [documentation](https://github.com/Cortexico/MSPR-RabbitMQ))
- **MongoDB** comme base de données, avec un fichier d'initialisation `init.js` pour créer un utilisateur et une base de données spécifique (`products_db`)
- Fichier `.env` correctement configuré avec les variables suivantes :

```plaintext
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=adminpassword
MONGO_DB=products_db
MONGO_USER=products
MONGO_PASSWORD=apiProducts
MONGO_HOST=db
MONGO_PORT=27017

API_HOST=0.0.0.0
API_PORT=8001

RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
```

#### Instructions de démarrage

#### **1. Cloner le dépôt de l'API Produits** :
   ```bash
   git clone https://github.com/Cortexico/MSPR-API-Produits.git
   ```
#### **2. Créer le réseau Docker partagé** (si non existant) :
   ```bash
   docker network create backend
   ```
#### **3. Créer un Environnement Virtuel**

Il est recommandé d'utiliser un environnement virtuel pour isoler les dépendances.

- **Sur Windows :**
  Création de l'environnement virtuel:
   ```bash
   python -m venv venv
   ```
  
  Lancement de l'environnement virtuel: 
   ```bash
   venv\Scripts\activate
   ```

- **Sur macOS/Linux :**

   Création de l'environnement virtuel:
   ```bash
   python3 -m venv venv
   ```
   
   Lancement de l'environnement virtuel:
   ```bash
   source venv\Scripts\activate
   ```

#### **4. Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```
   
#### **5. Lancer l’API avec Docker Compose** :
   ```bash
   docker-compose up --build
   ```
#### **6. Pour arrêter et supprimer les volumes Docker** (si nécessaire) :
   ```bash
   docker-compose down -v
   ```
#### **Sans Docker**

#### **1. Initialiser MongoDB en local**:
   
   Lancer le serveur MongoDB avec le fichier d'initialisation `init.js` pour créer l'utilisateur et configurer la base de données `products_db` :
   ```bash
   mongo --port 27017 < mongo-init/init.js
   ```
#### **2. Lancer l'API**

   ```bash
   uvicorn app.main:app --host ${API_HOST} --port ${API_PORT}
   ```

#### Documentation technique de l'API

##### Endpoints principaux
- **GET /products** : Récupère la liste des produits.
  - **Réponse** : JSON array contenant les informations de chaque produit.
  
- **POST /products** : Crée un nouveau produit.
  - **Corps** : JSON contenant `name`, `description`, `price`, et `stock`.
  - **Réponse** : Confirmation de création avec les détails du produit ajouté.
  
- **GET /products/{id}** : Récupère les détails d’un produit spécifique.
  - **Paramètre** : `id` du produit.
  - **Réponse** : Détails du produit en JSON.
  
- **PUT /products/{id}** : Met à jour les informations d’un produit.
  - **Corps** : JSON avec les champs à mettre à jour.
  - **Réponse** : Détails mis à jour du produit.
  
- **DELETE /products/{id}** : Supprime un produit.
  - **Paramètre** : `id` du produit.
  - **Réponse** : Confirmation de suppression.

##### Services RabbitMQ
L'API utilise RabbitMQ pour publier et consommer des messages relatifs aux produits.

- **Publisher** : Envoie des notifications lors de la création ou modification de produits.
- **Consumer** : Reçoit des messages des autres API (Clients et Commandes) pour vérifier les informations pertinentes.

#### Notes de sécurité et de debug
- **Sécurité** : Assurez-vous que le fichier `.env` contient des identifiants forts pour les bases de données et RabbitMQ.
- **Mode debug** : Utilisez `uvicorn` en mode `--reload` pour un développement plus rapide en local.
- **Surveillance MongoDB** : Utilisez MongoDB Compass ou un autre client MongoDB pour surveiller la base de données `products_db`.

### Documentation CI/CD - GitHub Actions

#### Contexte
L'intégration continue et le déploiement continu (CI/CD) sont configurés via GitHub Actions pour automatiser les tests, les vérifications de code et le déploiement de l’API Produits. Cette configuration permet de garantir la qualité du code et de faciliter les déploiements.

#### Configuration GitHub Actions
Le fichier de workflow GitHub Actions `.github/workflows/ci.yml` définit les étapes principales du pipeline CI/CD :

1. **Déclencheur** : Le workflow est configuré pour s'exécuter sur chaque `push` ou `pull request` vers la branche principale et pour toute nouvelle branche.
2. **Environnements de test** : Le fichier `ci.yml` installe les dépendances nécessaires, configure les variables d'environnement, et utilise une base de données de test MongoDB pour valider les fonctionnalités.

#### Étapes du Workflow CI/CD

1. **Configurer l'environnement** : 
   - Le workflow utilise une image de conteneur pour configurer l’environnement Python et MongoDB.
   - Installe les dépendances listées dans `requirements.txt` et configure MongoDB en utilisant les variables d’environnement définies dans le fichier `.env`.

2. **Lancer les tests unitaires** :
   - Les tests unitaires sont exécutés via `pytest` pour valider le fonctionnement de chaque endpoint de l’API.
   - Les tests se trouvent dans le répertoire `tests/`, comprenant :
     - `test_create_product.py` : Vérifie la création d'un produit.
     - `test_delete_product.py` : Vérifie la suppression d'un produit.
     - `test_get_product.py` et `test_get_products.py` : Valident les opérations de récupération de produits.
     - `test_update_product.py` : Vérifie la mise à jour d'un produit.

3. **Vérifications de code** :
   - Le workflow utilise `flake8` pour analyser la qualité et le formatage du code.
   - Tout échec de style ou de format déclenchera un échec de pipeline, ce qui permet de garantir un code propre et cohérent.

4. **Build et Déploiement (optionnel)** :
   - Si nécessaire, le pipeline peut être étendu pour inclure une étape de build et de déploiement.
   - Le déploiement peut être automatisé pour une infrastructure de production en ajoutant des étapes spécifiques au déploiement.

#### Variables d'environnement de test
Le workflow CI/CD configure les variables d'environnement nécessaires pour les tests. Les valeurs par défaut peuvent être modifiées dans le fichier `.env` ou directement dans la configuration GitHub Actions si des valeurs spécifiques sont requises pour l’environnement de test.


## **Notes Importantes pour Toutes les APIs**

### **Fichiers `.env`**

- Les fichiers `.env` sont essentiels pour le fonctionnement des APIs.
- Ils contiennent les variables d'environnement nécessaires à la configuration des bases de données et des services externes.
- Assurez-vous que ces fichiers sont placés à la racine de chaque projet.

### **Docker Compose**

- L'utilisation de Docker Compose est recommandée pour faciliter le déploiement des services dépendants comme les bases de données et RabbitMQ.
- Les commandes `docker-compose up --build` et `docker-compose down -v` permettent de gérer facilement les conteneurs.

### **Gestion des Dépendances**

- Les fichiers `requirements.txt` listent toutes les dépendances Python nécessaires.
- Après avoir activé l'environnement virtuel, installez les dépendances avec :

  ```bash
  pip install -r requirements.txt
  ```

### **Résolution des Problèmes Courants**

- **Ports Occupés :**

  - Si un port est déjà utilisé, modifiez la variable `API_PORT` dans le fichier `.env` et ajustez les ports exposés dans le `docker-compose.yml`.

- **Problèmes de Connexion aux Bases de Données :**

  - Vérifiez que les services de base de données sont en cours d'exécution.
  - Assurez-vous que les variables d'environnement correspondent aux configurations de vos services.

- **Erreurs lors de l'Activation de l'Environnement Virtuel :**

  - Assurez-vous que vous utilisez la bonne version de Python.
  - Vérifiez les permissions du dossier `venv`.

### **Documentation et Tests**

- Chaque API est fournie avec une documentation interactive accessible via `/docs`.
- Utilisez cet outil pour tester les endpoints et comprendre les modèles de données.

### **Sécurité**

- **Variables Sensibles :**

  - Ne partagez pas vos fichiers `.env` ou toute information sensible.
  - Pour un environnement de production, utilisez des gestionnaires de secrets sécurisés.

- **Mises à Jour :**

  - Gardez vos dépendances à jour en vérifiant régulièrement le fichier `requirements.txt`.