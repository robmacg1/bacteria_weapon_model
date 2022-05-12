
# Read Me

## Bacterial Bomb Model by Rory MacGregor


Repository contents:
> - readme.md: this read me with instructions to run the model and information about the project
> - modelv2.html: PyDoc documentation for the model
> - bacteria.html: PyDoc documentation for the bacteria module
> - modelv2.py: Python script to run the model
> - bacteria.py: Python bacteria module
> - bomb.raster: 300x300 raster image that contains the bomb location as a pixel with a value of 1

### About:
This is a model of the airborne dispersal of bacteria from a bio-bomb detonated above the skyline of a city. The model allows the user to set the wind conditions, the size of the bomb, and the height it is detonated at in a GUI and then plots a density map of the dispersal. The output can be saved as an image or as a .csv for further statistical analysis. Then the model can be reset or have its conditions changed and be run again!

### Instructions:
The model can be run from the command line, in which case the user must:

 - Open a command prompt
 - Either set the working directory to where model.py is located and enter "python model.py" minus the "".
 - Or enter "python c:/user/modeldirectory/model.py" with your own full file path to the model.
 
 It can also be run from inside an IDE such as Spyder or Microsoft Visual Studio Code.
 
#### Adjusting the model
When the model has opened you are faced with the GUI. On the left hand side are the model     parameters which can be adjusted using the sliders before the model is run. 
These are:

 - Bomb Size: Set between 1 and 10,000 (default 5000). It controls how many bacteria particles are modeled. More particles creates a more diffuse density map as values are more evenly spread across the image. I enjoy setting it to less than 1000.
 - Wind Direction North/South: Set between 0 (100% North) and 100 (100% South), default 50. Controls how likely a particle will be blown between North or South.
 - Wind Direction West/East: Set between 0 (100% West) and 100 (100% East), default 95. Controls how likely a particle will be blown between West or East.
 - Wind Speed: Set between 1 (default) and 4. Sets the possible speed a particle can move in m/s. Higher speeds also mean the particle is less likely to be caught in an eddy and stay still.
 - Detonation Altitude: Set between 1 and 150 (default 75). Controls the height in meters at which the bomb is detonated.  Below 75m, the particles are not affected by turbulence and will drop at 1m/s.
 
#### Detonating the bomb
Once the desired parameters are chosen, users can click the "Run Model" button and the heatmap of particles per square meter is visualised to the right of the window with the bomb's location also displayed. This output can either be saved using the "Save Image" button as output.png to the model directory , as a .csv using the save CSV button, or the user can adjust the parameters and run the model again. The model also shows how long in seconds for the last bacteria particle to reach the ground below the options.

### Development
##### Resources used
To better understand how to create the GUI using Tkinter and place elements where I wanted them, I used the website GeeksforGeeks.org. From there I learned how to place widgets in frames and dictate where those frames are within a grid. This was somewhat similar to the CSS grid formatting I have used before to structure my html work.
 
##### Modeling the wind:
I had to spend a significant amount of time conceptualising how to make the wind direction probability adjustable by the user. If I had used 4 sliders, one for each direction, a user could make the wind equally strong in opposite directions. In the end I settled on the following:

A particle's direction of movement each second is randomised between North, South, East or West. However, each possible direction is given a probability weighting using the python "Random" library function "random.choices". These weightings are taken from the 2 directional GUI sliders.  A particles probability to go North is inverse to its probability to go South and likewise for East and West so 2 values are taken from each slider, the "northness" and "southness", and the "eastness" and the "westness" . The random choices function takes these 4 values as a weight and orders the likelihoods a particle will move in each direction. If every value is 50, a particle is equally like to go in any direction. If North is set to 100, South must be set to 0, and it will not go South. If both North and East are set to 100, is equally likely to go either way but will not go South or West. If North is set to 80 and East is set to 50, then it is most likely to go North, equally less likely to go East or West and most unlikely to go South.

However, in testing the weights I realised that it wasn't working how I intended. If north was set to 100 and East and West to 50 each, a particle had a 50% chance to go either East or West, or North, when it should go north the majority of the time. To rectify this I changed the function that created the weights from the sliders to take the 4 values from the 2 sliders and put each of them to the 5th power making their relative sizes more disparate. This had the intended effect but like the rest of the model the values are arbitrary.

##### Testing:
Throughout model.py there are lines of commented code that if the commenting is removed will print values of variables as they are created or read. The testing of processing time taken when the run button is pressed is similarly still in the script at the start and end of where the run function is defined. This was done using the python "time" library.

#### Further development
To take the model further, I would like to be able to set a critical mass threshold of particles per meter that if reached could be plotted as the worst affected areas or where the bacteria would be self-sustaining and then quantify and output this area. I could also implement a way for the user to input their own raster image in the GUI, crop it, find the pixel with the highest or lowest value and take that as the bomb location.

##### Practical uses
A more rigorous version of this model built with the intention of using values derived from real case scenarios could be used to help understand or predict how particulates might disperse in an  environment. For example, pesticides released from planes over agriculture to find the wind conditions that would transport the pesticides over and cover the greatest area, or those conditions where the pesticides would land where they are not intended.

