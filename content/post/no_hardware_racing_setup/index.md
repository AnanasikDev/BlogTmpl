---
title: How I made my own steering wheel using only my laptop
description: I really wanted to play Horza Horizon 4 with a wheel... so I made one.
slug: no_hardware_racing_setup
date: "2024-11-20"
image: images/img1.png
coverHeight: xxxl
tags:
    - Games
    - Programming
    - Python
    - Computer Vision
    - Proof of concept
    - Essay
    - English
---

# Software-Driven Devices in gaming

In this essay, I want to discuss opportunities that computer vision (possibly in combination with other inputs) provides in gaming, how it can be implemented, describe several approaches to it and their benefits, and discuss the theoretical future of this technology.

My idea revolves around eliminating additional hardware accessories, leaving only a laptop, phone or tablet which are non-specific to gaming. Depending on the desired result, one may make marker-devices (MD for short) which are physical attributes one can use to play games.

### Why?

Hardware is expensive, inconvenient in transportation, difficult in distribution and modification, and barely sustainable in home conditions. In contrast, Software-Driven Devices (SDD for short) can be made at home; their price consists only of the cost of materials; and they are highly customizable.

## Racing setup

### What?

The term "racing setup" here refers to devices one needs to play racing video games. Racing setups usually include a steering wheel, two or three pedals, and, in more expensive models, also gearbox, turn signals and other car controls. The most important parts of it that I will cover more profoundly in this essay are steering wheel and gas and brake pedals.

### How?

Generally, the idea behind SDD is in utilizing computer vision (through camera) as the only (or, at least, primary) source of input for a computer, eliminating need in any classical, hardware-driven-devices.

#### Steering wheel

The steering wheel has only one key property - angle. It can easily be detected by using special colored markers on the wheel for software to detect their positions and movement. By using several (at least three, theoretically) markers of different colors, sizes, or distances from the center evenly distributed along the circumference for better accuracy, steering wheel can rotate freely by 360 degrees without blind zones. If camera can capture the whole surface of the steering wheel without interruptions, then one marker should be enough; otherwise (if any objects obscure the visibility of some parts of the wheel) the method described above will help achieve identical result.

To calculate angle, computer also has to know center point of the steering wheel, which can be defined at calibration (more about it later).

#### Pedals

A pedal has upper and lower limits and current value. Limits can be set at calibration, and current value can be calculated knowing position of the corresponding marker on the screen and size of the last.

Pedals are somewhat more creative in implementation than steering wheel. My approach was to hang a marker on a handle which can be moved up and down by pulling and releasing a string with your leg. This way I could achieve the best result both in terms of usability and accuracy and stability of results.

### Practical and theoretical advantages of SDDs in racing gaming

1.1 Near-zero cost of your SDDs<br>
1.2 Full customization of your controls<br>
1.3 Lightweight, simple to make, easy to take with you<br>
2.1 Usually provides acceptable or good control (for non-competitive gameplay) - can be improved<br>
2.2 Can use inputs from gestures and mimics (instead of or in addition to MDs)

### Requirements and limitations

Computer vision strictly depends on lighting and camera quality. Standard laptop camera can capture 20-30 frames per second which might cause a delay which can be crucial when playing racing games. Can be solved by connecting a phone with better camera or an external camera.

Lighting should be bright and even. If lighting changes between gaming sessions, software should be recalibrated.

## SDDs in other spheres

### Animal gaming

With SDD technologies animals can play video games naturally without using any hardware and adhering to physical constraints. Software could track animal's movements and sounds and read them as an input.

With such unpredictable input however, SDDs might need not just computer vision but an AI component to it to analyze input more accurately (AI might increase accuracy with any SDDs).

### Fighting, using magic wands etc

Playing fighting games where you actually fight (with air, at least), dancing where you dance, using magic wands with real hand gestures and pronouncing spells is also possible using SDDs. Similar to VR, you can use your own body as an input device.

### Natural visual or audio inputs

