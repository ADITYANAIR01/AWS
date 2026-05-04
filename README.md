# AWS Mini-Projects Portfolio

Welcome to my overall AWS projects repository! This repository contains various hands-on projects demonstrating real-world cloud architectures and DevOps practices on AWS.

Below is a detailed list of all the projects included in this workspace, along with their descriptions, AWS services used, and the underlying tools.

---

## 1. AWS-Resource-lifecycle-Tracker

- **Repo URL:** [AWS-Resource-lifecycle-Tracker](https://github.com/ADITYANAIR01/AWS-Resource-lifecycle-Tracker.git)
- **Description:** A self-hosted tool that monitors your AWS account and gives you a unified view of every resource — when it was created, how long it has been running, its current state, its tags, and an estimated cost. Alerts you when something looks wrong.

## 2. AWS Scalable Web Application — ALB + ASG

- **Dir:** [aws-scalable-webapp-alb](./aws-scalable-webapp-alb/AWS-SCALABLE-WEBAPP-ALB-README.md)
- **Description:** A self-healing, production-grade web application with automatic scaling, mimicking platforms like Heroku/Railway.
- **AWS Services Used:** VPC, EC2, Application Load Balancer (ALB), Auto Scaling Group (ASG), Launch Templates, IAM, CloudWatch, Security Groups.
- **Tools Used:** Nginx.

## 3. AWS VPC From Scratch

- **Dir:** [aws-vpc-from-scratch](./aws-vpc-from-scratch/AWS-VPC-FROM-SCRATCH-README.md)
- **Description:** A production-style custom AWS VPC implementation featuring public/private subnets, a Bastion Host, NAT Gateway, and layered network security.
- **AWS Services Used:** VPC, Internet Gateway, NAT Gateway, Route Tables, Security Groups, Network ACLs, EC2.
- **Tools Used:** SSH.

## 4. Containerdock

- **Dir:** [containerdock](./containerdock/containerdock.md)
- **Description:** A self-hosted container deployment platform built on ECS Fargate that deploys Dockerized applications, similar to Render or Railway.
- **AWS Services Used:** ECR, ECS Fargate, ALB, ACM, VPC, CloudWatch, IAM.
- **Tools Used:** Docker, Node.js.

## 5. GitNest

- **Dir:** [gitnest](./gitnest/GITNEST-README.md)
- **Description:** A self-hosted Git platform mimicking GitHub. It runs Gitea as a container securely on EC2 with persistent EFS storage.
- **AWS Services Used:** EC2, EFS, ALB, ACM, VPC, Security Groups, IAM.
- **Tools Used:** Gitea, Docker, Docker Compose, SQLite.

## 6. Mini Dropbox

- **Dir:** [mini-dropbox](./mini-dropbox/MINI-DROPBOX-README.md)
- **Description:** A cloud file storage platform replicating core Dropbox features like file upload/download, shareable links, and Google OAuth login.
- **AWS Services Used:** S3, RDS PostgreSQL, CloudFront, EC2, CloudWatch.
- **Tools Used:** Python (Flask), HTML5/Tailwind/JS, Authlib (Google OAuth), Nginx, Gunicorn.

## 7. PipelineX

- **Dir:** [pipelineX](./pipelineX/PIPELINEX-README.md)
- **Description:** A fully automated CI/CD container delivery pipeline. Pushing to GitHub triggers an image build, a push to a private registry, and rolling deployment to Fargate.
- **AWS Services Used:** CodeBuild, ECR, ECS Fargate, ALB, IAM, CloudWatch Logs.
- **Tools Used:** GitHub Actions, Docker.

## 8. PortfolioEdge

- **Dir:** [Portfolio](./Portfolio/PORTFOLIO-README.md)
- **Description:** A personal portfolio static website securely hosted on a private S3 bucket and cached globally, utilizing CI/CD for auto-deployments.
- **AWS Services Used:** S3, CloudFront, ACM, IAM.
- **Tools Used:** GitHub Actions.

## 9. TaskFlow

- **Dir:** [rds-ec2-taskapp](./rds-ec2-taskapp/RDS-EC2-TASKAPP-README.md)
- **Description:** A full-stack task manager demonstrating secure, private database connectivity. The app runs in Docker on EC2 and communicates with a private RDS database.
- **AWS Services Used:** EC2, RDS MySQL, VPC, Security Groups, IAM.
- **Tools Used:** Docker, Node.js, Express, MySQL.

---

## Practice Projects

Here are some smaller practice projects focused on individual AWS services, fundamental concepts, and self-contained tutorials.

## 1. Application Load Balancer (ALB)

- **Dir:** [PRACTICE/APPLICATION-LOAD-BALANCER](./PRACTICE/APPLICATION-LOAD-BALANCER/ALB-README.md)
- **Description:** A detailed overview and practice on setting up Application Load Balancers, routing HTTP/HTTPS traffic, and understanding OSI Layer 7 routing.
- **AWS Services Used:** Application Load Balancer.

## 2. Auto Scaling Group (ASG) with ELB

- **Dir:** [PRACTICE/AUTO-SCALING-GROUP-ELB](./PRACTICE/AUTO-SCALING-GROUP-ELB/ASG-README.md)
- **Description:** A setup demonstrating AWS Auto Scaling Groups working in tandem with Elastic Load Balancers to build high availability and self-healing infrastructure.
- **AWS Services Used:** EC2 Auto Scaling, Elastic Load Balancing.

## 3. EC2 - Elastic Compute Cloud

- **Dir:** [PRACTICE/EC2](./PRACTICE/EC2/EC2-README.md)
- **Description:** A foundational practice project focused on provisioning, connecting to, and managing individual Elastic Compute Cloud (EC2) instances.
- **AWS Services Used:** EC2.

## 4. S3 Static Website Hosting

- **Dir:** [PRACTICE/S3-STATIC-WEBSITE-HOSTING](./PRACTICE/S3-STATIC-WEBSITE-HOSTING/S3-STATIC-WEBSITE-HOSTING-README.md)
- **Description:** A project demonstrating how to host a static website securely and cost-effectively from a public Amazon S3 bucket.
- **AWS Services Used:** S3.

---
