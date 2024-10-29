FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000    
EXPOSE 8501    
CMD uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.port 8501 --server.address 0.0.0.0