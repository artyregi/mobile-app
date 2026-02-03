# B2B Mobile Application

A comprehensive B2B mobile application built with **Expo (React Native)** for the frontend and **FastAPI (Python)** for the backend, featuring role-based access control, order management, and multi-tenant architecture.

## 🚀 Features

### Phase 1 (MVP) - ✅ Complete
- **User Authentication**
  - JWT-based authentication with 7-day token expiry
  - Email + Mobile login support
  - Secure password hashing with bcrypt
  - Secure token storage using expo-secure-store

- **Role-Based Access Control**
  - **Admin**: Full system access (manage users, products, vendors, orders)
  - **Sales**: Create/manage orders, view inventory, track payments
  - **Buyer**: View orders, track status, make payments

- **Dashboard**
  - Role-specific stats and metrics
  - Real-time data updates with pull-to-refresh
  - Quick action buttons

- **Multi-Tenant Architecture**
  - Company-level data isolation
  - Secure company-based user management

- **Mobile-First UI/UX**
  - Bottom tab navigation (5 tabs)
  - Responsive design for iOS & Android
  - Clean, modern interface
  - Native-feeling interactions

### Coming Soon
- **Phase 2**: Product & Inventory Management
- **Phase 3**: Order Management (full lifecycle)
- **Phase 4**: Vendor Management
- **Phase 5**: Payment Processing (QR codes, bank details)
- **Phase 6**: Push Notifications

---

