# NaN-SpaceX CHALLENGE

The goal is to add cards in Trello.



## Instalation 👨‍💻

### Pre Requirements 📋

- **Docker-compose**


## Running 🏃

### Settings

Credentials: You must config your Tello Api Key and Token into the file src/credentials.json

Board: You must config the board where you want to work into the file src/trello_config.json


### Running with Docker 🐳

Pull the development in your local and excecute:
```cmd
- sudo docker-compose up --build -d
```
```cmd
- sudo docker-compose up
```

### Running with virtual enviroment
In your terminal install VENV
```cmd
-   python3 -m venv venv
```
Activate VENV
```cmd
-   source venv/bin/activate
```
Install requirements
```cmd
-   pip install -r requirements.txt
```
Run PYTHON
```cmd
-   python main.py
```


### localhost/8000

```yaml
url: localhost/8000
```



## Testing 🧪

**Pytest**
In your terminal (venv must be activated)
```cmd
-   python -m pytest
```

**Endpoints:**
- GET → ***v1/status***
- POST → ***v1/solution***

### 1) GET → v1/status

**[RESPONSE]**
```yaml
url: <endpoint>/v1/status

{
    "message": Nan/SpaceX Challenge is running",
    "status_code": 200,
    "version": "1.0"
}
```

### 2) POST → v1/create-task
```yaml
params:
{
    "type": "issue",
    "title": "An Issue",
    "description": "I'm an issue"
}
```
**[REQUEST]**
```yaml
url: <endpoint>/v1/create-task

{
    "attachments": [],
    "badges": {
        "attachments": 0,
        "attachmentsByType": {
            "trello": {
                "board": 0,
                "card": 0
            }
        },
        "checkItems": 0,
        "checkItemsChecked": 0,
        "checkItemsEarliestDue": null,
        "comments": 0,
        "description": true,
        "due": null,
        "dueComplete": false,
        "fogbugz": "",
        "location": false,
        "start": null,
        "subscribed": false,
        "viewingMemberVoted": false,
        "votes": 0
    },
    "cardRole": null,
    "checkItemStates": [],
    "closed": false,
    "cover": {
        "brightness": "dark",
        "color": null,
        "idAttachment": null,
        "idPlugin": null,
        "idUploadedBackground": null,
        "size": "normal"
    },
    "dateLastActivity": "2023-11-25T14:51:43.886Z",
    "desc": "I'm an issue",
    "descData": {
        "emoji": {}
    },
    "due": null,
    "dueComplete": false,
    "dueReminder": null,
    "email": null,
    "id": "656209ff0a7c1328dfab8713",
    "idAttachmentCover": null,
    "idBoard": "655f5b5f410e3d5e3f04702a",
    "idChecklists": [],
    "idLabels": [],
    "idList": "655f5b5f410e3d5e3f047031",
    "idMembers": [],
    "idMembersVoted": [],
    "idShort": 103,
    "isTemplate": false,
    "labels": [],
    "limits": {},
    "manualCoverAttachment": false,
    "name": "An Issue",
    "pos": 16384,
    "shortLink": "2gV1oRse",
    "shortUrl": "https://trello.com/c/2gV1oRse",
    "start": null,
    "stickers": [],
    "subscribed": false,
    "url": "https://trello.com/c/2gV1oRse/103-an-issue"
}
```
