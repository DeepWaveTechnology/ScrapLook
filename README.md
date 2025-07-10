# ScrapLook

## Table des matières

* [ScrapLook](#scraplook)
  * [Table des matières](#table-des-matières)
  * [Technologies utilisées](#technologies-utilisées-)
    * [Front](#front)
    * [Backend](#backend)
  * [Présentation](#présentation)
  * [Configuration du fichier .env ](#configuration-du-fichier-env )
  * [Installation et lancement du serveur back](#installation-et-lancement-du-serveur-back)
  * [Installation et lancement du serveur front](#installation-et-lancement-du-serveur-front)

## Technologies utilisées 

### Front

- **Framework** : Vue
- **Component library** : PrimeVue
- TypeScrypt
- Eslint

### Backend

## Présentation

- **Langage**: Python
- **ORM** : Prisma
- **Serveur back** : FastAPI
- **Routes**: 
    - /!\ Toutes les routes concernent une action d'un seul utilisateur.

    - **Récupérer les informations de l'utilisateur**:
        - Nom de l'endpoint: get 'user/:id_user' ==> fait
        - Description:
        - Paramètres: Identifiant de l'utilisateur où récupérer les informations, hors mails.
        - Retours: User

    - **Ajouter une adresse mail**: 
        - Nom de l'endpoint: get 'email_address/' ==> fait
        - Description:
        - Paramètres: Email à ajouter :
        ```py
            address: str
            userId: str
        ```
        - Retours: 201_CREATED

    - **Supprimer une adresse mail**:
        - Nom de l'endpoint: delete 'email_address/:id_email_address' ==> fait
        - Description: 
        - Paramètres: Identifiant de l'adresse mail à supprimer
        - Retours: 200_OK

    - **Modifier une adresse mail**:
        - Nom de l'endpoint: patch 'email_address/' ==> fait
        - Description: Modifier l'adresse mail d'un utilisateur, à savoir le champ **address** uniquement.
        - Paramètres: Identifiant de l'utilisateur et Email à modifier :
        ```py
            address: str
            userId: str
        ```
        - Retours: 200_OK

    - **Afficher les adresses mails**:
        - Nom de l'endpoint: get 'email_address/all' ==> fait
        - Description: 
        - Paramètres: 
        - Retours: List[Email]

    - **Afficher tous les mails envoyés**:
        - Nom de l'endpoint: get 'messages/sent_messages'
        - Description: 
        - Paramètres: Identifiant de l'addresse mail utilisée pour envoyer les mails.
        - Retours: List[Message]

    - **Afficher tous les mails reçus**:
        - Nom de l'endpoint: get 'messages/received_messages' ==> fait
        - Description: 
        - Paramètres: Identifiant de l'addresse mail utilisée pour recevoir les mails.
        - Retours:  List[Message]

    - **Afficher un mail**:
        - Nom de l'endpoint: get 'messages/:id_message' ==> fait
        - Description: 
        - Paramètres: Identifiant du message à afficher.
        - Retours: Message

    - **Envoyer un mail**:
        - Nom de l'endpoint: post 'messages/' ==> fait
        - Description: 
        - Paramètres: Email à envoyer :
        ```py
            class MessageRecipientInput(BaseModel):
                emailId: str
                type: str

            class MessageInput(BaseModel):
                subject: Optional[str] = None
                body: str
                fromId: str
                recipients: List[MessageRecipientInput]
        ```
        - Retours: 201_CREATED

    - **Supprimer un mail**:
        - Nom de l'endpoint: delete 'messages/:id_message' ==> quasiment fait (fonctionne pour les utilisateurs qui suppriment des mails qu'ils ont envoyés)
        - Description: 
        - Paramètres: Identifiant du message à supprimer.
        - Retours: 200_OK

## Configuration du fichier .env 

Le projet contient un fichier .env dans le répertoire **ScrapLook\scraplook-backend**. 
Il faut le remplir avant sa clé de cryptage et le temps en minute que va durer le token d'accès avant de lancer le projet. 
Il doit être écrit de cette façon : 
```bash
encryption_key="..."
access_token_duration_minutes=30
refresh_token_duration_hours=2
access_token_invalid_timeout_minutes=3
```
La clé de cryptage (encryption_key) peut être généré à l'aide de cette commande (par exemple, sur Linux) : 
```bash
openssl rand -base64 32
```

## Installation et lancement du serveur back

Se positionner dans le répertoire **ScrapLook\scraplook-backend**.

```bash
venv_init_scripts/env_build.bat
.\.venv\Scripts\activate
prisma db push
pdm dev #pdm prod ==> pour la production (configuration à éditer dans le fichier 'pyproject.toml')
```

Accéder à l'url <a href="http://127.0.0.1:8000/docs">localhost</a>, puis appeler l'endpoint **/seeder/populate**, pour créer un jeux de données de départ.

## Installation et lancement du serveur front

Se positionner dans le répertoire **ScrapLook\scraplook-frontend**.

```bash
npm install
npm run dev
```

Accéder à l'url <a href="http://127.0.0.1:5173/">localhost</a>. 


## Fonctionnalités du site 

Lorsqu'on lance le projet, on arrive sur la page d'accueil. Avant de pouvoir accéder aux fonctionnalités, du menu utilisateur, il faut se connecter. En effet, les fonctionnalités liés à un compte sont bloqués grâce à des guards côté front et à des dépendances côté back. 

### Connexion et déconnexion 

On peut se connecter via le bouton en haut à droite en utilisant par exemple les comptes ci-dessous : 

```bash
username : AntoninD, password : azerty
username : Alice, password : alice123
username : Jean, password : jean456
```

Notre système de connexion utilise un acces_token créé avec JWT et stocké dans le localStorage. En parralèle, un refresh_token est aussi créé de la même façon. Il a une date d'expiration plus longue que le premier et sert à régénérer l'access token si besoin. 

Lors de la déconnexion, on supprime le access_token et le refresh_token qui était stockés localement et on met à jour la page web. 

### Page de la liste des utilisateurs

A partir de là, on envoie le access_token dans chaque requête via un HTTP interceptor Axios. 

Sur cette page, il est possible de consulter tous les utilisateurs du site via une route dédiée. 
On peut aussi créer un utilisateur via le bouton en haut de la liste. Celui-ci sera ajouté à la base de données. Chaque mot de passe dans la base de données est crypté. 
Enfin, il est possible de supprimer une adresse mail à un utilisateur ou d'en rajouter une via cette page. Encore une fois, le changement sera réflété sur la base de données. 

### Détail d'une adresse mail

En cliquant sur une adresse mail et grâce à plusieurs routes, il est possible de : 

- Mettre à jour l'adresse mail 
- Envoyer un message 
- Visualiser et/ou supprimer les messages envoyés 
- Visualiser et/ou supprimer les messages reçus  