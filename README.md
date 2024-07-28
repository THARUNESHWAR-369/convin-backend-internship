# Convin Backend Intern Project (Daily Expense Sharing App)

## Prerequisites

- Python 3.11.7
- SQLite
- Docker (optional, if you prefer running the app in a container)
- Git

## Setup Instructions

### Clone the Repository

```bash
git https://github.com/THARUNESHWAR-369/convin-backend-internship.git
```
```bash
cd convin-backend-internship
```

### Install Dependencies

#### Windows & Linux
- Open Terminal / Command Prompt / Powershell.
- Navigate to the project directory.
- Install Requirements:
```bash
pip install requirements.txt
```

## SecretKet Setup
- Copy .env.example to .env file
- Open .env & update `SECRET_KEY`

```env
SECRET_KEY="<your key>"
```

## Running the Application

### Windows & Linux
```bash
uvicorn app.main:app --reload
```

### Docker Setup

#### Build the Docker Image
```bash
docker build -t convin-backend-internship.
```

#### Run the Docker Container
```bash
docker run -d --name convin-backend-intern -p 8000:8000 convin-backend-intern-project
```

### Open your browser and navigate to http://127.0.0.1:8000/docs#/ to see the application running.

## Running Tests

### Run Tests
```bash
pytest tests/
```

### Database Architecture Diagram
![db_arch](https://github.com/user-attachments/assets/2267b083-cf54-4076-992f-da30eeb1b9d0)

### Sample Screenshots
![s1](https://github.com/user-attachments/assets/de15a6ba-0ea7-4e2d-b26e-44dbd55a8067)

> #### Refer Sample Outputs directory for balance sheet file
