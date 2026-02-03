# B2B Mobile App - Frontend

A professional mobile application built with **Expo (React Native)** featuring role-based authentication, beautiful UI/UX, and cross-platform support for iOS, Android, and Web.

## 🎯 Tech Stack

- **Framework**: Expo SDK 54 with expo-router (file-based routing)
- **Language**: TypeScript
- **UI Components**: React Native (Native components)
- **State Management**: Zustand + React Context
- **Data Fetching**: React Query (@tanstack/react-query)
- **HTTP Client**: Axios
- **Navigation**: Expo Router (file-based) + React Navigation
- **Storage**: expo-secure-store (JWT tokens)
- **Forms**: React Hook Form
- **Icons**: @expo/vector-icons (Ionicons)

## 📁 Project Structure

```
frontend/
├── app/                          # File-based routing (expo-router)
│   ├── _layout.tsx              # Root layout with providers
│   ├── index.tsx                # Entry point (auto-redirect)
│   ├── auth/
│   │   ├── login.tsx            # Login screen
│   │   └── register.tsx         # Registration screen
│   └── (tabs)/                  # Tab navigation group
│       ├── _layout.tsx          # Tab navigator config
│       ├── dashboard.tsx        # Dashboard screen
│       ├── orders.tsx           # Orders screen (Phase 3)
│       ├── products.tsx         # Products screen (Phase 2)
│       ├── vendors.tsx          # Vendors screen (Phase 4)
│       └── profile.tsx          # Profile screen
├── contexts/
│   └── AuthContext.tsx          # Authentication context & hooks
├── assets/                       # Images, fonts, etc.
├── .env                          # Environment variables
├── app.json                      # Expo configuration
├── package.json                  # Dependencies
└── tsconfig.json                 # TypeScript config
```

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- Yarn or npm
- Expo Go app on your mobile device (for testing)

### Installation

```bash
# Install dependencies
yarn install

# Start development server
yarn start
```

### Running on Different Platforms

```bash
# Web browser
yarn web

# iOS simulator (macOS only)
yarn ios

# Android emulator
yarn android

# Scan QR code with Expo Go app
yarn start
```

## 🔐 Authentication Flow

### Registration
1. User fills registration form with:
   - Name, Email, Mobile, Role, Company, Password
2. Frontend validates input
3. Sends POST to `/api/auth/register`
4. Receives JWT token + user data
5. Stores token securely in expo-secure-store
6. Updates auth context
7. Navigates to dashboard

### Login
1. User enters email/mobile + password
2. Sends POST to `/api/auth/login`
3. Receives JWT token + user data
4. Stores token securely
5. Updates auth context
6. Navigates to dashboard

### Auto-Login
1. On app start, checks for stored token
2. If found, loads user data
3. Auto-navigates to dashboard
4. If not found, shows login screen

### Logout
1. User clicks logout in profile
2. Deletes token from secure storage
3. Clears auth context
4. Navigates to login

## 🎨 UI/UX Patterns

### Navigation
- **Bottom Tab Navigation**: 5 main tabs (Dashboard, Orders, Products, Vendors, Profile)
- **Stack Navigation**: Modal screens for auth flow
- **File-based Routing**: Using expo-router conventions

### Mobile-First Design
- **Safe Areas**: Proper handling with SafeAreaView
- **Keyboard**: KeyboardAvoidingView for forms
- **Touch Targets**: Minimum 44x44 points
- **Pull-to-Refresh**: Dashboard data refresh
- **Loading States**: ActivityIndicator for async operations

### Role-Based UI
Different dashboard views based on user role:
- **Admin**: All stats + full management
- **Sales**: Order/inventory management
- **Buyer**: Order viewing + payments

## 🔧 Environment Variables

Create `.env` file:

```env
# Backend API URL
EXPO_PUBLIC_BACKEND_URL=http://localhost:8001

# For physical device testing, use your computer's IP
# EXPO_PUBLIC_BACKEND_URL=http://192.168.1.x:8001
```

**Note**: Variables must be prefixed with `EXPO_PUBLIC_` to be accessible in the app.

## 📦 Key Dependencies

### Production Dependencies
```json
{
  "expo": "~54.0.33",
  "expo-router": "~6.0.23",
  "react": "19.1.0",
  "react-native": "0.81.5",
  "@tanstack/react-query": "^5.90.20",
  "axios": "^1.13.4",
  "expo-secure-store": "^15.0.8",
  "zustand": "^5.0.11",
  "react-hook-form": "^7.71.1",
  "@react-native-picker/picker": "^2.11.1"
}
```

