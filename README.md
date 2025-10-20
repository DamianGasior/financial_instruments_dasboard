A dashboard application for monitoring and visualizing financial data using Streamlit.

🧭 Project Goal

The goal of this project is to create an interactive dashboard for analyzing and visualizing financial data, such as stock prices and other financial instruments.

🛠️ Technologies

Streamlit – framework for building web applications in Python - not started 

Pandas – data manipulation and analysis - in progress 

Matplotlib / Plotly – data visualization - not started 



📁 Repository Structure
financial_instruments_dashboard/
├── .env.example        # Example configuration file with API key
├── requirements.txt    # List of dependencies
├── README.md           # Project documentation
├── app.py              # Main Streamlit application < not started>
├── src/                # Source code
│   ├── main.py                            # file to run the progran
│   ├── api_request_alphavantage.py        # get the data from rest api
│   ├── metrics_calcs.py                   # simple analysis
│   └── dashboard.py                       # graphs, dashboards (Streamlit) , tbc. 
├── tests/              # Unit tests  < option at the moment>

🚀 Installation

Clone the repository:

git clone https://github.com/DamianGasior/financial_instruments_dashboard.git
cd financial_instruments_dashboard


Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt


Copy .env.example to .env and fill in your configuration (e.g., API keys).
Follow the instruction  in file .env.example 

Run the backend:

python main.py



📄 License

This project is licensed under the MIT License.