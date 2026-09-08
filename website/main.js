import { makeErrorFunction, NotFoundError } from "./errorhandling.js";

const cityArray = await fetchLocations()

async function fetchLocations() {
        const response = await fetch("http://10.0.0.100:8000/api/weather/cities");
        if (!response.ok) {throw new Error(`Error: ${response.status}`)};
        const data = await response.json();
        const processedData = data.map(element => ({city: element[0]}));
        return processedData;
}


async function fetchWeather(city) {
    const payload = {city: city};
        const response = await fetch("http://10.0.0.100:8000/api/weather/", {method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)});
        if (!response.ok) { throw new Error(`Error: ${response.status}`); }
        return await response.json(); 
    }

function getFormInput(event) {
    event.preventDefault(); 
    const form = new FormData(event.target);
    const cityInput = form.get('city').toLowerCase();
    const result = cityInput
    return result;
}

function setWeather(weatherDetails) {
    document.getElementById('feels-like').innerText = `Feels Like: ${weatherDetails.feels_like} °C`;
    document.getElementById('temperature').innerText = `Temperature: ${weatherDetails.temp} °C`;
    document.getElementById('humidity').innerText = `Humidity: ${weatherDetails.humidity}%`;
    document.getElementById('wind-speed').innerText = `Wind Speed: ${weatherDetails.wind_speed} m/s`;
    document.getElementById('weather-status').innerText = `Condition: ${weatherDetails.weather}`;
}

async function formSubmitFunction(event) {
    try {   
    const formOutput = getFormInput(event);
    const cityResults = cityArray.find(e => e.city.toLowerCase() === (formOutput));
    if (cityResults === undefined) {throw new NotFoundError()};
    const weatherResults = await fetchWeather(cityResults.city);
    setWeather(weatherResults);
    
    }
    catch (error) {
        console.log(error)
        if (error.message.includes("NetworkError")) {
            makeErrorFunction('Network Error, either the server is down or your internet connection is the problem', 'network-error');
        };
        if (error.name === "NotFoundError") {
            makeErrorFunction('City/Country not found, please use the provided list.', 'notfound-error');
        };
    };
}

function findInArray(event) {
    const query = event.target.value.toLowerCase()
    const results = cityArray.filter(e => e.city.toLowerCase().startsWith(query));
    if (results.length === 0) {
        return []; 
    }
        else {
            return results.slice(0, 40);
        }
    };


function inputFunction(event) {
    const arrayResults = findInArray(event);
    const dom = document.querySelector("#cityi-ul");
    dom.innerHTML = ""
    if (arrayResults.length === 0) {
        dom.innerHTML = "No Results found"
    }
    arrayResults.forEach(e => {
        const item = document.createElement("li");
        item.addEventListener("mousedown", liClick)
        item.innerText = e.city;
        dom.appendChild(item);
    }); 
}



function liClick(event) {
    const contents = event.target.textContent;
    document.querySelector("#city-input").value = contents;
}

function blurFunction() {
    document.querySelector("#cityi-ul").innerHTML = "";
}


document.querySelector("#city-input").addEventListener("input",inputFunction);
document.querySelector("#weather-input-form").addEventListener("submit", formSubmitFunction);
document.querySelector("#city-input").addEventListener("blur", blurFunction)