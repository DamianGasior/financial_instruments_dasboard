  # Project Description
                
  The application gathers and analyzes market data for stocks, ETFs, cryptocurrencies, FX pairs, indices, commodities, and bond yields.

  For stocks and ETFs, the search is focused on instruments listed on US exchanges.
  For cryptocurrencies and FX pairs, the search scope is not limited to US markets.

  The tool provides basic descriptive information for selected instruments (such as description and classification) and enables users to analyze historical prices, correlations, and key financial metrics commonly used by professional investors.
    


   ## Project Goal
 

   The goal of this project is to provide individual, non-professional users with access to financial metrics and analytical tools that are typically used by professional investors.

   Individual investors often lack the tools, time, or resources required to calculate and interpret such metrics on their own.
   This project aims to bridge that gap by offering a transparent and educational analytical dashboard.

   Details of the calculated metrics are described in the **Main Functionalities** section.
   


   ## Main Functionalities

  ### Live Market Data
   
  - Live prices via **Finnhub WebSocket** for selected groups of instruments:
  - indices
  - commodities
  - FX pairs
  - bond yields
  - cryptocurrencies
    

  ### Instrument Search
    
  - Instrument search using a default data provider (**Twelve Data**)
  - Available instruments:
  - US-listed stocks
  - ETFs
  - cryptocurrencies
  - FX pairs
    

  ### Historical Data & Visualization
    
    For selected instruments and benchmarks:
    - Retrieve historical prices for a selected period:
    - daily
    - weekly
    - monthly
    - Display price charts for selected symbols
    - Display basic descriptive information for US-listed stocks
    

    ### Basic Statistical Metrics
    
    For a selected time period:
    - mean return
    - cumulative return
    - highest and lowest price
    - standard deviation
    

    ### Correlation Analysis
    
    - Calculate and display correlations between selected symbols and/or benchmarks
    

    ### Risk & Performance Metrics
   
    For selected symbols evaluated against multiple benchmarks (e.g. **SPY, QQQ, GLD, EEM**):
    - beta
    - volatility (standard deviation)
    - Sharpe ratio
    - correlation
    - R² (coefficient of determination)

    - Symbols and benchmarks are visualized on comparative charts, enabling quick assessment of relative performance and market positioning.


    
    # Project Structure
    ```    
    financial_instruments_dashboard/
    │
    ├─ app/ # Streamlit application (UI)
    │ └─ pages/ # Dashboard views
    │
    ├─ src/ # Application logic
    │ ├─ api_providers/ # Market data API integrations
    │ ├─ metrics/ # Financial metrics calculations
    │ ├─ pipeline/ # Data flow (download → transform → analysis)
    │ ├─ data/ # Data cache (raw / processed)
    │ └─ main.py # Application entry point
    │
    ├─ diagrams/ # Diagrams (BPMN, SVG)
    ├─ requirements.txt # Python dependencies
    ├─ README.md
    └─ LICENSE
    ```    

   ## Development
     pip install -r requirements.txt # required for deploy into streamlit cloud
     pip install -r requirements-dev.txt # required for developer for local development


  # How to Use
   
  A short demo video (approximately 3 minutes) demonstrating the main functionalities of the application will be provided here.
    

  # Project Characteristics & Disclaimer

    
  This project is created **purely for educational purposes** and must not be treated as financial advice.
    

   ## No Investment Advice
    
   The content provided by this project is for informational and educational purposes only and does not constitute:
   - investment advice,
   - an investment recommendation,
   - an investment analysis,
   - or any other form of financial advisory service.

   The information presented does not take into account the user's individual financial situation, investment objectives, or risk profile and must not be relied upon when making investment decisions.

   The author is not authorized to provide investment advisory services and is not supervised by the Polish Financial Supervision Authority (KNF).

   All investment decisions are made solely at the user's own risk.
    

   ## Legal Basis
    
   - Act on Trading in Financial Instruments (Poland)
   - Article 69(2)(5) – definition of investment advisory services
   - Article 76 – investment recommendations and analyses
   - Regulation (EU) No 596/2014 (Market Abuse Regulation – MAR)
   - Article 3(1)(34) – definition of an investment recommendation
   - Directive 2014/65/EU (MiFID II)

    

  # About me
    
  This project was created as an educational initiative.
  More about the author can be found in the **About the author** section of the application
    