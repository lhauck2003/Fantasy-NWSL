This is a web app for a Fantasy NWSL game
Current Functionality (as of 11/20/2025)
- one default user (login: testuser, password: test123), log in/out
- a default team
- ability to sub in/out players in My Team page (does not save yet)
- ability to transfer in/out players in Transfers page (does not save yet)
- ability to view players and sort by stat in Players Page

Planned Functionality
- save team
- auto scraping stats to update DB
- points by gameweek based on player stats
- leagues where fantasy teams can compete against eachother

How to run program:
- Download the codebase
- Run the create_db.py script and then the fill_db script in Fantasy-NWSL/app/db
- In the app folder (Fantasy-NWSL/app) run the API:
  `uvicorn main:app --reload`
- In a seperate terminal, in the fantasy-app folder (Fantasy-NWSL/app/fantasy-app), run:
  `npm start`
