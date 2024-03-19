import io
import math
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk

import requests
from PIL import Image, ImageTk
from geopy.geocoders import Nominatim


def search_location():
    messagebox.showinfo("Promień", f"Wybrano promień {slider.get()} kilometrów")
    distance = int(slider.get())
    g = Nominatim(user_agent="myGeocoder")
    location = g.geocode(search_entry.get())
    if location is not None:
        lat, lon = location.latitude, location.longitude
        current_lat, current_lon = get_current_location()
        map_data = get_map_data(lat, lon, distance, current_lat, current_lon)
        if map_data is not None:
            map_image = Image.open(io.BytesIO(map_data))
            map_photo = ImageTk.PhotoImage(map_image)
            map_canvas.delete("all")
            map_canvas.create_image(0, 0, image=map_photo, anchor="nw")
            map_canvas.image = map_photo


def get_map_data(lat, lon, distance, current_lat, current_lon):
    url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom=13&size=600x400&key=AIzaSyBarXcsdnp61VQTyk3y71J2C_rn3hk_1oY&scale=2&path=color:0xff0000ff|weight:5|{get_encoded_polygon(lat, lon, distance)}&markers=color:red%7Clabel:Current%20Location%7C{current_lat},{current_lon}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Błąd pobierania mapy: {response.status_code}")
        return None


def get_encoded_polygon(lat, lon, distance):
    # Get the four corners of a square centered at the given latitude and longitude
    # with a side length of 2*distance meters
    corner1_lat, corner1_lon = lat + distance / 111120.0, lon - distance / 111320.0 * math.cos(math.radians(lat))
    corner2_lat, corner2_lon = lat - distance / 111120.0, lon + distance / 111320.0 * math.cos(math.radians(lat))
    corner3_lat, corner3_lon = corner2_lat, corner2_lon - 2 * distance / 111320.0 * math.cos(math.radians(lat))
    corner4_lat, corner4_lon = corner1_lat, corner1_lon + 2 * distance / 111320.0 * math.cos(math.radians(lat))

    # Encode the four corners as a polygon
    polygon = "enc:"
    polygon += f"{corner1_lat},{corner1_lon};"
    polygon += f"{corner2_lat},{corner2_lon};"
    polygon += f"{corner3_lat},{corner3_lon};"
    polygon += f"{corner4_lat},{corner4_lon};"
    polygon += "e"

    return polygon


def get_current_location():
    g = Nominatim(user_agent="myGeocoder")
    location = g.geocode("My location", exactly_one=True)
    if location is not None:
        lat, lon = location.latitude, location.longitude
        return lat, lon
    else:
        return None


root = tk.Tk()
root.title("Lost And Found")

search_entry = ttk.Entry(root, width=40)
search_entry.grid(row=0, column=0, padx=10, pady=10)

slider = ttk.Scale(root, from_=0, to=100, orient="horizontal")
slider.grid(row=1, column=0, padx=10, pady=10)
slider_label = ttk.Label(root, text=f"{slider.get()} km")
slider_label.grid(row=1, column=2, padx=10, pady=10)
slider.bind("<ButtonRelease-1>", lambda e: slider_label.config(text=f"{slider.get()} km"))

search_button = ttk.Button(root, text="Szukaj", command=search_location)
search_button.grid(row=0, column=1, padx=10, pady=10)

map_frame = ttk.Frame(root, width=600, height=400)
map_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

map_canvas = tk.Canvas(map_frame, width=600, height=400)
map_canvas.pack(side="top", fill="both", expand=True)

root.mainloop()
