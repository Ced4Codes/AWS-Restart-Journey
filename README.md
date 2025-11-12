# AWS Restart Journey

A comprehensive repository documenting hands-on AWS labs and personal cloud infrastructure projects, showcasing practical experience with core AWS services, automation, monitoring, and best practices.

## 📋 Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Labs Completed](#labs-completed)
- [Personal Projects](#personal-projects)
- [Technologies & Services](#technologies--services)
- [Getting Started](#getting-started)
- [Key Learnings](#key-learnings)
- [Future Plans](#future-plans)
- [License](#license)

## 🎯 Overview

This repository serves as a portfolio of AWS cloud computing knowledge, featuring:

- **Structured Lab Documentation**: Step-by-step guides from the AWS Restart program covering foundational to advanced AWS concepts
- **Personal Cloud Projects**: Custom implementations and experiments demonstrating practical application of AWS services
- **Best Practices**: Real-world examples of infrastructure as code, security configurations, and monitoring setups

## 📁 Repository Structure

```
AWS-Restart-Journey/
├── LABS/                    # Core AWS service labs
├── Compute/                 # EC2, Auto Scaling, Load Balancing
├── Networking/              # VPC, Subnets, Security Groups
├── Storage/                 # S3, EBS, Snapshots
├── Database/                # RDS, Database Migration
├── Monitoring/              # CloudWatch, CloudTrail, Resource Tagging
├── Automation/              # CloudFormation, Infrastructure as Code
└── Personal-Projects/       # Custom AWS implementations (coming soon)
```

## 🧪 Labs Completed

### Core Services (LABS/)

#### [Lab 01: Introduction to IAM](LABS/LAB-01/)
- IAM user and group management
- Policy-based access control
- Best practices for AWS account security

#### [Lab 02: Amazon VPC - Build Your VPC and Launch Web Server](LABS/LAB-02/)
- Custom VPC creation with public and private subnets
- Internet Gateway and Route Table configuration
- Security Group setup for web server access

#### [Lab 03: Database Migration to RDS](LABS/LAB-03/)
- Application database migration from local to Amazon RDS
- Multi-AZ deployment configuration
- Database security and backup strategies

#### [Lab 04: Scaling and Load Balancing Your Architecture](LABS/LAB-04/)
- Application Load Balancer setup
- Auto Scaling Group configuration
- High availability architecture design

#### [Lab 05: Automating Infrastructure Deployment](LABS/LAB-05/)
- CloudFormation template creation
- Stack management and updates
- Infrastructure automation best practices

### Compute

#### [Lab 06: Working with Amazon EBS - Scalable Storage](Compute/LAB-06/)
- EBS volume creation and attachment
- File system configuration and mounting
- Volume snapshots and restoration
- Storage scalability demonstration

### Networking

#### [Lab 07: Migrating the Café App Database to Amazon RDS](Networking/LAB(RDS)-Migrate-Database/)
- VPC subnet configuration for RDS
- Security group rules for database access
- Database endpoint configuration
- Application connection string migration

### Storage

#### [Lab 08: Managing Storage with EBS Snapshots and S3 Sync](Storage/LAB(EBS)-Snapshots-S3-Sync/)
- Automated EBS snapshot creation
- S3 bucket lifecycle management
- Cross-region backup strategies
- Storage cost optimization

#### [Lab 10: S3 Bucket and Public Access Policy](Storage/LAB(S3)-Public-Access-Policy/)
- S3 bucket policy configuration
- Public access management
- Static website hosting
- Bucket ownership controls

### Monitoring

#### [Lab 09: Monitoring Infrastructure](Monitoring/LAB(Cloudwatch) Cloudwatch-and-Config/)
- CloudWatch metrics and dashboards
- Custom alarm creation
- AWS Config compliance monitoring
- Log aggregation and analysis

#### [Lab 11: AWS CloudTrail - Investigating the Café Website Hack](Monitoring/LAB(Cloudwatch)-Investigate-web-app/)
- CloudTrail log analysis and forensics
- Security incident investigation
- Athena queries for log exploration
- Account security hardening

#### [Lab 12: Managing Resources with Tagging](Monitoring/LAB(TAGS)-Managing-tags/)
- Resource tagging strategies
- Tag-based automation scripts
- Cost allocation through tags
- Compliance enforcement via tags

### Automation

#### [Lab 13: Automation with CloudFormation](Automation/LAB(Cloudformation)-Automate-deployment/)
- Infrastructure as Code principles
- CloudFormation template design
- Stack updates and change sets
- Resource dependency management

## 💼 Personal Projects

*This section will feature custom AWS implementations and experiments, including:*

- Serverless applications using Lambda and API Gateway
- CI/CD pipelines with CodePipeline and CodeBuild
- Multi-tier application architectures
- Cost optimization strategies and implementations
- Custom monitoring and alerting solutions
- Infrastructure automation scripts

## 🛠️ Technologies & Services

### AWS Services
- **Compute**: EC2, Auto Scaling, Lambda
- **Storage**: S3, EBS, Snapshots
- **Database**: RDS, Multi-AZ deployments
- **Networking**: VPC, Subnets, Security Groups, Load Balancers
- **Monitoring**: CloudWatch, CloudTrail, AWS Config
- **Security**: IAM, Security Groups, Bucket Policies
- **Automation**: CloudFormation, Systems Manager

### Tools & Languages
- AWS CLI
- AWS SDK for PHP
- Bash scripting
- YAML (CloudFormation templates)
- SQL (database management)
- Linux command-line utilities

## 🚀 Getting Started

Each lab directory contains:
- **Lab-##.md**: Detailed step-by-step documentation
- **screenshots/**: Visual references for each step
- **scripts/** (when applicable): Automation scripts and configuration files

## 📚 Key Learnings

### Infrastructure Design
- Design scalable, highly available architectures using AWS best practices
- Implement security at multiple layers (network, application, data)
- Optimize costs through right-sizing and automation

### Automation & IaC
- Write CloudFormation templates for repeatable infrastructure deployment
- Use AWS CLI for resource management and automation
- Implement tag-based resource governance

### Security & Compliance
- Apply principle of least privilege with IAM policies
- Configure security groups following defense-in-depth principles
- Use CloudTrail for audit logging and forensic analysis
- Implement bucket policies for granular S3 access control

### Monitoring & Operations
- Set up CloudWatch alarms for proactive monitoring
- Analyze logs using Athena queries
- Automate responses to infrastructure events
- Track resource compliance with AWS Config

## 🔮 Future Plans

- [ ] Implement serverless applications with Lambda and API Gateway
- [ ] Set up CI/CD pipelines for automated deployments
- [ ] Create multi-region architectures for disaster recovery
- [ ] Develop cost optimization dashboards and reports
- [ ] Build containerized applications using ECS/EKS
- [ ] Implement advanced networking with Transit Gateway
- [ ] Create custom CloudWatch metrics and dashboards
- [ ] Develop infrastructure testing and validation frameworks

## 📝 Documentation Standards

Each lab follows a consistent structure:
- **Overview**: Lab objectives and context
- **Goal**: Specific learning outcomes
- **Tools Used**: AWS services and utilities
- **Architecture**: Visual diagram of the infrastructure
- **Steps Performed**: Detailed implementation guide
- **Key Takeaways**: Lessons learned and best practices


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Connect

Feel free to reach out for discussions about AWS, cloud architecture, or collaboration opportunities:

- [LinkedIn](https://www.linkedin.com/in/paclicedric/)

---

**Note**: All labs are performed in sandbox environments. Credentials and sensitive information are never committed to this repository. Always follow AWS security best practices when working with cloud resources.

## 📊 Progress Tracker

| Category | Labs Completed | Status |
|----------|---------------|---------|
| Core Services | 5/5 | ✅ Complete |
| Compute | 1/1 | ✅ Complete |
| Networking | 1/1 | ✅ Complete |
| Storage | 2/2 | ✅ Complete |
| Database | 1/1 | ✅ Complete |
| Monitoring | 3/3 | ✅ Complete |
| Automation | 1/1 | ✅ Complete |
| Personal Projects | 0/∞ | 🚧 In Progress |

**Last Updated**: November 2025
