"""
Phincho Sherpa
CSCI 3725: Computational Creativity
PQ1: Markov Distinction
Sept 17th, 2024

Objective: Create a visual system that recommends different seasonal activites in a certain date using
           transitional matrix

"""
import numpy as np
import math
import matplotlib.pyplot as plt
from PIL import Image
from datetime import date, timedelta, datetime

FINAL_TRANSITION_MATRIX = dict()
RANDOM_VALUE_LIST = []

class SeasonalPlanner():
    """
    Stores all my favorite activities for each season
    """
    FALL = ["drink apple cider", "camping", "go apple picking", "hiking"]
    SPRING = ["camping", "gardening" "farmers market", "visit the zoo", "hiking", "camping"]
    WINTER = ["Make snowman", "skiing", "snowboarding", "snowshoeing", "ice fishing"]
    SUMMER = ["Beach", "BBQ with friends", "picnic", "camping"]
    SEASONS = ['Fall', 'Summer', 'Winter', 'Spring']
    
    def __init__ (self):
        user_season = self.fav_season()
        self.num_activities = self.num_activities()

    def fav_season(self):
        """
        Ask user for their favorite season
        
        Assign user's output to a variable
         """
        fav_season = input("What is your favorite season? ")
        if fav_season == "fall":
           self.user_season = self.FALL
        elif fav_season == "spring":
           self.user_season = self.SPRING
        elif fav_season == "winter":
           self.user_season = self.WINTER
        else:
           self.user_season = self.SUMMER
     
    def num_activities(self):
        """
        Ask user for number of activities recommendation
        
        Returns an integer
        """
        num_activities = input("How many recommendation do you want? ")
        return num_activities
     
    def random_num_sum_one(self, n):
        """
        Calculates random number with a sum of 1 that are associated with a key
        
        Returns a list of values with a sum of 1 
        """
        RANDOM_VALUE_LIST.clear()
        [random_values] = np.random.dirichlet(np.ones(n),size=1)
        for i in range(0,len(random_values)):
            RANDOM_VALUE_LIST.append(random_values[i])
        
    def create_transition_matrix(self):
        """
        Creates a specific matrix depending on the season
        
        Returns dictionary with user's favorite activity as a key and probability as a value
        """
        user_fav_season = self.user_season 
        length = len(user_fav_season)
        activity = [] 
        row = dict()
    
        for i in range(0, length):
            self.random_num_sum_one(length)
            for j in range(0,len(RANDOM_VALUE_LIST)):
                row.update({user_fav_season[j]:RANDOM_VALUE_LIST[j]})
            activity.append(row)
            row = {}
        return activity

    def final_transition_matrix(self):
        """
        Writes out the final season matrix
        
        Returns the final transition matrix
        """
        user_fav_season = self.user_season
        transition_matrix = dict()
        for i in range(0,len(user_fav_season)):
            transition_matrix.update({user_fav_season[i]:self.create_transition_matrix()[i]})
        FINAL_TRANSITION_MATRIX = transition_matrix
        return FINAL_TRANSITION_MATRIX
    
    def get_next_activity(self, current_activity):
        """
        Decides what activity to recommend depending on current activity
        
        Return the next activity based on the probability from the current one
        """
        matrix = self.final_transition_matrix()
        # print(self.final_transition_matrix().keys())
        return np.random.choice(list(matrix.keys()), 
                p = [matrix[current_activity][next_activity]for next_activity in matrix]
        )
        
    def get_activity(self, activity = "camping", time=5): 
        """
        Get a new activity and adds them in a list
        
        Returns a list of activity the user can do 
        """
        time = self.num_activities
        full_list = []
        while len(full_list) < int(time):
            next_activity = self.get_next_activity(activity)
            full_list.append(next_activity)
        return full_list
        
    def date_generator(self, start_date = date.today()):
        """
        Randomly generates date according to the season start and end date
        
        Returns days that a user could do the activity
        """
        self.start_date = start_date
        dates = {"SPRING":[date(2025, 3, 20), date(2025, 6, 20)],"SUMMER":[date(2025, 6, 20), date(2025, 9, 22)],
                "WINTER":[date(2024, 12, 20), date(2025, 3, 20)], "FALL": [date(2024, 9, 22), date(2024, 12, 20)]}
         
        num_activities = self.num_activities
        start_date = dates.get("SUMMER", [])
        end_date = dates.get("SUMMER", [])
        for keys in dates.keys():
            if keys == "SUMMER":
                start_date = datetime.strptime(str(start_date[0]), "%Y-%m-%d")
                end_date = datetime.strptime(str(end_date[1]), "%Y-%m-%d")  
        days_num = end_date - start_date
        random_days = np.random.choice(days_num.days, int(num_activities), replace = False)
        days = [start_date + timedelta(days = int(day)) for day in random_days]
        return days
        
    def activity_to_images(self, sequence):
        """
        Gets an image of the activity 
        
        Return a image depending on the activity
        """
        images = []
        for move in sequence:
            match move:
                case 'drink apple cider':
                    images.append("assets/apple_cider.jpg")
                case 'camping':
                    images.append("assets/camping.jpg")
                case 'go apple picking':
                    images.append("assets/apple_picking.jpeg")
                case 'hiking':
                    images.append("assets/hiking.jpg")
                case "camping":
                    images.append("assets/camping.jpg")
                case "gardening":
                    images.append("assets/gardening.jpeg")
                case "farmers market":
                    images.append("assets/farmers_market.jpeg")
                case "visit the zoo":
                    images.append("assets/visit_zoo.jpeg")
                case "Make snowman":
                    images.append("assets/make_snowman.jpg")
                case "skiing":
                    images.append("assets/skiing.jpg")
                case "snowboarding":
                    images.append("assets/snowboarding.jpg")
                case "ice fishing":
                    images.append("assets/ice_fishing.jpg")
                case "snowshoeing":
                    images.append("assets/snowshoeing.jpeg")
                case "BBQ with friends":
                    images.append("assets/bbq.jpeg")
                case "picnic":
                    images.append("assets/picnic.jpg")
        return images

def main():
    maker = SeasonalPlanner()
    date = maker.date_generator()
    activities = maker.get_activity()
    images = maker.activity_to_images(activities)
    
    # takes the images and uses the entire plot as an image frame 
    for i in range(1, int(maker.num_activities)+1):
        plt.subplot(math.ceil(int(maker.num_activities)/2), math.ceil(int(maker.num_activities)/2), i)
        plt.xticks([])
        plt.yticks([])
        plt.xlabel(date[i-1])
        plt.title(activities[i-1], weight = "bold")
        image = Image.open(images[i-1])
        plt.imshow(image)

    plt.show() 

if __name__ == "__main__":
    main()



   
        

     