# =============================================================================
# Bio-Bomb Model
# Created by Rory MacGrgegor
# =============================================================================

# =============================================================================
# Import Libraries 
# =============================================================================
import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use('TkAgg') 
import bacteria
import csv
import random
import matplotlib.animation
import matplotlib.ticker as tick
import time

random.seed(1)

# Create tkinter instance
root = tk.Tk() # main root

# =============================================================================
# Model Class 
# =============================================================================
class Model:
    def __init__(self, master):
        """
        Model Class containing GUI formatting, controls and model fucntions

        Parameters
        ----------
        master : Inital tkinter window
            Takes a tkinter instance window to use for the model and its GUI

        Returns
        -------
        None.

        """
        
        # =============================================================================
        # Build GUI         
        # =============================================================================
        # Create initial pyplot figure for visual output
        self.figure=plt.figure(figsize=(7,7))
        
        # Set master GUI window, size and title it
        self.master = master
        self.master.title('Bio Weapon')
        self.master.geometry('1024x850')
        
        # Create heading widget and place it on the tkinter grid in the master window
        self.heading = tk.Label(self.master, text='Bio-Weapon Fallout Modeler', font=30, pady=20)
        self.heading.grid(column=1, row=0, columnspan=2)
        
        # Create visual output frame place it on the tkinter grid in the master window
        self.map = tk.Frame(self.master)
        self.map.grid(column=1, row=1, columnspan=2, rowspan=2)
        
        # Create canvas frame that takes the pyplot figure and packs it in the visual output frame
        self.canvas = FigureCanvasTkAgg(self.figure, self.map)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, expand=0)
        
        # Create option control frame and place it on the grid in the master window
        self.options = tk.LabelFrame(self.master, text='Model Options')
        self.options.grid(column=0, row=1, columnspan=1, padx=20)
        
        # Create frame for buttons and place at the bottom of the options frame
        self.buttons = tk.Frame(self.options)
        self.buttons.pack(side=tk.BOTTOM, pady=20)
        
        # Create control sliders, label them, set parameters, orient them and place them in the options frame
        self.slider1 = tk.Scale(self.options, label="Bomb Size", from_=1, to=10000, resolution=1, orient=tk.HORIZONTAL)
        self.label2 = tk.Label(self.options, text="Wind Direction")
        self.slider2 = tk.Scale(self.options, label="North<->South", from_=0, to=100, resolution=1, orient=tk.HORIZONTAL)
        self.slider3 = tk.Scale(self.options, label="West<->East", from_=0, to=100, resolution=1, orient=tk.HORIZONTAL)
        self.slider5 = tk.Scale(self.options, label="Altitude", from_=0, to=150, resolution=1, orient=tk.HORIZONTAL)
        self.slider4 = tk.Scale(self.options, label="Wind Speed", from_=1, to=4, resolution=1, orient=tk.HORIZONTAL)
        self.slider1.pack()
        self.label2.pack(pady=10)
        self.slider2.pack()
        self.slider3.pack()
        self.slider4.pack()
        self.slider5.pack()
        # Set the slider defaults
        self.defaults()
        
        # Create the button controls and place them in the buttons frame
        self.runbutton = tk.Button(self.buttons, text="Run Model", command=self.run)
        self.runbutton.pack(pady=5)
        self.reset_b= tk.Button(self.buttons, text="Reset Parameters", command= self.defaults)
        self.reset_b.pack(pady=5)
        self.save_b= tk.Button(self.buttons, text='Save Image', command=self.save_img)
        self.save_b.pack(pady=5)
        self.save_csv= tk.Button(self.buttons, text='Save CSV', command=self.write_csv)
        self.save_csv.pack(pady=5)
        self.quit_b=tk.Button(self.buttons, text="Quit", command=self.quit)
        self.quit_b.pack(pady=5)
        
        # Create a text output frame and place it on the master grid below the options frame
        self.txt_output=tk.LabelFrame(self.master, text='Duration:')
        self.txt_output.grid(column=0, row=4, columnspan=2, pady=5, padx=5, sticky=tk.W)
        self.text = tk.Text(self.txt_output, height=3, width=35,)
        self.text.pack(expand=0)
        
    # =============================================================================
    # Model Functions
    # =============================================================================
    def run(self):
        """
        Run Model Function. Clears previous output and creates density map array of zeros. Finds Bomb Location from input raster and plots
        its location. Determines wind speed, direction, number of bacteria in bomb and its altitude from user inputs. Creates list of bacteria
        class objects with those inputs. Moves each bacteria dependent on input conditions and increases density map array by 1 where each lands.
        Creates plot of density map and draws it to the canvas GUI frame. Determines bacteria which was airborne longest and derives fallout duration.

        Returns
        -------
        None.

        """
        # Start testing processing time
        # start = time.time()

        # Clear previous outputs, initialise density map array
        self.text.delete(1.0,tk.END)
        self.figure.clear()
        self.density_map = [[float(0) for i in range(500)] for j in range(500)]
        #print(density_map)
        
        # Find bomb x,y coordinates from input raster, plot and annotate its location
        bomb_loc = self.find_bomb('bomb.raster')
        plt.scatter(bomb_loc[0], bomb_loc[1], c = 'red', s=2,)
        plt.annotate('Bomb', (bomb_loc[0]+2, bomb_loc[1]+2), color='white', size=7)
        #print(str(bomb_loc)+" are the bomb coordinates")
        
        # Determine wind direction and speed conditions from GUI inputs
        direction = self.get_winddirection()
        windspeed = self.slider4.get()
        #print(direction + windspeed)
        
        # Determine number of bacteria in bomb and its altitude from GUI inputs
        no_particles = self.slider1.get()
        altitude = self.slider5.get()
        #print(str(no_particles)+' airborne at '+ str(altitude) + ' meters')
        
        # Create empty list, populate with specified number of bacteria class instances
        particles = []
        for i in range(no_particles):
            particles.append(bacteria.Bacteria(i, self.density_map, direction, altitude, bomb_loc[1], bomb_loc[0]))
        # for i in particles:
        #     print(i)    
       
        # Move each bacteria until it lands, then move the next, etc.
        for i in range(len(particles)):
            particles[i].move(windspeed)
        
        # Create plot and label axes, plot density map array and legend color bar and draw it to the canvas GUI frame
        plt.xlim([0, 300])
        plt.ylim([0, 300])
        plt.xlabel("Meters")
        plt.ylabel("Meters")
        plt.imshow(self.density_map, cmap="gray")
        plt.colorbar(fraction=0.046, format=tick.FormatStrFormatter('%.0f')).set_label('Particle density per meter')
        self.canvas.draw()
        
        # Find which bacteria was airborne for the longest and print how long it took to land in the GUI output frame
        time_to_run = max(particles, key=lambda bacteria: bacteria.time)
        self.text.insert(tk.END, time_to_run)

        # Finish testing processing time
        # end = time.time()
        # total_time = end - start
        # print(str(total_time))

    def find_bomb(self, raster):
        """
        Funtion that takes an input raster of 0s with one pixel with value 1 and returns that pixel's x,y coordinates

        Parameters
        ----------
        raster : csv grid of integers
            Must contain all 0s except for one 1.

        Returns
        -------
        bomb_loc : List
            List of 2 integers, first being the y coordinate and the second be ing the x: [y,x]

        """
        # Create empty list
        city_map=[]
        
        # open input raster use csv.reader to read it in as an array
        with open(raster, newline="") as grid:
            city_grid = csv.reader(grid, delimiter = ",", quoting=csv.QUOTE_NONNUMERIC)
            # Go through the array and append each value to the city map list
            for i in city_grid:
                j = []
                for k in i:
                    j.append(k)
                city_map.append(j)
        # close the opened file
        grid.close()
        
        # Create blank x and y variables
        y = None
        x = None
        
        # go through city map array and find location list indices for where array has value 1, indices = y and x
        for i in city_map:
            for j in i:
                if j != 0:
                    y = city_map.index(i)
                    x = i.index(j)
        bomb_loc = [x, y]
        return bomb_loc

    def defaults(self):
        """
        Funtion that sets GUI sliders default values

        Returns
        -------
        None.

        """
        # No of bacteria. Between 1 and 10,000
        self.slider1.set(5000)
        # North/South wind direction 50 is equal. Between 1 and 100.
        self.slider2.set(50)
        # West/East  wind direction 50 is equal. Between 1 and 100
        self.slider3.set(95)
        # Windspeed m/s between 1 and 4
        self.slider4.set(1)
        # Altitude of bomb. Between 1 and 150
        self.slider5.set(75)

    def get_winddirection(self):
        """
        Function to return 4 values for wind direction analog. Takes the input of 2 GUI sliders, one for North/South wind amount where 100 is all in one direction and 0 is all in the other.
        and one for East/West the same. 

        Returns
        -------
        Tuple of the values for each direction to be used as weighting for random.choices fucntion

        """
        # Gets slider value for North/South and derives how close it is to south and how far it is from south and multiplies each by the power of 5
        # to exponentially increase the wights towards 100
        ns = self.slider2.get()
        s = ns ** 5
        n = (100 - ns) **5
        # Same as NOrth south but for East/West
        ew = self.slider3.get()
        e = ew**5
        w = (100 - ew)**5
        print(n,s,e,w)
        return(n,s,e,w)

    def save_img(self):
        """
        Function to save the pyplot output as a png into the model folder

        Returns
        -------
        None.

        """
        plt.savefig('output.png')

    def write_csv(self):
        """
        Function to write a csv of the density map
        """
        with open("output.csv", "w", newline="") as out_csv:
            writer = csv.writer(out_csv)
            writer.writerows(self.density_map)
    
    def quit(self):
        """
        Funtion to quit the model app
        """
        self.master.quit()

# =============================================================================
# Run Model
# =============================================================================
gui =  Model(root)

root.mainloop() 

# =============================================================================
# END
# =============================================================================
                     
                   
