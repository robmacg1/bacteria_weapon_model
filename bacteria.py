# =============================================================================
# Bacteria Class
# Created by Rory MacGrgegor
# =============================================================================

# =============================================================================
# Import Libraries 
# =============================================================================
import random as rn

# =============================================================================
# Bacteria Class and functions
# =============================================================================
class Bacteria:
    def __init__(self, i, density, direction, altitude, y = 0, x = 0):
        """
        Initialise function of Bacteria class object.

        Parameters
        ----------
        i : Number
            ID of class instance
        density : Array of numbers
            Array to plot density of landed bacteria
        direction : Tuple of 4 numbers
            4 values that represent probability of a particle moving in one of 4 directiosn each second
        altitude : Number
            altitude in meters of bacteria when initialised
        y : number, optional
            bacteria y coordinate. The default is 0.
        x : Number, optional
            bacteria x coordinate. The default is 0.

        Returns
        -------
        None.

        """
        self.id = i
        self.altitude = altitude
        self.x = x
        self.y = y
        # Create counter for each model second of movement
        self.time = 0
        self.density = density
        self.direction = direction

    def __str__(self):
        """
        Function to print number of model seconds bacteria is airborne for

        Returns
        -------
        String
            Number of seconds
        """
        return (str(self.time) + ' Seconds.')

    
    def move(self, speed=1):
        """
        Function to move bacteria once per model second (iteration of move) depending on wind direction weights.

        Parameters
        ----------
        speed : Integer
            Windspeed variable, dictates possible distance bacteria can move in one model second.

        Returns
        -------
        None.

        """
        # Keep iterating until bacteria lands
        while self.altitude > 0:
            # Model turbulence above building height
            if self.altitude >= 75:
                a = rn.random()
                # 70% chance to drop 1m
                if a < 0.7:
                    self.altitude -= 1
                # 20% chance to rise 1m
                if a > 0.8:
                    self.altitude += 1
                # remaining 10% chance to stay at same level
            # No turbulence below building height - bacteria always drops 1m/s
            else:
                self.altitude -= 1
            
            # model bacteria being blown in a direction
            # As speed increases bacteria has less chance to remain at same coordinate
            if rn.random() >0.2/speed:
                # create list for each direction
                nsew = [1,2,3,4]
                # Choose a direction based on weights derived from the wind direction
                b = rn.choices(nsew, weights=self.direction, k=1)
                if b == [1]:
                    #print(self.y)
                    self.y += rn.randint(1,speed)
                    #print(self.y)
                if b == [2]:
                    self.y -= rn.randint(1,speed)
                if b == [3]:
                    self.x += rn.randint(1,speed)
                if b == [4]:
                    self.x -= rn.randint(1,speed)
            
            # Increase model second counter by 1
            self.time += 1
        
        # Once bacteria lands loop ends and density map is increased by 1 at the coordiante of where the bacteria landed
        if self.altitude == 0:
            self.density[self.y][self.x] += 1
