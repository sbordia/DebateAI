import os
import openai
from flask import Flask, redirect, render_template, request, url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

########################################################################################################
### Globals ###
########################################################################################################

g_emotion_array = []
g_emotion_array.append("""Boring sentence: We should not provoke Russia because it would be bad for our future and society. 
Here I have written a persuasive sentence with more emotion: Every action has an equal and opposite reaction, the third law of physics, and if we poke Russia, why would they just sit back? Now, I sincerely ask, is our own personal agenda against a country more important than the progress of us as a society?""")
g_emotion_array.append("""Boring sentence: America is ruining its global image due to its political decisions, and we are isolating ourselves from our allies.  
Here I have written a persuasive sentence with more emotion: I see a U.S. administration using or threatening instruments of economic coercion, tariffs and sanctions like no administration has done before, and I don't see America winning. In fact, for now, I see it losing, and what I do see is America alienating its allies, its friends, and ultimately the undermining of American credibility and American legitimacy across the globe. If America truly wants to be known as a world leader, it is high time they start acting like it.""")
g_emotion_array.append("""Boring sentence: African Americans deserve to be free, as that is one of the founding ideals of our country. 
Here I have written a persuasive sentence with more emotion: This is no time to engage in the luxury of cooling off or to take the tranquilizing drug of gradualism, but instead now is the time to make real the promises of democracy by lifting our nation from the quick sands of racial injustice to the solid rock of brotherhood.""")
g_emotion_array.append("""Boring sentence: We need the press to keep our democracy functioning. 
Here I have written a persuasive sentence with more emotion: Our liberty depends on the freedom of the press, and that cannot be limited without it being lost. Our country is rooted in the ideals of liberty and democracy, but how can we claim to be a global leader if we ourselves fall victim to that dangerous drug known as hypocrisy. """)
g_emotion_array.append("""Boring sentence: We need to seek peace and be the leaders in doing so. 
Here I have written a persuasive sentence with more emotion: My fellow Americans, let us take that first step. Let us step back from the shadow of war and seek out the way of peace. And if that journey is a thousand miles, or even more, let history record that we, in this land, at this time, took the first step.""")
g_emotion_array.append("""Boring sentence: We will fight to defend our country no matter what happens and no matter how many hardships and obstacles we have to overcome. We will support our allies, and together we will win.
Here I have written a persuasive sentence with more emotion: Even though large tracts of Europe and many old and famous States have fallen or may fall into the grip of the Gestapo and all the odious apparatus of Nazi rule, we shall not flag or fail. We shall go on to the end, we shall fight in France, we shall fight on the seas and oceans, we shall fight with growing confidence and growing strength in the air, we shall defend our Island, whatever the cost may be, we shall fight on the beaches, we shall fight on the landing grounds, we shall fight in the fields and in the streets, we shall fight in the hills; we shall never surrender, and even if, which I do not for a moment believe, this Island or a large part of it were subjugated and starving, then our Empire beyond the seas, armed and guarded by the British Fleet, would carry on the struggle, until, in God's good time, the New World, with all its power and might, steps forth to the rescue and the liberation of the old.""")

