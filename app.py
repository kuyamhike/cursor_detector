from flask import Flask, jsonify, request
import pyautogui as pt
from pynput.mouse import Button, Listener #gumamit ako neto kahit wala ka sinabi cause di ko alam pano malaman kung nagclick yung mouse

app = Flask(__name__)

is_dragging = False #Current state ng mouse cause since di pa fucking ginagalaw

def on_click(x, y, button, pressed): #the onclick shit para malaman if clinick yung left button
    global is_dragging
    if button == Button.left:
        is_dragging = pressed

listener = Listener(on_click=on_click) #eto yung nakikinig if napindot yung mouse
listener.start()

@app.route('/cursormovement', methods=['GET']) #yung GET
def get_cursor(): 
    x, y = pt.position() #para malaman position ng cursor
    return jsonify({
        "position-x": x,
        "position-y": y,
        "is_dragging": is_dragging #returns the output para lumabas
    }) 

@app.route('/cursorpost', methods=['POST'])
def post_cursor():
    data = request.json
    x = data.get('x') #ngayon ko lang nalaman na di pala pede gumamit ng int(input) dito HSHHSAH
    y = data.get('y')
    pt.moveTo(x, y)   #para lumipat sya based sa pinalitan ng user, sa postman
    return jsonify({
        "move to": {"x": x, "y": y} #para maoutput
    })

@app.route('/cursorpost', methods=['PUT']) 
def put_cursor():
    global is_dragging
    is_dragging = not is_dragging #welp yung not operator binabaliktad ung boolean value
    return jsonify({
        "is_dragging": is_dragging #output
    })

@app.route('/cursorpost', methods=['DELETE']) 
def delete_cursor():
    global is_dragging  
    pt.moveTo(0, 0)
    is_dragging = False
    return jsonify({
        "position-x": 0,
        "position-y": 0,
        "is_dragging": is_dragging #need ko pa iexplain to? basically self explanatory na
    })

if __name__ == '__main__':
    app.run(debug=True) #para mag run tas debug=true para magdebug na don