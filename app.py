from flask import Flask, render_template, url_for, request, session
from flask import redirect
from datetime import timedelta

app = Flask(__name__)

app.secret_key = '123'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)



list_rent = [
    {'place': 'חיפה', 'name_store': 'סקיפס'},
    {'place': 'תל אביב', 'name_store': 'סנופסט'},
    {'place': 'ירושלים', 'name_store': 'גולשים'},
    {'place': 'כרמיאל', 'name_store': 'עכשיוסקי'},
    {'place': 'באר שבע', 'name_store': 'אסקימוסקי'}
]


user_dict = {
    'user1': {'name': 'Omer', 'email': 'benamiom@gmail.com'},
    'user2': {'name': 'Yarden', 'email': 'yardenZohar@gmail.com'},
    'user3': {'name': 'Noa', 'email': 'kiler@gmail.com'},
    'user4': {'name': 'OmerAdam', 'email': 'omeradam@gmail.com'},
    'user5': {'name': 'Merav', 'email': 'merav@gmail.com'},
}


@app.route('/')
def main_page():
    return redirect('/home')

@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/assigment3_1')
def assigment1():
    date = ('21.3-27.3', '28.3-4.4', '21.4-27.4')
    music = ['omer adam', 'noa kirel', 'eden hasson', 'mergi', 'eyal golan', 'skazi']
    return render_template('assigment3_1.html',
                           art=music,
                           dates=date)



@app.route('/assigment3_2', methods=['GET', 'POST'])
def assigment2():
    if 'place_name' in request.args:
        place_name = request.args['place_name']
        if place_name == '':
            return render_template('assigment3_2.html',
                                   all_list=list_rent)

        item_dic = next((item for item in list_rent if item['place'] == place_name), None)
        if item_dic is None:
            return render_template('assigment3_2.html',
                                   message='אין מקום להשכרת ציוד באזור המבוקש, בחר אזור אחר')
        else:
            return render_template('assigment3_2.html',
                                   place_name=place_name,
                                   name_store=item_dic['name_store'])

    if request.method == 'POST':
        userName = request.form['user']
        userEmail = request.form['email_res']

        session['user'] = userName
        numToAdd = len(user_dict) + 1
        new_user = 'user{userNumber}'.format(userNumber=numToAdd)

        for user, data in user_dict.items():
            if userEmail == data['email']:
                if userName == data['name']:
                    session['logedin'] = True
                    print(user_dict)
                    return render_template('assigment3_2.html',
                                        messageAgain='שמחים לראות אותך שוב', user_dic=user_dict.items())

                else:
                    return render_template('assigment3_2.html',
                                            messageCannot='האימייל קיים עם שם משתמש אחר, הכנס שם משתמש נכון, או בחר איימל אחר', user_dic=user_dict.items())

        user_dict.update({
            new_user: {
                'name': userName,
                'email': userEmail
            }
        })
        session['logedin'] = True
        print(user_dict)

    return render_template('assigment3_2.html', messageSign='ההרשמה בוצעה בהצלחה', user_dic=user_dict.items())


@app.route('/ContactUs')
def contactUs():
    return render_template('ContactUs.html')

@app.route('/Contact')
def contact():
    return redirect(url_for('contactUs'))

@app.route('/skiDealWeek')
def openSkiDealWeek():
    return render_template('skiDealWeek.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout_func():
    session['logedin'] = False
    session.clear()
    return redirect('/assigment3_2')


if __name__ == '__main__':
    app.run()

