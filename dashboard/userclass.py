from django.shortcuts import render
import requests
from requests.api import request

class Administrator_User:
     def __init__(self, firstname, lastname,username,role): 
        self.firstname = firstname 
        self.lastname = lastname
        self.username = username
        self.role = 'Administrator'

class Standard_User:
     def __init__(self, firstname, lastname,username,role): 
        self.firstname = firstname 
        self.lastname = lastname
        self.username = username
        self.role = 'Standard User'