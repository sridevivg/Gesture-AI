# Gesture-AI Frontend Subsystem

## Overview

The Gesture-AI frontend provides a real-time web application interface for computer vision telemetry, live camera gesture tracking, customizable action bindings, telemetry analytics, and platform configuration.

---

## Technology Stack

* **Core**: React 18, TypeScript (Strict Mode)
* **Build Tool**: Vite
* **Styling**: Tailwind CSS with custom glassmorphism and dark mode palette
* **Routing**: React Router v6
* **Data Fetching & State**: TanStack Query (React Query)
* **Network & WebSockets**: Axios and native WebSocket client
* **Icons & Charts**: Lucide React, Recharts
* **Validation**: Zod
* **Code Quality**: ESLint, Prettier

---

## Directory Organization

```
frontend/
├── src/
│   ├── assets/               # Static icons, vector images, and media
│   ├── components/           # Modular UI elements
│   │   ├── camera/           # Video feed and vision HUD overlays
│   │   └── common/           # Shared buttons, cards, headers, status badges
│   ├── hooks/                # Custom React hooks (useGestureStream, useSystemStatus)
│   ├── pages/                # Route view components
│   │   ├── DashboardPage.tsx
│   │   ├── GestureStudioPage.tsx
│   │   ├── ActionMappingsPage.tsx
│   │   ├── AnalyticsPage.tsx
│   │   └── SettingsPage.tsx
│   ├── routes/               # Routing declarations and layout shell
│   ├── services/             # API client and WebSocket streaming layer
│   ├── types/                # TypeScript interfaces and Zod validation schemas
│   ├── utils/                # Formatting and computational helpers
│   ├── App.tsx               # Root provider component
│   ├── main.tsx              # Application entrypoint
│   └── index.css             # Tailwind base styles and custom theme tokens
├── index.html                # HTML entry document
├── package.json              # Project dependencies and npm scripts
├── tsconfig.json             # TypeScript compiler settings
├── vite.config.ts            # Vite configuration and path aliases
├── tailwind.config.js        # Design tokens and theme extension
├── postcss.config.js         # PostCSS plugins
├── eslint.config.js          # ESLint rules
└── .prettierrc               # Prettier configuration
```

---

## Local Development

### 1. Environment Setup

```bash
cp .env.example .env
```

### 2. Dependency Installation

```bash
npm install
```

### 3. Start Development Server

```bash
npm run dev
```

The application will be accessible at `http://localhost:5173`.

---

## Quality and Verification

```bash
# Type check TypeScript code
npm run typecheck

# Lint source files
npm run lint

# Format code
npm run format
```
