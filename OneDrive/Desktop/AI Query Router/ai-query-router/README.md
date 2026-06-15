# AI Query Router (AQR)

An intelligent, high-availability microservice architecture that dynamically routes incoming LLM queries between Groq and Gemini based on performance metrics, payload sizes, token budgets, and live endpoint availability. Built with FastAPI, automated via a multi-stage GitLab CI/CD pipeline, and containerized under Kubernetes (k3s) orchestration.

---

## 🚀 Cloud Infrastructure & Architecture

The application is deployed inside a production-grade infrastructure on a secure AWS EC2 host:
* **Automation (CI/CD):** Integrated via GitLab CI/CD pipelines that continuously pull, test, and build verified code increments, pushing final tagged layers directly into a private AWS Elastic Container Registry (ECR).
* **Orchestration Layer:** Managed by a lightweight **Kubernetes (k3s)** cluster runtime.
* **Service Delivery:** Configured as an explicit, continuous foreground `uvicorn` deployment scaled to a balanced runtime footprint and exposed publicly via a load-balanced **Kubernetes NodePort Service** on port `30080`.

---

## 🛠️ Production Environment Tuning & Optimizations

During deployment on resource-constrained host environments (such as an AWS `t2.micro` tier), the following enterprise-level engineering modifications were executed to secure system stability and break through resource locks:

### 1. Virtual Memory Scaling (Linux Swap Allocation)
To prevent sudden kernel memory chokes and protect core services against Out-Of-Memory (OOM) killer terminations, a **2.0Gi low-latency emergency Swap space** was provisioned:
```bash
# Allocate, lock down, and mount a 2GB virtual memory cushion
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Make the mount configuration permanent across system reboots
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
2. Resolving Node Pressure Locks (Storage Cleanup)
When image builds and stale container layers trigger a cluster-wide node.kubernetes.io/disk-pressure taint lock (blocking the scheduler from initiating pending pods), run the following sequence to purge system bloat:

Bash
# Wipe dangling build caches, prune system log files, and flush the package manager
sudo docker system prune -a -f --volumes
sudo journalctl --vacuum-size=100M
sudo apt-get clean

# Restart the orchestrator core to re-evaluate storage health and lift the taint lock
sudo systemctl restart k3s
3. Ingress Routing Clearance (AWS Security Firewall)
To bridge public traffic down into the internal cluster, modify your active AWS EC2 Inbound Rules security panel (launch-wizard-2) to white-list ingress on the NodePort range:

Rule Protocol / Type: Custom TCP

Target Port Range: 30080 (Kubernetes NodePort Service Ingress)

Source Access Vector: Anywhere-IPv4 (0.0.0.0/0)

🎯 Production Verification & Health Diagnostics
The live, load-balanced container deployment can be queried and monitored remotely from any authenticated laptop shell terminal:

PowerShell
# Execute diagnostic check using Windows PowerShell
Invoke-RestMethod -Uri [http://13.204.143.119:30080/health](http://13.204.143.119:30080/health)
Bash
# Execute diagnostic check using standard Linux/macOS cURL
curl [http://13.204.143.119:30080/health](http://13.204.143.119:30080/health)
Expected Production Response Matrix:
JSON
{
  "status": "ok",
  "service": "ai-query-router"
}

Save this, commit it, push it, and you're good to go! Your project looks completely professional now.