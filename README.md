# Final Lab: Plant Identifier

### Project Idea

- This project idea started from my experience of buying plants at farmers markets, where vendors often only label the plants with prices and not their species names. This makes understanding how to care for the plants difficult down the road if I'm unaware of what the specific plant is. To solve this problem I created a device that takes a picture of a plant and categorizes the species using a built in convolutional neural network. The species name is then displayed on an onboard LCD screen for the user to review and find relevant resources online.

### Team
- Chris Kruger - crk78

### Initial Paper Prototype

My original paper prototype was built with the end goal of identifying bird species. After thinking through real world use cases however, I opted to focus on plant species identification since these subjects don't move (very quickly). Therefore when reviewing the paper prototypes please keep in mind that "bird species" should be saying "plant species":

<img src="https://i.imgur.com/OasfU5r.jpg" width=500 height=400><BR>Front View<BR><BR>
<img src="https://i.imgur.com/1f20Mrz.jpg" width=500 height=400><BR>Rear View<BR><BR>
<img src="https://i.imgur.com/jlWiKaD.jpg" width=500 height=400><BR>Bottom View<BR><BR>

### Hardware List

- Raspberry Pi
- Raspberry Pi Camera
- Raspberry Pi GPIO Extension Board
- Ribbon Cable
- Button
- 16x2 LCD Screen
- Half size breadboard

### Interaction Plan

- When a user has a plant they would like to know the species of, they can place it on a surface that is clear of clutter so the main object within frame will be the plant. After holding the plant identifier about 3-5 feet away from the plant, they will open the camera hatch 90 degrees towards the plant subject. Pressing the gray button located on top of the device will capture an image of the plant and drop it into a directory onboard the Raspberry Pi that is regularly listening for changes. Once a new picture is dropped into this directory, it will predict the plant within frame using a pre-trained network located onboard the Pi. After roughly 10 seconds of analysis the plant species name will display on a 16x2 LCD screen on the side of the Plant Identifier.

<img src="https://i.imgur.com/cnHPwuC.png">

### To Run...


`git clone https://github.com/ckruger0/IDD-Fa18-Final-Project.git` 
<BR>
`cd IDD-Fa18-Final-Project`
<BR>
`python3 label_image.py`

### Building Journey

##### Software

- Originally I had intended on training the neural network on a massive dataset of plant images (from iNaturalist, for example). However in practice after many failed attempts of downloading a 120GB file from a broken remote server I opted to just focus on a set of houseplants that I own. Final species class set was: `['hoya carnosa','philodendron','kolanchoe','snake plant']`
- Using a bulk image scraper I found online, I downloaded ~500 images of each plant species that I was interested in.
- Transfer learning was used to retrain the final layer of an Inception V3 network provided by Google.
- After final retraining the model achieved an test accuracy of 83%. While this is fairly high, there is a fair bit of overfitting error as evidenced by real world testing when there is background clutter within frame. For the purposes of this exercise I found it to have satisfactory performance.
- The model was loaded onto the Raspberry Pi and a script was setup to watch a directory for new images coming in. 

##### Hardware

- I decided to re-use the Useless Box from a prior lab to both save time and resources.
- For initial functionality development I built a working system with the Raspberry Pi and a GPIO pinout board on 2 breadboards.
- This was satisfactory for functionality testing, however when it came to fitting it within the Useless Box it became quite unweildy. 
- To counteract this I soldered the pinout board to a PCB board and moved the LCD display to a smaller breadboard. After soldering everything into place I realized the Useless Box was not wide enough to hold the breadboard-mounted LCD display in a user friendly manner.
- After testing multiple placements I chose to place the breadboard externally on the side of the Plant Identifier. While this was not a sleek implementation I did think it looked kind of cool with the exposed wiring - people I showed it to definitely thought it was more complex than it was. 
- There were also power issues that took a while to troubleshoot. Ultimately I realized that the main power cable was not soldered properly. After fixing those issues the Plant Identifier was up and running!

### Functionality Testing

<img src="https://i.imgur.com/kdg3hBr.jpg">

<BR> A video of the functional-phase plant identifier in action can be seen here: <a href="https://youtu.be/xIBPJVnL_bU">https://youtu.be/xIBPJVnL_bU</a>

### Packaged Plant Identifier

<img src="https://i.imgur.com/V6N6tMe.jpg">

<img src="https://i.imgur.com/tjbBXPX.jpg">

The final Plant Identifier placed within the Useless Box from a previous lab.

A video of the final Plant Identifier in action can be seen here: 
