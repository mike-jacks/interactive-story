# interactive-story

1. Mike Jacks - added sound files
1. Mike Jacks - added utilty.py file 1. with Utility class and Threading class
1. Mike Jacks - added animation.py file to help with animated text\
1. Mike Jacks - created .gitignore
1. Mike Jacks - fleshed out animation.py to animate text
1. Mike Jacks - add ascii_animation.py. Used to load, animate, and create ascii art images and animation from jpg/png images or image sequences
1. Mike Jacks - main_new.py reworked the story to work with all the built functions
1. Mike Jacks - messenger_terminal.py used apple script to launch a secondary terminal window for messages from hacker and other terminals
1. Mike Jacks - mission.py used to build missions to run
1. Mike Jacks - sound.py add the ability to play sounds from library in python project
1. Mike Jacks - terminal.py This is the big file of the project that makes the terminal work. Got this to work with the help of chat GPT.
1. Mike Jacks - text_color.py enum class to apply color to terminal text
1. Mike Jacks - utility.py Utility class to implement common commands like clear screen across scripts.

This was a very fun and challenging project. Part of the challenge was not having a dedicated partner from the getgo due to scheduling conflicts and changing partners. Marshall was great to collaborate ideas with and he helped implement some 3D graphics needed to display security footage as well as built the original structure of the story. 

I started off building the terminal system and branched out from there. Since after starting day 1, and losing my partner at the end of the day, I had to start over concept wise and take a greater ownership of the project. I continued on with the terminal, starting with basic pwd, ls, cd, mkdir, and touch. Other commands came about during the development of the game. 

Marshall was also very helpful in the beginning stages of creating a perpetual file system. After the initial build, I ran with it (with Chat GPTs help) and restructured it to what it is now. Overall it seems to work very well, and able to navigate pieces of it like a graph, with `/` as the root.

This filesystem .json setup allowed me to add a save state later, allowing a player to leave the game completely, and come back and continue the mission where the left off.

Initial challenges were getting the terminal to work, a lot of bugs were needed to be worked on in the begining. As it solidified, bugs became more cosmetic than operational. After the terminal was in good working order, I decided I wanted a messenger terminal to pop up as messages from the hacker (narrator) or enemy companies. This was interesting as Chat GPT lead me down the road to use applescript to launch and close a new window. 

Needless to say I learned a lot on this project pushing the limits of my skills, and gained confidence in my abilities. 