# PRUEBA_TECNICA_BACKEND

Este proyecto sirve como una evaluación técnica para un sistema backend, construido con Python 3.x, FastAPI y SQLAlchemy, que demuestra una arquitectura robusta basada en la Arquitectura Hexagonal, CQRS (Command Query Responsibility Segregation) y Bundle-Contexts. El objetivo es establecer una base sólida, mantenible y escalable para una aplicación backend.

## Tabla de Contenidos

- [PRUEBA_TECNICA_BACKEND](#prueba_tecnica_backend)
  - [Tabla de Contenidos](#tabla-de-contenidos)
  - [Objetivo del Proyecto](#objetivo-del-proyecto)
  - [Arquitectura](#arquitectura)
    - [Arquitectura Hexagonal](#arquitectura-hexagonal)
    - [CQRS (Command Query Responsibility Segregation)](#cqrs-command-query-responsibility-segregation)
    - [Bundle-Contexts](#bundle-contexts)
  - [Estructura de Carpetas](#estructura-de-carpetas)
  - [Tecnologías Utilizadas](#tecnologías-utilizadas)
  - [Características Implementadas](#características-implementadas)
  - [Primeros Pasos](#primeros-pasos)
    - [Prerrequisitos](#prerrequisitos)
    - [Ejecutar con Docker (Recomendado)](#ejecutar-con-docker-recomendado)
    - [Ejecutar Localmente](#ejecutar-localmente)
  - [Ejecutar Pruebas](#ejecutar-pruebas)
  - [Decisiones Arquitectónicas](#decisiones-arquitectónicas)
  - [Puntos de Evaluación](#puntos-de-evaluación)

## Objetivo del Proyecto

[cite_start]El objetivo principal de este proyecto es crear una base sólida para un proyecto backend que implemente: [cite: 3, 4]

- [cite_start]**Arquitectura Hexagonal**: Para garantizar la independencia del dominio. [cite: 5, 6]
- [cite_start]**CQRS**: Para operaciones diferenciadas de lectura y escritura. [cite: 7]
- [cite_start]**Bundle-contexts**: Como estrategia para agrupar lógicamente los componentes, facilitando la escalabilidad y el manejo modular del proyecto. [cite: 9]

[cite_start]Queremos evaluar tu capacidad para estructurar, configurar y pensar en un diseño robusto que permita crecer el proyecto sin comprometer la mantenibilidad. [cite: 10]

## Arquitectura

### Arquitectura Hexagonal

Este proyecto se adhiere al principio de la Arquitectura Hexagonal (también conocida como Puertos y Adaptadores). [cite_start]La lógica central del dominio está aislada de las preocupaciones externas. [cite: 16, 17]

- [cite_start]**Puertos**: Definen las interfaces que el dominio utiliza para interactuar con el mundo exterior. [cite: 18]
- [cite_start]**Adaptadores**: Implementan estos puertos, conectando el dominio a tecnologías específicas o sistemas externos (por ejemplo, bases de datos, frameworks web, colas de mensajes). [cite: 18, 19, 20]

[cite_start]Esto asegura que la lógica de negocio permanezca independiente y testeable, permitiendo un fácil intercambio de tecnologías externas sin afectar el núcleo. [cite: 17]

### CQRS (Command Query Responsibility Segregation)

[cite_start]CQRS se implementa para separar estrictamente las responsabilidades de comandos (operaciones de escritura) y consultas (operaciones de lectura). [cite: 21, 22, 23]

- **Comandos**: Operaciones que cambian el estado del sistema (por ejemplo, crear un usuario). [cite_start]Estos deben procesarse mediante RabbitMQ (con al menos un consumidor implementado). [cite: 24]
- **Consultas**: Operaciones que recuperan datos sin cambiar el estado del sistema (por ejemplo, obtener información de un usuario). [cite_start]Estas deben ejecutarse directamente contra el modelo de lectura. [cite: 25]

Esta separación permite la escalabilidad y optimización independiente de las cargas de trabajo de lectura y escritura.

### Bundle-Contexts

El proyecto está estructurado alrededor de "bundle-contexts", que son agrupaciones lógicas de componentes relacionados. [cite_start]Esto promueve la modularidad, la reutilización y una escalabilidad más sencilla. [cite: 9, 33]

[cite_start]Actualmente, se definen al menos dos contexts lógicos: `users` y `auth`. [cite: 27]

[cite_start]Cada context debe incluir: [cite: 28]

- [cite_start]`domain`: Lógica de negocio central y entidades específicas del contexto. [cite: 29]
- [cite_start]`application`: Casos de uso y servicios de aplicación que orquestan las interacciones del dominio. [cite: 30]
- [cite_start]`infrastructure`: Adaptadores para preocupaciones externas (por ejemplo, repositorios de bases de datos, APIs externas). [cite: 32]

## Estructura de Carpetas

.
├── PRUEBA*TECNICA_BACKEND_FUO
│ ├── .pytest_cache
│ ├── alembic
│ ├── app
│ │ ├── pycache*
│ │ ├── config
│ │ ├── contexts
│ │ │ ├── pycache*
│ │ │ ├── auth
│ │ │ │ ├── pycache*
│ │ │ │ ├── application
│ │ │ │ ├── domain
│ │ │ │ ├── infrastructure
│ │ │ │ └── init.py
│ │ │ ├── users
│ │ │ │ ├── pycache*
│ │ │ │ ├── application
│ │ │ │ ├── domain
│ │ │ │ ├── infrastructure
│ │ │ │ └── init.py
│ │ │ └── shared
│ │ │ ├── pycache*
│ │ │ ├── application
│ │ │ ├── domain
│ │ │ ├── infrastructure
│ │ │ └── init.py
│ │ ├── init.py
│ │ └── main.py
│ ├── docker
│ │ ├── Dockerfile
│ │ ├── start-app.sh
│ │ └── wait-for-sh.sh
│ ├── migrations
│ ├── tests
│ ├── .env
│ ├── .gitignore
│ ├── alembic.ini
│ ├── docker-compose.yml
│ ├── pytest.ini
│ └── README.md
│ └── requirements.txt

- `app/`: Contiene el código principal de la aplicación.
  - `app/config/`: Archivos de configuración.
  - `app/contexts/`: Aloja los bundle-contexts (`auth`, `users`, `shared`). Cada contexto sigue el patrón de Arquitectura Hexagonal con capas de `application`, `domain` e `infrastructure`.
  - `app/main.py`: El punto de entrada para la aplicación FastAPI.
- `docker/`: Archivos relacionados con Docker, incluyendo `Dockerfile`, `start-app.sh` y `wait-for.sh`.
- `migrations/`: Scripts de migración de base de datos (gestionados por Alembic).
- `tests/`: Pruebas unitarias y de integración para la aplicación.
- `.env`: Variables de entorno (debe crearse a partir de `.env.example` si se proporciona).
- `docker-compose.yml`: Define los servicios de la aplicación Docker multicontenedor (por ejemplo, aplicación FastAPI, RabbitMQ, base de datos).
- `requirements.txt`: Dependencias de Python.

## [cite_start]Tecnologías Utilizadas [cite: 12]

- [cite_start]**Python**: 3.x [cite: 13]
- [cite_start]**FastAPI**: Como framework web. [cite: 14]
- [cite_start]**SQLAlchemy**: Para manejo de datos. [cite: 15]
- [cite_start]**RabbitMQ**: Agente de mensajes para procesamiento asíncrono de comandos. [cite: 24]
- [cite_start]**Docker**: Para la contenerización y consistencia del entorno. [cite: 42, 43, 44]
- **Pytest**: Framework de pruebas.

## Características Implementadas

- [cite_start]**Gestión Básica de Usuarios**: Se implementa una gestión básica de usuarios. [cite: 35]
  - [cite_start]**Comando**: Crear un usuario con nombre, correo y contraseña (almacenada de forma segura). [cite: 36]
  - [cite_start]**Consulta**: Obtener información de un usuario por su ID. [cite: 37]
- [cite_start]**CQRS**: Separación estricta entre comandos y consultas, con comandos procesados mediante RabbitMQ y consultas ejecutadas directamente contra el modelo de lectura. [cite: 23, 24, 25]
- [cite_start]**Inyección de Dependencias**: Se agrega soporte para inyección de dependencias en todos los componentes, permitiendo una inicialización y configuración dinámica con bajo acoplamiento. [cite: 68, 69]

## Primeros Pasos

Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y prueba.

### Prerrequisitos

- Docker y Docker Compose (recomendado para una configuración sencilla)
- Python 3.x (si se ejecuta localmente sin Docker)
- Poetry (si se utiliza para la gestión de dependencias - no explícito en `requirements.txt` pero común en proyectos Python)

### Ejecutar con Docker (Recomendado)

La forma más sencilla de ejecutar el proyecto es usando Docker Compose. [cite_start]Esto configurará la aplicación FastAPI, RabbitMQ y la base de datos. [cite: 44]

1.  **Clonar el repositorio:**

    ```bash
    git clone [https://github.com/enriqueeee10/prueba_tecnica_backend](https://github.com/enriqueeee10/prueba_tecnica_backend)
    cd prueba_tecnica_backend
    ```

2.  **Crear archivo `.env`:**
    Crea un archivo `.env` en el directorio raíz, copiando el contenido de un `.env.example` si se proporciona, o define las variables de entorno necesarias como cadenas de conexión a la base de datos, credenciales de RabbitMQ, etc.

3.  **Construir y ejecutar los servicios:**

    ```bash
    docker-compose up --build
    ```

    Este comando construirá las imágenes de Docker e iniciará todos los servicios definidos en `docker-compose.yml`.

4.  **Acceder a la documentación de la API:**
    Una vez que los servicios estén activos, puedes acceder a la documentación interactiva de la API de FastAPI (Swagger UI) en `http://localhost:8000/docs` (o el puerto configurado).

### Ejecutar Localmente

Si prefieres ejecutar la aplicación directamente en tu máquina sin Docker:

1.  **Clonar el repositorio:**

    ```bash
    git clone [https://github.com/enriqueeee10/prueba_tecnica_backend](https://github.com/enriqueeee10/prueba_tecnica_backend)
    cd prueba_tecnica_backend
    ```

2.  **Crear un entorno virtual y activarlo:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3.  **Instalar dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar variables de entorno:**
    Crea un archivo `.env` en el directorio raíz y configura las variables de entorno necesarias (por ejemplo, URL de la base de datos, cadena de conexión a RabbitMQ).

5.  **Ejecutar migraciones de base de datos (si aplica):**

    ```bash
    alembic upgrade head
    ```

6.  **Iniciar la aplicación FastAPI:**
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```
    También necesitarás iniciar manualmente una instancia de RabbitMQ si estás ejecutando localmente y requieres su funcionalidad.

## Ejecutar Pruebas

[cite_start]Las pruebas unitarias son cruciales para asegurar la calidad y corrección del código. [cite: 39, 40]

1.  **Asegúrate de que las dependencias estén instaladas.**
2.  **Ejecutar pruebas usando pytest:**
    ```bash
    pytest
    ```
    [cite_start]Las pruebas buscan cubrir al menos el 80% del código de la capa de dominio. [cite: 41]

## [cite_start]Decisiones Arquitectónicas [cite: 49]

- **Independencia del Dominio**: La lógica de negocio central en las capas `domain` de cada contexto está diseñada para ser completamente independiente de frameworks externos o bases de datos. [cite_start]Esto se logra mediante el uso de interfaces (puertos) y sus implementaciones (adaptadores) en la capa de `infrastructure`. [cite: 17]
- [cite_start]**Clara Separación de Responsabilidades**: Cada capa (dominio, aplicación, infraestructura) y cada contexto (auth, users, shared) tiene una responsabilidad bien definida, minimizando el acoplamiento y maximizando la cohesión. [cite: 57, 58]
- [cite_start]**Procesamiento Asíncrono de Comandos**: Los comandos se manejan a través de RabbitMQ para desacoplar la solicitud del procesamiento real, mejorando la capacidad de respuesta y permitiendo una mejor escalabilidad para las operaciones de escritura. [cite: 24, 60]
- [cite_start]**Escalabilidad Modular**: El enfoque de bundle-contexts permite una fácil adición de nuevas funcionalidades (nuevos contextos) sin afectar significativamente el código existente, promoviendo la escalabilidad horizontal. [cite: 33, 34, 61, 62]
- [cite_start]**Testabilidad**: La arquitectura facilita pruebas unitarias exhaustivas, especialmente para la lógica del dominio, debido a su aislamiento. [cite: 40, 41, 63, 64, 65]
- [cite_start]**Inyección de Dependencias**: Utilizada para gestionar las dependencias de los componentes, haciendo el sistema más flexible, testeable y mantenible al permitir que las dependencias sean configuradas y proporcionadas en tiempo de ejecución. [cite: 68, 69]

## [cite_start]Puntos de Evaluación [cite: 50]

Este proyecto aborda los siguientes criterios clave de evaluación:

1.  [cite_start]**Diseño Modular**: Demostrado a través del uso correcto de la arquitectura hexagonal y la implementación efectiva de bundle-contexts. [cite: 51, 53, 54, 66, 67]
2.  [cite_start]**Separación de Responsabilidades**: Las capas están claramente definidas y respetan su propósito. [cite: 55, 57, 58]
3.  [cite_start]**CQRS**: Logrado a través de una separación adecuada entre lectura y escritura y el uso efectivo de RabbitMQ. [cite: 56, 59, 60]
4.  [cite_start]**Escalabilidad**: La estructura del código permite añadir nuevos contexts sin dificultades. [cite: 61, 62]
5.  [cite_start]**Pruebas**: Incluye pruebas unitarias para los casos de uso, asegurando al menos el 80% de cobertura del código de la capa de dominio. [cite: 39, 40, 41, 63, 64, 65]
6.  [cite_start]**Bundle-contexts**: Implementación clara y funcional de los contexts. [cite: 66, 67]
7.  [cite_start]**Inyección de Dependencias**: Soporte para inyección de dependencias en todos los componentes, permitiendo una inicialización y configuración dinámica con bajo acoplamiento. [cite: 68, 69]
