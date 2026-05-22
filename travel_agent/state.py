class TravelState:
    def __init__(self):
        self.budget = None
        self.dates = None
        self.destination = None
        self.preferences = []
        self.trip_duration = 5

    def is_budget_missing(self):
        return self.budget is None

    def is_dates_missing(self):
        return self.dates is None