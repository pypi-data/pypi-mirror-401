from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="insightconnect-plugin-runtime",
    version="6.4.2",
    description="InsightConnect Plugin Runtime",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Rapid7 Integrations Alliance",
    author_email="integrationalliance@rapid7.com",
    url="https://github.com/rapid7/komand-plugin-sdk-python",
    packages=find_packages(),
    install_requires=[
        "requests==2.32.5",
        "python_jsonschema_objects==0.5.2",
        "jsonschema==4.22.0",
        "certifi==2026.1.4",
        "Flask==3.1.2",
        "gunicorn==23.0.0",
        "greenlet==3.3.0",
        "gevent==25.5.1",
        "marshmallow==3.26.2",
        "apispec==6.5.0",
        "apispec-webframeworks==1.0.0",
        "blinker==1.9.0",
        "structlog==25.5.0",
        "python-json-logger==2.0.7",
        "Jinja2==3.1.6",
        "python-dateutil==2.9.0.post0",
        "opentelemetry-sdk==1.39.1",
        "opentelemetry-instrumentation-flask==0.60b1",
        "opentelemetry-exporter-otlp-proto-http==1.39.1",
        "opentelemetry-instrumentation-requests==0.60b1",
        "urllib3==2.6.3"
    ],
    tests_require=[
        "pytest",
        "docker",
        "dockerpty",
        "swagger-spec-validator",
    ],
    test_suite="tests",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: Software Development :: Build Tools",
    ],
)
