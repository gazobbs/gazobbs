import web




from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True)


Kakikomi = TAble(

urls = (
    '/', 'index'
)

class index:
    def GET(self):
        return "Hello, world!"

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

    
