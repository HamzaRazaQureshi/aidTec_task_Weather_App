import tkinter as tk
from tkinter import scrolledtext
import requests
from datetime import datetime

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        
        self.root.geometry("800x600")  
    
        self.location_label = tk.Label(root, text="Enter City:", font=("Helvetica", 14))
        self.location_label.pack(pady=10)
        
        self.location_entry = tk.Entry(root, font=("Helvetica", 12))
        self.location_entry.pack(pady=5)
        
        self.fetch_button = tk.Button(root, text="Fetch Weather", command=self.fetch_weather, font=("Helvetica", 12))
        self.fetch_button.pack(pady=10)
        
        self.weather_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Helvetica", 12))
        self.weather_text.pack(fill=tk.BOTH, expand=True)
        
    def fetch_weather(self):
        city = self.location_entry.get()
        api_key = "4aecd5c1d1939b3d51bea3b486297d81" 
        data = self.get_weather_data(api_key, city)
        
        if data["cod"] == "404":
            self.weather_text.config(state=tk.NORMAL)
            self.weather_text.delete("1.0", tk.END)
            self.weather_text.insert(tk.END, "City not found")
            self.weather_text.config(state=tk.DISABLED)
        else:
            forecast_info = self.extract_forecast_info(data)
            self.weather_text.config(state=tk.NORMAL)
            self.weather_text.delete("1.0", tk.END)
            self.weather_text.insert(tk.END, forecast_info)
            self.weather_text.config(state=tk.DISABLED)
    
    def get_weather_data(self, api_key, city):
        base_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
        
        response = requests.get(base_url)
        data = response.json()
        return data
    
    def extract_forecast_info(self, data):
        forecast_by_date = {}
        for forecast in data["list"]:
            timestamp = forecast["dt"]
            date = datetime.utcfromtimestamp(timestamp)
            temperature = forecast["main"]["temp"]
            humidity = forecast["main"]["humidity"]
            wind_speed = forecast["wind"]["speed"]
            description = forecast["weather"][0]["description"]
            
            if date.date() not in forecast_by_date:
                forecast_by_date[date.date()] = []
            
            forecast_by_date[date.date()].append((date.strftime('%H:%M'), temperature, humidity, wind_speed, description))
        
        formatted_forecast = ""
        for date, forecasts in forecast_by_date.items():
            formatted_forecast += f"{date.strftime('%Y-%m-%d')}:\n"  
            for time, temperature, humidity, wind_speed, description in forecasts:
                formatted_forecast += (
                    f"\n  Time: {time}, \n\tTemperature: {temperature}°C, \n\tHumidity: {humidity}%, \n\tWind Speed: {wind_speed} m/s, \n\tDescription: {description}\n\n"
                )
            formatted_forecast += "\n" 
        
        return formatted_forecast
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    app.run()
