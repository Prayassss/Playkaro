# PlayKaro - Video Platform

A modern video streaming platform built with React, TypeScript, and Tailwind CSS.

## Features

- **Video Discovery** - Browse and search through a collection of videos
- **Video Playback** - Watch videos with a clean, responsive player
- **Admin Dashboard** - Upload, edit, and manage video content
- **Authentication** - Secure login and signup system
- **Responsive Design** - Works seamlessly on desktop and mobile

## Tech Stack

- **Frontend**: React 18, TypeScript, Vite
- **Styling**: Tailwind CSS, shadcn/ui components
- **Backend**: Lovable Cloud (Supabase)
- **State Management**: React Query
- **Routing**: React Router DOM

## Getting Started

### Prerequisites

- Node.js (v18 or higher)
- npm or bun

### Installation

```bash
# Clone the repository
git clone https://github.com/Prayassss/Playkaro

# Install dependencies
npm install

# Start the development server
npm run dev
```

The app will be available at `http://localhost:5173`

## Project Structure

```
src/
├── components/       # Reusable UI components
│   ├── ui/          # shadcn/ui components
│   ├── Navbar.tsx   # Navigation bar
│   └── VideoCard.tsx # Video thumbnail card
├── pages/           # Page components
│   ├── Index.tsx    # Home page with video grid
│   ├── Watch.tsx    # Video player page
│   ├── Admin.tsx    # Admin dashboard
│   └── Auth.tsx     # Authentication page
├── lib/             # Utilities and helpers
├── hooks/           # Custom React hooks
└── integrations/    # External service integrations
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Screenshots

![Authentication](screenshots/authentication.png)
![Video Discovery](screenshots/discovervideo.png)
![Admin Dashboard](screenshots/admin_dashboard.png)
![Video Upload](screenshots/upload.png)
![Video Playback](screenshots/playback.png)

