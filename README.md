
# 🧓 Blockchain-Based Pension Management System

A transparent, secure, and decentralized pension management system built using **Django + Ethereum (Web3)**. This system enables users to apply for pensions, track application status, and claim funds directly via blockchain.

---

## 🚀 Features

* 🔐 **Aadhaar-based Authentication (OTP simulation)**
* 📝 **Online Pension Application**
* ⛓️ **Blockchain Registration (Ethereum Smart Contract)**
* 📊 **Real-time Dashboard (Funds, Users, Claims)**
* 💸 **Direct Pension Claim via MetaMask**
* 📜 **Transparent Transaction History**
* 👁️ **Application Status Tracking**
* 🔄 **Live Blockchain Event Fetching**

---

## 🏗️ Tech Stack

### 🌐 Backend

* Python
* Django

### 🎨 Frontend

* HTML, CSS, JavaScript
* Bootstrap / Custom UI

### 🔗 Blockchain

* Solidity Smart Contract
* Web3.py
* MetaMask Integration
* Ethereum (Sepolia Testnet)

---

## 📁 Project Structure

```
project/
│── pension_app/
│   ├── models.py
│   ├── views.py
│   ├── web3_config.py
│   ├── templates/
│   │   ├── apply-pension.html
│   │   ├── my-pension-status.html
│   │   └── transperancy-dashboard.html
│
│── static/
│── db.sqlite3
│── manage.py
```

---

## ⚙️ Smart Contract Overview

### Key Functionalities:

* `registerUser()` → Registers a pension applicant
* `claimPension()` → Allows user to claim funds
* `depositFunds()` → Government deposits funds
* `getDashboardStats()` → Returns real-time stats

### Events:

* `UserRegistered`
* `PensionClaimed`
* `FundsDeposited`

---

## 🔄 Application Flow

1. User enters Aadhaar → OTP Verification
2. User fills pension application
3. Data saved in Django DB
4. User is registered on Blockchain
5. Dashboard updates with real-time stats
6. User can claim pension via MetaMask
7. Transaction recorded on blockchain

---

## 🔧 Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/your-username/pension-blockchain.git
cd pension-blockchain
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Configure Blockchain

Update `web3_config.py`:

```python
RPC_URL = "https://sepolia.infura.io/v3/YOUR_PROJECT_ID"
PRIVATE_KEY = "YOUR_PRIVATE_KEY"
CONTRACT_ADDRESS = "DEPLOYED_CONTRACT_ADDRESS"
```

---

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 5. Start Server

```bash
python manage.py runserver
```

---

## 🦊 MetaMask Setup

* Install MetaMask extension
* Switch to **Sepolia Testnet**
* Import your test account
* Connect wallet in application

---

## 📊 API Endpoints

| Endpoint            | Description             |
| ------------------- | ----------------------- |
| `/apply-pension/`   | Submit application      |
| `/dashboard-stats/` | Get blockchain stats    |
| `/pension-status/`  | View application status |
| `/save-wallet/`     | Save wallet in session  |

---

## ⚠️ Known Issues

* Event fetching may fail depending on Web3 version
* Sessions are temporary (use DB for production)
* Gas fees required for transactions

---

## 💡 Future Improvements

* 🔐 Real OTP integration (SMS Gateway)
* 🏦 Bank account linking
* 📱 Mobile app version
* 🌍 Multi-chain support
* 📈 Advanced analytics dashboard
* 🧾 PDF generation for pension records

---

## 🤝 Contribution

Contributions are welcome!

```bash
fork → clone → create branch → commit → push → PR
```

---

## 📜 License

This project is licensed under the MIT License.

---

## 🙌 Acknowledgements

* Ethereum Documentation
* Web3.py Docs
* Django Framework

---