from autodj import create_app

# run a test server
if __name__ == '__main__':
    app = create_app('config')
    app.run()
