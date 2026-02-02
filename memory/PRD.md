# B2B Mobile Application - Product Requirements Document

## Project Overview
A comprehensive B2B Mobile Application for order management, procurement, and vendor operations.

## Tech Stack
- **Frontend**: Expo (React Native) - iOS & Android
- **Backend**: FastAPI (Python)
- **Database**: MongoDB
- **Authentication**: JWT-based (email + mobile login)

## User Roles & Permissions

### 1. Admin
- Full system access
- Manage users (create, update, delete)
- Manage products & inventory
- Manage vendors
- View/manage all orders
- Access payment tracking
- System configuration

### 2. Sales
- Create and manage orders
- View inventory
- Track payments
- Assign vendors to orders
- View vendor information
- Cannot delete users or modify system settings

### 3. Buyer
- View assigned orders
- Track order status
- Make payments
- View payment history
- View product catalog
- Cannot create orders or manage inventory

## Core Modules

### Phase 1 (MVP): Authentication + Dashboard
- User registration with role selection
- Login with email/mobile + password
- JWT token-based authentication
- Role-based dashboard with KPIs
- Profile management

### Phase 2: Product & Inventory Management
- Product catalog with SKU
- Stock management (in/out)
- Low stock alerts
- Product search and filtering
- Category management

### Phase 3: Order Management
- Order lifecycle: Draft → Confirmed → Fulfilled → Delivered → Closed
- Line items with quantity, price, tax
- Order history and search
- Status tracking with timestamps
- Order cancellation workflow

### Phase 4: Vendor Management
- Vendor onboarding
- Vendor approval workflow
- Vendor catalog and pricing
- Vendor performance tracking
- Vendor assignment to orders

### Phase 5: Payment Processing
- Display bank account details
- QR code generation for payments
- Email notifications for payment requests
- Payment status tracking: Pending, Success, Failed, Refunded
- Payment history

### Phase 6: Notifications
- Expo push notifications
- In-app notifications
- Email notifications (test/demo mode)

## Technical Requirements

### Backend
- REST APIs with FastAPI
- MongoDB with Motor (async)
- JWT authentication middleware
- Role-based access control
- Request validation with Pydantic
- Centralized error handling
- Structured logging

### Frontend (Mobile)
- Expo Router for navigation
- Bottom tab navigation for main sections
- JWT token storage (expo-secure-store)
- Offline read support
- Pull-to-refresh functionality
- Role-based UI rendering
- Safe area handling
- Keyboard-aware scrolling

### Security
- Password hashing with bcrypt
- JWT token expiration
- Secure token storage
- HTTPS for API calls
- Input validation on both client and server

## Non-Functional Requirements
- Multi-tenant architecture (company-level isolation)
- Scalable and cloud-ready
- Responsive mobile UI
- Fast API response times (<200ms for most endpoints)
- Proper error handling and user feedback

## Success Criteria
- Users can register and login with role-based access
- Dashboard displays role-specific information
- Mobile app works on both iOS and Android
- Secure authentication and authorization
- Clean, intuitive mobile UI

## MVP Scope (Phase 1)
Focus on getting Authentication + Dashboard working perfectly before moving to other modules.
