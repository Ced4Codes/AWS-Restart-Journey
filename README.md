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
├── Storage/                 # S3, EBS, Snapshots
├── Networking/              # VPC, ELB, Subnets, Security Groups
├── Compute/                 # EC2, LAMP Stack
├── Databases/               # RDS, Database Migration
├── Monitoring/              # CloudWatch, CloudTrail, Resource Tagging
├── Automation/              # CloudFormation, Infrastructure as Code
└── Personal-Projects/       # Custom AWS implementations (coming soon)
```

## 🧪 Labs Completed

### Storage
- [Lab 01: Hosting a Static Website in Amazon S3 using AWS CLI](Storage/LAB(S3)-Website/)
- [Lab 06: Working with Amazon EBS - Scalable Storage](Storage/LAB(EBS)-EBS/)
- [Lab 08: Managing Storage with EBS Snapshots and S3 Sync](Storage/LAB(EBS)-Snapshots-S3-Sync/)
- [Lab 10: S3 Bucket and Public Access Policy](Storage/LAB(S3)-Public-Access-Policy/)

### Networking
- [Lab 02: Create a VPC with Public/Private Subnets and Deploy a Web Server on EC2](Networking/LAB(VPC)-VPC-with-Server/)
- [Lab 04: Scaling and Load Balancing Your Architecture](Networking/LAB(ELB)-Scaling-Architecture/)

### Compute
- [Lab 05: Troubleshooting an EC2 LAMP Deployment with AWS CLI](Compute/LAB(EC2)-LAMP-Troubleshoot/)

### Databases
- [Lab 07: Migrating the Café App Database to Amazon RDS](Databases/LAB(RDS)-Migrate-Database/)

### Monitoring
- [Lab 09: Monitoring Infrastructure](Monitoring/LAB(Cloudwatch)-Cloudwatch-and-Config/)
- [Lab 11: AWS CloudTrail - Investigating the Café Website Hack](Monitoring/LAB(Cloudwatch)-Investigate-web-app/)
- [Lab 12: Managing Resources with Tagging](Monitoring/LAB(TAGS)-Managing-tags/)

### Automation
- [Lab 13: Automation with CloudFormation](Automation/LAB(Cloudformation)-Automate-deployment/)

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
| Storage | 4/4 | ✅ Complete |
| Networking | 2/2 | ✅ Complete |
| Compute | 1/1 | ✅ Complete |
| Databases | 1/1 | ✅ Complete |
| Monitoring | 3/3 | ✅ Complete |
| Automation | 1/1 | ✅ Complete |
| Personal Projects | 0/∞ | 🚧 In Progress |

**Last Updated**: November 2025
