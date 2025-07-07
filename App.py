from http.client import responses
from tkinter import *
from mydb import Database
from tkinter import messagebox
from myapi import HuggingFaceNLP
import os
from dotenv import load_dotenv


class NLPApp:

    def __init__(self,hf_model):

        #creating database object
        self.dbo = Database()

        self.huggingface = hf_model

        #login window
        self.root = Tk()
        self.root.title('NLP-App')
        self.root.iconbitmap('resources/favicon.ico')
        self.root.geometry('350x600')
        self.root.configure(bg='#edd6cb')

        self.login_gui()

        self.root.mainloop()

    def login_gui(self):
        self.clear()
        heading = Label(self.root,text="NLPApp",bg='#edd6cb',fg='#000000')
        heading.pack(pady=(30,30))
        heading.configure(font=('verdana',24,'bold'))

        label1=Label(self.root,text="Enter Email")
        label1.pack(pady=(10,10))

        self.email_input = Entry(self.root,width=50)
        self.email_input.pack(pady=(5,10),ipady=4)

        label2 = Label(self.root, text="Enter Password")
        label2.pack(pady=(10, 10))

        self.password_input = Entry(self.root, width=50,show="*")
        self.password_input.pack(pady=(5, 10), ipady=4)

        login_btn = Button(self.root,text='Login',width=30,height=2,command=self.perform_login)
        login_btn.pack(pady=(10,10))

        label3 =Label(self.root, text="Not a Member?")
        label3.pack(pady=(10,5))

        redirect_btn=Button(self.root,text="Register Now", command=self.register_gui)
        redirect_btn.pack(pady=(2,2))

    def register_gui(self):
        self.clear()

        heading = Label(self.root, text="NLPApp", bg='#edd6cb', fg='#000000')
        heading.pack(pady=(30, 30))
        heading.configure(font=('verdana', 24, 'bold'))

        label10 = Label(self.root, text="Enter Name")
        label10.pack(pady=(10, 10))

        self.name_input = Entry(self.root, width=50)
        self.name_input.pack(pady=(5, 10), ipady=4)

        label1 = Label(self.root, text="Enter Email")
        label1.pack(pady=(10, 10))

        self.email_input = Entry(self.root, width=50)
        self.email_input.pack(pady=(5, 10), ipady=4)

        label2 = Label(self.root, text="Enter Password")
        label2.pack(pady=(10, 10))

        self.password_input = Entry(self.root, width=50, show="*")
        self.password_input.pack(pady=(5, 10), ipady=4)

        register_btn = Button(self.root, text='Register', width=30, height=2,command=self.perform_registration)
        register_btn.pack(pady=(10,10))

        label3 = Label(self.root, text="Already a Member?")
        label3.pack(pady=(10,5))

        redirect_btn = Button(self.root, text="Login Now", command=self.login_gui)
        redirect_btn.pack(pady=(2,2))

    def clear(self):
        for i in self.root.pack_slaves():
            i.destroy()

    def perform_registration(self):
        name = self.name_input.get()
        email = self.email_input.get()
        password = self.password_input.get()

        response = self.dbo.add_data(name, email,password)

        if response:
            messagebox.showinfo("Sucess","Registration Successful.You can login now.")
        else:
            messagebox.showerror("Email Already Exists.")

    def perform_login(self):
        email = self.email_input.get()
        password = self.password_input.get()

        response = self.dbo.search(email,password)
        if response:
            messagebox.showinfo("Success","Login Successful")
            self.home_gui()
        else:
            messagebox.showerror("Error","Incorrect Login Credentials.")

    def home_gui(self):
        self.clear()
        heading = Label(self.root, text="NLPApp", bg='#edd6cb', fg='#000000')
        heading.pack(pady=(30, 30))
        heading.configure(font=('verdana', 24, 'bold'))


        sentiment_btn = Button(self.root, text='Sentiment Analysis', width=30, height=2, command=self.sentiment_gui)
        sentiment_btn.pack(pady=(10, 10))

        ner_btn = Button(self.root, text='Named Entity Recognition', width=30, height=4, command=self.ner_gui)
        ner_btn.pack(pady=(10, 10))

        emotion_btn = Button(self.root, text='Emotion Prediction', width=30, height=2, command=self.emotion_gui)
        emotion_btn.pack(pady=(10, 10))

        logout_btn = Button(self.root, text="LogOut", command=self.login_gui)
        logout_btn.pack(pady=(2, 2))

    def sentiment_gui(self):
        self.clear()

        heading = Label(self.root, text="NLPApp", bg='#edd6cb', fg='#000000')
        heading.pack(pady=(30, 30))
        heading.configure(font=('verdana', 24, 'bold'))

        heading2= Label(self.root, text="Sentiment Analysis", bg='#edd6cb', fg='#000000')
        heading2.pack(pady=(10, 20))
        heading2.configure(font=('verdana', 20))

        label1 = Label(self.root, text="Enter the text")
        label1.pack(pady=(10, 5))

        self.sentiment_input = Entry(self.root, width=50)
        self.sentiment_input.pack(pady=(5, 10), ipady=4)

        sentiment_btn = Button(self.root, text='Analyze Sentiment', width=30, height=2,
                             command=self.perform_sentiment_analysis)
        sentiment_btn.pack(pady=(10, 10))

        self.sentiment_result = Label(self.root, text="",bg='#edd6cb',fg='#000000')
        self.sentiment_result.pack(pady=(10, 5))
        self.sentiment_result.configure(font=('verdana', 16))

        goback_btn = Button(self.root, text='Go Back<<', width=30, height=2,
                               command=self.home_gui)
        goback_btn.pack(pady=(10, 10))

    def perform_sentiment_analysis(self):
        text = self.sentiment_input.get()
        result = self.huggingface.sentiment_analysis(text)

        try:
            # ✅ Handle double-nested list
            if isinstance(result, list) and isinstance(result[0], list):
                top_result = max(result[0], key=lambda x: x['score'])  # get highest score label
                label = top_result['label']
                score = top_result['score']
                self.sentiment_result.config(text=f"You seem to be feeling {label.capitalize()} ({round(score*100)}% confident)")

            else:
                raise ValueError("Unexpected response format.")

        except Exception as e:
            print("❌ Error while parsing result:", e)
            messagebox.showerror("Error", "Could not analyze sentiment. Invalid response from model.")

    def emotion_gui(self):
        self.clear()

        heading = Label(self.root, text="Emotion Detection", bg='#edd6cb', fg='#000000')
        heading.pack(pady=(30, 20))
        heading.configure(font=('verdana', 20, 'bold'))

        label1 = Label(self.root, text="Enter the text")
        label1.pack(pady=(10, 5))

        self.emotion_input = Entry(self.root, width=50)
        self.emotion_input.pack(pady=(5, 10), ipady=4)

        emotion_btn = Button(self.root, text='Detect Emotion', width=30, height=2,
                             command=self.perform_emotion_detection)
        emotion_btn.pack(pady=(10, 10))

        self.emotion_result = Label(self.root, text="", bg='#edd6cb', fg='#000000')
        self.emotion_result.pack(pady=(10, 5))
        self.emotion_result.configure(font=('verdana', 16))

        goback_btn = Button(self.root, text='Go Back <<', width=30, height=2,
                            command=self.home_gui)
        goback_btn.pack(pady=(10, 10))

    def perform_emotion_detection(self):
        text = self.emotion_input.get()
        result = self.huggingface.emotion_detection(text)

        try:
            if isinstance(result, list) and isinstance(result[0], list):
                top_result = max(result[0], key=lambda x: x['score'])
                label = top_result['label']
                score = top_result['score']

                emoji_map = {
                    "joy": "😊", "anger": "😠", "sadness": "😢", "fear": "😨", "surprise": "😲", "love": "❤️",
                    "disgust": "🤢"
                }

                icon = emoji_map.get(label.lower(), "🔍")
                self.emotion_result.config(
                    text=f"{icon} Emotion: {label.capitalize()} ({round(score * 100)}% confident)")

            else:
                raise ValueError("Unexpected response format.")

        except Exception as e:
            print("❌ Error while parsing emotion result:", e)
            messagebox.showerror("Error", "Could not detect emotion. Invalid response from model.")

    def ner_gui(self):
        self.clear()

        heading = Label(self.root, text="Named Entity Recognition", bg='#edd6cb', fg='#000000')
        heading.pack(pady=(30, 20))
        heading.configure(font=('verdana', 20, 'bold'))

        label1 = Label(self.root, text="Enter the text")
        label1.pack(pady=(10, 5))

        self.ner_input = Entry(self.root, width=50)
        self.ner_input.pack(pady=(5, 10), ipady=4)

        ner_btn = Button(self.root, text='Recognize Entities', width=30, height=2,
                         command=self.perform_ner)
        ner_btn.pack(pady=(10, 10))

        self.ner_result = Label(self.root, text="", bg='#edd6cb', fg='#000000', wraplength=300, justify=LEFT)
        self.ner_result.pack(pady=(10, 5))
        self.ner_result.configure(font=('verdana', 12))

        goback_btn = Button(self.root, text='Go Back <<', width=30, height=2,
                            command=self.home_gui)
        goback_btn.pack(pady=(10, 10))

    def perform_ner(self):
        text = self.ner_input.get()
        result = self.huggingface.named_entity_recognition(text)

        try:
            if isinstance(result, list):
                entities = []
                for ent in result:
                    word = ent.get("word", "")
                    entity = ent.get("entity", "")
                    score = round(ent.get("score", 0) * 100)
                    entities.append(f"{word} → {entity} ({score}%)")

                self.ner_result.config(text="\n".join(entities))
            else:
                raise ValueError("Unexpected NER response format.")

        except Exception as e:
            print("❌ Error while parsing NER result:", e)
            messagebox.showerror("Error", "Could not extract entities. Invalid response from model.")


if __name__ == "__main__":

    load_dotenv()
    token = os.getenv("HF_TOKEN")
    hf_model = HuggingFaceNLP(token)

    app = NLPApp(hf_model)



