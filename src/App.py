# Entry point for the application.

from . import app
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import googlemaps
from src.controller.RouteController import RouteController
from src.view.view import MapView

gmaps = googlemaps.Client(key='AIzaSyCC19S4I6tEZYE9Iv4zhsNRixctc6gp_Dc')

@app.route("/")
def home():
	return render_template("index.html")

@app.route('/<request>', methods=['GET'])
def index(request):
	if bool(request):

		request = request.replace("%2C", "," )
		request = request.replace("%20", " " )
		start_location, end_location, percentage, minmax_elev_gain = request.split(":")
		print("Input Parameters")
		print(start_location)
		print(end_location)
		print(percentage)
		print(minmax_elev_gain)
		

		start_coordinates = [gmaps.geocode(start_location)[0]['geometry']['location']['lat'], gmaps.geocode(start_location)[0]['geometry']['location']['lng']]
		end_coordinates = [gmaps.geocode(end_location)[0]['geometry']['location']['lat'], gmaps.geocode(end_location)[0]['geometry']['location']['lng']]

		view = MapView()
		controller = RouteController()
		
		controller.calculate_final_route(start_coordinates, end_coordinates, percentage, minmax_elev_gain, view)
		path_coordinates, total_distance, calculated_elevation = view.get_route_params()
		path_coordinates = [i[::-1] for i in path_coordinates]
		path = [[]]
		route_cds = []
		c = 0
		print("Path Coordinates:")
		print(len(path_coordinates), path_coordinates)
		
		for coordinate in path_coordinates:
			if c == 23:
				c = 0
				path.append([])
			path[-1].append(coordinate)
			c += 1
		print("Elevation:", calculated_elevation)
	return jsonify(origin=start_coordinates, des=end_coordinates,path=path, dis=total_distance, elev=calculated_elevation)