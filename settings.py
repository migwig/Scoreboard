class AppState:
	def __init__(self):
		self.settings = {
			"period_time": 20, 
			"num_periods": 3,
			"break_time" : 15,
			"home_team" : "Home",
			"away_team" : "Away"
		}
		self.home_score = 0
		self.away_score = 0
		self.strip_status = False
		self.timer_status = False
		self.start_time = 0
		self.display_time = self.settings['period_time']

state = AppState()