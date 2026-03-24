# CSF Rating Tenis

Backend para gestión de jugadores y cálculo de ranking dinámico de tenis, utilizando un sistema de rating competitivo inspirado en Elo, desarrollado como proyecto con enfoque DevOps end-to-end.

---

## Run locally

docker compose up --build

Access:
- API → http://localhost:8000/docs  
- pgAdmin → http://localhost:5050  

---

## Stack

- Backend: FastAPI (Python)
- Database: PostgreSQL
- Containerization: Docker & Docker Compose
- CI/CD: GitHub Actions
- Registry: Docker Hub
- Orchestration (conceptual): Kubernetes
- Testing: pytest

---

## Qué hace la app

- Crear jugadores
- Asignar rating inicial
- Registrar resultados de partidos
- Actualizar automáticamente el rating
- Consultar ranking
- Documentación automática en `/docs`

---

## Estructura del proyecto

- `app/` → lógica de la API  
- `tests/` → tests  
- `k8s/` → manifests de Kubernetes  

---

## Entorno local

El proyecto corre con múltiples servicios usando Docker Compose:

- API (FastAPI)
- PostgreSQL
- pgAdmin

Esto simula un entorno real con servicios desacoplados.

---

## CI/CD

Cada push ejecuta automáticamente:

- instalación de dependencias  
- ejecución de tests  
- validación de la app  
- build de imagen Docker  
- push a Docker Hub  

Imagen disponible en:

`tomas1aws/csf-rating-tenis`

---

## Kubernetes

Se incluyen manifests básicos en `/k8s`:

- Deployments (app + db)  
- Services  
- Persistent Volume  
- Secrets  

Implementa los conceptos fundamentales de orquestación de contenedores.

---

## Testing

Tests simples enfocados en la lógica de rating:

- validación de cálculo  
- comportamiento ante distintos resultados  

---

## Enfoque del proyecto

Este proyecto no es solo una API.

Simula un flujo real de desarrollo:

Code → GitHub → CI → Docker → Docker Hub → Kubernetes

Objetivo: practicar integración entre desarrollo y DevOps.

---

## Próximas mejoras

- Deploy en cloud (AWS / GCP)
- Terraform para infraestructura
- Autenticación
- Mejorar lógica de ranking
- Versionado de imágenes

---

## Autor

Tomás Perticaro