g_evidence_array = []
g_evidence_array.append("""Boring sentence: Turkey is necessary in NATO has it provides a legitimate deterrence towards Russia, due to its weapons and geographical proximity.
Here I have written a persuasive sentence with more evidence: Turkey’s NATO membership allows it to freely sell drones to Ukraine, enabling deterrence against Russia. According to the Washington Post, Ankara relies on its NATO security guarantee to cooperate closely with Ukraine for its own economic interests, maximizing the market share of its drones and keeping its own drone fleet flying.""")
g_evidence_array.append("""Boring sentence: The US is to blame for the Yemen War as we are sponsoring Saudi Arabia's misuse of weapons.
Here I have written a persuasive sentence with more evidence: The war in Yemen is America’s war as Saudi Arabia has spent a fortune buying arms from America to prosecute a war that has killed almost 250,000 people — the world’s worst humanitarian catastrophe in our lifetime. Continuing to provide weapons shows the world US is determined to keep aiding a Saudi-backed war.""")
g_evidence_array.append("""Boring sentence: Legalization of drugs is necessary as they can actually reduce drug-related deaths.
Here I have written a persuasive sentence with more evidence: Legalization of marijuana has empirically been shown to reduce opioid emergencies, as a University of Pittsburgh study finds that in the four states that legalized marijuana, CA, Maine, Nevada, and Massachusetts, opioid emergencies went down 7.6%.""")
g_evidence_array.append("""Boring sentence: Even though progress has been made, women are still paid less than men.
Here I have written a persuasive sentence with more evidence: In 2020, women made 83 cents for every dollar earned by men, according to the U.S. Census Bureau. Women of color are at an even greater disadvantage. The gender wage gap was much larger in 1960, when women's pay was 61 percent of men's. But progress has stalled over the last 15 or more years.""")
g_evidence_array.append("""Boring sentence: Guns are killing many people in the US, and it is on a larger scale than other developed countries.
Here I have written a persuasive sentence with more evidence: The US accounts for just 4 percent of the world's population but 35 percent of global firearm suicides. Americans are 25 times more likely to be killed in a gun homicide than people in other high-income countries.""")
g_evidence_array.append("""Boring sentence: Most people in the world are affected by climate change, and many countries have lost billions of dollars due to climate related disasters.
Here I have written a persuasive sentence with more evidence: At least 85 percent of the global population has experienced weather events made worse by climate change, according to research published Monday in the journal Nature Climate Change. In fact, in the United States, climate disasters have already led to more than $100 billion in damage this year, according to The Washington Post.""")

g_emotion_user_selection = []
g_evidence_user_selection = []

g_ip_user = {}

########################################################################################################
### Routes ###
########################################################################################################

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        if request.form.get('action5') == "Submit":
            user = request.form["name"]
            nameobj = {"name": user, "count": 1}
            g_ip_user[GetIP(request)] = nameobj
            print(g_ip_user, flush=True)
            return redirect(url_for("index2"))

    result = request.args.get("result")
    return render_template("index.html", result=result)

@app.route("/index2", methods=("GET", "POST"))
def index2():
    if request.method == "POST":
        if request.form.get('action1') == 'Results':
                sentence = request.form["Sentence"]

                # Use pretrained emotion and feed it back to the model 2 additional times (this is Variation 1)
                response = openAIPretrainedEmotionCreate(sentence)
                response1 = openAIPretrainedEmotionCreate(response.choices[0].text)
                response2 = openAIPretrainedEmotionCreate(response1.choices[0].text)

                update_pretrained_emotion_results(GetIP(request), sentence, response2.choices[0].text)

                # Use pretrained evidence and feed it back to the model 2 additional times (this is Variation 2)
                response_1 = openAIPretrainedEvidenceCreate(sentence)
                response1_1 = openAIPretrainedEvidenceCreate(response_1.choices[0].text)
                response2_1 = openAIPretrainedEvidenceCreate(response1_1.choices[0].text)

                update_pretrained_evidence_results(GetIP(request), sentence, response2_1.choices[0].text)

                return redirect(url_for("index2", result= "Here is Variation 1:\n" + response2.choices[0].text.strip() + "\n\nHere is Variation 2:\n" + response2_1.choices[0].text.strip()))
        
        elif request.form.get('action2') == 'Submit':
                option = request.form["recommed"]
                update_pretrained_users_v1_results(GetIP(request), option)
                option1 = request.form["recommend"]
                update_pretrained_users_v2_results(GetIP(request), option1)
                sentence = request.form["Sentence"]
                update_pretrained_users_explanation(GetIP(request), sentence)

    result = request.args.get("result")
    return render_template("index2.html", result=result) 

@app.route("/user", methods=("GET", "POST"))
def user():
    if request.method == "POST":
        if request.form.get('action3') == 'Submit':
            option_1 = request.form.get("inp-1")
            if option_1:
                g_emotion_user_selection.append(0)

            option_2 = request.form.get("inp-2")
            if option_2:
                g_emotion_user_selection.append(1)

            option_3 = request.form.get("inp-3")
            if option_3:
                g_emotion_user_selection.append(2)

            option_4 = request.form.get("inp-4")
            if option_4:
                g_emotion_user_selection.append(3)

            option_5 = request.form.get("inp-5")
            if option_5:
                g_emotion_user_selection.append(4)

            option_6 = request.form.get("inp-6")
            if option_6:
                g_emotion_user_selection.append(5)

            return redirect(url_for("userevidence"))

    return render_template("user.html")

