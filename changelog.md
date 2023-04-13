# Changelog
This is a log listing all major changes to the DAY 15 bot since the creation of this GitHub repository. The bot has seen a few major changes before the creation
of this repository, but this log will start at version 19 (v19), which marks the creation of this repository. Versions which only make minor changes are omitted from
this log.

## v22 - Public GitHub repository created!
- Created README and changelog files for the GitHub repository
- Established a workflow and Git system that allows for a public repository of the bot to be shared
- Changed initialization print message to print all servers the bot is currently connected to, rather than just 1. Deleted DISCORD_GUILD environment variable
- Added 1 new user command
  - /repo15 - sends a message sharing a link to the public GitHub repository

## pre-v22 - Initial release & development
- Bot created and deployed
- Added DAY 15 functionality; bot will send a message on 15th day of every month
- Added 3 user commands
  - /help15 - sends a message with introduction and commands to the bot
  - /timetill15 - sends a message containing the time until the next DAY 15, in Mountain Daylight Time
  - /howareyou15 - sends a message reflecting how the bot is feeling. only responds with a single message as of now.
- Regenerated and updated the Discord Bot Token in light of a security issue
