# AWS Restart Journey

A comprehensive repository documenting hands-on AWS labs and personal cloud infrastructure projects, showcasing practical experience with core AWS services, automation, monitoring, and best practices.

## 📋 Table of Contents

- [Overview](#overview)
- [Skills Demonstrated](#skills-demonstrated)
- [Repository Structure](#repository-structure)
- [Labs Completed](#labs-completed)
- [Personal Projects](#personal-projects)
- [Technologies & Services](#technologies--services)
- [Getting Started](#getting-started)
- [Key Learnings](#key-learnings)
- [License](#license)

## 🎯 Overview

This repository serves as a portfolio of AWS cloud computing knowledge, featuring:

- **Structured Lab Documentation**: Step-by-step guides from the AWS Restart program covering foundational to advanced AWS concepts
- **Personal Cloud Projects**: Custom implementations and experiments demonstrating practical application of AWS services
- **Best Practices**: Real-world examples of infrastructure as code, security configurations, and monitoring setups

## 💡 Skills Demonstrated

### AWS Services Expertise
- **Compute**: Amazon EC2, Auto Scaling Groups, Application Load Balancer
- **Storage**: Amazon S3 (static websites, versioning, lifecycle policies), Amazon EBS (volumes, snapshots)
- **Database**: Amazon RDS (MariaDB, Multi-AZ deployments, migrations)
- **Networking**: Amazon VPC, Subnets, Internet Gateways, NAT Gateways, Security Groups, Route Tables
- **Monitoring & Logging**: Amazon CloudWatch (metrics, alarms, dashboards), AWS CloudTrail (audit logging, forensics), AWS Config (compliance)
- **Infrastructure as Code**: AWS CloudFormation (template design, stack management, drift detection, troubleshooting)
- **Cost Management**: AWS Pricing Calculator, resource optimization, right-sizing strategies
- **Security & Identity**: IAM policies, security group configuration, S3 bucket policies

### Technical Skills
- **Cloud Architecture**: Designing scalable, highly available, and cost-effective solutions
- **Infrastructure as Code (IaC)**: Writing and debugging CloudFormation YAML templates
- **AWS CLI Proficiency**: Resource management, automation scripts, query operations with JMESPath
- **Linux System Administration**: Bash scripting, cron jobs, log analysis, package management
- **Database Management**: MySQL/MariaDB administration, data migration strategies
- **Troubleshooting**: Debugging failed deployments, analyzing CloudWatch logs, investigating security incidents
- **Version Control**: Git workflow, branch management, pull requests
- **Documentation**: Technical writing, architecture diagrams, step-by-step guides

### Cloud Best Practices
- Multi-AZ deployments for high availability
- Security at multiple layers (network, application, data)
- Tag-based resource governance and cost allocation
- Automated backup and disaster recovery strategies
- Principle of least privilege for IAM and security groups
- Infrastructure automation and consistency through CloudFormation

## 📁 Repository Structure

```
AWS-Restart-Journey/
├── Storage/                 # S3, EBS, Snapshots
├── Networking/              # VPC, ELB, Subnets, Security Groups
├── Compute/                 # EC2, LAMP Stack
├── Databases/               # RDS, Database Migration
├── Monitoring/              # CloudWatch, CloudTrail, Resource Tagging
├── Automation/              # CloudFormation, Infrastructure as Code
├── Cost/                    # AWS Pricing Calculator, Cost Optimization
└── Personal-Projects/       # Custom AWS implementations (coming soon)
```

## 🧪 Labs Completed

### Storage
- [Lab 01: Hosting a Static Website in Amazon S3 using AWS CLI](Storage/LAB(S3)-Website/)
- [Lab 05: Working with Amazon EBS - Scalable Storage](Storage/LAB(EBS)-EBS/)
- [Lab 07: Managing Storage with EBS Snapshots and S3 Sync](Storage/LAB(EBS)-Snapshots-S3-Sync/)
- [Lab 09: S3 Bucket and Public Access Policy](Storage/LAB(S3)-Public-Access-Policy/)

### Networking
- [Lab 02: Create a VPC with Public/Private Subnets and Deploy a Web Server on EC2](Networking/LAB(VPC)-VPC-with-Server/)
- [Lab 03: Scaling and Load Balancing Your Architecture](Networking/LAB(ELB)-Scaling-Architecture/)

### Compute
- [Lab 04: Troubleshooting an EC2 LAMP Deployment with AWS CLI](Compute/LAB(EC2)-LAMP-Troubleshoot/)

### Databases
- [Lab 06: Migrating the Café App Database to Amazon RDS](Databases/LAB(RDS)-Migrate-Database/)

### Monitoring
- [Lab 08: Monitoring Infrastructure](Monitoring/LAB(Cloudwatch)-Cloudwatch-and-Config/)
- [Lab 10: AWS CloudTrail - Investigating the Café Website Hack](Monitoring/LAB(Cloudwatch)-Investigate-web-app/)
- [Lab 11: Managing Resources with Tagging](Monitoring/LAB(TAGS)-Managing-tags/)

### Automation
- [Lab 12: Automation with CloudFormation](Automation/LAB(Cloudformation)-Automate-deployment/)
- [Lab 13: CloudFormation Troubleshooting Journey](Automation/LAB(Cloudformation)-Cloudformation-Troubleshoot/)
- [Lab 15: Using AWS CloudFormation to Create an AWS VPC and EC2 Instance](Automation/LAB(Cloudformation)-Create-AWS-Resources/)

### Cost Optimization
- [Lab 14: Optimizing Resource Utilization for the Café Web Application](Cost/LAB(Pricing Calculator)-Optimize-Cafe-Resourcces/)

## 💼 Personal Projects

*This section will feature custom AWS implementations and experiments, including:*

-N/A for now

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
- **scripts/** or **YAML templates** (when applicable): Automation scripts, CloudFormation templates, and configuration files

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

## 📝 Documentation Standards

Each lab follows a consistent structure:
- **Overview**: Lab objectives and context
- **Goal**: Specific learning outcomes
- **Tools Used**: AWS services and utilities
- **Architecture**: Visual diagram of the infrastructure
- **Steps Performed**: Detailed implementation guide
- **Key Takeaways**: Lessons learned and best practices


## 📄 License

This work is licensed under the [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License](https://creativecommons.org/licenses/by-nc-nd/4.0/).

**What this means:**
- ✅ You can view and share this work
- ✅ You must give appropriate credit
- ❌ You cannot use it for commercial purposes
- ❌ You cannot copy, modify, or claim it as your own work

See the [LICENSE](LICENSE) file for full details.

## 🔗 Connect

Feel free to reach out for discussions about AWS, cloud architecture, or collaboration opportunities:

- [LinkedIn](https://www.linkedin.com/in/paclicedric/)

---

**Note**: All labs are performed in sandbox environments. Credentials and sensitive information are never committed to this repository. Always follow AWS security best practices when working with cloud resources.

**Last Updated**: November 2025
