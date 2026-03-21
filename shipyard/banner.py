def print_banner() -> None:
    print(
        """
╔══════════════════════════════════════╗
║              SHIPYARD                ║
║   Local Laravel Runtime Manager      ║
╚══════════════════════════════════════╝

Commands
  shipyard init                     Initialise the Shipyard runtime
  shipyard adopt <path>             Adopt a Laravel project
  shipyard up                       Start Shipyard core services
  shipyard restart <project>        Restart a project
  shipyard rebuild <project>        Restart a project and rebuild all containers
  shipyard up <project>             Start a project
  shipyard down                     Stop all projects and core services
  shipyard restart                  Restart core services. You should not have to do this routinely
  shipyard rebuilt                  Rebuild core services. You should not have to do this routinely
  shipyard down <project>           Stop a specific project
  shipyard attach <project>         Open a shell inside the app container
  shipyard attach <project> <svc>   Attach to a specific service
  shipyard list                     Show runtime status

Examples
  shipyard up
  shipyard up evolutioncrm
  shipyard attach evolutioncrm
"""
    )
