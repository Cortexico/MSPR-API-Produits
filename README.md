## **API Produits**

### **Description**

Cette API gère les informations des produits. Elle permet de créer, lire, mettre à jour et supprimer des produits dans la base de données MongoDB.

### **Prérequis**

- **Python 3.9+**
- **Virtualenv** (optionnel mais recommandé)
- **Docker et Docker Compose** (si vous souhaitez utiliser Docker)
- **Fichier `.env`** contenant les variables d'environnement (fourni séparément)

### **Installation**

#### **1. Cloner le Repository**

```bash
git clone https://github.com/Cortexico/MSPR-API-Produits.git
cd API_produits
```

#### **2. Créer un Environnement Virtuel**

- **Sur Windows :**

  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

- **Sur macOS/Linux :**

  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

#### **3. Installer les Dépendances**

```bash
pip install -r requirements.txt
```

#### **4. Configurer les Variables d'Environnement**

Assurez-vous que le fichier `.env` est présent à la racine du projet avec les variables suivantes :

```
# Variables pour MongoDB
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=adminpassword
MONGO_DB=products_db
MONGO_USER=products
MONGO_PASSWORD=apiProducts
MONGO_HOST=db
MONGO_PORT=27017

# Variables pour l'API
API_HOST=0.0.0.0
API_PORT=8001

# Variables pour RabbitMQ
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
```

### **Lancement de l'API**

#### **Avec Docker Compose (Recommandé)**

```bash
docker-compose up --build
```

- Cette commande va construire les images Docker et lancer les services définis dans `docker-compose.yml`, y compris MongoDB et RabbitMQ.

#### **Sans Docker**

**1. Lancer la Base de Données MongoDB**

- Assurez-vous que MongoDB est installé et en cours d'exécution.
- Créez un utilisateur et une base de données correspondant aux variables d'environnement.

**2. Lancer l'API**

```bash
uvicorn app.main:app --host ${API_HOST} --port ${API_PORT}
```

### **Accès à la Documentation de l'API**

- Une fois l'API lancée, accédez à la documentation interactive :

  ```
  http://localhost:8001/docs
  ```

## **Notes Importantes pour Toutes les APIs**

### **Activation de l'Environnement Virtuel**

- **Windows :**

  - Pour activer l'environnement virtuel, exécutez :

    ```bash
    venv\Scripts\activate
    ```

- **macOS/Linux :**

  - Pour activer l'environnement virtuel, exécutez :

    ```bash
    source venv/bin/activate
    ```

- **Désactivation :**

  - Pour désactiver l'environnement virtuel, exécutez :

    ```bash
    deactivate
    ```

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