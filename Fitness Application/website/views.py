#This file is used to store the data for the webpages that are going to be viewed by the user that are NOT related to authentication (logging in, logging out, etc)
from flask import Blueprint, render_template, request, flash, jsonify, url_for, redirect
from flask_login import current_user, login_required
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


#this sets up the workout journal and allows for the user to submit new entries
@views.route('/journal', methods=['GET', 'POST'])
@login_required
def journal():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Entry is too short!', category='error')
        else: 
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Your entry has been added!', category='success')

    return render_template('journal.html', user=current_user)

#this is a simple view that just send the user back to the home page
@views.route('/')
def about():
    return render_template('about.html', user=current_user)
    

@views.route('/delete-note', methods=['POST'])
#this function allows for the user to delete their entries from the journal
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note_to_delete = Note.query.get(noteId)

    if note_to_delete:
        if note_to_delete.user_id == current_user.id:
            db.session.delete(note_to_delete)
            db.session.commit()

    return jsonify({'redirect': url_for('views.journal')})   #ensures that the user stays on the workout journal page after deleting their entry

#Sets up the array that will be used to store the exercises that the user can filter through and examine
exercises_data = [
    {'name': 'Bicep Curl', 'body_type': 'upper', 'description': 'Bicep Curls are a weight training exercise for your biceps, a muslce on your upper arm.\
     This exercise  is typically preformed with dumbells, kettle bells, resistance bands or a cable machine. To preform a bicep curl,\
     hold the weight with in your hand with your palms facing up and your arms\
     at the side of your body. Bend your elbows and lift the weights until they reach your shoulders, then slowly lower back to the starting position.'},
    {'name': 'Deadlift', 'body_type': 'upper', 'description': 'Deadlifts are a weight training exercise that works the entire body, but specifically creates a \
     lot of muscle activation in the lower back erectors. This exercise consists of lifting a weight from a rested position on the floor to an upright position. \
     To preform a deadlift, start with your feet shoulder width apart with your feet under the bar (if you\'re using a barbell). Then, lower your torso to the bar by pushing your glutes back and hinging at the waist.\
     Then grasp the bar in your hands. Squeeze your shoulder blades together to engage your lats, and then engage your core. Make sure to keep your hips lower than your shoulders, head, and neck.\
     Push through your feet and pull the weight up. The bar should stay relatively close to the shins while pulling. Squeeze your glutes to lock at the top of the lift.\
     Lower to the floor the the reverse manner.'},
    {'name': 'Lateral Raise', 'body_type': 'upper', 'description': 'Lateral raises are a weight training exercise that work the lateral head of your deltoids (shoulders).\
     To preform a lateral raise, hold a weight at your side palms facing your body. Then you raise the weight laterally, until your arm is fulle extended at shoulder height.'},
    {'name': 'Overhead Press', 'body_type': 'upper', 'description': 'Overhead press is a weight training exercise that works the deltoids, with a focus on the front head\
     of the deltoids. You can do overhead presses with a machine, barbells, dumbbells, or a kettle bell. To preform an overhead press, Hold a weight in each hand at shoulder height,\
     and slowly raise it slowly above your head. Then slowly lower the weight back to the starting position and repeat.'},  
    {'name': 'Bench Press', 'body_type': 'upper', 'description': 'Bench press is a weight training exercise that works multiple muscles, and therefore is known as a compound exercise.\
     Bench presses target the following muscles: pectorals, front deltoids, triceps, and the biceps. Depending on the variation of bench press, it may predominantly target one muscle\
     more than others. To preform a standard bench press, you will need to lie flat on a bench and press the weight (either in the form of a dumbbell or barbell) upwards. You then lower\
     the weight down to chest level, and press upwards again extending your arms.'},
    {'name': 'Incline Bench Press', 'body_type': 'upper', 'description': 'Incline bench press is a variation of the bench press the focuses more on your upper chest muscles compared\
     to the standard bench press. To preform an incline bench press, you will want to adjust the bench so it is angled at about 45 degrees, letting you lean back into the bench as\
     opposed to lying flat. The movement for the incline bench press is the same as the standard bench press.'},
    {'name': 'Skull Crushers', 'body_type': 'upper', 'description': 'Skull crushers are a weight training exercise that works the triceps. This exercise can be preformed with either\
     dumbbell, or an EZ curl bar. To preform a skull crusher, you will need to lie flat on a bench holding the weight above your chest with your elbows about shoulder width apart.\
      Flex the elbows lowering the weight towards your head, making sure that your arms stay perpendicular to your body so your triceps remain isolated. Continue lowering the weight\
     behind your head, and then finally bring the weight back to the starting position above your chest.'},
    {'name': 'Lat Pulldowns', 'body_type': 'upper', 'description': 'Lat pulldowns are a weight training exercise that work your back muscles. This exercise is typically preformed with\
     a machine that has adjustable weights. While seated at the machine, you pull a hanging bar just below your chin almost at chest level. Depending on how you grip the bar, it may predominantly target one muscle\
     more than others. For example, the wider your grip, the more your back muscles are targeted.'},
    {'name': 'Rows', 'body_type': 'upper', 'description': 'Rows are a weight training exercise that target your back muscles. Rows can be preformed with machines, or dumbbells or barbells.\
     The row movement consists of pulling a weight towards you. Using the bent row as an example, you start bent over at about a 45 degree angle. Keeping the barbell or dumbbells\
     hanging down straight to start, bend your elbows and pull with your back to bring the weight parallel with your stomach, then lower the weight back to the starting position.'},
    {'name': 'Chest Flies', 'body_type': 'upper', 'description': 'Chest flies are a weight training exercise that work your chest muscles. This exercise can be performed with dumbbells,\
     a cable machine, or a dedicated fly machine. To perform a chest fly, your arms need to be fully outstrectched to each side. With a weight in each hand,\
     bringing the weights from that outstretched postion to your chest while keeping your arms extended. Then slowly return to the starting position and repeat.'},
    {'name': 'Squats', 'body_type': 'lower', 'description': 'Squats are another compound exercise, much like the bench press or deadlifts. The main muscles it focuses on\
     are the lower body muscles such as the quadriceps, hamstrings, and glutes. There are many variations of squats, but we will cover the bodyweight squad, which is good for\
     beginners. To start, you want to stand with your feet shoulder width apart. Tighten your core, and push out your chest sligtly. Leading with your glutes, bend your \
     hips and descend into a squat position while keeping your knees in line with your toes. Once you have descended to the bottom of the squat, your thighs should be parallel\
     to the ground. Then push back up tightening your glutes at the top position.'},
    {'name': 'Leg Extension', 'body_type': 'lower', 'description': 'Leg  exensions are a weight training exercise that mainly target your quadriceps. It is also typically done on a machine\
     To preform a leg extension, you want to set the machine up so that the pad of the machine is at the top of your foot, near the ankles. Keep your knees at a 90 degree angle, then\
     lift the weight with your legs until they are nearly straightened. Keep in mind you do not want to lock your knees in place.Then lower the weight back to the starting postion and repeat.'},
    {'name': 'Leg Curls', 'body_type': 'lower', 'description': 'Leg curls are a weight training exercise that target your hamstrings, calves and glutes, with the majority of the tension\
     being on the hamstrings. Leg curls can be done standing, or with a specialized machine. There are also two different variations of machines, with one being the seated leg curl, and the\
     other being a prone leg curl. To perform a leg curl, the movement entails flexing your knees pulling your ankles as close to your glutes as possible. Then slowly return your foot\
     to the starting positon. This movement carries across to all variations of the leg curl, the only difference being whether you are seated, in a prone position, or standing.'},
    {'name': 'Calf Raises', 'body_type': 'lower', 'description': 'Calf raises are a simple weight training exercise that targets your calves. They can be preformed with or without \
     weights. To preform a standing calf raise, you simply raise your heels off the ground slowly until you\'re standing on the tips of your toes. Then slowly lower your heels \
     back to the ground, and repeat.'},
    {'name': 'Forward Lunges', 'body_type': 'lower', 'description': 'Forward lunges are an exercise that mainly targets your quadriceps. They can be preformed with or without weights.\
     To perform a forward lunge, you want to stand with feet hip width apart. Take a large step forward with one leg, then lower yourself down until your thigh is parallel to the floor.\
     Then drive back up with the leg you stepped forward with until you have returned to the starting position.'},
    {'name': 'Reverse Lunges', 'body_type': 'lower', 'description': 'Reverse lunges are an exercise that has more of a focus on your hamstrings. It is a similar motion to the\
     forward lunge, however instead of taking a large step forward, you step back.'},
    {'name': 'Hip Thrusts', 'body_type': 'lower', 'description': 'Hip thrusts are an exercise that targets the glutes. They can be preformed with or without weights. To perform a hip thrust, set\
      your back against an elevated surface such as a bench. Make sure that your knees are bent, and your feet are flat against the ground. The surface your back is leaning against\
     should be right below your shoulders. While keeping your head tucked in, push through your feet to raise your hips until your thighs are parallel to the ground. At the top of the motion,\
     you should be squeezing your glutes.'},
    {'name': 'Sit-Ups', 'body_type': 'core', 'description': 'Sit-ups are a basic exercise to help strengthen your core. To perform a sit-up, lie down face up with your hands behind\
     your head, knees bent and feet flat against the ground. Then, in a controlled motion, lift your torso up to your thighs then lower yourself back down.'},
    {'name': 'Planks', 'body_type': 'core', 'description': 'Planks are another great core strengthening exercise. To perform a plank, lay face fown on the ground. Then, raise yourself\
     off the ground using your abdominal muscles to stablizie yourself hold that position for 15-20 seconds. Then lower yourself back down.'},
    ]

@views.route('/exercises', methods=['GET', 'POST'])
#this function allows for the user to filter through the list of exercises based on a body type (upper, lower, core)
def exercises():
    if request.method == 'POST':
        selected_body_type = request.form.get('body_type')
        print(f"selected_body_type: {selected_body_type}") #this line is here to help with debugging
        exercises = filter_exercises(selected_body_type)
    else:
        exercises = exercises_data #shows all by default

    return render_template('exercises.html', user=current_user, exercises=exercises)
#this initializes the function that filters through the exercises based on the body type
def filter_exercises(body_type):
    if body_type == 'all':
        return exercises_data
    return [exercise for exercise in exercises_data if exercise['body_type'] == body_type]
            
   
