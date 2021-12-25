#build a streamlit app
import streamlit as st
from PIL import Image
import youtube_transcript_api
import simplejson
from youtube_transcript_api import YouTubeTranscriptApi
import urllib.request
import json
import urllib
import os 


#Favicon and Header
st.set_page_config(
        page_title='Search YouTube content                 ',
        page_icon="🔎"
        )


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 








list_of_video_ids = ['EWfZ907Cpy8', 'sx93aUj4A_o', 'GE_00MgKMEI', 'gF69voHU_ys', 'tAtaIZD0Ebs', '3E75UvmY9GA', 'fOPP9Qe10Rg']
all_transcripts = []


# Loop videos:


for VideoID in list_of_video_ids: 
  params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % VideoID}
  url = "https://www.youtube.com/oembed"
  query_string = urllib.parse.urlencode(params)
  url = url + "?" + query_string
  
  with urllib.request.urlopen(url) as response:
      response_text = response.read()
      data = json.loads(response_text.decode())
      #print('Title: ' + data['title'])
  
  # Separator? - not sure its purpose...
  print(' ')
  
  # retrieve the available transcripts
  transcript_list = YouTubeTranscriptApi.list_transcripts(VideoID)
  
  # iterate over all available transcripts
  for transcript in transcript_list: 
    # fetch the actual transcript data
    #print(transcript.fetch())
    data = transcript.fetch()

    #data = transcript.fetch() # [{'text': "i'm gonna attempt to collect 30 million", 'start': 0.0, 'duration': 4.16}, {'text': '...
    #print(type(data)) # <class 'list'>

    # Add "video_id" for recover it later: 
    data.insert(0, {'video_id': VideoID})

    # Add the fetched data to the "all_transcripts" global variable.
    all_transcripts += data
      
  # you can also directly filter for the language you are looking for, using the transcript list
  #transcript = transcript_list.find_transcript(['en']) 
  #print(type(transcript))
  #print(all_transcripts[:len(all_transcripts)-1])
  #print(str(len(all_transcripts)))
  #print(type(all_transcripts))




img = Image.open("google.jpg")


col1, col2, col3, col4, col5 = st.columns([1,1,5,1,1])

with col1:
        st.write("")
        
with col3:
        st.image(img)
        
        st.write("")
        option = st.selectbox(
     'What YouTube channel do you want to search?',
     ('ChubbyEmu', 'Lorem ipsum2', 'Lorem ipsum3'))

        st.write(option)
        st.write("")



        #add a search bar
        user_input = st.text_input("Type in the words/sentences you want to search", "")
        user_input = user_input.lower()
        st.write(' ')

        if len(user_input) > 60:
                        st.write("Your sentence is too long. Try shorter ones.")                
        
        
        # We use here the global list "all_transcripts": 
        dictionary = all_transcripts

        # Function to loop all transcripts and search the captions thath contains the 
        # user input.
        # TO-DO: Validate when no data is found.
        def search_dictionary(user_input, dictionary): 
                link = 'https://youtu.be/'

                # Get the video_id: 
                v_id  = ""

                # I add here the debbuged results: 
                lst_results = []

                # string body:
                matched_line = ""

                # You're really looping a list of dictionaries: 
                for i in range(len(dictionary)): # <= this is really a "list".
                        try:
                #print(type(dictionary[i])) # <= this is really a "dictionary".
                #print(dictionary[i])

                # now you can iterate here the "dictionary": 
                                for x, y in dictionary[i].items():
        
                                        if (x == "video_id"): 
                                                v_id = y
                                        if (user_input in str(y) and len(v_id) > 0):
                                                matched_line = str(dictionary[i]['text']) + '...' + str(dictionary[i]['start']) + ' min und ' + str(dictionary[i]['duration']) + ' sec :: ' + link + v_id + '?t=' + str(int(dictionary[i]['start'] - 1)) + 's'
                
          
                        # Check if line does not exists in the list of results: 
                                        if len(lst_results) == 0:
                                                lst_results.append(matched_line)
                                        if matched_line not in lst_results: 
                                                lst_results.append(matched_line)

                        except Exception as err: 
                                st.write('Unexpected error - see details below:')
                                st.write(err)

                        # Just an example for show "no results":
                if (len(lst_results) == 0):
                        st.write("No results found with input (" + user_input + ")")
                else: 
                        st.write("All time stamps: ")
                        st.write("__________________")

                        #st.write("\n".join(lst_results)) # <= this is for show the results with a line break.
                        
                        #make a new line after each https link:
                        new_lst_results = []
                        for i in range(len(lst_results)):
                                new_lst_results.append(lst_results[i] + '\n')
                        st.write("\n".join(new_lst_results)) # <= this is for show the results with a line break.
                        # Function ends here.
        

        if st.button("Search"):
                
                search_dictionary(user_input, dictionary)  
        
        






footer="""<style>
a:link , a:visited{
color: red;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: blue;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: transparent;
color: grey;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with ❤️  by <a style='display: block; text-align: center;' href="https://www.instagram.com/max_mnemo/" target="_blank">Max Mnemo </a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)





