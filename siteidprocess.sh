git add -A
git commit -m "site id changed"
git push origin main
git push heroku main
heroku open https://lms-on-django.herokuapp.com/login/