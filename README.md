
# CLI Deployment Tool

A command-line deployment tool that automates the process of cloning, building, and deploying React/Vite applications to AWS infrastructure with monitoring capabilities.

## Features

- **Automated deployment**: Clones, builds, containerize, and deploys applications
- **Infrastructure as Code**: Uses Terraform to provision AWS EC2 instances
- **Container orchestration**: Docker-based deployment with automated image building and pushing
- **Monitoring stack**: Integrated Prometheus, Grafana, and Node Exporter for application monitoring
- **Rollback capability**: Easy rollback to previous application versions
- **GitHub Actions integration**: Automated CI/CD workflows

## Prerequisites

### Required Software
- **Python 3.7+** with pip
- **Docker** (with Docker Hub account for image pushing) and docker running before running the application
- **Terraform** (v1.0+)
- **Git**
- **Node.js and npm** (for building React/Vite applications)

### Required Accounts & Services
- **AWS Account** with programmatic access 
- **Docker Hub Account** for container registry
- **GitHub Account** with repository access

### AWS Configuration
1. Create an AWS free tier account user
2. Configure AWS credentials (access key and secret key)
3. Ensure you have an EC2 key pair created in `ap-south-1` region replace that in `terraform/main.tf` and add it github secrets for pipeline execution

### Environment Setup
1. **AWS Credentials**:  uncomment the credentials in `cmd/deploy/` and Update the hardcoded credentials in:
   - `cmd/deploy/deployment.py`
   - `cmd/deploy/infra.py`
   - `cmd/deploy/s3push.py`
   
2. **Docker Hub**: Configure Docker Hub credentials for pushing images to your repository and the repo should be public

3. **GitHub Secrets**: Set up the following secrets in your GitHub repository:
   - `USERNAME`: EC2 instance username (ubuntu)
   - `KEY`: Private key content for EC2 access that you created in `ap-south-1` region

## Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd cli-tool
   ```

2. **Install Python dependencies**:
   ```bash
   pip install gitpython boto3 requests
   ```

3. **AWS configure**:
   ```bash
   aws configure
   ```

4. **Login to Docker Hub**:
   ```bash
   docker login
   ```

## Usage

### Starting the CLI Tool
```bash
python cmd/main.py
```

### Available Commands

#### 1. Initialize Project
```
deploy-tool init
```
- Prompts for Git repository URL
- Clones the repository to a temporary directory
- Detects application type (React)
- Builds the application
- Uploads build artifacts to S3

#### 2. Deploy Application
```
deploy-tool deploy
```
- Creates Docker image from the built application
- Pushes image to Docker Hub
- Provisions AWS infrastructure using Terraform
- Deploys application with monitoring stack
- Provides application URL

#### 3. Rollback Application
```
deploy-tool roll-back
```
- Rolls back to the previous application version
- Updates the running container with the previous image

#### 4. Monitor Application
```
monitor-status
```
- Provides monitoring dashboard URLs:
  - Prometheus: `http://<public-ip>:9090`
  - Grafana: `http://<public-ip>:3000` (admin/admin)

#### 5. Help
```
--help
```
- Displays available commands

## Project Structure

```
cli-tool/
├── cmd/
│   ├── main.py                 # Main CLI application
│   └── deploy/
│       ├── detect_logic.py     # Application type detection
│       ├── build.py           # Docker build and push
│       ├── deployment.py      # GitHub Actions workflow trigger
│       ├── infra.py          # Terraform infrastructure management
│       └── s3push.py         # S3 artifact storage
├── Docker/
│   ├── Dockerfile-react       # Dockerfile for React apps
│   └── Dockerfile-vite        # Dockerfile for Vite-built apps
├── terraform/
│   ├── main.tf               # AWS infrastructure definition
│   ├── provider.tf           # Terraform providers
│   └── output.tf             # Infrastructure outputs
├── .github/workflows/
│   ├── deploy-monitor.yml    # Deployment workflow
│   └── roll-back-monitor.yml # Rollback workflow
└── docker-setup.sh           # Docker installation script
```

## Monitoring Stack

The deployed application includes:
- **Prometheus** (port 9090): Metrics collection and alerting
- **Grafana** (port 3000): Visualization dashboards
- **Node Exporter** (port 9100): System metrics
- **Blackbox Exporter** (port 9115): Application health checks

## Security Considerations

⚠️ **Important**: This project contains hardcoded credentials and tokens. For production use:
1. Use environment variables or AWS IAM roles
2. Rotate GitHub personal access tokens regularly
3. Implement proper secret management
4. Review and restrict AWS IAM permissions

## Troubleshooting

### Common Issues
1. **Docker build fails**: Ensure Docker is running and you're logged into Docker Hub
2. **Terraform errors**: Check AWS credentials and permissions
3. **Application not accessible**: Verify security group rules and instance status
4. **GitHub workflow fails**: Check repository secrets and permissions

### Logs and Debugging
- Check Docker container logs: `docker logs <container-name>`
- Monitor Terraform state: `terraform show`
- GitHub Actions logs available in repository Actions tab