@app.route("/userevidence", methods=("GET", "POST"))
def userevidence():
    if request.method == "POST":
        if request.form.get('action4') == 'Submit':
            option_1 = request.form.get("inp-1")
            if option_1:
                g_evidence_user_selection.append(0)

            option_2 = request.form.get("inp-2")
            if option_2:
                g_evidence_user_selection.append(1)

            option_3 = request.form.get("inp-3")
            if option_3:
                g_evidence_user_selection.append(2)

            option_4 = request.form.get("inp-4")
            if option_4:
                g_evidence_user_selection.append(3)

            option_5 = request.form.get("inp-5")
            if option_5:
                g_evidence_user_selection.append(4)

            option_6 = request.form.get("inp-6")
            if option_6:
                g_evidence_user_selection.append(5)

            return redirect(url_for("userindex"))

    return render_template("userevidence.html")

@app.route("/userindex", methods=("GET", "POST"))
def userindex():
    if request.method == "POST":
        if request.form.get('action1') == 'Results':
                sentence = request.form["Sentence"]

                # Use usertrained emotion and feed it back to the model 2 additional times (this is Variation 1)
                response = openAIUserEmotionCreate(sentence)
                response1 = openAIUserEmotionCreate(response.choices[0].text)
                response2 = openAIUserEmotionCreate(response1.choices[0].text)

                update_usertrained_emotion_results(GetIP(request), sentence, response2.choices[0].text)

                # Use usertrained evidence and feed it back to the model 2 additional times (this is Variation 2)
                response_1 = openAIUserEvidenceCreate(sentence)
                response1_1 = openAIUserEvidenceCreate(response_1.choices[0].text)
                response2_1 = openAIUserEvidenceCreate(response1_1.choices[0].text)

                update_usertrained_evidence_results(GetIP(request), sentence, response2_1.choices[0].text)

                return redirect(url_for("userindex", result= "Variation 1:\n" + response2.choices[0].text.strip() + "\n\nVariation 2:\n" + response2_1.choices[0].text.strip()))
        elif request.form.get('action6') == 'Submit':
                option = request.form["recommed"]
                update_usertrained_users_v1_results(GetIP(request), option)
                option1 = request.form["recommend"]
                update_usertrained_users_v2_results(GetIP(request), option1)
                sentence = request.form["Sentence"]
                update_usertrained_users_explanation(GetIP(request), sentence)

    result = request.args.get("result")
    return render_template("userindex.html", result=result)

@app.route("/final", methods=("GET", "POST"))
def final():
    if request.method == "POST":
        if request.form.get('action7') == 'Submit':
            option = request.form["recommend"]
            update_users_preferences(GetIP(request), option)
            sentence = request.form["Sentence"]
            update_post_users_preferences(GetIP(request), sentence)
            return redirect(url_for("final2"))

    result = request.args.get("result")
    return render_template("final.html", result=result)

@app.route("/final2", methods=("GET", "POST"))
def final2():
    result = request.args.get("result")
    return render_template("final2.html", result=result)

########################################################################################################
### Helpers ###
########################################################################################################
def GetIP(request):
    return request.remote_addr

def createParentDir(ip):
    user = g_ip_user.get(ip)
    username = user.get("name")
    path = "files" +  "/" + username
    os.makedirs(path, exist_ok = True)
    return path

