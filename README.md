# LabDemos
A few python scripts to use as deoms in UTA's labs

# Installing 

## Requirements:
 - Python 3
 - Numpy 
 - PyQt5 

These should be easy to download with your package manager 

## Installing Dependencies

### Linux 

You can just use the pre-installed package manager (`apt`), and installing the dependencies should be as easy as opening a command terminal (Ctrl + Alt + T)
```
sudo apt-get install git python3 python3-numpy python3-pyqt5 
```
then it should ask you for your password, ask for approval, and install these things. Then go to a directory of your choice and run 
```
git clone git@github.com:BenSmithers/LabDemos.git
```
Then change directories `cd LabDemos/Unit6` into the Unit 6 folder, and follow the instructions below! 

### Mac OSX 

I haven't done this myself, but there's a guide [here](https://docs.python-guide.org/starting/install3/osx/) for installing python 3 and "brew" on Mac computers. Then you _should_ be able to just do
```
brew install pyqt5 git
pip3 install numpy 
```
I'm not sure if this will install it for python2 or python3 though. So take care! But from here, you should be able to follow the steps outlined in the Linux part from the git cloning onwards.

### Windows

This is a lot harder to do. There are a few options
1. Get an IDE like Enthought Canopy or Microsoft Visual Studio
2. Use that, or git bash, to clone this repository. Or you can just download it manually. 
3. Use whichever IDE you have from (1) to download the appropriate packages
4. Run `launch.py`

# Unit 6: Rotational Equilibrium 

This is a little demo to play around with torque and rotational equilibrium

## Instructions: 

Launch file using `python launch.py` or `./launch.py`

 - You can use square brackets '[' and ']' to zoom in and out, respectively 
 - The circle is 10 inches in radius
 - You can add masses by clicking the "place new button." They are created at the coordinates shown and with the mass shown. 
 - You can move the masses around by clicking and dragging
 - by clicking on a mass, its coordinates and mass is shown. You need to click right at the center! There is a slight tolerance but not a lot. 
 - The color of the circle represents how imbalanced it is. The more red, the less balanced. The more green, the more balanced. 
 - An arrow is drawn representing the current net torque on the system. 

Try follow along the lab manual's instructions! 

# Unit 8: Archimede's Principle

Demo showing measured force felt by force-meter due to suspended masses. Watch as the force shrinks, as you dip them in the water, due to the action of the buoyant force on the masses! 

## Instructions: 

Launch file using `python launch.py` or `./launch.py`

 - You can use square brackets '[' and ']' to zoom in and out, respectively 
 - Click and drag the top of the masses to move them around 
 - There are four masses: three cylinders (blue, black, orange), and one irregularly shaped mass. 
 - Use the force-meter to see the apparent weight of the suspended mass
 - use the drop-down menu on the right to change the fluid in the cup