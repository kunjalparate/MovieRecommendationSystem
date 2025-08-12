
from flask import Flask,request, render_template, request
import pickle
import requests
import pandas as pd
from patsy import dmatrices


movies = pickle.load(open('model/movies_list.pkl','rb'))
similarity = pickle.load(open('model/similarity.pkl','rb'))
'''
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

'''
'''
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        response = requests.get(url, timeout=5)  # Set timeout
        response.raise_for_status()  # Raise error for bad status
        data = response.json()
        poster_path = data.get('poster_path', None)
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"
    except Exception as e:
        print(f"Error fetching poster for movie_id {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=Error"
'''
'''
import os

def fetch_poster(movie_id):
    local_path = f"/static/posters/{movie_id}.jpg"
    if os.path.exists("static/posters/" + str(movie_id) + ".jpg"):
        return local_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster"
'''
import os
'''
def fetch_poster(movie_id):
    try:
        api_key = "8964c0ab7362d7bbcdd9589255c66ed8"
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path', None)
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"
    except Exception as e:
        print(f"Error fetching poster for movie_id {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=Error"
'''

#OPTION 1
'''
def fetch_poster(movie_id):
    try:
        api_key = "8964c0ab7362d7bbcdd9589255c66ed8"  # Replace with your working TMDb API key
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
        response = requests.get(url, timeout=10)  # timeout increased
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"
    except requests.exceptions.Timeout:
        print(f"Timeout while fetching movie_id {movie_id}")
        return "https://via.placeholder.com/500x750?text=Timeout"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for movie_id {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=Error"



'''
#OPTION 2

import os

def fetch_poster(movie_id):
    local_path = f"static/posters/{movie_id}.jpg"
    if os.path.exists(local_path):
        return "/" + local_path
    else:
        try:
            api_key = "8964c0ab7362d7bbcdd9589255c66ed8"
            url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return "https://image.tmdb.org/t/p/w500/" + poster_path
            else:
                return "https://via.placeholder.com/500x750?text=No+Poster+Available"
        except Exception as e:
            print(f"Error fetching movie_id {movie_id}: {e}")
            return "https://via.placeholder.com/500x750?text=Error"



def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse= True, key = lambda x:x[1])
    recommended_movies_name=[]
    recommended_movies_poster=[]
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies_name.append(movies.iloc[i[0]].title)
    return recommended_movies_name, recommended_movies_poster
    

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/recommendation', methods = ['GET','POST'])
def recommendation():
    movie_list = movies['title'].values
    status = False
    if request.method == "POST":
        try :
            if request.form:
                movies_name = request.form['movies']
                print(movies_name)
                recommended_movies_name, recommended_movies_poster = recommend(movies_name)
                print(recommended_movies_name)
                print(recommended_movies_poster)
                status = True
                return render_template ("recommendation.html", movies_name= recommended_movies_name, poster = recommended_movies_poster, movie_list= movie_list, status=status)
                
        except Exception as e :
            error = {'error':e}
            return render_template("recommendation.html",error = error, movie_list= movie_list,status=status)
                
                
    else :
        return render_template("recommendation.html",movie_list= movie_list,status=status)

if __name__ =='__main__':
    app.debug=True
    app.run()
    
    

