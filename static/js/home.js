import flask
flask import Flask
from flask import json


def findLocation() {
	console.log("HERE"); 
	var place = document.getElementById('place1')
	console.log("What?"+jsonify(place)); 
	window.location= "http://127.0.0.1:5000/location/"+jsonify(place);  
	console.log(window.location)
    	}