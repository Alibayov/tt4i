**TestOps Task Report**

# **1. Project Overview**
This document provides a detailed explanation of the TestOps technical task execution. It includes an overview of the implemented Selenium test automation, Kubernetes deployment, and AWS EKS setup.

# **2. Technologies Used**
- **Programming Language**: Python
- **Test Framework**: Selenium
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **Cloud Provider**: AWS (Amazon EKS)
- **CI/CD & Deployment**: kubectl, AWS CLI

# **3. Selenium Test Automation**
## **3.1. Test Cases**
The Selenium tests cover the following functionalities:
1. Visiting Insider Homepage and verifying its availability.
2. Navigating to the **Company > Careers** section and checking for expected elements.
3. Filtering **Quality Assurance** job postings by **Location: Istanbul, Turkey**.
4. Ensuring all job listings contain the expected **department and location**.
5. Clicking the "View Role" button and verifying redirection to the **Lever application form**.

## **3.2. Test Execution Strategy**
- The tests are executed inside a **Kubernetes pod (test-controller)**.
- A **headless Chrome Node** is used for running the tests.
- The **test logs** are collected for verification.

# **4. Kubernetes Deployment**
## **4.1. Kubernetes Architecture**
- **Test Controller Pod**: Manages and runs Selenium tests.
- **Chrome Node Pod**: Runs headless Chrome for browser-based testing.
- **HPA (Horizontal Pod Autoscaler)**: Ensures scalability of Chrome Node.

## **4.2.1 Deployment Steps**
1. Deploy Kubernetes Resources using the automated script:
   ```bash
   python deploy_and_run_tests.py
   ```
   This script:
   - Connects to the **AWS EKS cluster**
   - Deploys the required **Kubernetes resources**
   - Verifies that all **pods are running**
## **4.2.2 Deployment Steps (manual)**

To deploy the test infrastructure on Kubernetes, follow these steps:

Ensure Kubernetes Context is Set
   ```bash
kubectl config use-context <your-eks-cluster-name>
   ```
Apply the Chrome Node Deployment
   ```bash
kubectl apply -f chrome-node.yaml
   ```
Apply the Chrome Node HPA Configuration
   ```bash
kubectl apply -f chrome-node-hpa.yaml
   ```
Wait for Chrome Node to be Ready (Optional Verification)
   ```bash
kubectl get pods -l app=chrome-node
   ```
Apply the Test Controller Deployment
   ```bash
kubectl apply -f test-controller.yaml
   ```
Verify All Pods are Running
   ```bash
kubectl get pods
   ```

Monitor Logs for Test Execution
### **Screenshots of Deployment:**
![image](https://github.com/user-attachments/assets/75894e43-e7f5-4e7a-8a7c-5ad9a027ea82)
![image](https://github.com/user-attachments/assets/e0196088-8f55-4afd-ac50-d0a271527934)

### **Logs of test-controller pod:**

![image](https://github.com/user-attachments/assets/73f27b0d-bda9-4d7c-ac18-195f280b9806)
![image](https://github.com/user-attachments/assets/be3603a0-b11c-486e-97d6-f56cb15a2290)


📌 **Script runs inside a loop to continuously monitor pod status.**

### **Logs of chrome-node:**
![image](https://github.com/user-attachments/assets/5ebec6b2-1cde-4a05-acce-e6c4ef063127)


# **5. AWS EKS Screenshots**
![image](https://github.com/user-attachments/assets/6bb05b94-f45e-48aa-9d29-d9e23d076179)
![image](https://github.com/user-attachments/assets/694782e8-4784-4f75-830f-7101db3d570d)

## **5.1. Cluster Setup**
The Kubernetes cluster was deployed on **AWS EKS**:
- **Cluster Name**: eks-cluster
- **Instance Type**: t3.medium
- **Tools Used**: AWS CLI, eksctl, kubectl

### **Cluster Nodes:**
![image](https://github.com/user-attachments/assets/b854835b-d8f7-4726-b9cd-eb43f8a4d709)

### **Current Setup on AWS:**
✅ **2x t3.medium nodes** for **EKS cluster**
✅ **1x t2.micro node** for **free-tier EC2 instance**

![image](https://github.com/user-attachments/assets/bb03cf93-907a-4b4e-b350-b0db9325ad6f)


---

📌 **Prepared by:** `[Shahriyar Alibayov]`