With computer monitoring player's mimics, gestures, body movements and words, gaming might become more natural, with games receiving emotional feedback directly* rather than analyzing player actions and outcomes. It can suit highly emotional games like horrors, visual novels, (possibly new genres, revolving around emotional feedback from player) and so on with classic algorithms or AIs analyzing player's emotions through camera and microphone and adjusting the game correspondingly.

*mimics, eye movement and body language can reflect one's mood better than actions in a game which are easier to control and less prone to emotional influence.

## Overall technology advantages

1.1 Near-zero cost of your SDDs<br>
1.2 Full customization of your controls<br>
1.3 Lightweight, simple to make, easy to take with you<br>
2.1 Usually provides acceptable or good control (for non-competitive gameplay)<br>
2.2 Can be extended to any kind of visual inputs (specific attributes, mimics, hand/body gestures, dance pad and so on) (might even eliminate need for any physical "devices")<br>
2.3 Can be used by multiple users and animals<br>
2.4 Can be extended to be usable in non-racing games (VR with SDDs or other)<br>
3.1 Can give new gaming experience

## Implementation details

### Using bounding boxes for static or semi-static* inputs

Dealing with computer-vision-based input, we should always contraint it to prevent ambiguous or wrong calculations. When setting up an input marker (steering wheel, pedal, buttons, triggers etc) we shall always (unless dealing with body inputs) define areas where it is located. This way, markers can share the same color scheme and still be unambiguous to the software as they are defined in different contexts.

*semi-static inputs here refer to inputs which always adhere to same rules and whose properties can be predicted (e.g. a marker moving only vertically)

### Using spectrum of colors

Using contrast colors for markers and algorithms to analyze colors is crucial for accuracy and stability in CV-based SDDs. Acceptable color range depends on lighting conditions, camera quality, marker color and background color.

When making a CV-based controller in Python, you can simply use ```numpy``` and ```cv2``` libraries as following:

```py
def detect_color_spots(hsv, lower_bound, upper_bound, area):
    # constrain inputs to color range
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # constrain inputs to area
    mask = mask[area[0][1]:area[1][1], area[0][0]:area[1][0]] 
   
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        
        # find largest contour found
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)

        # calculate center position
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"]) + area[0][0]
            cY = int(M["m01"] / M["m00"]) + area[0][1]
            return (cX, cY)

    return None
```

and then find all spots of the given color range

```py
red_range = (np.array([100, 0, 0]), np.array([255, 120, 120]))

spot_position = detect_color_spots(hsv, red_range[0], red_range[1], areas['steering'])
if spot_position:
    # store the calculated position
    steering_spot_position = spot_position
```

### Calibration

Calibration is necessary to adapt software to current lighting and setup. Calibration might include steps such as setting positions, default values, limits, defining areas, adjusting color sensitivity. It might be done automatically (when feedback is given by computer itself), semi-automatically (when user gives feedback) and manually (when user sets all values themselves).

Calibration methods can be combined to achieve best accuracy and customization. In my racing setup I used semi-automatic approach for inferring steering wheel center and radius with user fixing these values by pressing certain keys on keyboard. This way, user can fine tune final values without doing tedious and prone-to-error calculations themselves.

## Afterthoughts

It must have certainly been invented before me and I am sure games and technologies as I described and designed already exist, but they remain unknown to the public. I would love to see (and possibly make) this industry grow and thrive to let everyone feel gaming differently.

I think playing games by actually moving your body, making gestures that mean something in the digital universe, talking to NPCs with your own voice can bring gaming to a whole new level. Gaming can become physically active, diverse, even more immersive and even more accessible.

Less accessible but more immersive option I am thinking about is playing in front of a huge screen with camera put somewhere, when you can play bowling or fight with orcs or shoot a bow as flawlessly and seamlessly as it was real life or VR, but with no equipment and no risks.

This essay is inspired by one of my projects - [Racing CV Controller (github link)](https://github.com/AnanasikDev/RacingCVController). I already wrote a post on reddit [here](https://www.reddit.com/r/computervision/comments/1gi8xwx/homemade_nohardware_racing_setup/) but later I wanted to extend it with more general and detailed thoughts. I think it's more than a joke project and one day it could bring a lot of joy and new good experience to people.

Video:

{{< youtube "giQNNACyR_M" >}}