from autodj import create_app

# run a test server
if __name__ == '__main__':
    app = create_app({
        'TESTING': True,
        'SECRET_KEY': 'dev'
    })
    app.run(debug=True)
