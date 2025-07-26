# Ransferrx Infrastructure - Terraform Configuration

## 🚨 **IMPORTANT: USAGE RESTRICTIONS**

> **⚠️ PROPRIETARY AND CONFIDENTIAL - UNAUTHORIZED USE PROHIBITED** ⚠️
> 
> **This infrastructure configuration contains proprietary code for the Ransferrx healthcare pharmacy management system.**
> 
> **❌ YOU ARE NOT ALLOWED TO USE, COPY, MODIFY, OR DISTRIBUTE THIS CODE WITHOUT EXPLICIT PERMISSION.**
> 
> **✅ If you need to use this code, you MUST contact us first for licensing approval: minamdoss@outlook.com**

---

> **PROPRIETARY AND CONFIDENTIAL** - This directory contains the Azure infrastructure configuration for the Ransferrx healthcare pharmacy management system. Unauthorized access, copying, or distribution is strictly prohibited.

## 🏗️ **Infrastructure Overview**

This Terraform configuration deploys a comprehensive Azure infrastructure for the Ransferrx healthcare pharmacy management system, designed for HIPAA compliance and high availability.

## 📁 **Configuration Files**

- **`main.tf`** - Main resource definitions and infrastructure components
- **`provider.tf`** - Azure provider configuration
- **`variables.tf`** - Variable definitions (sensitive data)
- **`terraform.tf`** - Terraform version and backend configuration
- **`terraform.tfvars.example`** - Example variables file (DO NOT commit actual values)

## 🚀 **Quick Start**

### **Prerequisites**
- **Azure CLI** installed and authenticated
- **Terraform** (version 1.0+)
- **Azure Subscription** with appropriate permissions

### **Deployment Steps**

1. **Clone and Navigate**
   ```bash
   cd Terraform/
   ```

2. **Configure Variables**
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your actual values
   ```

3. **Initialize Terraform**
   ```bash
   terraform init
   ```

4. **Plan Deployment**
   ```bash
   terraform plan
   ```

5. **Apply Configuration**
   ```bash
   terraform apply
   ```

## 🏥 **Deployed Services**

### **Core Infrastructure**
- **Resource Group**: `rg-ransferrx-prod`
- **Virtual Network**: `ransferrx-vnet` with multiple subnets
- **Network Security Groups**: Separate NSGs for each subnet

### **Data Services**
- **Azure SQL Server**: `ransferrx-sql-primary`
- **Azure SQL Database**: `ransferrx-db`
- **Private Endpoints**: Secure database connectivity

### **Storage Services**
- **Log Archive Storage**: `ransferrxlogarchive` (ZRS)
- **Queue Storage**: `ransferrxqueue` (LRS)
- **Function Storage**: `rgransferrxprodb884` (LRS)

### **Security Services**
- **Key Vault**: `ransferrx-keyvault` (Premium SKU)
- **Private DNS Zones**: For private endpoint resolution
- **Network Security**: Comprehensive security groups

### **Application Services**
- **Function App**: `ransferrx-retry-handler`
- **Service Plans**: Linux EP1 and P1v3 plans
- **Application Insights**: Monitoring and telemetry

### **Monitoring & Logging**
- **Log Analytics Workspace**: `ransferrx-law`
- **Application Insights**: `ransferrx-api`, `ransferrx-retry-handler`
- **Monitor Action Groups**: Alerting and notifications

## 🔒 **Security Features**

### **Network Security**
- **Private Endpoints**: Secure database and storage access
- **Network Security Groups**: Traffic filtering by subnet
- **Virtual Network**: Isolated network environment

### **Data Protection**
- **Encryption**: All data encrypted at rest and in transit
- **Key Vault**: Centralized secrets management
- **Access Control**: Role-based access control (RBAC)

### **Compliance**
- **HIPAA**: Healthcare data protection compliance
- **Audit Logging**: Comprehensive audit trails
- **Monitoring**: Real-time security monitoring

## 📚 **Documentation**

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Detailed deployment guide
- **[SERVICES.md](SERVICES.md)** - Service-specific documentation
- **[SECURITY_FIXES.md](SECURITY_FIXES.md)** - Security fixes and best practices
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Development guidelines
- **[SECURITY.md](SECURITY.md)** - Security policies

## 🔧 **Maintenance**

### **Regular Tasks**
- **Monthly**: Review and rotate secrets
- **Quarterly**: Update Terraform versions and providers
- **Annually**: Security assessments and compliance reviews

### **Monitoring**
- **Azure Monitor**: Infrastructure health monitoring
- **Application Insights**: Application performance monitoring
- **Log Analytics**: Centralized logging and analysis

## 🆘 **Support**

### **Infrastructure Issues**
- **Deployment Problems**: Check [DEPLOYMENT.md](DEPLOYMENT.md)
- **Configuration Issues**: Review Terraform documentation
- **Security Concerns**: Contact Security team

### **Emergency Contacts**
- **Infrastructure Emergency**: devops@ransferrx.com
- **Security Emergency**: security@ransferrx.com

## 📄 **Legal**

### **Proprietary Information**
This infrastructure configuration contains proprietary and confidential information of Ransferrx. Unauthorized access, copying, modification, or distribution is strictly prohibited.

### **Licensing Inquiries**
**If you need to use this infrastructure code or would like to license any part of this configuration, please contact us:**

- **Email**: minamdoss@outlook.com
- **Subject**: "LICENSING INQUIRY: [Brief Description of Use Case]"

---

**© 2025 Ransferrx. All rights reserved.** 