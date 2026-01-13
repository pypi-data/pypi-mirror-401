"""Setup script for the Agent Observability SDK."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="agent-observability",
    version="1.2.0",
    author="Agent Observability Team",
    author_email="hello@agentobs.io",
    description="Structured logging, cost tracking, and compliance audit trails for AI agents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blueskylineassets/agent-observability",
    project_urls={
        "Homepage": "https://api-production-0c55.up.railway.app",
        "Documentation": "https://api-production-0c55.up.railway.app/docs",
        "Pricing": "https://api-production-0c55.up.railway.app/pricing.json",
        "OpenAPI": "https://api-production-0c55.up.railway.app/openapi.json",
        "Source": "https://github.com/blueskylineassets/agent-observability",
        "Bug Tracker": "https://github.com/blueskylineassets/agent-observability/issues",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Logging",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: AsyncIO",
        "Framework :: FastAPI",
    ],
    keywords=[
        "agent",
        "observability",
        "logging",
        "compliance",
        "audit",
        "ai-agent",
        "langchain",
        "autogpt",
        "crewai",
        "monitoring",
        "analytics",
        "cost-tracking",
        "agent-logging",
        "structured-logging",
    ],
    python_requires=">=3.9",
    install_requires=[
        "httpx>=0.24.0",
        "pydantic>=2.0.0",
        "tenacity>=8.2.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "mypy>=1.0.0",
        ],
    },
)
