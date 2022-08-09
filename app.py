from crypt import methods
from flask import Flask, render_template, request

app = Flask(__name__) 
 
@app.route('/table')
def table():
    return render_template('min1.html')

@app.route('/form', methods=['GET','POST'])
def form():
    return render_template('min2.html')

@app.route('/button')
def button():
    return render_template('min3.html')
 
if __name__ == '__main__': 
    app.run(host="0.0.0.0") 
