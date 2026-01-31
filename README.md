# 🌍 Global COVID-19 Interactive Dashboard
An interactive, real-time data visualization dashboard built with **Python**, **Dash**, and **Plotly**. This project tracks the pandemic's progression globally and at the country level using data from Kaggle.

## 📊🦠 Live Preview
![Dashboard Screenshot]


<img width="1819" height="924" alt="Image" src="https://github.com/user-attachments/assets/0bb49d0f-6066-4771-ad1b-81511d0260b5" />

<img width="1815" height="577" alt="Image" src="https://github.com/user-attachments/assets/0ad1aea1-7cbd-425f-b9ae-b5ec44268ba9" />

## ✨ Key Features
- **Dark Mode Interface**: A sleek, professional design using a dark theme with red-toned visualizations.
- **Global & Local Insights**: Switch between a "Global View" and specific countries (like Egypt) via an interactive dropdown.
- **Interactive Map**: A Choropleth map with a **Logarithmic Scale** to clearly show case variations across all countries.
- **Dynamic Indicators**: Large, easy-to-read cards showing Total Confirmed, Deaths, Recovered, and Active cases.
- **Multi-Metric Analysis**: 
  - **Bar Chart**: Top 10 countries by confirmed cases or deaths.
  - **Line Chart**: Trends of Confirmed, Deaths, and Recovered over time.
  - **Scatter Plot**: Relationship between Fatality and Recovery rates.
  - **Pie Chart**: Distribution of active vs. closed cases.

## 🛠️ Tech Stack
- **Language**: Python 3.13.9
- **Framework**: Dash (Plotly)
- **Data Manipulation**: Pandas, NumPy
- **Visuals**: Plotly Express

## 📂 Dataset
The dashboard uses the COVID-19 Complete Dataset from Kaggle
https://www.kaggle.com/datasets/imdevskp/corona-virus-report
, specifically:
- `full_grouped.csv`: For time-series analysis.
- `country_wise_latest.csv`: For current global snapshots.

## ⚙️ Installation & Usage
1. **Clone the repository**:
   ```bash
   git clone [https://github.com/your-username/covid19-dashboard.git](https://github.com/your-username/covid19-dashboard.git)

2. Install dependencies:
    ```bash
        pip install dash pandas plotly numpy
    ```
    ## ⚖️ License
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

---
Copyright (c) 2024 **Amatalrahman**
3. Run the app:
    ```bash
        python covid_dashboard.py
    ```
4. Open http://127.0.0.1:8050/ in your browser.
