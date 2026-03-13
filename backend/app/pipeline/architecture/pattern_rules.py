from dataclasses import dataclass


@dataclass(frozen=True)
class PatternRule:
    name: str
    folder_signals: list[str]
    file_signals: list[str]
    weight: float


PATTERN_RULES: list[PatternRule] = [
    PatternRule(
        name="MVC",
        folder_signals=["models", "views", "controllers", "templates"],
        file_signals=["model.py", "view.py", "controller.py", "router.py"],
        weight=1.0,
    ),
    PatternRule(
        name="Layered",
        folder_signals=["service", "services", "repository", "repositories", "controller", "controllers", "domain"],
        file_signals=["service.py", "repository.py", "controller.py", "dao.py"],
        weight=1.0,
    ),
    PatternRule(
        name="Microservices",
        folder_signals=["services", "gateway", "discovery", "broker", "consumer", "producer"],
        file_signals=["docker-compose.yml", "docker-compose.yaml", "gateway.py", "broker.py"],
        weight=1.2,
    ),
    PatternRule(
        name="Monolithic",
        folder_signals=["app", "core", "common", "shared", "utils", "helpers"],
        file_signals=["app.py", "main.py", "server.py", "wsgi.py", "asgi.py"],
        weight=0.8,
    ),
    PatternRule(
        name="Serverless",
        folder_signals=["functions", "handlers", "lambdas"],
        file_signals=["serverless.yml", "serverless.yaml", "handler.py", "function.py"],
        weight=1.1,
    ),
    PatternRule(
        name="Event-Driven",
        folder_signals=["events", "listeners", "handlers", "consumers", "publishers"],
        file_signals=["event.py", "listener.py", "consumer.py", "publisher.py", "dispatcher.py"],
        weight=1.1,
    ),
]