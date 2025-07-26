# Ransferrx - Healthcare Pharmacy Management System

## 🚨 **IMPORTANT: USAGE RESTRICTIONS**

> **⚠️ PROPRIETARY AND CONFIDENTIAL - UNAUTHORIZED USE PROHIBITED** ⚠️
> 
> **This repository contains proprietary code for the Ransferrx healthcare pharmacy management system.**
> 
> **❌ YOU ARE NOT ALLOWED TO USE, COPY, MODIFY, OR DISTRIBUTE THIS CODE WITHOUT EXPLICIT PERMISSION.**
> 
> **✅ If you need to use this code, you MUST contact us first for licensing approval.**

---

## 🏥 **Project Overview**

Ransferrx is a comprehensive healthcare pharmacy management system that provides secure, HIPAA-compliant prescription transfer and management capabilities. This repository contains both the Azure infrastructure (Terraform) and the core API services.

## 📁 **Repository Structure**

```
Ransferrx/
├── Terraform/                 # Azure Infrastructure as Code
│   ├── main.tf               # Main Terraform configuration
│   ├── provider.tf           # Azure provider configuration
│   ├── variables.tf          # Variable definitions
│   ├── terraform.tf          # Terraform settings
│   ├── terraform.tfvars.example # Example variables file
│   ├── README.md             # Infrastructure documentation
│   ├── DEPLOYMENT.md         # Deployment guide
│   ├── SERVICES.md           # Service documentation
│   ├── SECURITY_FIXES.md     # Security fixes documentation
│   ├── CONTRIBUTING.md       # Contribution guidelines
│   └── SECURITY.md           # Security policy
├── ransfer_api/              # RX Transfer Service (FastAPI)
│   ├── app/                  # FastAPI application
│   ├── tests/                # Comprehensive test suite
│   ├── README.md             # API documentation
│   └── DOCUMENTATION.md      # Technical documentation
├── api/                      # Main API documentation
├── .github/                  # GitHub workflows and templates
├── README.md                 # This file
├── LICENSE                   # Proprietary license
└── .gitignore               # Git ignore rules
```

## 🚀 **Quick Start**

### **Infrastructure Deployment**
```bash
# Navigate to Terraform directory
cd Terraform/

# Copy example variables file
cp terraform.tfvars.example terraform.tfvars

# Edit with your actual values
nano terraform.tfvars

# Initialize and deploy
terraform init
terraform plan
terraform apply
```

### **API Development**
```bash
# Navigate to API directory
cd ransfer_api/

# Install dependencies
pip install -r requirements.txt

# Run development server
python -m uvicorn app.main:app --reload

# Run tests
python tests/run_comprehensive_tests.py
```

## 🏗️ **System Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend Application                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                    Ransferrx API                            │
│              (FastAPI - Prescription Validation)            │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                    Azure Infrastructure                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Azure     │  │   Storage   │  │   Private   │         │
│  │   SQL DB    │  │   Accounts  │  │   Endpoints │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Key       │  │   Log       │  │   Monitor   │         │
│  │   Vault     │  │   Analytics │  │   & Alert   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

## 📋 **Key Features**

### **Infrastructure**
- **Azure SQL Database**: Secure prescription data storage
- **Azure Key Vault**: Secrets and certificate management
- **Storage Accounts**: Log archiving and queue management
- **Private Endpoints**: Secure network connectivity
- **Application Insights**: Monitoring and telemetry
- **Network Security**: Comprehensive security groups

### **API Services**
- **Prescription Validation**: NCPDP SCRIPT 2017071 compliance
- **Digital Signature Verification**: DEA EPCS requirements
- **Comprehensive Testing**: 100% test coverage
- **HIPAA Compliance**: Full healthcare data protection
- **Performance Monitoring**: Real-time metrics and logging

## 🔗 **API Endpoints**

