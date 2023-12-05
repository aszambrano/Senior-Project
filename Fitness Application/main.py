from website import create_app  #imports the create_app function from the website folder. This is the main function that runs the application

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)  #running the application in debug mode allows for edits to be made while the application is running, although it is not recommended for production use.

