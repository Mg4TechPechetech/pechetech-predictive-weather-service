# PecheTech Predictive Weather Service

## 📝 Overview
This Python-based service leverages Machine Learning (specifically LSTM models) to predict weather patterns. These predictions are integrated within the PecheTech ecosystem to optimize operations dependent on environmental conditions.

## 🛠 Tech Stack
- **Language:** Python
- **Machine Learning:** PyTorch / TensorFlow (LSTM modeling)
- **Containerization:** Docker

## 📂 Project Structure
- `/src`: Source code
  - `/api`: REST API endpoints for fetching predictions
  - `/ml`: Machine learning models and inference logic
  - `/data_ingestion`: Scripts to ingest and clean weather data
  - `/core`: General configurations
- `/notebooks`: Jupyter notebooks for data preparation and LSTM model training
- `/tests`: Unit tests
- `/docker`: Docker and Compose files
- `/docs`: Documentation detailing the LSTM model architecture

## ⚙️ Prerequisites
- Python 3.9+
- Docker & Docker Compose

## 🚀 Setup & Installation
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🏃‍♂️ Running the Application
**Local API:**
```bash
python src/main.py
```

**Using Docker:**
```bash
docker-compose -f docker/docker-compose.yml up --build
```

## 🧪 Testing
```bash
pytest tests/
```
