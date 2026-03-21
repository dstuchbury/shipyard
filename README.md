# ⚓ Shipyard

![version](https://img.shields.io/badge/version-2.0-blue)
![platform](https://img.shields.io/badge/platform-Linux%20%7C%20WSL2-blue)
![docker](https://img.shields.io/badge/docker-required-2496ED?logo=docker)
![bash](https://img.shields.io/badge/shell-bash-4EAA25?logo=gnubash)
![status](https://img.shields.io/badge/status-internal%20tool-purple)

Change the above!

**Shipyard** is a lightweight CLI for managing local Docker development stacks.

It provides a single command — `dev` — to start projects, attach to containers, view logs, and manage your development environment.

---

## Quick Example

```bash
shipyard up
shipyard up your-project

shipyard attach your-project
shipyard logs web your-project

shipyard list
shipyard down
```

---

## WIPs

* [ ] Allow custom Dockerfiles
* [ ] Make docker-compose.generated.yml use dynamic build context and Dockerfiles
* [ ] Regenerate published files after a config change to use custom Dockerfiles 

---

---

## Roadmap & Ideas

* [ ] Command to tail and follow laravel.log (also support laravel-yyyy-mm-dd.log for today)
* [ ] Healthcheck
* [ ] Support for multiple queue workers - define in config, then regenerate?
* [ ] Laravel Telescope
* [ ] beanstalkd and Beanstalk Console for queue management.
* [ ] Write a great README to sell the idea

---

# License
MIT Licence

Copyright 2026 Dan Stuchbury

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
