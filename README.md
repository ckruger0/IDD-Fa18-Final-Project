# IDD-Fa18-Final-Project

### Project Idea

- This project idea started from my experience of buying plants at farmers markets, where vendors often only label the plants with prices instead of species names. This makes understanding how to care for the plants difficult down the road if I'm unaware of what the specific plant is. To solve this problem I created a device that takes a picture of a plant and categorizes the species using a built in convolutional neural network. The species name is then displayed on an onboard LCD screen for the user to review. 

### Team
- Chris Kruger - crk78

### Initial Paper Prototype

The initial paper prototype was built with the end goal of identifying bird species. After thinking through real world use cases however, I opted to focus on plant species identification since these subjects don't move (very quickly). 

<img src="https://i.imgur.com/OasfU5r.jpg" width=500 height=400><BR>Front View<BR><BR>
<img src="https://i.imgur.com/1f20Mrz.jpg" width=500 height=400><BR>Rear View<BR><BR>
<img src="https://i.imgur.com/jlWiKaD.jpg" width=500 height=400><BR>Bottom View<BR><BR>

### Initial Expected Parts
- Raspberry Pi
- Raspberry Pi Camera
- External Battery Pack
- Case
- Button
- 16x2 LCD Screen

The RPi will be entirely internal, whereas the LCD Screen, Button, and Camera (imaging piece) will be externally exposed. The Battery Pack will be entirely external and power the device through a microUSB port located on the bottom of the case.

### Interaction Plan
- A user will aim the frontside camera at a mystery plant and press the capture picture button. After identifying which plant species it is, the name will display on a 16x2 LCD screen on the back of the device.

### Building Journey
- Originally I had intended on training the neural network on a massive dataset of plant images (from iNaturalist, for example). However in practice after many failed attempts of downloading a 120GB file from a broken remote server I opted to just focus on a set of houseplants that I own. Final species class set was: `['hoya carnosa','philodendron','kolanchoe','snake plant']`
- Using a bulk image scraper I found online, I downloaded ~500 images of each plant species that I was interested in.
- Transfer learning was used to retrain the final layer of an Inception V3 network provided by Google.
- After final retraining the model achieved an test accuracy of 83%. While this is fairly high, there is a fair bit of overfitting as evidenced by real world testing when there is background clutter within frame.
- The model was loaded onto the Raspberry Pi and hardware was put together. 
- There were power issues that took a while to troubleshoot. Ultimately realized that the main power cable was not soldered properly.

### Functioning Design

<img src="https://i.imgur.com/kdg3hBr.jpg">

<BR><BR> A video of the final plant identifier in action can be seen here: <a href="https://youtu.be/xIBPJVnL_bU">https://youtu.be/xIBPJVnL_bU</a>
  
### Final Used Parts
- Raspberry Pi
- Raspberry Pi Camera
- Raspberry Pi GPIO Extension Board
- Ribbon Cable
- Button
- 16x2 LCD Screen
- Half size breadboard

### Packaged Plant Identifier

