# Project 2 - Pairs Trading Strategy

## Authors:
- **Axel Santiago Molina Ceja**
- **Pablo Lemus Castellanos**

---

## 📌 Overview

### **Pairs Trading Strategy Using MSFT and AMD**  
This project presents a **Pairs Trading Strategy** implemented in Python, focusing on the statistical arbitrage between **Microsoft (MSFT) and Advanced Micro Devices (AMD)**. The objective is to construct a robust trading model by identifying co-integrated assets, estimating the hedge ratio dynamically, and generating trading signals based on statistical thresholds.

---

## 📊 Project Overview  

### 🔹 **1. Data Acquisition**  
- We collect **10 years of historical price data** for MSFT and AMD using **Yahoo Finance**.  

### 🔹 **2. Co-Integration Analysis**  
- We verify that the assets maintain a stable economic relationship by testing for **stationarity and co-integration** through:
  - **Augmented Dickey-Fuller (ADF) test**  
  - **Ordinary Least Squares (OLS) regression**  
  - **Johansen Co-Integration Test**  
  - **Vector Error Correction Model (VECM)**  

### 🔹 **3. Hedge Ratio Estimation**  
- The hedge ratio is dynamically updated using a **Kalman Filter**, implemented from scratch (without external libraries).  

### 🔹 **4. Trading Strategy**  
- The **spread (Z-score of residuals)** is calculated, and trading signals are generated based on statistical thresholds:
  - **Sell (Short) the spread** when it exceeds **+1.5 standard deviations**  
  - **Buy (Long) the spread** when it falls below **-1.5 standard deviations**  
  - **Close positions** when the spread returns to equilibrium.  

### 🔹 **5. Backtesting**  
- The strategy is backtested with an **initial capital of $1,000,000 USD**.  
- We account for **margin requirements** and **commissions of 0.125%** per trade.  

---

## 🏛 **Economic Relationship Between MSFT and AMD**  

Microsoft and AMD share a strong economic relationship due to their involvement in the **technology and semiconductor industries**.  
- **Microsoft** develops software, cloud services, and gaming consoles (Xbox).  
- **AMD** supplies processors and GPUs, many of which power **Microsoft's Azure cloud services and Xbox consoles**.  
- Both companies are exposed to similar market factors, including **tech sector trends, macroeconomic conditions, and interest rates**.  

This **supply-chain dependency and fundamental linkage** support their **co-integration**, making them a strong candidate pair for this statistical arbitrage strategy.

---

## 🚀 **How to Run the Project**
### **1️⃣ Install Required Dependencies**
Before running the code, install the necessary Python libraries:
```sh
install pandas numpy matplotlib statsmodels yfinance

```
2️⃣ Run main.py
Execute the main script:
````
sh
python main.py

````

This will:

Download and process data.
Conduct statistical tests.
Perform backtesting.
Generate visualizations of the strategy's performance.

## 3️⃣ Outputs
After execution, you will get:

- ✅ Historical Price Comparison (MSFT vs AMD)
- ✅ Z-Score Trading Signal
- ✅ Portfolio Performance Graph
- 📈 Results and Findings

High correlation and co-integration were confirmed between MSFT and AMD.
The Kalman Filter successfully updated the hedge ratio dynamically.
The trading signals were consistent, yielding market-neutral trades.
Risk-adjusted returns were improved by dynamically adjusting positions.

## 📚 Sources and References
This project was developed based on the following sources:

- 📖 Microestructuras de Trading (Course Materials)
- 📂 Class Presentations from Microestructuras de Trading
- 🔗 Yahoo Finance API (Stock Data Retrieval)
- 🤖 ChatGPT Assistance (Technical Guidance & Code Optimization)
