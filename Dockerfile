FROM python:3.9.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y git \
    && git clone https://github.com/kameshcodes/chroma-detector.git . \
    && pip install --upgrade pip \
    && pip install seaborn scikit-learn streamlit

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "Scripts/streamlit_file.py", "--server.port=8501", "--server.address=0.0.0.0"]