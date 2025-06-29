# ScrapLook

## Technologies utilisées 

### Front

- **Framework** : Vue
- **Component library** : PrimeVue
- TypeScrypt
- Eslint

### Backend

- **ORM** : Prisma
  - Pour lancer le server web : `npx prisma generate && npx prisma migrate dev && npx prisma db push && npx prisma studio`
- **Langage**: Python
- **Serveur back** : FastAPI
- **Routes**: 
    - /!\ Toutes les routes concernent une action d'un seul utilisateur.

    - **Récupérer les informations de l'utilisateur**:
        - Nom de l'endpoint: get 'user/:id_user'
        - Description:
        - Paramètres: Identifiant de l'utilisateur où récupérer les informations, hors mails.
        - Retours: User

    - **Ajouter une adresse mail**: 
        - Nom de l'endpoint: get 'email_address/'
        - Description:
        - Paramètres: Email à ajouter.
        - Retours: 201_CREATED

    - **Supprimer une adresse mail**:
        - Nom de l'endpoint: delete 'email_address/:id_email_address'
        - Description: 
        - Paramètres: Identifiant de l'adresse mail à supprimer
        - Retours: 200_OK

    - **Modifier une adresse mail**:
        - Nom de l'endpoint: patch 'email_address/'
        - Description: Modifier l'adresse mail d'un utilisateur, à savoir le champ **address** uniquement.
        - Paramètres: Email à modifier.
        - Retours: 200_OK

    - **Afficher les adresses mails**:
        - Nom de l'endpoint: get 'email_address/all'
        - Description: 
        - Paramètres: 
        - Retours: List[Email]

    - **Afficher tous les mails envoyés**:
        - Nom de l'endpoint: get 'messages/sent_messages'
        - Description: 
        - Paramètres: /
        - Retours: List[Message]

    - **Afficher tous les mails reçus**:
        - Nom de l'endpoint: get 'messages/received_messages'
        - Description: 
        - Paramètres: /
        - Retours:  List[Message]

    - **Afficher un mail**:
        - Nom de l'endpoint: get 'messages/:id_message'
        - Description: 
        - Paramètres: Identifiant du message à afficher.
        - Retours: Message

    - **Envoyer un mail**:
        - Nom de l'endpoint: post 'messages/'
        - Description: 
        - Paramètres: Email à envoyer.
        - Retours: 201_CREATED

    - **Supprimer un mail**:
        - Nom de l'endpoint: delete 'messages/:id_message'
        - Description: 
        - Paramètres: Identifiant du message à supprimer.
        - Retours: 200_OK