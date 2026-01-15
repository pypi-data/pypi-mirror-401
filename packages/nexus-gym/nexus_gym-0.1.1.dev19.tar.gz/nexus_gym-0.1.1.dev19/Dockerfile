FROM python:3.11-slim

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -e .[sb3]
RUN pip install --no-cache-dir fastapi uvicorn websockets tensorboard tqdm rich wandb python-dotenv hydra-core

# Build the JS game simulation
RUN cd sim && npm install && npm run build
RUN mkdir -p src/nexus_env/static && cp -r sim/dist/* src/nexus_env/static/

# Hugging Face uses port 7860 by default
EXPOSE 7860

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:7860/ || exit 1

# Entrypoint for RL training
ENTRYPOINT ["python", "main_train.py"]
CMD ["env.theme=cyber_district", "algo=ppo_stable"]
