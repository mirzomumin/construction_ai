# CONSTRUCTION AI

AI-Powered Construction Task Manager

## Set Up

1. Clone project repository

```shell
git clone https://github.com/mirzomumin/construction_ai.git
```

2. Move to project directory

```shell
cd construction_ai
```

3. Create a virtual environment depends on your OS

`Linux/MacOS:`
```shell
python3 -m venv venv
```

`Windows:`
```shell
python -m venv venv
```

4. Activate virtual environment depends on your OS

`Linux/MacOS:`
```shell
source venv/bin/activate
```

`Windows:`
```shell
venv\Scripts\activate
```

5. Install all project dependencies with command

```shell
pip install -r requirements.txt
```

6. Launch the app

```shell
fastapi dev app/main.py
```

## Endpoints

1. `POST /projects/` → Create a new construction project

Request
```shell
curl -X 'POST' \
  'http://127.0.0.1:8000/projects/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "project_name": "Restaurant",
  "location": "San-Francisco"
}'
```

Response
```shell
HTTP/1.1 200 OK
Date: Thu, 5 Mar 2025 12:36:30 GMT
Status: 200 OK
Connection: close
Content-Type: application/json

{
  "id": 1,
  "project_name": "Restaurant",
  "location": "San-Francisco",
  "status": "processing",
  "tasks": [
    {
      "name": "Secure Funding and Investment",
      "status": "pending"
    },
    {
      "name": "Find a Suitable Location in San Francisco",
      "status": "pending"
    },
    {
      "name": "Obtain Necessary Permits and Licenses",
      "status": "pending"
    },
    {
      "name": "Develop a Menu and Source Ingredients",
      "status": "pending"
    },
    {
      "name": "Hire and Train Staff",
      "status": "pending"
    }
  ]
}
```

2. `GET /projects/{project_id}` → Retrieve project details.

Request
```shell
curl -X 'GET' \
  'http://127.0.0.1:8000/projects/1' \
  -H 'accept: application/json'
```

Response
```shell
```shell
HTTP/1.1 200 OK
Date: Thu, 5 Mar 2025 12:36:30 GMT
Status: 200 OK
Connection: close
Content-Type: application/json

{
  "id": 1,
  "project_name": "Restaurant",
  "location": "San-Francisco",
  "status": "processing",
  "tasks": [
    {
      "name": "Secure Funding and Investment",
      "status": "pending"
    },
    {
      "name": "Find a Suitable Location in San Francisco",
      "status": "pending"
    },
    {
      "name": "Obtain Necessary Permits and Licenses",
      "status": "pending"
    },
    {
      "name": "Develop a Menu and Source Ingredients",
      "status": "pending"
    },
    {
      "name": "Hire and Train Staff",
      "status": "pending"
    }
  ]
}
```
```