def openAIPretrainedEmotionCreate(text):
    return openai.Completion.create(
        model="text-davinci-002",
        prompt=generate_pretrained_emotion_prompt(text),
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response  

def openAIPretrainedEvidenceCreate(text):
    return openai.Completion.create(
        model="text-davinci-002",
        prompt=generate_pretrained_evidence_prompt(text),
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

def openAIUserEmotionCreate(text):
    return openai.Completion.create(
        model="text-davinci-002",
        prompt=generate_user_emotion_prompt(text),
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

def openAIUserEvidenceCreate(text):
    return openai.Completion.create(
        model="text-davinci-002",
        prompt=generate_user_evidence_prompt(text),
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

########################################################################################################
### Pretrained Model ###
########################################################################################################

def generate_pretrained_emotion_prompt(sentence):
    dynamic_set = "Convert a boring sentence into a more persuasive sentence by using more emotion:."
    for x in g_emotion_array:
        dynamic_set += x
    dynamic_set += """Boring sentence:: {}
                    Here I have written a persuasive sentence with more emotion:"""
    return dynamic_set.format(sentence.capitalize())

def generate_pretrained_evidence_prompt(sentence):
    dynamic_set = "Convert a boring sentence into a more persuasive sentence by using more evidence:."
    for x in g_evidence_array:
        dynamic_set += x
    dynamic_set += """Boring sentence:: {}
                    Here I have written a persuasive sentence with more evidence:"""
    return dynamic_set.format(sentence.capitalize())

def update_pretrained_emotion_results(ip, input, output):
    filename = createParentDir(ip) + "/" + "pretrained_results_emotion.txt"
    f= open(filename,"a")
    f.write("\nInput:\n" + input.strip())
    f.write("\nOutput:\n" + output.strip())
    f.close()

def update_pretrained_evidence_results(ip, input, output):
    filename = createParentDir(ip) + "/" + "pretrained_results_evidence.txt"
    f= open(filename,"a")
    f.write("\nInput:\n" + input.strip())
    f.write("\nOutput:\n" + output.strip())
    f.close()

def update_pretrained_users_explanation(ip, input):
    filename = createParentDir(ip) + "/" + "pretrained_results_explanation.txt"
    f= open(filename,"a")
    f.write("\nInput:\n" + input.strip())
    f.close()


def update_pretrained_users_v1_results(ip, option):
    filename = createParentDir(ip) + "/" + "pretrained_results_user_v1.txt"
    f= open(filename,"a")
    f.write("\nVariation1: " + option.strip())
    f.close()

def update_pretrained_users_v2_results(ip, option):
    filename = createParentDir(ip) + "/" + "pretrained_results_user_v2.txt"
    f= open(filename,"a")
    f.write("\nVariation2: " + option.strip())
    f.close()

########################################################################################################
### User Model ###
########################################################################################################

def generate_user_emotion_prompt(sentence):
    dynamic_set = "Convert a boring sentence into a more persuasive sentence by using more emotion:."
    for x in g_emotion_user_selection:
        dynamic_set += g_emotion_array[x]
    dynamic_set += """Boring sentence:: {}
                    Here I have written a persuasive sentence with more emotion:"""
    return dynamic_set.format(sentence.capitalize())

def generate_user_evidence_prompt(sentence):
    dynamic_set = "Convert a boring sentence into a more persuasive sentence by using more evidence:."
    for x in g_evidence_user_selection:
        dynamic_set += g_evidence_array[x]
    dynamic_set += """Boring sentence:: {}
                    Here I have written a persuasive sentence with more evidence:"""
    return dynamic_set.format(sentence.capitalize())

def update_usertrained_emotion_results(ip, input, output):
    filename = createParentDir(ip) + "/" + "usertrained_results_emotion.txt"
    f= open(filename,"a")
    f.write("\nInput:\n" + input.strip())
    f.write("\nOutput:\n" + output.strip())
    f.close()

def update_usertrained_evidence_results(ip, input, output):
    filename = createParentDir(ip) + "/" + "usertrained_results_evidence.txt"
    f= open(filename,"a")
    f.write("\nInput:\n" + input.strip())
    f.write("\nOutput:\n" + output.strip())
    f.close()

def update_usertrained_users_results(ip, option):
    filename = createParentDir(ip) + "/" + "usertrained_results_user.txt"
    f= open(filename,"a")
    f.write("\n\nOption: " + option.strip())
    f.close()

def update_users_preferences(ip, option):
    filename = createParentDir(ip) + "/" + "update_users_preferences.txt"
    f= open(filename,"a")
    f.write("\n\nOption: " + option.strip())
    f.close()

def update_usertrained_users_explanation(ip, input):
    filename = createParentDir(ip) + "/" + "usertrained_results_explanation.txt"
    f= open(filename,"a")
    f.write("\nInput:\n" + input.strip())
    f.close()


def update_usertrained_users_v1_results(ip, option):
    filename = createParentDir(ip) + "/" + "usertrained_results_user_v1.txt"
    f= open(filename,"a")
    f.write("\nVariation1: " + option.strip())
    f.close()

def update_usertrained_users_v2_results(ip, option):
    filename = createParentDir(ip) + "/" + "usertrained_results_user_v2.txt"
    f= open(filename,"a")
    f.write("\nVariation2: " + option.strip())
    f.close()

def update_post_users_preferences(ip, option):
    filename = createParentDir(ip) + "/" + "update_post_users_explanation.txt"
    f= open(filename,"a")
    f.write("\n\nExplanation: " + option.strip())
    f.close()


