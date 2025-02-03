# Project Name

_A brief description of your project goes here._

## Prerequisites

- **Python 3.x**
- **Node.js**
- Other dependencies as required (e.g., FastAPI, Uvicorn, etc.)

## Installation & Setup

### 1. Install Python Dependencies

Install all the necessary packages by running:

```bash
pip install -r requirements.txt
```

### 2. Start the FastAPI Backend

Launch your FastAPI application using Uvicorn:

```bash
uvicorn main:app
```

### 3. Run the Frontend

Navigate to the frontend repository (if it's in a separate folder) and start the development server:

```bash
npm run dev
```

### 4. Access the Application

Once both servers are running, open your browser and navigate to:

```
http://localhost:3000
```

## Additional Information

### Backend Configuration

- **Create `credentials.json`**

  In the root directory of the backend folder, add a file named `credentials.json` with the following structure:

  ```json
  {
    "GEMINI_API_KEY": "<your gemini api key here>",
    "TBO_SIGHTSEEING_API_USERNAME": "<SightseeingApi Username>",
    "TBO_SIGHTSEEING_API_PASSWORD": "<Sightseeing Api password>",
    "TBO_SIGHTSEEING_API_CLIENT_ID": "<Sightseeing Api client id>",
    "TBO_Hotel_API_USERNAME": "<Hotel api username>",
    "TBO_Hotel_API_PASSWORD": "<Hotel api password>"
  }
  ```

- **Create `firebase_creds.json`**

  In the root directory of the backend folder, add another file named `firebase_creds.json`. To generate this file:
  - Create a Firebase project.
  - Go to **Project Settings → Service Accounts**.
  - Create a service account on Google Cloud for your Firebase project.
  - Download the credentials as a JSON file.

- **Obtain a Gemini API Key**

  To obtain a **Gemini API Key**, visit [Google AI Studio](https://aistudio.google.com/), click on **Create API Key**, and follow the instructions.

### Frontend Configuration

- **Copy Configuration Files**

  Place the same `firebase_creds.json` and `credentials.json` files in the root directory of the frontend folder.

- **Create `.env.local` File**

  In the frontend folder, create a `.env.local` file with the following content:

  ```env
  # Firebase Client Config
  NEXT_PUBLIC_FIREBASE_API_KEY=YOUR_FIREBASE_API_KEY
  NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=YOUR_FIREBASE_AUTH_DOMAIN
  NEXT_PUBLIC_FIREBASE_DATABASE_URL=YOUR_FIREBASE_DATABASE_URL
  NEXT_PUBLIC_FIREBASE_PROJECT_ID=YOUR_FIREBASE_PROJECT_ID
  NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=YOUR_FIREBASE_STORAGE_BUCKET
  NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=YOUR_FIREBASE_MESSAGING_SENDER_ID
  NEXT_PUBLIC_FIREBASE_APP_ID=YOUR_FIREBASE_APP_ID

  # Firebase Admin SDK
  FIREBASE_PROJECT_ID=YOUR_FIREBASE_PROJECT_ID
  FIREBASE_CLIENT_EMAIL=YOUR_FIREBASE_CLIENT_EMAIL
  # Note: The private key must be in one line with \n for newlines
  FIREBASE_PRIVATE_KEY="YOUR_FIREBASE_PRIVATE_KEY"

  # Backend URL
  NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
  ```