Key API endpoints include:
- `GET /health` - Health check
- `POST /api/v1/transfers/validate-transfer` - Validate prescription transfer
- `POST /api/v1/transfers/verify-signature` - Verify digital signature

## 📚 **Documentation**

### **Infrastructure**
- **[Terraform/README.md](Terraform/README.md)** - Infrastructure overview
- **[Terraform/DEPLOYMENT.md](Terraform/DEPLOYMENT.md)** - Deployment guide
- **[Terraform/SERVICES.md](Terraform/SERVICES.md)** - Service documentation
- **[Terraform/SECURITY_FIXES.md](Terraform/SECURITY_FIXES.md)** - Security fixes

### **API**
- **[ransfer_api/README.md](ransfer_api/README.md)** - API overview
- **[ransfer_api/DOCUMENTATION.md](ransfer_api/DOCUMENTATION.md)** - Technical documentation
- **[api/README.md](api/README.md)** - API development guide

## 🔒 **Security & Compliance**

### **Security Features**
- **Private Repository**: Access restricted to authorized personnel only
- **Encrypted Data**: All data encrypted in transit and at rest
- **Access Control**: Role-based authentication and authorization
- **Audit Logging**: Comprehensive audit trails
- **Network Security**: Private endpoints and security groups

### **Compliance Standards**
- **HIPAA**: Full healthcare data protection compliance
- **DEA EPCS**: Electronic prescriptions for controlled substances
- **NCPDP SCRIPT**: Standard prescription transfer protocol
- **SOC 2**: Security and availability controls

## 🛠️ **Development**

### **Prerequisites**
- **Azure CLI**: For infrastructure management
- **Terraform**: For infrastructure as code
- **Python 3.8+**: For API development
- **Node.js**: For frontend development (if applicable)

### **Development Workflow**
1. **Infrastructure**: Deploy using Terraform
2. **API Development**: Use FastAPI framework
3. **Testing**: Comprehensive test suite included
4. **Deployment**: Automated CI/CD pipelines

## 🔄 **Maintenance**

### **Regular Tasks**
- **Daily**: Monitor application health and performance
- **Weekly**: Review security logs and access patterns
- **Monthly**: Review and rotate secrets
- **Quarterly**: Security assessments and compliance reviews

### **Monitoring**
- **Application Insights**: Real-time performance monitoring
- **Log Analytics**: Centralized logging and analysis
- **Azure Monitor**: Infrastructure monitoring and alerting

## 🆘 **Support**

### **Internal Support**
- **Infrastructure Issues**: Contact DevOps team
- **API Issues**: Contact Backend Development team
- **Security Concerns**: Contact Security team

### **Emergency Contacts**
- **Infrastructure Emergency**: devops@ransferrx.com
- **API Emergency**: api-support@ransferrx.com
- **Security Emergency**: security@ransferrx.com

## 📄 **Legal & Licensing**

### **Proprietary Information**
This repository contains proprietary and confidential information of Ransferrx. Unauthorized access, copying, modification, or distribution is strictly prohibited.

### **Usage Restrictions**
**❌ YOU ARE NOT ALLOWED TO:**
- Use this code without explicit permission
- Copy, modify, or distribute this code
- Reverse engineer any part of this system
- Use this code for commercial purposes
- Share this code with unauthorized parties

### **Licensing Inquiries**
**✅ IF YOU NEED TO USE THIS CODE, YOU MUST:**

**Contact us for licensing approval:**
- **Email**: minamdoss@outlook.com
- **Subject**: "LICENSING INQUIRY: [Brief Description of Use Case]"
- **Include**: 
  - Your organization name
  - Intended use case
  - Contact information
  - Timeline for implementation
  - Number of users/systems

**We will review all licensing requests and respond within 5 business days.**

### **Legal Notice**
Any unauthorized use, copying, or distribution of this code may result in legal action. This code is protected by copyright and other intellectual property laws.

---

**© 2025 Ransferrx. All rights reserved.**
**Unauthorized use is strictly prohibited.** 