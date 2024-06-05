from bottle import request, route, run, static_file, template, error
from mysql.connector import connect

# Funktion zur Erstellung von der DatenBank
def connectDB():
    mydb = connect(
      host="web3.kinet.ch",    
      user="omdb_user",
      database="omdb",
      password="QhPSNctsBRgsYOKEbASI"
    )
    return mydb

@route('/static/<filename>')
def static(filename):
    return static_file(filename, root="static")

@route('/')
def index():
    import random
    zahl=random.randint(1,240108)
    mydb = connectDB()
    mycursor = mydb.cursor(named_tuple=True)    
   mycursor.execute(str("SELECT * FROM movies WHERE name LIKE '%")+ query.q + str("%' OR id LIKE '%")+query.q+ str("%'"))

    myresult = mycursor.fetchone()
    
    mydb.close()
    print(myresult)
    
    return template("../views/index.html", title="Startseite", vorschlag=myresult)

# Routing der about page
@route("/about")
def about():
    return template("../views/about.html", title="About")

@route("/search")
def search():
    try:
        query = request.query.decode()
        mydb = connectDB()
        mycursor = mydb.cursor(named_tuple=True)
        mycursor.execute(f"SELECT * FROM movies WHERE name LIKE '%{query.q}%'")
    
        myresult = mycursor.fetchone()
    
        print(myresult)
    
        mydb.close()
        
        return template("../views/search.html", movie=myresult)
    except:
        return template("../views/error.html", movie=None)
    
@error(404)
def error404(error):
    return 'DU HSOHN HAST NACH FALSCHEN SACHEN GESUCHT'

run(reloader=True, host='localhost', port=8000)