class Movie:
    def __init__(self, name_of_movie, number_of_tickets, total_cost):
        self.name_of_movie = name_of_movie
        self.number_of_tickets = number_of_tickets
        self.total_cost = total_cost

    def __str__(self):
        return (
            f"Movie : {self.name_of_movie}\n"
            f"Number of Tickets : {self.number_of_tickets}\n"
            f"Total Cost : {self.total_cost}"
        )
