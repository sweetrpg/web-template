from setuptools import setup

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="sweetrpg-COMPONENT-web",
    install_requires=[
        "Flask-Caching",
        "Flask-Cors",
        "Flask-DotEnv",
        "Flask-Session",
        "Flask>=2.0",
        "Flask-Migrate",
        "Flask-MongoEngine",
        "gunicorn",
        "python-dotenv",
        "python-editor",
        "redis",
        "requests",
        "sentry-sdk[flask]==1.5.0",
        "analytics-python<2.0",
        "sweetrpg-db",
        "sweetrpg-web-core",
        "sweetrpg-COMPONENT-model",
        "sweetrpg-client"
    ],
    extras_require={},
)
