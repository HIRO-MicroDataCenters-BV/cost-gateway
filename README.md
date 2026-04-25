[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/HIRO-MicroDataCenters-BV/cost-gateway)

# Cost Gateway

Gather different types of costs and expose them via prometheus

  * [Installation](#installation)
  * [Package](#package)
  * [Docker](#docker)
  * [Helm chart](#helm-chart)
  * [Release](#release)
  * [GitHub Actions](#github-actions)
  * [Act](#act)
- [Collaboration guidelines](#collaboration-guidelines)


## Table of Contents

- [Cost Gateway](#cost-gateway)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
    - [Development](#development)
    - [Deployment](#deployment)
  - [Development](#development-1)
  - [Docker](#docker)
  - [Manual build and deployment on minikube](#manual-build-and-deployment-on-minikube)
  - [Package](#package)
  - [Helm chart](#helm-chart)
  - [Release](#release)
  - [Helm Chart Versioning](#helm-chart-versioning)
  - [GitHub Actions](#github-actions)
  - [Act](#act)
  - [Collaboration guidelines](#collaboration-guidelines)

## Prerequisites
### Development
  - [Python 3.15](https://www.python.org/downloads/) - The project requires Python 3.15 or higher
  - [uv](https://docs.astral.sh/uv/) - Fast Python package installer and resolver
  - [docker](https://docs.docker.com/get-docker/)
  - [Helm](https://helm.sh/en/docs/)
  - [minikube](https://minikube.sigs.k8s.io/docs/start/)
  - [Act](#act)

### Deployment
  - [Github Actions](#github-actions) - repository use Github Actions to automate the build, test, release and deployment processes. For your convinience we recommend to fill necessary secrets in the repository settings.



## Development

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if you don't have it:
```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or using pip
pip install uv
```

2. Install dependencies:
```bash
uv sync --locked --all-extras --dev
```

3. Install `pre-commit` hooks:
```bash
uv run pre-commit install
```

4. Launch the project:
```bash
uv run python -m cost_gateway.main --config ./etc/config.yaml
```

5. Running tests:
```bash
uv run pytest
```

6. Running style checks:
```bash
uv run mypy ./src
uv run isort ./src --check --diff
uv run flake8 ./src
uv run black ./src --check --diff
```


## Docker
Build a [Docker](https://docs.docker.com/) image and run a container:
```bash
docker build . -t <image_name>:<image_tag>
docker run <image_name>:<image_tag>
```

Upload the Docker image to the repository:
```bash
docker login -u <username>
docker push <image_name>:<image_tag>
```


## Manual build and deployment on minikube
1. Install [minikube](https://minikube.sigs.k8s.io/docs/start/).
2. Start minikube:
```bash
minikube start
```
3. Build a docker image:
```bash
docker build . -t <image_name>:<image_tag>
```
4. Upload the docker image to minikube:
```bash
minikube image load <image_name>:<image_tag>
```
5. Deploy the service:
```bash
helm upgrade --install <app_name> ./charts/app --set image.repository=<image_name> --set image.tag=latest --version 0.1.0
```

## Package
To build and publish a package on pypi.org, execute the following commands:
```bash
# Build the package
uv build

# Publish to PyPI (requires PyPI token to be set)
uv publish --token <pypi_token>
```

`pypi_token` - API token for authentication on [PyPI](https://pypi.org/help/#apitoken). 


## Helm chart
Authenticate your Helm client in the container registry:
```bash
helm registry login <container_registry> -u <username>
```

Create a [Helm chart](https://helm.sh/docs/):
```bash
helm package charts/<chart_name>
```

Push the Helm chart to container registry:
```bash
helm push <helm_chart_package> <container_registry>
```

Deploy the Helm chart:
```bash
helm repo add <repo_name> <repo_url>
helm repo update <repo_name>
helm upgrade --install <release_name> <repo_name>/<chart_name>
```

## Release
To create a release, add a tag in GIT with the format a.a.a, where 'a' is an integer.
```bash
git tag 0.1.0
git push origin 0.1.0
```
The release version for branches, pull requests, and other tags will be generated based on the last tag of the form a.a.a.

## Helm Chart Versioning
The Helm chart version changed automatically when a new release is created. The version of the Helm chart is equal to the version of the release.

## GitHub Actions
[GitHub Actions](https://docs.github.com/en/actions) triggers testing, builds, and application publishing for each release.  


The process of building and publishing differs for web services and libraries.

### Service
The default build and publish process is configured for a web application (`.github\workflows\service.yaml`).
During this process, a Docker image is built, a Helm chart is created, an `openapi.yaml` is generated, and the web service is deployed to a Kubernetes cluster.

## Act
[Act](https://github.com/nektos/act) allows you to run your GitHub Actions locally (e.g., for developing tests)

Usage example:
```bash
act push -j deploy --secret-file my.secrets
```

# Collaboration guidelines
HIRO uses and requires from its partners [GitFlow with Forks](https://hirodevops.notion.site/GitFlow-with-Forks-3b737784e4fc40eaa007f04aed49bb2e?pvs=4)
