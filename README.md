# ⚓ Shipyard

![version](https://img.shields.io/badge/version-1.0-blue)
![platform](https://img.shields.io/badge/platform-Linux%20%7C%20WSL2-blue)
![docker](https://img.shields.io/badge/docker-required-2496ED?logo=docker)
![bash](https://img.shields.io/badge/shell-bash-4EAA25?logo=gnubash)
![status](https://img.shields.io/badge/status-internal%20tool-purple)

**Shipyard** is a lightweight CLI for managing local Docker development stacks.

It provides a single command — `dev` — to start projects, attach to containers, view logs, and manage your development environment.

---

## Quick Example

```bash
dev up
dev up api-gateway

dev attach api-gateway
dev logs web api-gateway

dev list
dev down
```

---

## What Shipyard Solves

Managing multiple Docker Compose projects can become repetitive and inconsistent.

Shipyard provides a simple, consistent interface for:

- Starting project stacks
- Attaching to containers
- Viewing logs
- Restarting services
- Checking environment status
- Diagnosing setup issues

All from a single command.

---

## CLI Philosophy

Shipyard focuses on:

- **Consistency across projects**
- **Minimal commands**
- **Fast developer workflows**
- **Zero complexity**

Most developers only need to remember:

```
dev up
dev attach
dev logs
dev list
dev down
```

---

# Installation

Clone the repository and run the install script.

```bash
git clone <repo-url> 
cd shipyard
./install.sh
source ~/.bashrc
```

The installer will:

- Install **yq** if it is not already installed
- Add the Shipyard `bin` folder to your `$PATH`
- Make the `dev` command available everywhere

---

# Configuration

Edit the project configuration file:

```
config/projects.yml
```

Example:

```yaml
master:
  path: ~/code/php/phpdev
  composeFileName: docker-compose.yml

projects:
  - name: api-gateway
    path: ~/code/php/api-gateway
    composeFileName: docker-compose-dev-wsl.yml
    appContainer: api-fpm
    webContainer: api-nginx

  - name: status-notification-service
    path: ~/code/php/status-notification-service
    composeFileName: docker-compose-dev-wsl.yml
    appContainer: sns-fpm
    webContainer: sns-nginx
```

Each project requires:

| Field | Description |
|-----|-----|
| `name` | Name used in CLI commands |
| `path` | Folder containing the docker compose file |
| `composeFileName` | Docker compose file name |
| `appContainer` | PHP / application container name |
| `webContainer` | Web server container name |

---

# Commands

## Start master stack

```bash
dev up
```

---

## Start a project

```bash
dev up api-gateway
```

---

## Stop everything

Stops:

- master compose stack
- all configured projects

```bash
dev down
```

---

## Stop a specific project

```bash
dev down api-gateway
```

---

## Restart a project

```bash
dev restart api-gateway
```

---

# Container Access

Shipyard can automatically attach to containers.

If the project is **not running**, it will automatically start it.

---

## Attach to application container

```bash
dev attach api-gateway
```

---

## Attach to web container

```bash
dev attach web api-gateway
```

---

# Logs

## Application container logs

```bash
dev logs api-gateway
```

---

## Web server logs

```bash
dev logs web api-gateway
```

Logs will follow the container output.

---

# Project Status

Show all configured projects and whether they are running.

```bash
dev list
```

Example output:

```
PROJECT                              STATUS
------------------------------------ ------------
api-gateway                          🟢 running
status-notification-service          🔴 stopped
```

---

# Diagnostics

Run environment checks.

```bash
dev doctor
```

This verifies:

- Docker installed
- Docker Compose available
- yq installed
- Configuration file present
- Project configuration validity
- Project running status

---

# Typical Workflow

Start environment:

```bash
dev up
```

Start a project:

```bash
dev up api-gateway
```

Attach to PHP container:

```bash
dev attach api-gateway
```

View logs:

```bash
dev logs api-gateway
```

Check status:

```bash
dev list
```

Shutdown everything:

```bash
dev down
```

---

# Philosophy

Shipyard focuses on:

- **Consistency** across projects
- **Minimal commands**
- **Fast developer workflows**
- **Zero complexity**

Most developers only need to remember:

```
dev up
dev attach
dev logs
dev list
dev down
```

---

# License
MIT Licence

Copyrigy 2026 Dan Stuchbury

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
