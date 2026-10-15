"""A stand-in app, so pushes and pull requests in this demo repository have something to change."""


def greet(name: str) -> str:
    return f"Hello, {name}!"


if __name__ == "__main__":
    print(greet("Airflow"))
