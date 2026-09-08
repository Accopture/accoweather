# accoweather
weather site with an unnecessary python backend

## i made EVERYTHING myself, there isnt a singular line of ai generated code or design
though i did use ai to:
1. clean up my css (cause it was actually rancid)
2. teach me how to make this (my first ever time making something like this, still 0 code tho)

## Architecture
okay so basically, the backend uses a postgresql database consisting of 50 thousand something city names, alongside their coordinates (basically its own geocoding api)
loads just the 50k cities into the browser's ram, and then it checks if whatever's in the input box matches anything in the object array

it uses the openweathermap api (use open-meteo tho its better)


## preview of the website
<img width="1726" height="1017" alt="image" src="https://github.com/user-attachments/assets/b1833c95-94dd-4195-81a2-a02cdec521e5" />
<img width="1726" height="1017" alt="image" src="https://github.com/user-attachments/assets/664fc097-3fd1-47ad-91e5-3b4bbb99c541" />

