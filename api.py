import requests
import json
from collections import namedtuple

class API:

	HOST = 'http://theconsidition.se/'
	_apiKey = ""
	_silent = False

	def __init__(self, apiKey):
		self._apiKey = apiKey


	### Private functions ###

	def _log(self, message):
		if not self._silent: 
			print("API: " + message)
		

	def _handleResponseError(self, e):
		self._log(e.message)
		exit()


	def _handleResponse(self, response):
		if not response.status_code == 200:
			self._log(response.statusCode + ': ' + response.statusMessage)
			exit()


	def _handleResponseData(self, data):
		if data.type == 'Error':
			message = 'An API error occured: ' + data.message
			self._log(message)
			exit()
		if data.type == 'GameError':
			message = 'Your solution gave an error: ' + data.error
			self._log(message)
			exit()

	def _get(self, path, queryStringParams = ''):
		headers = {'X-ApiKey': self._apiKey}
		url = self.HOST + path
		return requests.get(url, headers=headers, params=queryStringParams)


	def _post(self, path, queryStringParams = '', jsonBody = ''):
		headers = {'Accept': 'application/json', 'Content-Type': 'application/json','X-ApiKey': self._apiKey}
		url = self.HOST + path
		return requests.post(url, headers=headers, params=queryStringParams, json=jsonBody)		

	#### Public functions ###

	def silence(self):
		self._silent = True

	def unsilence(self):
		self._silent = False

	def initGame(self):
		response = self._get("considition/initgame")
		self._handleResponse(response)
		gameResponse = json2obj(response.text)
		self._handleResponseData(gameResponse)
		self._log("Created new game with ID " + str(gameResponse.gameId))
		return gameResponse.gameId

	def getMyLastGame(self):
		response = self._get("considition/getgame")
		self._handleResponse(response)
		gameResponse = json2obj(response.text)
		self._handleResponseData(gameResponse)
		self._log("Retrieved game with ID " + str(gameResponse.gameState.id))
		return gameResponse.gameState

	def getGame(self, gameStateId):
		queryStringParams = {"gameStateId" : str(gameStateId)}
		response = self._get("considition/getgame", queryStringParams)
		self._handleResponse(response)
		gameResponse = json2obj(response.text)
		self._handleResponseData(gameResponse)
		self._log("Retrieved game with ID " + str(gameResponse.gameState.id))
		return gameResponse.gameState

	def submitSolution(self, solution, gameStateId):
		queryStringParams = {"gameStateId" : str(gameStateId)}
		response = self._post("considition/submit", queryStringParams, solution)
		self._handleResponse(response)
		gameResponse = json2obj(response.text)
		self._handleResponseData(gameResponse)
		self._log("Your solution gave " + str(gameResponse.points) + " points")
		return gameResponse.points


### Helper functions ###
def json2obj(data): return json.loads(data, object_hook=_json_object_hook)
def _json_object_hook(d): return namedtuple('Anonymous', d.keys())(*d.values())