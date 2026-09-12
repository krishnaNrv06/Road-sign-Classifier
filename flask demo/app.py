from flask import Flask,render_template,request

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact',methods=['GET','POST'])
def contact():

    message=" "
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        feedback=request.form['feedback']
        print("Name:",name)
        print("Email:",email)
        print("Feedback:",feedback)
        message="Thank you for contacting us!"
    return render_template('contact.html',message=message)

if __name__ =='__main__':
    app.run(debug=True)