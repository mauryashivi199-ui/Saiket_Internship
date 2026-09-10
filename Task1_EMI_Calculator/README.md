# 💳 Task 1: Professional Loan EMI Calculator

**Saiket Internship Assignment - Task 1**

This project includes **3 Interfaces** to showcase flexibility and high-quality implementation:
1. 🖥️ **Modern Desktop GUI Application** (`gui_calculator.py`) - Tkinter with live sliders, instant dynamic calculation & Donut breakdown chart.
2. 🌐 **Modern Web Application** (`index.html`) - Responsive Tailwind CSS & Chart.js dashboard.
3. ⌨️ **CLI Console Version** (`emi_calculator.py`) - Fast terminal-based execution.

---

## 🧮 Mathematical Formula

$$EMI = P \times r \times \frac{(1+r)^N}{(1+r)^N - 1}$$

- **$P$** = Principal Loan Amount
- **$r$** = Monthly Interest Rate in Decimal ($\frac{\text{Rate } \%}{100}$)
- **$N$** = Total Tenure in Months

---

## 🚀 How to Run

### Option 1: Modern Desktop GUI (Recommended ⭐)
```powershell
python gui_calculator.py
```
- Interactive sliders for Loan Amount, Rate, and Tenure
- Real-time dynamic Donut chart showing Principal vs Interest share
- Quick loan preset buttons (Home, Car, Personal Loan)

### Option 2: Modern Web Dashboard
Double click or open [`index.html`](index.html) in any browser (Chrome, Edge, Firefox).

### Option 3: Command-Line Interface (CLI)
```powershell
python emi_calculator.py
```
