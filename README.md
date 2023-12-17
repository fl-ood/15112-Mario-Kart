 # 15112-Mario-Kart
Description:
Mario Kart SNES 112
My project is trying to recreate Mario Kart but the SNES Version.
See Here:
- https://www.youtube.com/watch?v=AlAmXXNz5ac
I achieved a mode 7 like transformation using PIL and numPy to mimick the look of the original SNES version. Unfortunately I was unable to implement an AI into the game so it is mostly a racing game to see how fast you can go around the track. 

How to run:
- Make sure you have all assests (images and sprites) that are in images and sprites folders shared in the deliverable. The python file should be in the same folder/directory as the images and sprites folders, not inside either of the folders. This also applies to sprites.py which is the sprites class I created
  
You will also need these libraries to run the code:
- cmu_graphics
- PIL
- numPy

Controls:
- On the title screen press 'b' as directed and then move your mouse to select which speed you would like(it will highlight when you hover over it) 50cc or 100cc
- Use "w", "a", "s", "d" to move forward, turn left, move backwars, turn right as you would in most games when on the track
- Press space to skip between screens, title ---> select ----> game
- Press '1' when at the select screen to go back to the title screen and change the speed
- When on the select screen, use the arrows to select your character and press return twice when you are sure of your character
- If you are unsure of your character, press backspace, you change characters after pressing enter once if you do not press backspace
- Press 'k' for a secret character ;

Bugs:
- When selecting characters, toads sprite is special and random but it has only 4 images in the sprite sheet, so for some reason when switching quickly, if app.spriteCounter > 4 before you switch to toad, it will return an index error. This also happens on other characters like dk but it is less common since their spritesheets are bigger.
- The finish line is glitched you can simply just go backwards and forward and win easily since I couldn't really figure out how to configure it before TP3. Also, the first lap is set equal to -1 to counteract the first lap counting as a lap.
- The collisions with the walls are also glitched, I couldn't figure out how to transfer collision detection from the camera's position to the sprites position so you can go a little past the barriers and sometimes get either stuck in the barriers or go through them. However, this shouldn't be too much of an issue unless you are actively trying to run into walls.
  


Citations:
- Sprites come from The Spriters Resource or Mario Universe
- Spriters Resource: https://www.spriters-resource.com/snes/smariokart/
- Mario Universe: https://www.mariouniverse.com/sprites-snes-smk/

The 1st player buttons are crops from this SNES Long Play Video:
https://www.youtube.com/watch?v=AlAmXXNz5ac

- Title Screen is from The Spriters Resource but was edited with Adobe
- Selection screen is also from the spriters resource
- Map is also from the spriters resource

