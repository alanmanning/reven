# reven

## Introduction

### "Why am I paying those a**holes at BC Hydro so much?"

That's the question my mother (a resident of British Columbia) posed to me, and it's the question this project seeks to answer for anyone. I can just go visit my parents and observe their consumption habits, but what if I couldn't? Can the available data reveal enough useful information?

Luckily, hour-by-hour records of your electricity meter is available for download from BC Hydro's website. However, this is the net power use for the entire household. Further analysis is required to tease out useful information about a household's appliances and habits, and to see if there are any simple energy and money-saving changes they could make. For example, on a spring night when no heating or AC is required, there's only quiescent consumption from appliances like refrigerators, freezers, computers, and "parasitic loads" from anything that is in standby. If this is abnormally high, then completely turning things off at night (using a powerbar switch) may help.

Weather generally plays the most significant role in energy consumption through air conditioning and heating. Quantifying this effect is crucial.

This project was a way for me to learn more about web development. Ultimately, I want a website (built using Django) where anyone could have their consumption data analyzed. Technologies I have been playing with are AWS EC2 (for the analysis and downloading), Django, Celery (for running the analysis), and SQL databases.

### The analysis
#### Inputs
- Hour by hour consumption data (downloaded from BC Hydro's website using the billing credentials)
- Hour by house weather data (downloaded from Environment Canada -- eventually will be put in a database)
- BC Hydro billing policy
- Household information, including:
    - number of residents
    - working hours
    - number of refrigerators and freezers
    - type of heating (electricity, natural gas, geothermal, etc.)
    - air conditioning?
    - etc.

#### Obtaining input data (done, needs polishing)

1. **BC Hydro consumption data**: The BC Hydro website doesn't have an api, so I'm using a headless browser (JSDrive with selenium) and a requests module to simulate a login.
2. **Weather data**: Environment canada has a simple url-based downloading scheme for historical weather data, but you can only download so many per web page. I'm using a bash script to download this and paste it together.

#### Correlation with temperature (done)

I'm using an Autoregressive Moving Average (ARMA) model to correlate the temperature with consumption. To do this, I've binned the temperature into high, medium, and low ranges.

#### Presentation of data (in progress)

#### Survey to obtain household data (in progress)

## Django-based website