# Interactive Smart Mirror
Interactive Smart Mirror - Senior Design Project

### Team:
Alisha Forrest, ahf5

Alec Rosenbaum, alr152

Daxton Scholl, djs129 

# Design Considerations:

## Software

* The OS will be linux-based (currently testing on ubuntu, but may move to a lighter-weight alternative)
* We will use Google Chrome (or Chromium) with a custom extension to drive the display
* We will write an application utilizing the Leap Motion API for gesture control

## Hardware

* The hardware used for this project needs to be under the $400 budget set by the Senior Design Instructor.
* Processing will be done onboard to keep network traffic low, and to eliminate remote processing overhead and complexity
* We have a 21" LCD and 60GB SSD, so those will be used for the display and storage
* The mirror will be bezel-less, but the mirror diagonal will be larger than the LCD by a few inches
* We will use the Leap Motion sensor as input for hand-tracking

## Gesture Interaction Design

There will be two primary forms of gesture interaction: one finger or two fingers.
Users will use either one or two fingers to interact with a plane floating a few inches off of the surface of the mirror. Using only the index finger will do things that moving a mouse would normally do. In the case of our widgets it might make configuration buttons appear on hover, or highlight a widget. Using two index fingers will allow touchscreen-style gestures. An example of this could be scrolling around an application.  As we determine what exact gestures and details are included in each of the above categories, we will fill out the below sections.

### One Finger

* move cursor
* click on long hover

### Two Fingers

* scrolling