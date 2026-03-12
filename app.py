from flask import Flask, request, jsonify

app = Flask(__name__)

class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title
    
    def to_dict(self):
        return {"id": self.id, "title": self.title}
        
# Sample data store
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

#GET -read an event
@app.route('/events/<int:id>', methods=["GET"])
def get_event(id):
    event = next((e for e in events if e.id == id), None)
    return jsonify(event.to_dict()) if event else ("Event not found", 404)

#POST- create an event
@app.route("/events", methods=["POST"])
def create_event():
    #extracts the json data sent by the client into the python dict
    data = request.get_json()
    #max Finds the highest existing ID to ensure the new ID is unique (Auto-increment)
    new_id = max((e.id for e in events), default=0) + 1
    new_event = Event(id=new_id, title=data['title'])
    events.append(new_event)
    # Returns the new object as JSON with a 201 Created status code
    return jsonify(new_event.to_dict()), 201        

#PATCH -update an event
@app.route('/events/<int:id>', methods=["PATCH"])
def update_event(id):
    data = request.get_json()
    event = next((e for e in events if e.id == id), None)
    if not event:
        return ("Event not found", 404)
    if "title" in data:
        event.title = data["title"]
        return jsonify(event.to_dict())
    
#DELETE -an event
@app.route('/events/<int:id>', methods=["DELETE"])
def delete_event(id):
    global events
    event = next((e for e in events if e.id == id), None)
    if not event:
        return ("Event not found", 404)
    events = [e for e in events if e.id != id]
    return ("Event deleted", 204)






if __name__ == "__main__":
    app.run(debug=True)
