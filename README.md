# House Overpayment Experiment

This is an interactive web application built with Streamlit to simulate and analyze house buying behavior. The application includes both an experimental interface for manual house selection and a simulation component for automated analysis.

## Features

### Experiment Page
- Sequential house presentation
- Real-time price display
- Benchmark information for location-based properties
- History tracking of viewed properties
- Round-by-round purchase history
- Budget constraints:
  - Round 1: $100
  - Rounds 2-3: $150

### Simulation Page
- Automated simulation with 5 buyers
- Comprehensive data visualization:
  - Price distribution by round
  - Tier distribution (Value/Median/Premium)
  - Property type distribution (Location/Property)
- Detailed buyer behavior analysis:
  - Budget utilization rates
  - Property type preferences
  - Price trends across rounds
  - Individual buyer summaries

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Apple008811/house-overpayment.git
cd house-overpayment
```

2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

3. Run the application:
```bash
streamlit run Home.py
```

## Project Structure
- `Home.py` - Main application entry point
- `pages/01_Experiment.py` - Experimental interface
- `pages/02_Simulation.py` - Simulation and analysis
- `requirements.txt` - Project dependencies

## Dependencies
- streamlit==1.32.0
- pandas==2.2.0
- numpy==1.26.4
- plotly==5.19.0 