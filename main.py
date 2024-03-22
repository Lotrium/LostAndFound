import tkinter as tk
import geopy.geocoders as geocoders
import requests
from tkintermapview import TkinterMapView
from geopy.exc import GeocoderUnavailable


def search_location():
    try:
        geolocator = geocoders.Nominatim(user_agent="your_app_name")
        location = geolocator.geocode("Your search")
        if location is not None:
            map_widget.set_position(location.latitude, location.longitude)
        else:
            show_error_message("Location not found. Please try again with a different search query.")
    except GeocoderUnavailable as e:
        print(f"Error: {e}")
        show_error_message("Failed to connect to the geocoding service. Please try again later.")
    except requests.exceptions.ConnectionError as e:
        print(f"Error: {e}")
        show_error_message("Failed to connect to the geocoding service. Please try again later.")


def show_error_message(message):
    error_window = tk.Toplevel(root_tk)
    error_window.title("Error")
    error_label = tk.Label(error_window, text=message)
    error_label.pack()
    ok_button = tk.Button(error_window, text="OK", command=error_window.destroy)
    ok_button.pack()


def open_second_window():
    second_window = tk.Toplevel(root_tk)
    second_window.geometry("300x200")
    second_window.title("Search Radius")

    # create slider
    slider = tk.Scale(second_window, from_=0, to=100, orient=tk.HORIZONTAL, label="Search Radius (km)")
    slider.pack()

    # create search button
    search_button = tk.Button(second_window, text="Search", command=lambda: search_location_with_radius(slider.get()))
    search_button.pack()


def search_location_with_radius(radius):
    try:
        geolocator = geocoders.Nominatim(user_agent="your_app_name")
        location = geolocator.geocode("Your search")
        if location is not None:
            map_widget.set_position(location.latitude, location.longitude)
        else:
            show_error_message("Location not found. Please try again with a different search query.")
    except GeocoderUnavailable as e:
        print(f"Error: {e}")
        show_error_message("Failed to connect to the geocoding service. Please try again later.")
    except requests.exceptions.ConnectionError as e:
        print(f"Error: {e}")
        show_error_message("Failed to connect to the geocoding service. Please try again later.")


root_tk = tk.Tk()
root_tk.geometry(f"{800}x{600}")
root_tk.title("map_view_example.py")

# create map widget
map_widget = TkinterMapView(root_tk, width=800, height=600, corner_radius=0)
map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# create search button
search_button = tk.Button(root_tk, text="Search Location", command=open_second_window)
search_button.pack()

root_tk.mainloop()
