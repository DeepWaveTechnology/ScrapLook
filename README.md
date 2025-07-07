# ScrapLook

## Table des matières

* [ScrapLook](#scraplook)
  * [Table des matières](#table-des-matières)
  * [Technologies utilisées](#technologies-utilisées-)
    * [Front](#front)
    * [Backend](#backend)
  * [Présentation](#présentation)
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