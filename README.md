# Microservices-Ecosystem-Demo

## О проекте (RU)

Этот проект - моя попытка реализовать концепцию распределённой системы и бросить себе вызов, создав небольшую экосистему микросервисов (песочницу). Здесь реализованы принципы модульности: нет жёстких зависимостей, каждый сервис работает в своей среде и знает только о себе и о том, куда отправлять сообщения. Это демонстрационный проект, в котором не всё задуманное реализовано, но основной функционал работает: сервисы можно регистрировать и интегрировать в экосистему через сервис **Cascade** - он выступает "лицом" всей системы для внешнего мира.

**Ключевые особенности:**
- Модульная архитектура: каждый сервис изолирован и независим.
- Взаимодействие через брокер сообщений (RabbitMQ).
- Регистрация и интеграция сервисов через центральный сервис Cascade.
- Использование FastAPI, SQLAlchemy, Redis, RabbitMQ.
- Docker-окружение для быстрого запуска.

**Структура репозитория:**
- `Cascade/` - центральный сервис для регистрации и маршрутизации микросервисов.
- `Importer/` - сервис-импортёр, помогает интегрировать новые сервисы.
- `Microservice/` - пример пользовательского микросервиса (например, сервис пользователей).
- `Database/` - сервис для работы с базой данных.
- `Cache/` - сервис кэширования (Redis).
- `docker-compose.yaml` - оркестрация всех сервисов.

**Запуск:**
```sh
docker-compose up --build
```


## About the Project (EN)

This project is my attempt to implement the concept of a distributed system and challenge myself by building a small microservices ecosystem (sandbox). The project is based on modularity: there are no strict dependencies, each service runs in its own environment and only knows about itself and where to send its messages. It's a demonstration project - not everything planned is implemented, but the core functionality works: you can register and integrate services into the ecosystem via the Cascade service, which acts as the "face" of the system to the outside world.

**Key Features:**
- Modular architecture: each service is isolated and independent.
- Communication via message broker (RabbitMQ).
- Service registration and integration through the central Cascade service.
- Uses FastAPI, SQLAlchemy, Redis, RabbitMQ.
- Docker environment for easy startup.
- Repository Structure:

- `Cascade/` - central service for microservice registration and routing.
- `Importer/` - importer service to help integrate new services.
- `Microservice/` - example user microservice (e.g., user service).
- `Database/` - database service.
- `Cache/` - caching service (Redis).
- `docker-compose.yaml` - orchestration for all services.

**How to run:**
```sh
docker-compose up --build
```
