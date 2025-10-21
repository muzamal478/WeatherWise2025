# WeatherWise CLI App - Python Programming Internship

## Overview
Week 4 Task for Python Programming Internship at BKR Tech Solutions. WeatherWise is a command-line tool using the OpenWeather API. Week 4 focused on showcasing the project on LinkedIn and Facebook, tagging BKR Tech Solutions, and setting up Fiverr/Upwork profiles.

## Project Structure
- `weather.py`: Main script with all features.
- `config.yaml`: User preferences (default city, units).
- `requirements.txt`: Dependencies (`aiohttp`, `requests-cache`, `rich`, `pandas`, `pyyaml`, `pytest`, `pytest-asyncio`, `python-dotenv`).
- `.env`: Store API key (e.g., `API_KEY=your_key_here`).
- `tests/test_weather.py`: Unit and integration tests.
- `.github/workflows/ci.yml`: GitHub Actions CI workflow.
- `docs/research_findings.md`: API research from Week 1.
- `docs/feature_plan.md`: Feature plan from Week 1.
- `screenshots/`: Outputs (`multi_city_rich.png`, `export_csv.png`, `summary_report.png`, `alert_rich.png`).
- `data/search_history.txt`: City search history.
- `exports/`: Exported files (`weather_data.csv`, `weather_data.json`).
- `.gitignore`: Ignores virtual env, sensitive files.
- `portfolio/`: Social media posts, video demo, freelancer profiles.
- `submission/`: PDF for Google Classroom.

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
Run commands with subparsers:
```bash
python weather.py fetch Paris,London --graph --units metric
python weather.py export Paris --type csv --file weather_data.csv
python weather.py summary London
python weather.py config --default-city Karachi --units imperial
python weather.py history
```

## Example Output
```
WeatherWise: Paris
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric          ┃ Value                 ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━┩
│ Temperature     │ 10.06°C               │
│ Humidity        │ 94%                   │
│ Condition       │ ☁️ Overcast clouds    │
│ Wind Speed      │ 0.54 m/s              │
│ Local Time      │ 2025-10-14 22:01      │
└─────────────────┴───────────────────────┘
3-Day Forecast:
┏━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ Date       ┃ Avg Temp   ┃ Condition           ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ 2025-10-15 │ 10.14°C    │ ☁️ Overcast clouds  |
│ 2025-10-16 │ 14.39°C    │ ☁️ Overcast clouds  │
│ 2025-10-17 │ 12.22°C    │ ☀️ Clear sky        │
└────────────┴────────────┴─────────────────────┘
```

## API Setup
- Register at [OpenWeatherMap](https://openweathermap.org/api).
- Store API key in `.env` to avoid hardcoding.

## Testing
Run tests:
```bash
pytest tests/test_weather.py -v
```
## Social Media Showcase
- **LinkedIn Post**: https://www.linkedin.com/posts/muzamalasgharofficial  
- **Facebook Post**: https://www.facebook.com/muzamalasgharofficial/  
- **Freelancer Profiles**:  
  - Fiverr: https://www.fiverr.com/muzamilcreator?public_mode=true
  - Upwork: https://upwork.com/freelancers/muzamala


## Author
Muzamil Asghar  
LinkedIn: [https://www.linkedin.com/in/muzamalasgharofficial/](https://www.linkedin.com/in/muzamalasgharofficial/)  
GitHub: [https://github.com/muzamal478](https://github.com/muzamal478)

## License
MIT