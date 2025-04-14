### prerequisits

start ollama with mistral(or any better model you got a performant system)

### Structure

-postgres db using pgadmin(optional) in a docker container
-n8n server in docker
-flask server for chat

### starting

```
docker-compose up (-d optional argument)
```

configure the webhook
start the venv

```
python app.py
```

### further development

need some tweaking for the prompt, maybe some parsers between chat and sql executer
