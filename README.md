# 🚀 Credit Risk Analyzer – Setup & Run Guide

This guide will help you **quickly set up and run the project (Frontend + Backend)** in NeoCoder or any local environment.

---

# 📌 Prerequisites

Make sure you have:

* ✅ **Node.js v20** (mandatory for Angular)
* ✅ **Python 3.9+**
* ✅ `pip` installed

---

# 🌐 Frontend Setup (Angular)

## ⚠️ Step 1: Use Node 20

# 🟢 Install Node.js (Required)
 
This project requires **Node.js v20**.
 
## ▶️ Step 1: Install using NVM (Recommended)
 
```bash
sudo chown -R $(whoami) /usr/local/nvm

nvm install 20

## 📂 Step 2: Navigate to frontend folder

```bash
cd ~/project/workspace/credit-risk-agent-repo/frontend/credit-risk-ui
```

---

## 📦 Step 3: Install dependencies

```bash
npm install
```

> ✅ This installs Angular and all required packages from `package.json`
> ❌ You do **NOT** need to install Angular globally

---

## ▶️ Step 4: Run the Angular app

```bash
npx ng serve --host 0.0.0.0 --port 8080
```

> ⚠️ Always use `npx ng serve` (do NOT use global `ng`)

---

## 🌍 Access Frontend

* In **NeoCoder**, the platform will automatically expose the app via its own URL
* You do **NOT** need to use `localhost:8080`

---

# ⚙️ Backend Setup (FastAPI)

## 📂 Step 1: Navigate to backend folder

```bash
cd ~/project/workspace/credit-risk-agent-repo/backend
```

---

## 🐍 Step 2: Create virtual environment

```bash
python3 -m venv venv
```

---

## ▶️ Step 3: Activate virtual environment

```bash
source venv/bin/activate
```

---

## 📦 Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Step 5: Run the FastAPI server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8081
```

---

## 🌐 Backend API

* Runs on port **8081**
* In NeoCoder, it will be exposed via platform URL automatically

---

# 🔄 How It Works

* Frontend → Port **8080**
* Backend → Port **8081**
* Angular app calls FastAPI APIs for analysis

---

# ⚠️ Troubleshooting

## ❌ Angular not working

* Ensure Node 20 is set correctly:

```bash
node -v
```

---

## ❌ Dependencies missing

```bash
npm install
pip install -r requirements.txt
```

---

## ❌ CORS issues

* Backend already configured
* Ensure both servers are running

---

# 🎯 You're Ready!

1. Start backend
2. Start frontend
3. Open NeoCoder preview URL
4. Enter company → Analyze

---

💡 *Tip: Run frontend and backend in separate terminals for smooth execution*
