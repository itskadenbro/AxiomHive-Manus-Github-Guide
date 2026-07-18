# AxiomHive Technical Reference Manual

This document provides technical specifications for system administrators and developers maintaining the AxiomHive infrastructure.

## 1. System Requirements

| Component | Minimum Specification | Recommended Specification |
| :--- | :--- | :--- |
| **Compute** | 64-core CPU, 256GB RAM | 128-core CPU, 512GB RAM |
| **Storage** | 10TB NVMe (High IOPS) | 50TB NVMe (RAID 10) |
| **Network** | 10Gbps Dedicated Fiber | 40Gbps Low-Latency Interconnect |
| **GPU** | 4x NVIDIA A100 (80GB) | 8x NVIDIA H100 (80GB) |

## 2. API Architecture

AxiomHive exposes a RESTful API for integration with external intelligence sources.

### 2.1 Authentication
All API requests must include a valid JWT in the Authorization header. Tokens are issued via the Secure Token Service (STS) and rotate every 60 minutes.

### 2.2 Endpoint Overview
- `GET /v1/intelligence/threats`: Retrieve current threat levels.
- `POST /v1/ingestion/raw`: Securely upload raw sensor data.
- `GET /v1/models/explain/{id}`: Retrieve the reasoning path for a specific AI output.

## 3. Database Schema Overview

AxiomHive utilizes a polyglot persistence strategy:
- **Relational (PostgreSQL)**: Manages user roles, permissions, and system metadata.
- **Document (MongoDB)**: Stores flexible intelligence reports and unstructured text.
- **Time-Series (Cassandra)**: Optimized for high-velocity sensor data and audit logs.

## 4. Maintenance and Backups

- **Hot Backups**: Performed every 4 hours for the relational database.
- **Snapshotting**: Daily snapshots of the entire storage cluster.
- **Security Patching**: Automated weekly patching with a zero-downtime rolling update strategy.
