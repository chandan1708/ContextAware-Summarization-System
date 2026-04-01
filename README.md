# Context Aware Summarization System

This project implements a modular, end-to-end abstractive text summarization system using a fine-tuned PEGASUS model. The system is designed to handle long-form text and dialogues, producing context-aware summaries through a robust NLP pipeline.

## Features

- **Modular Pipeline**: A structured pipeline for data ingestion, preprocessing, model training, and evaluation.
- **Fine-tuned PEGASUS**: Utilizes a fine-tuned PEGASUS model for high-quality abstractive summarization.
- **FastAPI Service**: A production-ready API service for real-time summarization requests.
- **Docker Deployment**: Containerized application for consistent deployment across environments.
- **AWS Deployment**: Infrastructure and scripts for deploying the application on AWS.

## Project Structure

```
ContextAware-Summarization-System/
├── src/
│   ├── contextAwareSummarizationSystem/
│   │   ├── __init__.py
│   │   ├── components/
│   │   │   ├── __init__.py
│   │   │   ├── data_ingestion.py
│   │   │   ├── data_preprocessing.py
│   │   │   ├── model_training.py
│   │   │   ├── model_evaluation.py
│   │   │   └── summarization.py
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   └── common.py
│   │   ├── logging/
│   │   │   ├── __init__.py
│   │   │   └── logger.py
│   │   ├── config/
│   │   │   ├── __init__.py
│   │   │   └── configuration.py
│   │   ├── pipeline/
│   │   │   ├── __init__.py
│   │   │   └── training_pipeline.py
│   │   ├── entity/
│   │   │   ├── __init__.py
│   │   │   └── config_entity.py
│   │   └── constants/
│   │       ├── __init__.py
│   │       └── constants.py
├── config/
│   └── config.yaml
├── params.yaml
├── app.py
├── main.py
├── Dockerfile
├── requirements.txt
├── setup.py
└── research/
    └── trails.ipynb
```

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd ContextAware-Summarization-System
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Training the Model

To train the summarization model, run the main training script:

```bash
python main.py
```

This will execute the training pipeline, which includes:
1.  Data ingestion
2.  Preprocessing
3.  Model training
4.  Evaluation

### Running the API Service

To start the FastAPI service for real-time summarization:

```bash
uvicorn src.contextAwareSummarizationSystem.app:app --reload
```

The API will be available at `http://localhost:8000`.

### API Endpoints

-   **POST `/summarize`**: Summarize text.
    -   **Request Body**: `{"text": "Your long text here..."}`
    -   **Response**: `{"summary": "Generated summary..."}`

-   **GET `/health`**: Health check.
    -   **Response**: `{"status": "ok"}`

## Docker Deployment

To build and run the application using Docker:

1.  **Build the Docker image**:
    ```bash
    docker build -t summarization-app .
    ```

2.  **Run the container**:
    ```bash
    docker run -p 8000:8000 summarization-app
    ```

The application will be accessible at `http://localhost:8000`.

## AWS Deployment

To deploy this application on AWS, follow these steps:

1.  **Configure AWS Credentials**:
    ```bash
    aws configure
    ```

2.  **Build and push Docker image to ECR**:
    ```bash
    # Create ECR repository
    aws ecr create-repository --repository-name summarization-app
    
    # Authenticate Docker to ECR
    aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.<your-region>.amazonaws.com
    
    # Tag and push the image
    docker tag summarization-app:latest <your-account-id>.dkr.ecr.<your-region>.amazonaws.com/summarization-app:latest
    docker push <your-account-id>.dkr.ecr.<your-region>.amazonaws.com/summarization-app:latest
    ```

3.  **Deploy to AWS** (using ECS, EKS, or EC2):
    Refer to the deployment scripts in the `aws/` directory (if available) or use your preferred AWS deployment method.

## License

This project is licensed under the terms of the MIT license.
