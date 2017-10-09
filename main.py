from api import API
### TODO: Enter your API key
API_KEY = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXX'
_api = API(API_KEY)

def solve(game):
	
	# --- Available commands ---
	# TRAVEL [NORTH|SOUTH|WEST|EAST]
	# [BUS|TRAIN|FLIGHT] {CityName}
	# SET_PRIMARY_TRANSPORTATION [CAR|BIKE]
	 
	
	# TODO: Implement your solution
	
	# Example solution
	solution = list();
	x = game.start.x;
	y = game.start.y;
	while (x < game.end.x):
		x+=1;
		solution.append("TRAVEL EAST");
	while (y < game.end.y):
		y+=1;
		solution.append("TRAVEL SOUTH");
	
	return solution;


def main():
	_api.initGame()
	game = _api.getMyLastGame()
    #Or get by gameId:
	#game = _api.getGame();
	solution = solve(game)
	_api.submitSolution(solution, game.id)

main()