## 📋 Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running Locally](#running-locally)
- [Deployment](#deployment)
- [How to Use the Application](#how-to-use-the-application)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)

---

## 🛠 Prerequisites

### Required Software
- **Node.js**: v18+ ([Download](https://nodejs.org/))
- **Python**: 3.11+ ([Download](https://www.python.org/))
- **MongoDB**: 4.4+ ([Download](https://www.mongodb.com/try/download/community))
- **Yarn**: 1.22+ (`npm install -g yarn`)
- **Expo CLI**: Latest (`npm install -g expo-cli`)

### For Mobile Testing
- **Expo Go App**: Install on your iOS/Android device
  - [iOS App Store](https://apps.apple.com/app/expo-go/id982107779)
  - [Google Play Store](https://play.google.com/store/apps/details?id=host.exp.exponent)

---

## 📦 Installation

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd <your-project-folder>
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env  # If example exists, or create .env manually
```

**Configure `.env` file:**
```env
MONGO_URL=mongodb://localhost:27017/
DB_NAME=b2b_mobile_app
SECRET_KEY=your-super-secret-key-change-in-production
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
yarn install

# Set up environment variables
```

**Configure `.env` file:**
```env
EXPO_PUBLIC_BACKEND_URL=http://localhost:8001
```

---

## 🏃 Running Locally

### 1. Start MongoDB
```bash
# macOS/Linux
mongod --dbpath ~/data/db

# Windows
mongod --dbpath C:\data\db

# Or use MongoDB Compass with default connection: mongodb://localhost:27017
```

### 2. Start Backend Server
```bash
cd backend
source venv/bin/activate  # Activate virtual environment
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

Backend will be available at: `http://localhost:8001`
API Documentation: `http://localhost:8001/docs` (Swagger UI)

### 3. Start Frontend (Expo)

#### For Web Development:
```bash
cd frontend
yarn start

# Or specifically for web:
yarn web
```

#### For Mobile Development:
```bash
cd frontend
yarn start
```

Then:
- **iOS**: Press `i` or scan QR code with Camera app (opens Expo Go)
- **Android**: Press `a` or scan QR code with Expo Go app
- **Web**: Press `w` or visit `http://localhost:3000`

---

## 🚀 Deployment

### Backend Deployment (FastAPI)

#### Option 1: Heroku
```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create new app
heroku create your-app-name

# Add MongoDB addon
heroku addons:create mongolab:sandbox

# Set environment variables
heroku config:set SECRET_KEY=your-production-secret-key

# Deploy
git subtree push --prefix backend heroku main

# Or create a separate git repo for backend
cd backend
git init
git add .
git commit -m "Initial commit"
heroku git:remote -a your-app-name
git push heroku main
```

#### Option 2: Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
cd backend
railway init

# Add MongoDB
railway add

# Deploy
railway up
```

#### Option 3: Docker
```bash
cd backend

# Build Docker image
docker build -t b2b-backend .

# Run container
docker run -d -p 8001:8001 \
  -e MONGO_URL=your-mongo-connection-string \
  -e SECRET_KEY=your-secret-key \
  b2b-backend
```

**Create `Dockerfile` in backend:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001"]
```

### Frontend Deployment (Expo)

#### Option 1: Expo EAS Build (Native Apps)
```bash
cd frontend

# Install EAS CLI
npm install -g eas-cli

# Login to Expo
eas login

# Configure project
eas build:configure

# Build for iOS
eas build --platform ios

# Build for Android
eas build --platform android

# Submit to App Stores
eas submit --platform ios
eas submit --platform android
```

#### Option 2: Expo Web Build (Web App)
```bash
cd frontend

# Build for web
npx expo export:web

# Deploy to Vercel
npm install -g vercel
vercel --prod

# Or deploy to Netlify
npm install -g netlify-cli
netlify deploy --prod --dir web-build
```

#### Update Backend URL for Production
Update `frontend/.env`:
```env
EXPO_PUBLIC_BACKEND_URL=https://your-backend-url.com
```

---

## 📱 How to Use the Application

### First Time Setup

1. **Access the Application**
   - Web: Navigate to your deployed URL or `http://localhost:3000`
   - Mobile: Open Expo Go and scan the QR code

2. **Register a New Account**
   - Click "Register" on the login screen
   - Fill in your details:
     - Full Name
     - Email address
     - Mobile number (10-15 digits)
     - Select your role: **Admin**, **Sales**, or **Buyer**
     - Company name (optional, defaults to "Default Company")
     - Password (minimum 6 characters)
   - Click "Register"

3. **Automatic Login**
   - After registration, you'll be automatically logged in
   - You'll be redirected to the role-based dashboard

### User Roles & Permissions

#### 👨‍💼 Admin
**Full System Access:**
- ✅ View all users in the company
- ✅ Manage products and inventory
- ✅ View all orders and vendors
- ✅ Access payment tracking
- ✅ View comprehensive dashboard stats

**Dashboard Shows:**
- Total Orders
- Pending Orders
- Completed Orders
- Total Products
- Low Stock Items
- Total Vendors
- Pending Payments
- Total Revenue

#### 💼 Sales
**Order & Inventory Management:**
- ✅ Create and manage orders
- ✅ View inventory levels
- ✅ Track payments
- ✅ Assign vendors to orders
- ❌ Cannot manage users or system settings

**Dashboard Shows:**
- Total Orders
- Pending Orders
- Completed Orders
- Total Products
- Pending Payments
- Total Revenue

#### 🛒 Buyer
**View-Only Access:**
- ✅ View assigned orders
- ✅ Track order status
- ✅ View payment history
- ✅ Make payments
- ❌ Cannot create orders or manage inventory

**Dashboard Shows:**
- My Orders
- Pending Orders
- Pending Payments
- Total Revenue

### Navigation

The app uses **Bottom Tab Navigation** with 5 main sections:

1. **🏠 Dashboard**
   - Overview of key metrics
   - Quick action buttons
   - Role-specific information

2. **📋 Orders** *(Coming in Phase 3)*
   - Create new orders
   - View order history
   - Track order status

3. **📦 Products** *(Coming in Phase 2)*
   - Product catalog
   - Inventory management
   - Stock tracking

4. **👥 Vendors** *(Coming in Phase 4)*
   - Vendor directory
   - Vendor performance
   - Vendor assignment

5. **👤 Profile**
   - View account information
   - Access settings
   - Logout

### Common Tasks

#### Logging In
1. Open the app
2. Enter your email OR mobile number
3. Enter your password
4. Click "Login"

#### Refreshing Dashboard Data
- Pull down on the dashboard to refresh stats
- Data updates automatically from the server

#### Viewing Profile
1. Tap the "Profile" tab
2. View your account details
3. Access settings (coming soon)

#### Logging Out
1. Go to Profile tab
2. Scroll to bottom
3. Tap "Logout" button
4. Confirm logout

---

## 📚 API Documentation

### Base URL
- **Local**: `http://localhost:8001/api`
- **Production**: `https://your-domain.com/api`

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "mobile": "+1234567890",
  "password": "securepassword",
  "name": "John Doe",
  "role": "Admin",
  "company_name": "My Company"
}

Response: 200 OK
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "email": "user@example.com",
    "name": "John Doe",
    "role": "Admin"
  }
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "login": "user@example.com",  // or mobile number
  "password": "securepassword"
}

Response: 200 OK
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": { ... }
}
```

#### Get Current User
```http
GET /api/auth/me
Authorization: Bearer <token>

Response: 200 OK
{
  "id": "507f1f77bcf86cd799439011",
  "email": "user@example.com",
  "mobile": "+1234567890",
  "name": "John Doe",
  "role": "Admin",
  "company_id": "507f1f77bcf86cd799439012",
  "created_at": "2025-02-03T10:00:00",
  "is_active": true
}
```

### Dashboard Endpoints

#### Get Dashboard Stats
```http
GET /api/dashboard/stats
Authorization: Bearer <token>

Response: 200 OK
{
  "total_orders": 0,
  "pending_orders": 0,
  "completed_orders": 0,
  "total_products": 0,
  "low_stock_products": 0,
  "total_vendors": 0,
  "pending_payments": 0,
  "total_revenue": 0.0
}
```

### User Management (Admin Only)

#### Get All Users
```http
GET /api/users
Authorization: Bearer <token>

Response: 200 OK
[
  {
    "id": "507f1f77bcf86cd799439011",
    "email": "user1@example.com",
    "name": "User One",
    "role": "Admin",
    ...
  }
]
```

### Error Responses

#### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

#### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

#### 400 Bad Request
```json
{
  "detail": "Email already registered"
}
```

---

## 🐛 Troubleshooting

### Backend Issues

#### MongoDB Connection Error
```
Problem: pymongo.errors.ServerSelectionTimeoutError
Solution:
1. Ensure MongoDB is running: mongod --dbpath ~/data/db
2. Check MONGO_URL in .env file
3. Verify MongoDB is accessible: mongo localhost:27017
```

#### Port Already in Use
```
Problem: Address already in use: 8001
Solution:
1. Find process: lsof -i :8001 (Mac/Linux) or netstat -ano | findstr :8001 (Windows)
2. Kill process: kill -9 <PID>
3. Or use different port: uvicorn server:app --port 8002
```

#### Import Errors
```
Problem: ModuleNotFoundError: No module named 'fastapi'
Solution:
1. Activate virtual environment: source venv/bin/activate
2. Install dependencies: pip install -r requirements.txt
```

### Frontend Issues

#### Metro Bundler Error
```
Problem: Metro bundler fails to start
Solution:
1. Clear cache: npx expo start --clear
2. Delete node_modules: rm -rf node_modules && yarn install
3. Reset Metro: rm -rf .expo .metro-cache
```

#### Cannot Connect to Backend
```
Problem: Network request failed
Solution:
1. Check backend is running: curl http://localhost:8001/api/
2. Update .env: EXPO_PUBLIC_BACKEND_URL=http://localhost:8001
3. For physical device, use computer's IP: http://192.168.1.x:8001
```

#### Expo Go Version Mismatch
```
Problem: "This app is not compatible with Expo Go"
Solution:
1. Update Expo Go app to latest version
2. Ensure SDK versions match in package.json
3. Run: npx expo install --fix
```

#### Navigation Errors (LinkingContext)
```
Problem: Couldn't find a LinkingContext context
Solution:
1. Remove conflicting packages: yarn remove @react-navigation/native
2. Reinstall: npx expo install @react-navigation/native
3. Clear cache: rm -rf .expo .metro-cache && yarn start
```

### Common Issues

#### White Screen on Mobile
```
Solution:
1. Check Expo logs in terminal
2. Shake device → "Reload"
3. Ensure backend URL is accessible from device
4. Check network connectivity
```

#### Login Not Working
```
Solution:
1. Check backend logs for errors
2. Verify email/mobile format
3. Check JWT token generation
4. Clear app data and try again
```

#### Dashboard Stats Not Loading
```
Solution:
1. Ensure user is authenticated (valid token)
2. Check /api/dashboard/stats endpoint
3. Verify network connection
4. Pull down to refresh
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 📞 Support

For issues or questions:
- Create an issue in the repository
- Contact: support@yourcompany.com

---

## 🎯 Roadmap

- [x] Phase 1: Authentication & Dashboard (MVP)
- [ ] Phase 2: Product & Inventory Management
- [ ] Phase 3: Order Management
- [ ] Phase 4: Vendor Management
- [ ] Phase 5: Payment Processing
- [ ] Phase 6: Push Notifications
- [ ] Phase 7: Offline Mode
- [ ] Phase 8: Analytics & Reporting

---

**Built with ❤️ using Expo, FastAPI, and MongoDB**
