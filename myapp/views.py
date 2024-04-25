from django.shortcuts import render,redirect
from .models import people
from .models import feedback
from django.contrib import messages
import numpy as np
import tensorflow as tf
import pickle

# Create your views here.
def prediction(request):
    if 'username' in request.session:
        current=request.session['username']
                # Load the saved model
        model = tf.keras.models.load_model('static/h5/toxic-comment-model.h5')

        # Load the saved vectorizer
        with open('static/h5/text-vectorizer.pkl', 'rb') as f:
            vectorizer_data = pickle.load(f)
            vectorizer_config = vectorizer_data['config']
            vectorizer_weights = vectorizer_data['weights']
        # Reconstruct the TextVectorization layer
        vectorizer = tf.keras.layers.TextVectorization.from_config(vectorizer_config)
        vectorizer.set_weights(vectorizer_weights)
        # Function to preprocess user input and make predictions
        def predict_toxicity(user_input):
            input_text = vectorizer(np.array([user_input]))  # Vectorize user input
            result = model.predict(input_text)  # Make prediction
            return result
                # Function to print the toxicity predictions with labels
        label_names = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
        def print_toxicity_predictions(predictions):
            predictions_dict = {label_names[i]: predictions[0][i] for i in range(len(label_names))}
            for label, probability in predictions_dict.items():
                messages.success(request,f"{label}: {probability:.5f}")
                print(f"{label}: {probability:.5f}")
        if request.method=='POST':
                        # Example usage:
            user_input = request.POST['message']
            toxicity_prediction = predict_toxicity(user_input)
            messages.success(request,"Toxicity Prediction:")
           
            print("Toxicity Prediction:")
            print_toxicity_predictions(toxicity_prediction)
            return render(request,"prediction.html",{'current_user':current,'user_input':user_input})

        return render(request,"prediction.html",{'current_user':current})
    return render(request,'prediction.html')

    
def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        phone=request.POST['phone']
        email=request.POST['email']
        msg=request.POST['message']
        feedback.objects.create(name=name,email=email,phone=phone,message=msg)
        return redirect('/')
    return render(request,'contact.html')

    

def index(request):
    if 'username' in request.session:
        current=request.session['username']
        return render(request,"index.html",{'current_user':current})
    return render(request,'index.html')

def project(request):
    if 'username' in request.session:
        current=request.session['username']
        return render(request,"project.html",{'current_user':current})
    return render(request,'project.html')

def service(request):
    if 'username' in request.session:
        current=request.session['username']
        return render(request,"service.html",{'current_user':current})
    return render(request,'service.html')


def testimonial(request):
    if 'username' in request.session:
        current=request.session['username']
        return render(request,"testimonial.html",{'current_user':current})
    return render(request,'testimonial.html')



def login(request):
    if request.method=='POST':
        uname=request.POST['uname']
        passw=request.POST['pass']
        user=people.objects.filter(username=uname,password=passw)
        if user:
            request.session['username']=uname
            return redirect('/')
        else:
            messages.error(request,"usename and password doesnt match")
    return render(request,'login.html')


    
def register(request):
    if request.method=='POST':
        nam=request.POST['name']
        em=request.POST['email']
        ph=request.POST['phone']
        gen=request.POST['gender']
        un=request.POST['uname']
        passw=request.POST['pass']
        emailexists=people.objects.filter(email=em)
        if emailexists:
            messages.info(request,"EmailID Already registered")
        else:
            people(name=nam,email=em,phone=ph,gender=gen,username=un,password=passw).save()
            return redirect('/')
    return render(request,'register.html')

def logout(request):
    del request.session['username']
    return redirect('/')

