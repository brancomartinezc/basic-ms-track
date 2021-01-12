from flaskapp import create_app, db

app = create_app()
#Use this only the first time to create de DB
'''with app.app_context():
    db.create_all()'''

if __name__ == '__main__':
    app.run(debug=True)