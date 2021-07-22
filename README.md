# Cs50-Final-Project
#### Video Demo:  https://www.youtube.com/watch?v=zcETs6LxURQ
#### Description:
For my final project, I decided to make a moderation bot on discord that uses a flask API
to store data on a database with a "many to many relationship" I chose to do it like this,
because I thought it nicely incorporated some of what I learned in CS50.

##### dc_bot:
This folder contains two files. The bot and the requirements as for what the bot does
it's just a simple moderation bot that the staff can use to warn, mute, kick and ban members
that don't follow the rules the bot logs every warn, mute, kick and ban it lets the staff
keep track of what's happening in a more user-friendly way

##### flask_app:
This folder contains two files. The API and the requirements:
the API is what stores and sends the data to the bot this made it easy to debug and figure outif a bug was in the API or the bot.

The db table schema concists of five tables servers, users, user_servers, violations
and user_violations with user_servers combining users and servers and with user_violations
combining users and violations

#### features:
##### logs:
logs just logs every time a user get warned, muted, kicked or banned in the formatter
\<admin> \<action> \<member>

##### setup:
setup sets up the server by adding the server and it's users to the database
usage: /setup

##### warn:
used to warn users 10 warns will result in an automatic ban
usage: /warn \<user> \<reason>

##### mute:
used to mute users you can specify seconds, minutes and hours
usage: /mute \<user> \<time> \<unit> \<reason>

##### kick:
used to kick users from the server
usage: /kick \<user> \<reason>

##### ban:
used to ban users from the server
usage: /ban \<user> \<reason>
