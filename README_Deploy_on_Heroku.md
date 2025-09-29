Deploy a FastAPI API directly on Heroku (Not needed if using docker)

1. Create a Heroku account on their website at heroku.com

2. Create a Procfile (in the root directory of your application, to explicitly declare what command to execute to start your app)
- content of file is as simple as "web: uvicorn main:app --host=0.0.0.0 --port=$PORT"

3. Update requirements.txt with necessary librairies (pip freeze -> requirements.txt while in project virtual environement)

4. Install Heroku and deploy in 3 command line
- heroku login (then enter credentials)
- heroku create Deployed_model_API
- git push heroku <git-branch>
- heroku ps:scale web=1 (If error "Couldn't find that process type (web)", it means your app is still deploying. Wait a few minutes and try again.)
- heroku open (to validate succesful deployment)
- heroku logs --tail (To generate more log messages, refresh the app’s homepage in your browser.)

5. scale the app
- heroku ps (check how many dyno are running c.a. lightweight containe)
- heroku ps:scale web=1 (specify numbers of dyno)

6. Continuous integration
- heroku local --port 5006 -f Procfile (run app locally, makes changes, commit to git)
- git push heroku <git-branch> (push the branch that was updated)
- heroku open (to validate succesful deployment)

7. Advanced monitoring
- heroku addons:create papertrail (By default, Heroku stores 1500 lines of logs from your application, but the full log stream is available as a service, c.a. exemple Papertrail)
- heroku addons (list teh addons)
- heroku addons:open papertrail (Opens up a Papertrail web console that shows the latest log events. The interface lets you search and set up alerts.)

8. Advanced development 
- heroku run python manage.py shell (run scripts and applications that are part of the app)
- heroku config:<get|set|unset> ENV_VARIABLE=value (saved API_TOKENS, Config var values are persistent–they remain in place across deploys and app restarts)

9. Provision and add database (add psycopg to requirements.txt, add release: ./manage.py migrate --no-input to Procfile)
- heroku addons:create heroku-postgresql:essential-0 (An essential-0 Postgres size costs $5 a month, prorated to the minute. )
- heroku config (displays the URL that your app uses to connect to the database, DATABASE_URL)
- heroku pg:psql (connect to the remote database and see all the rows)