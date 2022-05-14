import datetime
import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import pyjokes
import requests
from bs4 import BeautifulSoup


def call_command():
    try:
        with sr.Microphone() as source:
            # print('Raju waiting')
            voice = listener.listen(source, 5, 2.5)
            call = listener.recognize_google(voice)
            call = call.lower()
            print(call)
            if call == name_va:
                take_query()
            else:
                call_command()

    except sr.UnknownValueError:
        call_command()


def speak(x):
    speaker.say(x)
    speaker.runAndWait()


def tell_time():
    time = str(datetime.datetime.now())
    hour = int(time[11:13])
    check = 'am'
    if hour > 12:
        hour = hour - 12
        check = 'pm'
    minutes = time[14:16]
    speak(f'The time now is {hour} {minutes} {check}')

    if check == 'pm' and hour > 9:
        speak("Its late, you have to sleep !!")

    call_command()


def check_movie(movie):
    print(movie)
    movie = movie.replace(' available', '')
    movie = movie.replace(' ', '-')
    print(movie)
    html_text = requests.get(f'https://123series.top/search/{movie}').text
    soup = BeautifulSoup(html_text, 'lxml')
    all_details = soup.find_all('div', attrs={'class': 'film-detail'})
    title = []
    year = []
    duration = []
    for i in all_details:
        title.append(i.find('h2', attrs={'class': 'film-name'}).text)
        year.append(i.find('span', attrs={'class': 'fdi-item'}).text)
        duration.append(i.find('span', attrs={'class': 'fdi-item fdi-duration'}))

    print(title[0].strip())
    print(year[0])
    print(duration[0].text)


def change_name(name):
    global name_va
    name_va = name.lower()
    print(name_va)
    speak(f'Ok. From now you can call me {name_va}')


def execute_query(command):
    print(command)
    command = command.lower()
    if command == 'stop':
        speak('OK')
        call_command()
    time_ask = ['time', 'time please', 'what is the time', 'what''s the time', 'time kya hai']
    for i in time_ask:
        if command == i:
            tell_time()

    if 'wikipedia' in command or 'wiki' in command or 'who is' in command:
        command = command.replace('wikipedia', '')
        command = command.replace('wiki', '')
        command = command.replace('who is', '')
        info = wikipedia.summary(command, 2)
        speak(f' According to the Wikipedia, {info}')
        call_command()

    elif 'change your name to' in command:
        command = command.replace('change your name to ', '')
        change_name(command)
        call_command()

    elif 'google search' in command:
        command = command.replace('Google search', '')
        pywhatkit.search(command)
        call_command()

    elif command[0:4] == 'play' or command[0:6] == 'stream':
        command = command.replace('play', '')
        command = command.replace('stream', '')
        speak(f"Playing {command} on YouTube")
        pywhatkit.playonyt(command)
        call_command()

    elif 'joke' in command:
        speak(pyjokes.get_joke())
        call_command()

    elif 'is the movie' in command or '':
        speak('Just a second')
        movie = command.replace('is the movie', '')
        check_movie(movie)
        call_command()

    else:
        speak('I cant understand, Please Repeat')
        take_query()


def take_query():
    i = 0
    try:
        with sr.Microphone() as source:
            speak('I''m Listening')
            voice = listener.listen(source, 10, 4)
            command = listener.recognize_google(voice)
            execute_query(command)

    except sr.UnknownValueError:
        if i == 2:
            call_command()
        speak('I cant understand, Please Repeat')
        i += 1
        take_query()

    except :
        speak('No Internet')
        print('Waiting again')
        call_command()


if __name__ == "__main__":
    listener = sr.Recognizer()
    speaker = pyttsx3.init()
    voices = speaker.getProperty('voices')
    speaker.setProperty('voice', voices[0].id)
    name_va = 'hello'
    print('Waiting ....')
    call_command()