### Development Dependencies
```json
{
  "typescript": "~5.9.2",
  "@types/react": "~19.1.10",
  "eslint": "^9.25.0",
  "eslint-config-expo": "~10.0.0"
}
```

## 🧪 Testing

### Manual Testing Checklist

#### Authentication
- [ ] Register with valid data
- [ ] Register with invalid email
- [ ] Register with short password
- [ ] Login with email
- [ ] Login with mobile
- [ ] Login with wrong password
- [ ] Auto-login on app restart
- [ ] Logout functionality

#### Dashboard
- [ ] Stats load correctly
- [ ] Pull-to-refresh works
- [ ] Role-specific stats display
- [ ] Quick actions visible
- [ ] User info card displays

#### Navigation
- [ ] All tabs accessible
- [ ] Back navigation works
- [ ] Deep linking works
- [ ] Auth screens are modal

#### Cross-Platform
- [ ] Works on iOS
- [ ] Works on Android
- [ ] Works on Web
- [ ] Responsive on different screen sizes

## 🐛 Troubleshooting

### Common Issues

#### "Metro bundler fails to start"
```bash
# Clear cache and restart
npx expo start --clear
```

#### "Cannot connect to backend"
```bash
# Check backend is running
curl http://localhost:8001/api/

# For physical device, use computer's IP in .env
EXPO_PUBLIC_BACKEND_URL=http://192.168.1.x:8001
```

#### "Module not found" errors
```bash
# Reinstall dependencies
rm -rf node_modules
yarn install
```

#### "Couldn't find a LinkingContext"
```bash
# Remove conflicting navigation packages
yarn remove @react-navigation/native @react-navigation/bottom-tabs
npx expo install @react-navigation/native
rm -rf .expo .metro-cache
yarn start
```

#### White screen on device
```bash
# Check Expo logs in terminal
# Shake device → "Reload"
# Verify backend URL is accessible from device
```

## 🚀 Deployment

### Build for Production

#### iOS
```bash
# Install EAS CLI
npm install -g eas-cli

# Login to Expo
eas login

# Build for iOS
eas build --platform ios --profile production

# Submit to App Store
eas submit --platform ios
```

#### Android
```bash
# Build for Android
eas build --platform android --profile production

# Submit to Play Store
eas submit --platform android
```

#### Web
```bash
# Export web build
npx expo export:web

# Deploy to Vercel
vercel --prod

# Or Netlify
netlify deploy --prod --dir web-build
```

### Update Environment for Production

```env
EXPO_PUBLIC_BACKEND_URL=https://your-production-api.com
```

## 📱 App Configuration

Edit `app.json` for app metadata:

```json
{
  "expo": {
    "name": "B2B Mobile App",
    "slug": "b2b-mobile-app",
    "version": "1.0.0",
    "orientation": "portrait",
    "icon": "./assets/images/icon.png",
    "scheme": "b2bapp",
    "splash": {
      "image": "./assets/images/splash.png",
      "resizeMode": "contain",
      "backgroundColor": "#ffffff"
    },
    "ios": {
      "bundleIdentifier": "com.yourcompany.b2bapp",
      "supportsTablet": true
    },
    "android": {
      "package": "com.yourcompany.b2bapp",
      "adaptiveIcon": {
        "foregroundImage": "./assets/images/adaptive-icon.png",
        "backgroundColor": "#ffffff"
      }
    }
  }
}
```

## 🔒 Security Best Practices

✅ **Implemented:**
- JWT tokens stored in secure storage (expo-secure-store)
- No sensitive data in AsyncStorage
- Password never stored in frontend
- API calls use HTTPS in production
- Input validation on forms

⚠️ **TODO for Production:**
- Enable certificate pinning
- Implement biometric authentication
- Add token refresh mechanism
- Set up error tracking (Sentry)
- Implement rate limiting UI

## 📚 Resources

- [Expo Documentation](https://docs.expo.dev/)
- [Expo Router Docs](https://expo.github.io/router/docs/)
- [React Native Docs](https://reactnative.dev/)
- [React Query Docs](https://tanstack.com/query/latest)

## 🎯 Future Enhancements

- [ ] Offline mode with data sync
- [ ] Biometric authentication
- [ ] Push notifications
- [ ] Image uploads
- [ ] QR code scanning
- [ ] Dark mode
- [ ] Multi-language support
- [ ] Analytics integration

---

**Built with ❤️ using Expo and React Native**