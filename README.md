# DevSecOps CI/CD Pipeline — Flask + GitHub Actions + Docker + AWS EC2
---

A production-grade, end-to-end DevSecOps CI/CD pipeline built from scratch. This project deploys a simple Python (Flask) application using GitHub Actions, Docker, and AWS EC2 — with security, quality gates, and a manual approval gate baked in at every stage.

---
My Production-CI-CD Pipeline Result

<img width="1899" height="871" alt="Screenshot 2026-03-12 053856" src="https://github.com/user-attachments/assets/19f2e3d9-d0f4-491e-b880-46373a910a65" />


---
CI/CD Pipeline Architecture
Trigger
The pipeline fires automatically on every git push to the main branch.

<img width="1536" height="1024" alt="CI-Cd" src="https://github.com/user-attachments/assets/5d4924b7-06fd-4dd9-b329-4cba40e11dcc" />

---

## DevSecOps Implementation: 

1. Non-Root Docker User  
The Dockerfile runs the application as a non-root user — a critical security practice that limits what an attacker can do if they compromise the running container.

2. Secrets and Credentials — Never Hardcoded  
All sensitive values (DockerHub credentials, EC2 SSH key, server IP) are stored as GitHub Actions Secrets and passed via environment variables. Nothing sensitive is ever committed to the repository.

<img width="1858" height="653" alt="Screenshot 2026-03-12 054106" src="https://github.com/user-attachments/assets/e246f05e-7a9a-4ee4-9b82-2cf27f9d9222" />


4. Docker Image Vulnerability Scan(Trivy)  
A dedicated images-scan job scans the Docker image for known vulnerabilities before it is pushed to DockerHub or deployed to production. The pipeline halts if critical CVEs are found.

## 🛑 Manual Approval Gate — Environment Protection  
Before deploying to EC2, the pipeline pauses and waits for a human to approve. This prevents broken or untested code from reaching production automatically.
How it works:

The deploy job is linked to a GitHub Environment named production.  
That environment has a required reviewer protection rule configured under Settings → Environments.  
When the pipeline reaches the deploy step, it pauses and sends a notification.  
A reviewer approves or rejects directly from the GitHub Actions UI.  
Only after approval does the pipeline SSH into EC2 and run the container.  

---
Screenshot of Reviewer Protection

<img width="1910" height="855" alt="Screenshot 2026-03-12 045547" src="https://github.com/user-attachments/assets/9e75bd3b-94ff-4378-b244-ba902a28bd4e" />

Afrer Approve on Ec2 instance Application is Deployed:  

<img width="1412" height="230" alt="Screenshot 2026-03-12 053834" src="https://github.com/user-attachments/assets/70330e85-2d9d-4f23-b23b-d7fc06bf80b6" />

Final Result we can access through the browser:

<img width="1888" height="949" alt="image" src="https://github.com/user-attachments/assets/9858f784-6685-40f1-b857-3d1eb43b06fa" />



---

## 🐛 Debugging — Learning Through Failures  
Every error during development was a lesson. Key problems solved:  

* **workflow_run vs workflow_call**
  `workflow_run` triggers separate pipeline runs which makes the pipeline messy in the Actions tab.
  `workflow_call` creates one unified and visual CI/CD pipeline, which is better for production.

* **Secrets not passed to reusable workflows**
  Reusable workflows do not automatically receive secrets from the parent workflow.
  Fixed by adding `secrets: inherit` to the job call.

* **Incorrect job dependency (`needs`)**
  Wrong dependency order caused jobs to run out of order or skip execution.
  Fixed by defining the correct pipeline order:
  `lint → test → artifact → image-scan → docker-push → deploy`

* **Non-root container permission error**
  Container crashed because files were owned by `root` while running as a non-root user.
  Fixed by setting proper file ownership in the Dockerfile before switching the user.

* **Environment approval not triggering**
  GitHub Environments must be created manually in **Repository Settings → Environments**.
  They are not automatically created from workflow YAML.

<img width="1919" height="762" alt="Screenshot 2026-03-12 054016" src="https://github.com/user-attachments/assets/45d4221e-5bd2-49b9-bf68-8581c3b5294c" />

  
---
## Key Takeaways

Test individually before combining — running each job solo with workflow_run before wiring everything together with workflow_call is the right approach.

<img width="1834" height="821" alt="Screenshot 2026-03-12 054146" src="https://github.com/user-attachments/assets/36135219-8ed5-48fa-8753-0dc25823084c" />

<img width="1834" height="821" alt="Screenshot 2026-03-12 054146" src="https://github.com/user-attachments/assets/82b74f91-12a6-4356-85fd-50d51b142f8e" />

---

## 🔐 DevSecOps Principles Learned

* **Security must be inside the pipeline** — non-root containers, image scanning, and secret management are requirements, not optional extras.
* **Manual approval protects production** — GitHub Environments with required reviewers add a human checkpoint before deployment.
* **Pin GitHub Action versions** — using `@v4` is safer than `@latest` to avoid unexpected breaking changes.
* **Failures are part of learning** — every red ❌ in GitHub Actions helped me understand CI/CD and debugging much better.


