# Usa imagem base Python 3.13 slim
FROM python:3.13-slim

# Instala dependências do sistema necessárias para build de libs Python
RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# Instala o gerenciador UV
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos do projeto (pyproject.toml e o código)
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-cache

# Copia o restante do código
COPY . .

# Expõe a porta padrão
EXPOSE 8000

# Comando padrão para rodar o servidor Django
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
