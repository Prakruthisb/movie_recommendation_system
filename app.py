import streamlit as st
import pickle 
import requests


new_df = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb')) 
df = pickle.load(open('df.pkl','rb')) 

def fetch_poster(movie_name):
    url =  f"http://www.omdbapi.com/?t={movie_name}&apikey=f4d089de" 

    response = requests.get(url) 
    data = response.json() 

    if data['Response'] == 'True':
        return data['Poster']
    else:
        return 'No' 

def recommend(movie):
    movie_index = new_df[new_df['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)),key=lambda x:x[1],reverse=True)[1:11]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movie_list:
        recommended_movies.append(new_df.iloc[i[0]]['title'])

        #fetch poster from api
        poster = fetch_poster(new_df.iloc[i[0]]['title']) 
        if poster != 'No':
            recommended_movies_poster.append(poster) 
        else:
            recommended_movies_poster.append('Movie poster not found!!!')

    return recommended_movies,recommended_movies_poster

st.title("Movies Recommendation System")

selected_movie = st.selectbox(
    'Which movie do you like best?',
     new_df['title']) 

if st.button("Recommend"):
    selected_movie_poster = fetch_poster(selected_movie)
    st.markdown("<h2 style='text-align: center;'>"+selected_movie+"</h2>", unsafe_allow_html=True)

    col1,col2 = st.columns([1,2]) 

    with col1:
        if selected_movie_poster != 'No':
            st.image(selected_movie_poster) 
        else:
            st.write("Movies Poster Not Found!!!") 

    with col2:
        st.write(":rainbow[TITLE] :  "+selected_movie) 

        st.write(":rainbow[OVERVIEW] : ")
        overview = " ".join(df[df['title']==selected_movie]['overview'].tolist()[0])
        st.write(overview)  

        st.write(":rainbow[GENERE] :  " + " , ".join(df[df['title']==selected_movie]['genres'].tolist()[0]))        





    
    st.header(":rainbow[_RECOMMENDED MOVIES FOR YOU_]") 
    movies_name,movies_poster = recommend(selected_movie)




    # for i in range(len(movies_poster)):
    #     if movies_poster[i] != 'Movie poster not found!!!':
    #         st.image(movies_poster[i], caption=movies_name[i]) 
    #     else:
    #         st.write(movies_poster[i]) 
    #         st.write(movies_name[i]) 

    # col1, col2, col3, col4, col5 = st.columns(5)

    # with col1:
    #     st.caption(movies_name[0])
    #     st.image(movies_poster[0])

    # with col2:
    #     st.caption(movies_name[1])
    #     st.image(movies_poster[1])

    # with col3:
    #     st.caption(movies_name[2])
    #     st.image(movies_poster[2])

    # with col4:
    #     st.caption(movies_name[3])
    #     st.image(movies_poster[3])
    
    # with col5:
    #     st.caption(movies_name[4])
    #     st.image(movies_poster[4])




    for i in range(0, len(movies_name), 5):
        cols = st.columns(5)
        for j, col in enumerate(cols):
            if i + j < len(movies_name):
                if movies_poster[i+j] != 'Movie poster not found!!!': 
                    col.caption(movies_name[i+j]) 
                    col.image(movies_poster[i + j])
                else:
                    continue 


