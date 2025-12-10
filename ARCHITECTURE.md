# Architecture Documentation

## System Overview

This is a multi-tenant organization management service where each organization gets its own isolated data collection within a shared MongoDB database.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Client Layer                         │
│  (Web Browser, Mobile App, API Clients)                 │
└────────────────────┬────────────────────────────────────┘
                     │ HTTPS
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   FastAPI Server                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Routes Layer                                     │  │
│  │  - /org/* (Organization Management)               │  │
│  │  - /admin/* (Authentication)                      │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Business Logic Layer                             │  │
│  │  - Organization Service                           │  │
│  │  - Authentication Service                         │  │
│  │  - Collection Management                          │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Security Layer                                   │  │
│  │  - JWT Token Generation/Validation                │  │
│  │  - Password Hashing (bcrypt)                      │  │
│  │  - Authorization Middleware                       │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │ Motor (Async Driver)
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   MongoDB Database                       │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Master Database (master_db)                      │  │
│  │  ┌────────────────────────────────────────────┐  │  │
│  │  │  organizations collection                   │  │  │
│  │  │  - organization_name                        │  │  │
│  │  │  - collection_name                          │  │  │
│  │  │  - admin_id                                 │  │  │
│  │  │  - admin_email                              │  │  │
│  │  │  - created_at                               │  │  │
│  │  └────────────────────────────────────────────┘  │  │
│  │  ┌────────────────────────────────────────────┐  │  │
│  │  │  admins collection                          │  │  │
│  │  │  - email                                    │  │  │
│  │  │  - password (hashed)                        │  │  │
│  │  │  - organization_name                        │  │  │
│  │  │  - created_at                               │  │  │
│  │  └────────────────────────────────────────────┘  │  │
│  │  ┌────────────────────────────────────────────┐  │  │
│  │  │  org_acme_corp (Dynamic Collection)        │  │  │
│  │  │  - (organization-specific data)             │  │  │
│  │  └────────────────────────────────────────────┘  │  │
│  │  ┌────────────────────────────────────────────┐  │  │
│  │  │  org_tech_startup (Dynamic Collection)     │  │  │
│  │  │  - (organization-specific data)             │  │  │
│  │  └────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Organization Creation Flow

```
Client                FastAPI              MongoDB
  │                      │                    │
  │  POST /org/create    │                    │
  ├─────────────────────>│                    │
  │                      │                    │
  │                      │ Check if org exists│
  │                      ├───────────────────>│
  │                      │<───────────────────┤
  │                      │                    │
  │                      │ Hash password      │
  │                      │                    │
  │                      │ Insert admin       │
  │                      ├───────────────────>│
  │                      │<───────────────────┤
  │                      │                    │
  │                      │ Insert org metadata│
  │                      ├───────────────────>│
  │                      │<───────────────────┤
  │                      │                    │
  │                      │ Create collection  │
  │                      ├───────────────────>│
  │                      │<───────────────────┤
  │                      │                    │
  │<─────────────────────┤                    │
  │  201 Created         │                    │
```

### 2. Authentication Flow

```
Client                FastAPI              MongoDB
  │                      │                    │
  │  POST /admin/login   │                    │
  ├─────────────────────>│                    │
  │                      │                    │
  │                      │ Find admin by email│
  │                      ├───────────────────>│
  │                      │<───────────────────┤
  │                      │                    │
  │                      │ Verify password    │
  │                      │                    │
  │                      │ Generate JWT token │
  │                      │                    │
  │<─────────────────────┤                    │
  │  { access_token }    │                    │
```

### 3. Protected Operation Flow

```
Client                FastAPI              MongoDB
  │                      │                    │
  │  DELETE /org/delete  │                    │
  │  + Bearer Token      │                    │
  ├─────────────────────>│                    │
  │                      │                    │
  │                      │ Validate JWT       │
  │                      │                    │
  │                      │ Check authorization│
  │                      ├───────────────────>│
  │                      │<───────────────────┤
  │                      │                    │
  │                      │ Drop collection    │
  │                      ├───────────────────>│
  │                      │<───────────────────┤
  │                      │                    │
  │                      │ Delete org metadata│
  │                      ├───────────────────>│
  │                      │<───────────────────┤
  │                      │                    │
  │<─────────────────────┤                    │
  │  200 OK              │                    │
```

## Security Architecture

### Authentication & Authorization

1. **Password Security**
   - Passwords hashed using bcrypt (cost factor: 12)
   - Never stored in plain text
   - Salt automatically generated per password

2. **JWT Tokens**
   - HS256 algorithm
   - Contains: email, organization_id, organization_name
   - Expiration: 30 minutes (configurable)
   - Stateless authentication

3. **Authorization**
   - Token validation on protected routes
   - Organization ownership verification
   - Admin-only operations enforced

## Database Schema

### organizations Collection
```json
{
  "_id": ObjectId,
  "organization_name": "acme_corp",
  "collection_name": "org_acme_corp",
  "admin_id": "admin_object_id",
  "admin_email": "admin@acme.com",
  "created_at": ISODate
}
```

### admins Collection
```json
{
  "_id": ObjectId,
  "email": "admin@acme.com",
  "password": "$2b$12$hashed_password",
  "organization_name": "acme_corp",
  "created_at": ISODate
}
```

### org_<name> Collections (Dynamic)
```json
{
  "_id": ObjectId,
  "initialized": true,
  "created_at": ISODate,
  "organization": "acme_corp",
  // ... organization-specific fields
}
```

## Scalability Considerations

### Current Limitations

1. **Single Database Instance**
   - All organizations share one MongoDB instance
   - Limited by single server resources
   - No geographic distribution

2. **Collection Proliferation**
   - Each org creates a new collection
   - MongoDB has collection limits (~24,000)
   - Performance degrades with many collections

3. **No Caching**
   - Every request hits database
   - Repeated queries not optimized
   - Higher latency for frequent operations

### Scaling Solutions

#### Phase 1: Vertical Scaling (0-1000 orgs)
- Increase MongoDB server resources
- Add indexes for faster queries
- Implement connection pooling

#### Phase 2: Horizontal Scaling (1000-10,000 orgs)
```
┌──────────────┐
│ Load Balancer│
└──────┬───────┘
       │
   ┌───┴───┐
   │       │
┌──▼──┐ ┌──▼──┐
│ API │ │ API │  (Multiple instances)
└──┬──┘ └──┬──┘
   │       │
   └───┬───┘
       │
   ┌───▼────┐
   │ Redis  │  (Caching layer)
   └───┬────┘
       │
   ┌───▼────────┐
   │  MongoDB   │
   │  Replica   │
   │    Set     │
   └────────────┘
```

#### Phase 3: Microservices (10,000+ orgs)
```
┌─────────────────────────────────────────┐
│          API Gateway (Kong)              │
└────┬──────────┬──────────┬──────────────┘
     │          │          │
┌────▼────┐ ┌──▼────┐ ┌───▼──────┐
│  Auth   │ │  Org  │ │  Data    │
│ Service │ │Service│ │ Service  │
└────┬────┘ └──┬────┘ └───┬──────┘
     │         │           │
     └─────────┴───────────┘
               │
     ┌─────────┴─────────┐
     │                   │
┌────▼────┐      ┌───────▼──────┐
│  Redis  │      │   MongoDB    │
│ Cluster │      │   Sharded    │
└─────────┘      │   Cluster    │
                 └──────────────┘
```

## Trade-offs Analysis

### Current Design

**Pros:**
- ✅ Simple to understand and implement
- ✅ Fast development time
- ✅ Easy to deploy and maintain
- ✅ Good for MVP and small scale
- ✅ Cost-effective for startups

**Cons:**
- ❌ Limited scalability
- ❌ Single point of failure
- ❌ No geographic distribution
- ❌ Collection limit constraints
- ❌ No caching layer

### Alternative: Database per Organization

**Pros:**
- ✅ True isolation
- ✅ Better scalability
- ✅ Easier to backup/restore individual orgs
- ✅ Can distribute across servers

**Cons:**
- ❌ More complex connection management
- ❌ Higher operational overhead
- ❌ More expensive (more database instances)
- ❌ Harder to implement cross-org features

### Alternative: Shared Tables with Tenant ID

**Pros:**
- ✅ Simpler database structure
- ✅ Easier to query across organizations
- ✅ Better for analytics

**Cons:**
- ❌ Less isolation
- ❌ Risk of data leakage
- ❌ Harder to scale individual orgs
- ❌ Complex query filtering

## Recommended Production Setup

```yaml
Infrastructure:
  - Load Balancer: AWS ALB / Nginx
  - API Servers: 3+ instances (auto-scaling)
  - Cache: Redis Cluster (3 nodes)
  - Database: MongoDB Atlas (M30+, Replica Set)
  - Monitoring: Prometheus + Grafana
  - Logging: ELK Stack
  - CI/CD: GitHub Actions
  
Security:
  - HTTPS only (TLS 1.3)
  - Rate limiting (100 req/min per IP)
  - DDoS protection (Cloudflare)
  - Regular security audits
  - Automated backups (daily)
  
Performance:
  - Response time: < 200ms (p95)
  - Availability: 99.9% uptime
  - Database indexes on all query fields
  - Connection pooling (100 connections)
```

## Conclusion

This architecture is **excellent for MVP and small-to-medium scale** (up to 1000 organizations). For larger scale, consider:

1. Implementing Redis caching
2. Moving to MongoDB sharding
3. Splitting into microservices
4. Adding message queues for async operations
5. Implementing proper monitoring and alerting