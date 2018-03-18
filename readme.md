# Fantasy Color Guy

![alt text](https://github.com/D-TUCKER/Color-Guy/blob/master/assets/fantasy_color_guy.png?raw=true "Fantasy Color Guy Logo")

## Inspiration

Given the rising prominence of daily fantasy sports over the last five years, and the obvious opportunity to win cash as a result of playing, there are obviously players who use all the data and tools available to them to gain an upper hand and win a larger share of the pot. We wanted to give more casual game players the opportunity to make better decisions in managing their line-up, but in a more lightweight, user-friendly way, to hopefully bridge the gap between the hardcore player and the casual.

We also wanted to bring in another timeless element of sports - color commentary. Planning a line-up can be stressful, we wanted to inject a bit of humor and fun into the experience.

## What it does

Fantasy Color Guy is a Facebook Messenger-based chatbot that takes the massive amount of statistical information available and condenses it down to inform a single decision point: Should I start a player, and if not, who should I start? It then gives algorithmically-derived color commentary on the player, team, or park using an algorithm we call Methodical Analytical Differentiated Enigmatic-Upper-Percentage, or MADE-UP for short.

## How we built it

We condensed every 2017 single season's at-bats and, based on DraftKing's scoring rules for baseball, determined the likely scores for every batter and every pitcher, as well as the average score for each position over the course of the season. (In reality, we modeled two players and two pitchers, given the limitations on time and computing power).

We then trained an NLP agent, Wit.ai, to interpret requests from users with the intent of discovering (a) whether a certain player should start on a certain day, or (b) which player should start for a given position. This agent was exposed using the Facebook Messenger platform, which is the primary interface (for now) to the experience.

The color commentary was written by the team, but in the real world would be created by AI trained by listening to years of Harry Caray, Tony Kornheiser, and others.

## Challenges we ran into

For the team, it was the first time building a Facebook Messenger app, and getting Wit.ai to play well with Heroku proved a challenge.

## Accomplishments that we're proud of

We trained an AI in a day to give fantasy baseball advice. That's kind of awesome.

## What we learned

That Python's wit package does not play well with Heroku
That Facebook's documentation is a bit sparse when it comes to the Messaging Platform
That Wit.ai is powerful and simple at the same time
What's next for Fantasy Color Guy
We're going seed round, and we're aiming for a quick acquisition by DraftKings. :)
