# ⚓ Shipyard

**Shipyard** is a production-shaped local development runtime for Laravel projects.

It provides a shared Docker-based environment that mirrors modern infrastructure while remaining simple to operate from the command line.

Shipyard manages:

- A shared local runtime (Traefik, MySQL, Redis, Mailpit)
- Per-project service orchestration
- Automatic TLS for `.test` domains
- Container lifecycle
- Shell access into running services

The result is a local environment that feels much closer to **real production architecture** than typical single-project stacks.

---

## Quick Examples

Adopt an existing Laravel project:

```bash
shipyard adopt ~/code/my-laravel-project
```

Start the shared runtime:

```bash
shipyard up
```

Start a specific project:

```bash
shipyard up my-laravel-project
```

Attach to the application container:

```bash
shipyard attach my-laravel-project
```

Check runtime status:

```bash
shipyard list
```

Stop everything:

```bash
shipyard down
```

---

## Why Shipyard?

Many Laravel development setups fall into one of two categories.

### Per-project Docker environments

Tools like Sail or custom Compose setups run a **full stack per project**, which often leads to:

- multiple MySQL instances
- duplicated infrastructure
- port conflicts
- inconsistent environments

### Host-based tooling

Solutions like Valet or Herd run services directly on the host, which is convenient but diverges from production infrastructure.

---

## Shipyard's approach

Shipyard separates **shared infrastructure** from **application services**.

A single shared runtime provides:

```
Traefik
MySQL
Redis
Mailpit
```

Each Laravel project runs only its own services:

```
PHP
Nginx
Node
Queue workers
Scheduler
```

Everything runs in Docker and is routed through Traefik with automatic TLS.

This creates a predictable, scalable development environment without unnecessary duplication.

---

## Features

### Shared runtime environment

Shipyard runs a single shared infrastructure stack.

Services include:

- Traefik reverse proxy
- MySQL 8
- Redis
- Mailpit

All projects connect to this environment automatically.

---

### Automatic `.test` domains with TLS

Each project is assigned a domain such as:

```
https://evolutioncrm.test
https://endeavour-production.test
```

Certificates are generated using **mkcert** and managed by Shipyard.

---

### Project adoption

Existing Laravel repositories can be adopted into Shipyard:

```bash
shipyard adopt /path/to/project
```

Shipyard generates the runtime configuration required to run the application.

---

### Docker-based architecture

All services run inside containers.

Benefits include:

- consistent environments
- predictable networking
- isolation between projects
- easy cleanup

---

### Simple CLI workflow

Shipyard keeps the command surface small and focused.

Core commands:

```
shipyard init
shipyard adopt <path>
shipyard up
shipyard up <project>
shipyard attach <project>
shipyard list
shipyard down
```

---

## Installation

Shipyard is installed as a global CLI using **pipx**.

### Install pipx

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

Restart your shell afterwards.

---

### Install Shipyard

From the repository:

```bash
pipx install -e .
```

This installs the `shipyard` command globally without requiring a virtual environment.

---

## Initialising the runtime

Before adopting projects, initialise the Shipyard runtime:

```bash
shipyard init
```

This will:

- create the Shipyard runtime directory
- install Traefik configuration
- configure certificates
- prepare shared services

---

## Running projects

Start the shared runtime:

```bash
shipyard up
```

Start a project:

```bash
shipyard up <project>
```

Shipyard automatically ensures the core runtime is running.

---

## Accessing containers

Attach to the application container:

```bash
shipyard attach <project>
```

Attach to a specific service:

```bash
shipyard attach <project> nginx
shipyard attach <project> node
shipyard attach <project> queue
```

---

## Runtime status

Check the status of the environment:

```bash
shipyard list
```

Example output:

```
core: up
projects:
  - endeavour-production: up
  - evolutioncrm: down
```

---

## Architecture

Shipyard separates infrastructure from project services.

### Core runtime

Located at:

```
~/shipyard
```

Contains:

```
docker-compose.yml
traefik/
certs/
projects/
```

Services:

```
Traefik
MySQL
Redis
Mailpit
```

---

### Project runtime

Each adopted project gets its own runtime directory:

```
~/shipyard/projects/<project>
```

Containing:

```
docker-compose.generated.yml
shipyard.yml
docker/
nginx/
support/
```

---

## Custom Dockerfiles

Shipyard supports both:

- Shipyard-managed Dockerfiles
- custom Dockerfiles from the project repository

Configuration is stored in:

```
shipyard.yml
```

Example:

```yaml
dockerfiles:
  mode: custom
  php: /path/to/project/.docker/php/Dockerfile-dev
  nginx: /path/to/project/.docker/nginx/Dockerfile-dev
  node: /path/to/project/.docker/node/Dockerfile-dev
```

---

## Goals

Shipyard aims to provide:

- a **production-shaped development environment**
- **minimal developer friction**
- **repeatable project setups**
- a **simple CLI interface**

It is designed specifically for **Laravel development workflows**.

---

## WIPs

* [ ] Allow custom Dockerfiles
* [ ] Make docker-compose.generated.yml use dynamic build context and Dockerfiles
* [ ] Regenerate published files after a config change to use custom Dockerfiles 

---

## Roadmap & Ideas

* [ ] .env file change requirements - i.e. database host and credentials.
* [ ] Command to tail and follow laravel.log (also support laravel-yyyy-mm-dd.log for today)
* [ ] Healthcheck
* [ ] Support for generating multiple queue workers - define in config, then regenerate?
* [ ] beanstalkd and Beanstalk Console for queue management.
* [ ] Write a great README to sell the idea

---

# License
MIT Licence

Copyright 2026 Dan Stuchbury

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
