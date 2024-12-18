# SkadeService

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Swagger](https://img.shields.io/badge/Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)
![Azure](https://img.shields.io/badge/Microsoft%20Azure-0078D4?style=for-the-badge&logo=microsoft-azure&logoColor=white)

---

## Introduktion
`skadeService` er en API-gateway, der håndterer skaderapporter og dataudveksling mellem forskellige tjenester. Applikationen er bygget ved hjælp af Flask og dokumenteret med Swagger (Flasgger).

## Indholdsfortegnelse

1. [Funktioner](#funktioner)
2. [Arkitektur](#arkitektur)
3. [Forudsætninger](#forudsætninger)
4. [Opsætning og installation](#opsætning-og-installation)
5. [Filstruktur](#filstruktur)
6. [General information](#general-information)
7. [JWT Autentificering](#JWT-autentificering)
8. [Endpoints](#endpoints)
9. [Swagger](#swagger)
10. [Kontakt](#kontakt)

## Funktionaliteter
- Hent alle skaderapporter
- Tilføj en ny skaderapport
- Slet en skaderapport
- Send data til en anden tjeneste
- Hent kundedata og beregn skader
- Behandl skadedata fra Lejeaftale Service

## Arkitektur
Applikationen er opdelt i forskellige moduler:
- `app.py`: Hovedfilen, der indeholder API-endepunkterne og konfigurationen af Flask og Swagger.
- `service/skader.py`: Indeholder funktioner til at hente, tilføje og slette skaderapporter.
- `service/connections.py`: Indeholder funktioner til at hente data fra aftaletjenesten, beregne priser og sende skaderapporter.

## Opsætning og Installation
Følg disse trin for at installere og køre applikationen:

1. Klon repository:
   ```bash
   git clone https://github.com/dit-repo/skadeService.git
   cd skadeService
2. Opret of aktiver virtuelt miljø:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # På macOS/Linux
3. Installer dependencies:
   ```bash
   pip install -r requirements.txt
4. Kør applikationen
   ```bash
   python3 app.py
## Filstruktur
```bash
skadeService/
│
├── [app.py](http://_vscodecontentref_/0)
├── [requirements.txt](http://_vscodecontentref_/1)
├── service/
│   ├── __init__.py
│   ├── skader.py
│   └── connections.py
├── swagger/
│   ├── config.py
│   ├── home.yaml
│   ├── skadeRapporter.yaml
│   ├── tilføjSkadeRapporter.yaml
│   ├── sletSkadeRapporter.yaml
│   ├── sendData.yaml
│   ├── sendKundeData.yaml
│   └── processDamageData.yaml
├── database/
│   ├── import_json.py
│   ├── skader.db
```

## Endpoints

### Home
URL: /
Metode: GET
Beskrivelse: Hent API-dokumentation
Output:
  ```json
  {
    "service": "API Gateway",
    "available_endpoints": [
      {
        "path": "/skadeRapporter",
        "method": "GET",
        "description": "Fetch all damage reports"
      },
      {
        "path": "/skadeRapporter",
        "method": "POST",
        "description": "Add a new damage report"
      },
      {
        "path": "/skadeRapporter/<int:reportID>",
        "method": "DELETE",
        "description": "Delete a damage report by ID"
      },
      {
        "path": "/send-data",
        "method": "GET",
        "description": "Send data to another service"
      },
      {
        "path": "/send-kunde-data/<int:lejeaftaleID>",
        "method": "GET",
        "description": "Send request to get customer data and calculate damages"
      },
      {
        "path": "/process-damage-data",
        "method": "POST",
        "description": "Process damage data from Lejeaftale Service"
      }
    ]
  }
  ```
### Hent alle skaderapporter
URL: /skadeRapporter
Metode: GET
Beskrivelse: Hent alle skaderapporter
Output:
  ```json
  [
    {
      "id": 1,
      "description": "Broken window",
      "date": "2023-10-12",
      "status": "Pending"
    },
  ]
```
### Tilføj en ny skaderapport
URL: /skadeRapporter
Metode: POST
Beskrivelse: Tilføj en ny skaderapport
Input:
  ```json
  {
    "description": "Broken window",
    "date": "2023-10-12",
    "status": "Pending"
  }
```
Output:
  ```json
  {
    "id": 1,
    "description": "Broken window",
    "date": "2023-10-12",
    "status": "Pending"
  }
```
Fejlbesked:
400
  ```json
  {
    "error": "Missing required fields"
  }
```
### Slet en skaderapport
URL: /skadeRapporter/<int:reportID>
Metode: DELETE
Beskrivelse: Slet en skaderapport
Output:
  ```json
  {
    "message": "Damage report deleted successfully"
  }
```
Fejlbeskeder:
404
  ```json
  {
  "error": "Damage report not found"
  }
```
### Send data
URL: /send-data
Metode: GET
Beskrivelse: Send data til en anden tjeneste
Output:
  ```json
  {
  "message": "Data sent successfully"
  }
```
Fejlbeskeder:
500
  ```json
  {
    "error": "Internal server error"
  }
```
### Hent kundedata og beregn skader
URL: /send-kunde-data/<int:lejeaftaleID>
Metode: GET
Beskrivelse: Hent kundedata og beregn skader baseret på lejeaftaleID
Output:
  ```json
  {
    "customerData": {
      "name": "John Doe",
      "email": "john.doe@example.com"
    },
    "damages": [
      {
        "id": 1,
        "description": "Broken window",
        "cost": 150.0
      },
    ]
  }
```
Fejlbeskeder:
404
  ```json
  {
    "error": "Rental agreement not found"
  }
```
### Behandl skadedata
URL: /process-damage-data
Metode: POST
Beskrivelse: Behandl skadedata fra Lejeaftale Service
Input:
  ```json
  {
    "data": "Damage data in JSON format"
  }
```
Output:
  ```json
  {
    "message": "Damage data processed successfully"
  }
```
Fejlbeskeder:
400
  ```json
  {
    "error": "Invalid input data"
  }
```
500
  ```json
  {
    "error": "Internal server error"
  }
```
Se Swagger-dokumentationen for en komplet liste over endpoints.

Ved at følge denne README-fil kan du nemt installere, køre og forstå skadeService-applikationen. Hvis du har spørgsmål eller problemer, er du velkommen til at oprette en issue i repositoriet.

---

## Swagger Dokumentation
Swagger-dokumentation er tilgængelig for alle endpoints. Når servicen kører kan man få adgang til Swagger UI på:
`http://localhost:5002/apidocs`

---


### Kontakt

Hvis du har nogen spørgsmål eller oplever problemer, så er du velkommen til at kontakt udviklerteamet: Natazja, Sofie og Viktor.

