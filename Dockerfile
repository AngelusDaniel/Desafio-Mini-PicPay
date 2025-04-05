# Use uma imagem base do Python
FROM python:3.12-slim

# Defina o diretório de trabalho no container
WORKDIR /app

# Copie o requirements.txt para dentro do container
COPY requirements.txt .

# Instale as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código do seu projeto para dentro do container
COPY . .

# Exponha a porta que o servidor Django vai rodar (por padrão, Django usa a porta 8000)
EXPOSE 8000

# Defina o comando para rodar o servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

RUN pip install --upgrade pip
