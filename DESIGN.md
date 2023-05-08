# Design Document
This file should discuss how you implemented your project and why you made the design decisions you did, both technical and ethical. Your design document as a whole should be at least several paragraphs in length. Whereas your README.md is meant to be a user’s manual, consider your DESIGN.md your opportunity to give the staff a tour of your project underneath its hood.

## Technical Decisions
### In this section, share and justify the technical decisions you made.
You don't need to respond to all questions, but you might find some of the following helpful:
* Was there a feature in your project you could have implemented in multiple ways? Which way did you choose, and why?

I could have implemented many of the features I created in different ways. I chose to implement them the way I did based on one my most limiting factor which is my overall experience in coding. I relied heavily on basic documentation and was unable to implement certain highly complex ideas. For example, I originally wanted to add an interactive water pong rack, which would change as input was given, but found it to be beyond my current skill level, so I decided to use a static reference image and stationary buttons instead.

Another example is how I displayed information to the users. In the record table for shots displayed in html/shotrecord, I originally wanted to directly display the data from the "shotnumber" column in userstats.db, but I instead opted to use {{ index.length }} since the userstats.db table is used for multiple users, and it was displaying the absolute shot number, rather than the sequential value of shotnumber for the current user. These kind of decisions can be identified frequently, as I was much more focused on functionality than anything else.

## Ethical Decisions
### What motivated you to complete this project? What features did you want to create and why?

The idea of quantifying water pong performance is what motivated me to complete this project. I have often observed people arguing about who is better at water pong so I wanted to make this project in order to have some kind of statistic to reference when comparing players. I wanted to implement shot records as well as game records. I also wanted to implement other rules, but found they were more time consuming to implement than I originally thought they would be.

### Who are the intended users of your project? What do they want, need, or value?

The intended users of my project inclue anyone who plays the game water pong and wants to keep track of their accuracy and win ratio. They might want to compare their accuracy to determine which techniques have the highest success rate or what kind of form works best for them. You could also track your improvements through the use of multiple profiles. Overall, this project is for people who either want to improve at water pong, or simply want to quantify just how good they are at the game.

### How does your project's impact on users change as the project scales up?

My projects impact on users could change in many ways as it scales up. One possibility of scaling would be adding a master leaderboard of sorts to the project. If there was a large userbase, it would be interesting to have a leaderboard which ordered all users of the project in an interactive way. For example, in this scenario, a user could look at this leaderboard and find out which user has recorded the most shots, missed the most shots, etc. This could possibly add an interesting social dynamic to the project, as people might compete to top the leaderboards. This could impact people in a variety of different ways. It could discourage users whose stats are below average, and inflate the egos of the people whose stats are above average.

