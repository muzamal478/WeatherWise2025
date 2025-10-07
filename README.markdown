# WeatherWise CLI App - Python Programming Internship

## Overview
Week 2 Task for Python Programming Internship at BKR Tech Solutions. WeatherWise is a command-line tool using the OpenWeather API to fetch real-time weather data. Features include city search history, multi-city weather fetching, visualizations, time zone support, and weather alerts. Fixed Unicode encoding issues for file output.

## Project Structure
- `weather.py`: Main script with all features.
- `requirements.txt`: Dependencies (`requests`, `tabulate`, `colorama`, `argparse`, `matplotlib`, `pytz`, `python-dotenv`).
- `.env`: Store API key (e.g., `API_KEY=your_key_here`).
- `docs/research_findings.md`: API research from Week 1.
- `docs/feature_plan.md`: Feature plan from Week 1.
- `screenshots/`: Outputs (`multi_city_output.png`, `temp_graph.png`, `humidity_graph.png`, `alert_example.png`).
- `data/search_history.txt`: Stores city search history.
- `.gitignore`: Ignores virtual env, sensitive files.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/muzamal478/WeatherWise2025.git
   cd WeatherWise2025
   ```
2. Set up virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Add OpenWeatherMap API key:
   - Create a `.env` file with:
     ```
     API_KEY=your_key_here
     ```
   - Get key from [OpenWeatherMap](https://openweathermap.org/api).

## Usage
Run with city names (single or multiple):
```bash
python weather.py Paris
python weather.py Paris,Lahore,Tokyo --graph
```
Options:
- `--graph`: Show temperature/humidity graphs.
- `--history`: View last 5 searched cities.
- `--clear-history`: Clear search history.

## Example Output
```
WeatherWise: Paris
╒═══════════════════╤══════════════════╕
│ Current Weather   │                  │
╞═══════════════════╪══════════════════╡
│ Temperature       │ 10.06°C          │
│ Humidity          │ 94%              │
│ Condition         │ Overcast clouds  │
│ Wind Speed        │ 0.54 m/s         │
│ Local Time        │ 2025-10-07 07:19 │
╘═══════════════════╧══════════════════╛

3-Day Forecast:
╒════════════╤════════════╤═════════════════╕
│ Date       │ Avg Temp   │ Condition       │
╞════════════╪════════════╪═════════════════╡
│ 2025-10-07 │ 10.14°C    │ Overcast clouds │
│ 2025-10-08 │ 14.39°C    │ Overcast clouds │
│ 2025-10-09 │ 12.22°C    │ Clear sky       │
╘════════════╧════════════╧═════════════════╛
```

## API Setup
- Register at [OpenWeatherMap](https://openweathermap.org/api).
- Store API key in `.env` to avoid hardcoding.

## Author
Muzamil Asghar  
LinkedIn: [https://www.linkedin.com/in/muzamalasgharofficial/](https://www.linkedin.com/in/muzamalasgharofficial/)  
GitHub: [https://github.com/muzamal478](https://github.com/muzamal478)

## License
MIT