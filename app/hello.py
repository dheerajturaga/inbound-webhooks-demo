"""A stand-in app, so pushes and pull requests in this demo repository have something to change."""

GREETINGS = {"en": "Hello", "fr": "Bonjour"}


def greet(name: str, language: str = "en") -> str:
    return f"{GREETINGS[language]}, {name}!"


if __name__ == "__main__":
    print(greet("Airflow"))
    print(greet("Airflow", language="fr"))
