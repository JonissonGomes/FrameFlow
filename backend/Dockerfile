# backend/Dockerfile

FROM python:3.9

# Instala dependências do sistema necessárias para o OpenCV
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY requirements.txt .

# Copia o arquivo .env para o container
COPY .env .env

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código para o container
COPY . .

# Expõe a porta da API
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "run.py"]
