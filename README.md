# Air Canvas

Tired of listening to Powerpoints remotely? <br />
Finding new ways to communicate effectively through digital media? <br />
Want to create a fun and interactive learning environment? <br />

Try out the Air Canvas!!! <br />
You can use any object with a colored tip (e.g. defaulting using a blue expo marker) as a stylus. <br />

![demo](demo.gif)

## Getting Started

### Installing

Download this repository by clicking the green button on the upper right corner

or for advanced users:  

```
git clone git@github.com:flynn-chen/air-canvas.git
conda -n air_canvas create -f environment.yml
conda activate air_canvas
```


### Running

For macOS users,
a terminal will pop up and ask for your password for sudo, 
because keyboard tracking requires multi-threading.

double click
```
run.command
```
or for advanced users:  
```
python air_canvas.py
```

### Usage

Press <kbd>Space</kbd> to track colored tip and start writing <br />
Press <kbd>z</kbd> to unwrite <br />
Press <kbd>b</kbd> to collect a background if you or the background changed <br />
Press <kbd>s</kbd> to save the current screen of writing without video <br />
Press <kbd>q</kbd> or <kbd>esc</kbd> to quit <br />

Place colored tip onto the squares on the top of the screen 
and press <kbd>Space</kbd> to clear or change colors. <br />


## Built With

* [pyinstaller](https://www.pyinstaller.org/) - Build cross-platform executables
* [OpenCV](https://pypi.org/project/opencv-python/) - Accessing video-camera and tracking
* [Numpy](https://numpy.org/) - Numerical operations and signal processing
* [Keyboard](https://pypi.org/project/keyboard/) - Keyboard tracking


## Authors

* **Flynn Chen** Yale College 2020' 
* **Antonio Medina** Yale College 2018'

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
