This is the new version of the code, which freezes the images to the MicroPython firmware instead of compiling them and storing them like normal.

This firmware was made by adding an 'images' module that contains all the image files for the project, as well as the card dictionary. This is meant to prevent the program from loading any of the images to ram, which prevents memory errors, as well as speeds up the process somewhat.
From my testing, this change seems to have completely prevented any memory errors from occurring, even when I turn up the glitch effects to use more memory. 

Additionally, this code updates the ePaper driver, allowing us to use just a single driver rather than the 2 from before. I have modified that driver slightly, by shortening the 'sleep' times and deleting the non-PIO version of the code. 
