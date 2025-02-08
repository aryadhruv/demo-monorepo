# demo-monorepo
Let's play with frontend for Chatbot UI

# 

Welcome to the project! This repository is part of a monorepo that includes both the frontend and backend of the application. Below you’ll find instructions on setting up, running, and building the application, as well as an overview of the technology stack.

Forked from [Vercel AI Python SDK](https://github.com/vercel-labs/ai-sdk-preview-python-streaming)⭐️

---

## Preview - 
<img width="933" alt="image" src="https://github.com/user-attachments/assets/c215ddaa-7e26-4a0e-a56f-c066eae8dd6e" />

## Plans
Vercel provide a very powerful SDK, but demo is quite vanilla. My plans for this repo is to build all much desired features in for an complete ready to use tool. Features like - injecting dynamic convo starters, mode change, labelling, auth and others.

## Prerequisites

Before running the application, ensure you have the following installed:

- **Node.js** (v14+ recommended) and your package manager of choice (e.g., [pnpm](https://pnpm.io/), npm, or yarn)
- **Python 3.8+** for the backend
- **Poetry** for Python dependency management (see [Poetry installation](https://python-poetry.org/docs/#installation) for details)

---

## Setup

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/aryadhruv/demo-monorepo.git
cd demo-monorepo/frontend
```

### 2. Install Frontend Dependencies

If you are using pnpm (as suggested by the scripts):

```bash
pnpm install
```

Alternatively, if you are using npm or yarn, adjust the install command accordingly.

### 3. Install Backend Dependencies

Navigate to the backend directory and install the dependencies using Poetry:

```bash
cd ../backend
poetry install
```

---

## Running the Application

The project is set up to run both the frontend and backend concurrently.

### Development Mode

From the frontend directory, you can start both servers using:

```bash
pnpm run run-app
```

This command uses [concurrently](https://github.com/open-cli-tools/concurrently) to run:
- **Frontend:** `pnpm run dev` (powered by Vite)
- **Backend:** `pnpm run fastapi-dev` (starts FastAPI with Uvicorn)

If you prefer to run them separately:
- **Frontend Only:**  
  ```bash
  pnpm run dev
  ```
- **Backend Only:**  
  ```bash
  pnpm run fastapi-dev
  ```

### Preview Production Build

To build and preview a production build of the frontend:

```bash
pnpm run build
pnpm run preview
```

---

## Additional Scripts

- **Linting:**  
  Check your code for linting issues using:
  ```bash
  pnpm run lint
  ```

- **Build:**  
  Build the TypeScript project and bundle the application:
  ```bash
  pnpm run build
  ```

---

## TechStack

- **Frontend:**
  - React & React DOM:
  - TypeScript
  - Vite
  - Tailwind CSS
  
- **Backend:**
  - FastAPI
  - Uvicorn
  - Poetry

---
