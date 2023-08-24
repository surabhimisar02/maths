from . import text_to_picture
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .response_class import ResponseClass
import random

from functools import reduce
import spacy
import re
nlp = spacy.load("en_core_web_sm")
import copy
import ast
from random import choice

############################################# text-to-speech #########################
from django.http import FileResponse
from rest_framework.decorators import api_view

from gtts import gTTS
import io

from googletrans import Translator
translator = Translator()

def generate_audio(text,lang):
    """
    Given a text and destination language, this function generates audio in that language.

    Input_param:
        text : input text
        lang : destination lang. code

    Output_param: 
        response : audio file
    """
    out = translator.translate(text,dest=lang)
    tts = gTTS(text=out.text, lang=lang,slow=False)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    response = FileResponse(fp, content_type='audio/mpeg')
    response['Content-Disposition'] = 'attachment; filename="audio.mp3"'
    return response

@api_view(['GET'])
def text_to_speech(request):
    try:
        
        text  = request.META.get('HTTP_TEXT')
        lang    = request.META.get('HTTP_LANG')

        if text and lang:
             
            dict_data = generate_audio(text,lang)
            return dict_data
        else:
            response_obj = ResponseClass(400, "text and lang parameter cannot be null")
            return JsonResponse(response_obj.__dict__, status=400)

    except KeyError as e:
            response_obj = ResponseClass(400, "no field called text and lang")
            return JsonResponse(response_obj.__dict__, status=400) 


############################################# text-to-speech end #########################



############################################# Text-to-Text ###########################
from googletrans import Translator
translator = Translator()
def text_to_text_conversion(text,lang):
    """
    Given a text and destination language, this function converts sourse text to destination text.

    Input_param:
        text : input text
        lang : destination lang. code

    Output_param: 
        out.text : converted text in destination language 
    """
    out = translator.translate(text,dest=lang)
    return {"converted_text":out.text}

@api_view(['GET'])
def txt_to_txt(request):
    try:
        
        text  = request.META.get('HTTP_TEXT')
        lang    = request.META.get('HTTP_LANG')

        if text and lang:
             
            dict_data = text_to_text_conversion(text,lang)
        
            response_obj = ResponseClass(200, "Add Successful",dict_data)
            return JsonResponse(response_obj.__dict__, status=200)
        else:
            response_obj = ResponseClass(400, "text and lang parameter cannot be null")
            return JsonResponse(response_obj.__dict__, status=400)

    except KeyError as e:
            response_obj = ResponseClass(400, "no field called text and lang")
            return JsonResponse(response_obj.__dict__, status=400) 



############################################# Text-to-Text-end #######################

############################################## Fahads Code ###########################

Add_question = "Anand has 27 stickers. Nitin has 5 stikers. How many stickers they have together?" 
Sub_question = "Anand has 27 stickers. He gives 5 stickers to Sita. How many stickers does Anand left?"
Multi_question = "Anand has 27 stickers. He bought each of 5 rupees. What is the total cost?"
Div_question = "Anand has 9 stickers. He distrubted among 3 children. How much stickers does each child got?"

def text_explanation(answer,question_type,obj_extractor,version=None):
    """
    Given a question, generating its solution explanation.

    Input_param:
        answer : answer of the question under consideration
        question_type : operation type of the question( i.e. addition or subtraction etc)
        obj_extractor : dictionary which stores info of object related to the question (i.e. numbers,names,objects)
        version : version number of the question

    Output_param: 
        ques : generated quesion
        text_exp : generated text explanation(solution) of the question
    """
    
    if question_type == "addition":
        
        if version == '5':
            extracted_objects = obj_extractor
            num_01 = extracted_objects['numbers'][0]
            num_02 = extracted_objects['numbers'][1]
            object = extracted_objects['objects'][0]

            start = int(num_01)
            end = int(num_01) + int(num_02)

            numbers = [str(num) for num in range(start + 1, end)]
            result = ', '.join(numbers) + ' and ' + str(end)
            word_numbers = ["zero","one","two","three","four","five","six","seven","eight"]

            ques = f"{num_01} + {num_02} = ?"

            text_exp ={
                        0 : {
                                "commentary" : f"We are asked to find out {num_01} + {num_02} = how much?",
                            },
                        1 : {
                                "commentary" : f"We know that addition is bringing things together or mixing them. It means we will mix or add {num_02} objects to {num_01} objects and count the total.",
                            },  
                        2 : {
                                "commentary" : f"We already have {num_01} objects & after adding {num_02} more they will increase by {num_02}. Counting all of them together will give us the answer.",
                            },        
                        3 : {
                                "commentary" : f"To achieve this we will count {num_02} ahead of {num_01}. That is {result}",  
                            }, 
                        4 : {
                                "commentary" : f"This is called as forward counting. Let us see how we can do this.",  
                            }, 
                        5 : {
                                "commentary" : f"We have {num_01}. We want to further count {num_02} more. This process can be done in 2 ways.",  
                            }, 
                        6 : {
                                "commentary" : f"Method 1: We will count further by one every time which is same as adding one. This will be done as many times equal to the number to be added. Let us repeat it {num_02} times as we are to add {num_02}.",  
                            },   
                        7 : {
                                "commentary" : f"This way we have added 1 {word_numbers[int(num_02)]} times to {num_01} to get the answer as {num_01} + {num_02} = {answer}",  
                            }, 
                        8 : {
                                "commentary" : f"Method 2: Alternatively we can do the same addition as follows. We will start with {num_01} and count {num_02} numbers forward to get the answer.",  
                            },   
                        9 : {
                                "commentary" : f"Thus we have added {num_02} to {num_01} to get the answer, as {answer}. Thus our answer is {answer} and is written as {num_01} + {num_02} = {answer}",  
                            },
                        10 : {
                                "commentary" : f"Thus {num_01}+{num_02} is found out by counting {num_02} ahead of {num_01}. That is {result}",  
                            },   
                        11 : {
                                "commentary" : f"This is called as forward counting.",  
                            },                             
                    }
        elif version == '4':
            extracted_objects = obj_extractor
            num_01 = extracted_objects['numbers'][0]
            num_02 = extracted_objects['numbers'][1]
            object = extracted_objects['objects'][0]
            first_name = extracted_objects['names'][0]
            if len(extracted_objects['names']) == 2:
                second_name = extracted_objects['names'][1]
                if first_name == second_name:
                    second_name = "Akshay"
            else:
                second_name = "Akshay"


            ques = f"{first_name}  has {num_01} {object} and {second_name} has {num_02} {object}. How many {object} they have together ?"

            text_exp ={
                0 : {
                        "commentary" : f"To find how many {object} {first_name} and {second_name} have together,we need to do the addition of the {object} each of them have,",
                    },
                1 : {
                        "commentary" : f"To find the total, read out numbers next to the number of {object} {first_name} has.",
                    },  
                2 : {
                        "commentary" : f"{first_name} has {num_01} {object} and {second_name} has {num_02} {object}. To find the total number of {object}, count {num_02} numbers next to {num_01}.",
                    },        
                3 : {
                        "commentary" : f"Thus it would be ",   
                    },    
                4 : {
                        "commentary" : f"Therefore the total number of {object} are {int(num_01) + int(num_02)}.",   
                    },               
            }   

        elif version == '3':
            extracted_objects = obj_extractor
            num_01 = extracted_objects['numbers'][0]
            num_02 = extracted_objects['numbers'][1]
            object = extracted_objects['objects'][0]

            ques = f"{num_01} + {num_02} = ?"

            text_exp ={
                        0 : {
                                "commentary" : f"Here plus sign indicates addition",
                            },
                        1 : {
                                "commentary" : f"Addition is nothing but bringing the things together or mixing the things together or joining the things together or combining two or more things together.",
                            },  
                        2 : {
                                "commentary" : f"For example,Let Umesh has {num_01} {object} in one basket.",
                            },        
                        3 : {
                                "commentary" : f"and Rahim has {num_02} {object} in other basket",  
                            }, 
                        4 : {
                                "commentary" : f"To add them together, we need to combine {num_01} and {num_02} {object}.",  
                            }, 
                        5 : {
                                "commentary" : f"Now let us count these combined {object}.",  
                            }, 
                        6 : {
                                "commentary" : f"Mathematically this is represented as.",  
                            },   
                        7 : {
                                "commentary" : f"Therefore {num_01} plus {num_02} is equal to {int(num_01) + int(num_02)}.",  
                            },                     
                    }
            
        elif version == '2':
            extracted_objects = obj_extractor
            num_01 = extracted_objects['numbers'][0]
            num_02 = extracted_objects['numbers'][1]
            object = extracted_objects['objects'][0]

            ques = f" There are {num_01} {object} in one basket. And {num_02} {object} in another basket. How many total {object} are there? "
            
            text_exp ={
                0 : {
                        "commentary" : f"There are {num_01} {object} in one basket",
                    },
                1 : {
                        "commentary" : f"And {num_02} {object} in another basket.",
                    },  
                2 : {
                        "commentary" : f"To find the answer for this we need to combine the {object} from both the baskets together in a new basket.",
                    },        
                3 : {
                        "commentary" : f"This is called addition. Addition is nothing but bringing the things together or mixing the things together or joining the things together or combining two or more things together.",      
                    }, 
                4 : {
                        "commentary" : f"Now let us count these combined {object}.",      
                    }, 
                5 : {
                        "commentary" : f"Mathematically this is represented as",      
                    }, 
                6 : {
                        "commentary" : f"This sign is called equal to and it represents result.",      
                    }, 
                7 : {
                        "commentary" : f"So the total number of {object} are {int(num_01) + int(num_02)}.",      
                    },                               
            } 

        elif version == '1':
            extracted_objects = obj_extractor
            num_01 = extracted_objects['numbers'][0]
            num_02 = extracted_objects['numbers'][1]
            object = extracted_objects['objects'][0]
            
            ques = f"There are some {object} in one basket. And  some {object} in another basket.How many total {object} are there ?"

            text_exp ={
                0 : {
                        "commentary" : f"There are some {object} in one basket",
                    },
                1 : {
                        "commentary" : f"And some {object} in another basket.",
                    },  
                2 : {
                        "commentary" : f"To find the answer for this we need to combine the {object} from both the baskets together.",
                    },        
                3 : {
                        "commentary" : f"This is called addition and it is symbolically represented as.",      
                    }, 
                4 : {
                        "commentary" : f"This sign is called plus and it represents addition.",      
                    }, 
                5 : {
                        "commentary" : f"Addition is nothing but bringing the things together or mixing the things together or joining the things together or combining two or more things together.",      
                    }, 
                6 : {
                        "commentary" : f"Now let us count these combined (total) {object}.",      
                    }, 
                7 : {
                        "commentary" : f"So the total number of {object} are {int(num_01) + int(num_02)}.",      
                    },                               
            } 
        return ques,text_exp 
        
    if question_type == "subtraction":
        marathi_obj_dict = {"Apples":"सफरचंद","Oranges":"संत्रा","Bats":"बॅट्स","Balls":"बॉल्स","Pens":"पेन","Books":"पुस्तके","Cupcakes":"कपकेक","Donuts":"डोनट्स","Lanterns":"कंदील","Toys":"खेळणी"}

        if version == '1':
            extracted_objects = obj_extractor
            num_01 = extracted_objects['numbers'][0]
            num_02 = extracted_objects['numbers'][1]
            object = extracted_objects['objects'][0]
            ques = f"""There are some {object} in the basket.एका टोपलीत काही {marathi_obj_dict[object]} आहेत. Some {object} were given away and are shown as crossed {object}. त्यातील काही {marathi_obj_dict[object]} दिले गेले. दिलेल्या {marathi_obj_dict[object]} तिरपी रेष मारून खोडलेल्या दाखविल्या आहेत. How many {object} are remaining? आता किती {marathi_obj_dict[object]} शिल्लक आहेत"""

            text_exp ={
                0 : {
                        "commentary" : f"There are some {object} in the basket.एका टोपलीत काही {marathi_obj_dict[object]} आहेत.",
                    },
                1 : {
                        "commentary" : f"some of them were given away and are shown as crossed {object}.त्यातील काही {marathi_obj_dict[object]} दिले गेले. दिलेल्या {marathi_obj_dict[object]} तिरपी रेष मारून खोडलेल्या दाखविल्या आहेत.",
                    },     
                2 : {
                        "commentary" : f"Let us understand the meaning of this action.आपण या कृतीचा अर्थ समजावून घेऊ",
                    },  
                3 : {
                        "commentary" : f"Of the given quantity, when something is removed, taken away, broken, something is eaten, damaged, given away, lost, used, consumed, etc. we know that all such processes reduce the original quantity.असलेल्या गोष्टींपैकी काही गोष्टी काढून घेतल्या, तुटल्या, खाल्ल्या, खराब झाल्या, देऊन टाकल्या, हरवल्या, वापरल्या गेल्या, पडल्या, ई. अशा सर्व वेळी असलेल्या वस्तूंची संख्या आधीच्या पेक्षा कमी होते.",
                    },        
                4 : {
                        "commentary" : f"And this process is called subtraction.आणि या कमी होण्याच्या कृतीला आपण वजाबाकी असे म्हणतो.",      
                    }, 
                5 : {
                        "commentary" : f"Now the {object} which are not crossed are the  remaining {object} and we see them in the basket .Here we have removed the {object} which are already given away.आता ज्या {marathi_obj_dict[object]}वर तिरपी रेषा मारून खोडलेल्या नाहीत अशा {marathi_obj_dict[object]} शिल्लक राहिलेल्या आहेत. आणि फक्त तेवढ्या {marathi_obj_dict[object]} आपल्याला चित्रात दिसत आहेत. येथे आपण दिलेल्या गोळ्या चित्रातून काढून टाकल्या आहेत",      
                    }, 
                6 : {
                        "commentary" : f" Now let us count the remaining {object}.आता आपण उरलेल्या {marathi_obj_dict[object]} मोजू. ",      
                    }, 
                7 : {
                        "commentary" : f"Therefore the remaining {object} are {answer} is the answer.म्हणून उरलेल्या {marathi_obj_dict[object]} {answer} आहेत हे उत्तर. ",      
                    },                               
            } 

        if version == '2':
            extracted_objects = obj_extractor
            num_01 = extracted_objects['numbers'][0]
            num_02 = extracted_objects['numbers'][1]
            object = extracted_objects['objects'][0]
            # first_name = extracted_objects['names'][0]
            first_name = 'Malati'

            ques = f"There are {num_01} {object} in the basket.एका टोपलीत {num_01} {marathi_obj_dict[object]} आहेत.{first_name} took {num_02} {object} from it.मालतीने त्यातून {num_02} {marathi_obj_dict[object]} घेतली. How many {object} are remaining? किती {marathi_obj_dict[object]} शिल्लक आहेत?"

            text_exp ={
                0 : {
                        "commentary" : f"We can see that there are some {object} in the basket and they are {num_01} {object}.आपल्याला हे दिसते आहे की टोपलीत {num_01} {marathi_obj_dict[object]} आहेत ",
                    },
                1 : {
                        "commentary" : f"{first_name}  took {num_02} {object} from this basket.मालतीने त्या टोपलीतून {num_02} {marathi_obj_dict[object]} घेतली",
                    },  
                2 : {
                        "commentary" : f"To find the remaining {object} we need to take out {num_02} {object} from {num_01} {object}.उरलेली {marathi_obj_dict[object]} किती हे शोधण्यासाठी आपल्याला {num_01} मधून {num_02} {marathi_obj_dict[object]} काढून घ्यावी लागतील.",
                    },        
                3 : {
                        "commentary" : f"{num_02} {object} are taken away.{num_02} {marathi_obj_dict[object]} काढून घेतली",      
                    }, 
                4 : {
                        "commentary" : f"Now we see the remaining {object} in the basket.आता आपण पाहू शकतो की टोपलीत उरलेली {marathi_obj_dict[object]} दिसत आहेत",      
                    }, 
                5 : {
                        "commentary" : f"Let us understand the meaning of this action. We are removing {object} from the basket. Thus the {object} remaining in the basket are getting reduced. Taking out something, giving away, being used, being consumed, separating out, being damaged, being eaten, being thrown away etc. all such similar actions decreases the original quantity.This is called subtraction. आता आपण या कृतीचा अर्थ समजावून घेऊया.आपण टोपलीतून {marathi_obj_dict[object]} काढून घेत आहोत. म्हणून टोपलीत उरलेली {marathi_obj_dict[object]} कमी होत आहेत.काहीतरी काढून घेणे, देऊन टाकणे, देणे, वापरणे, संपवणे, बाजूला काढणे, वेगळे करणे, खराब होणे, नादुरुस्त होणे, खाऊन टाकणे, फेकून देणे, ई. आणि या सारख्या इतर सर्व कृतीमधून मूळ असलेल्या वस्तूंची संख्या कमी होत असते.या सारख्या कृतींना वजाबाकी असे म्हणतात ",      
                    }, 
                6 : {
                        "commentary" : f"Now let us count the remaining {object} in the basket one by one.आता टोपली मधील उरलेली सगळी {marathi_obj_dict[object]} एक एक करून मोजू. ",      
                    }, 
                7 : {
                        "commentary" : f"Remaining {object} are {answer} is the answer.उरलेली {marathi_obj_dict[object]} {answer} आहेत हे उत्तर",      
                    },    
                8: {
                        "commentary" : f"Mathematically this is represented as {num_01} - {num_02} = {answer}.गणिती भाषेत हे {num_01} - {num_02} = {answer} असे दाखविले जाते.",      
                    },  
                9: {
                        "commentary" : f"This sign is called minus and it represents the process of subtraction, or we simply call it as subtraction.या - चिन्हाला वजा असे म्हणतात आणि या क्रियेला वजाबाकी करणे अथवा वजाबाकी असे म्हणतात ",      
                    },                               
            } 
        if version == '3':
            extracted_objects = obj_extractor
            num_01 = extracted_objects['numbers'][0]
            num_02 = extracted_objects['numbers'][1]
            object = extracted_objects['objects'][0]
            

            ques = f"{num_01} - {num_02} = ?"

            text_exp ={
                0 : {
                        "commentary" : f"We are asked to find {num_01} - {num_02} = ?.Here minus sign indicates subtraction.आपल्याला येथे {num_01} - {num_02} = ? हे शोधायचे आहे.येथे, (-) हे चिन्ह वजाबाकी करायची आहे, असे दाखविते",
                    },
                1 : {
                        "commentary" : f"We are already aware, that when something is being taken out, giving away, being used, being consumed, separated out, being damaged, being eaten, being thrown away and such similar actions leads to process of Subtraction.आपल्याला हे माहिती आहे की, जेव्हा कशातून तरी काही तरी काढून घेतले जाते, दिले जाते, वापरले जाते, संपवले जाते, वेगळे केले जाते, नादुरुस्त होते, खाल्ले जाते, टाकून दिले जाते किंवा अशाच प्रकारे मूळ वस्तूंची संख्या कमी होते, अशा क्रियेला वजाबाकीची क्रिया असे म्हणतात",
                    },  
                2 : {
                        "commentary" : f"Here in all these actions, remaining quantity is always less than the original quantity and original quantity gets reduced.येथे या सर्व घटनांमध्ये शिल्लक राहिलेल्या वस्तूंची संख्या मूळ वस्तूंच्या संख्येपेक्षा कमी होत असते.",
                    },        
                3 : {
                        "commentary" : f"This is a Subtraction problem.To find the answer for this we need to subtract {num_02} from {num_01}. This is same as taking out {num_02} things from {num_01} things and then count remaining to get the answer.हे वजाबाकीची गणित आहे.याचे उत्तर शोधण्यासाठी आपल्याला {num_01} मधून {num_02} वजा करायला लागेल म्हणजेच आपल्याला {num_01} मधून {num_02} वस्तू काढून टाकाव्या लागतील आणि उरलेल्या वस्तू मोजाव्या लागतील.म्हणजे आपल्याला हवे असलेले उत्तर मिळेल ",      
                    }, 
                4 : {
                        "commentary" : f"For example, Let Radhika has {num_01} {object} in the basket.उदाहरणार्थ राधिकाकडे टोपलीत {num_01} {marathi_obj_dict[object]} आहेत असे मानू",      
                    }, 
                5 : {
                        "commentary" : f" Rosy took out {num_02} {object} from the basket for herself. To find the remaining {object}, let us take away {num_02} {object} from {num_01} {object}.रोजीने त्यातून स्वतःसाठी {num_02} {marathi_obj_dict[object]} काढून घेतली.आता किती {marathi_obj_dict[object]} उरली हे शोधण्यासाठी आपण,{num_01} {marathi_obj_dict[object]} मधून {num_02} {marathi_obj_dict[object]} काढून घेऊ. ",      
                    }, 
                6 : {
                        "commentary" : f"After removing {num_02} {object}, the remaining {object} in the basket will be the answer. So, let us count these remaining {object}.{num_02} {marathi_obj_dict[object]} काढून घेतल्यानंतर जी उरलेली {marathi_obj_dict[object]} आहेत, तेच आपले उत्तर असेल.म्हणून, आता उरलेली {marathi_obj_dict[object]} मोजुया",      
                    },
                7 : {
                        "commentary" : f"Therefore the remaining {object} are {answer} is the answer.उरलेली {marathi_obj_dict[object]} = {answer} हे उत्तर  "
                    },                                   
            } 

        if version == '4':
            extracted_objects = obj_extractor
            num_01 = extracted_objects['numbers'][0]
            num_02 = extracted_objects['numbers'][1]
            object = extracted_objects['objects'][0]
            first_name = extracted_objects['names'][0]

            ques = f"One shop has {num_01} {object}. Out of those {num_02} {object} were sold. How many {object} are left in the shop?.एका दुकानात {num_01} {marathi_obj_dict[object]} आहे. त्यापैकी {num_02} {marathi_obj_dict[object]} विकले गेले. दुकानात किती {marathi_obj_dict[object]} शिल्लक आहेत?."

            text_exp ={
                0 : {
                        "commentary" : f"There are {num_01} {object}.दुकानात {num_01} {marathi_obj_dict[object]} आहेत.",
                    },
                1 : {
                        "commentary" : f"Out of these {num_01} {object}, {num_02} were sold.{num_01} {marathi_obj_dict[object]} पैकी, {num_02} विकले गेले.",
                    },  
                2 : {
                        "commentary" : f"To find remaining {object}, we need to remove those {object} which were sold.बाकी {marathi_obj_dict[object]} शोधण्यासाठी, आम्हाला ते {marathi_obj_dict[object]} काढून टाकणे आवश्यक आहे जे विकले गेले होते.",
                    },        
                3 : {
                        "commentary" : f"We will cross the {num_02} sold {object}.आम्ही विकलेला {num_02} {marathi_obj_dict[object]}वर फुलीची खूण करू .",      
                    }, 
                4 : {
                        "commentary" : f"As we have crossed the {num_02} sold {object}, this is a subtraction.आपण {num_02} {marathi_obj_dict[object]} फुलीची खूण केली याचा अर्थ हे वजाबाकीचे गणित आहे.Thus it is a subtraction of {num_02} from {num_01} and is shown as {num_01} - {num_02} = ?.अशा प्रकारे हे {num_01} मधून {num_02} ची वजाबाकी आहे.आणि {num_01} - {num_02} = ? म्हणून दर्शविले आहे. To find the remaining {object}, we can count the number of {object} which are not crossed.बाकी {marathi_obj_dict[object]} शोधण्यासाठी, आपण ज्या {marathi_obj_dict[object]}वर फुलीची खूण केलेली नाही, अशा {marathi_obj_dict[object]} मोजू. ",      
                    }, 
                5 : {
                        "commentary" : f"There are 2 methods by which this can be done.हे शोधण्यासाठी आपण दोन पद्धती वापरू शकतो ",      
                    }, 
                6 : {
                        "commentary" : f"Method 1: To find the remaining {object}, we can count the number of {object} which are not crossed.बाकी {marathi_obj_dict[object]} शोधण्यासाठी,चित्रात ज्या {marathi_obj_dict[object]} फुली मारलेली नाही अशा सर्व {marathi_obj_dict[object]} मोजू.And they come out to be {answer}.त्या मोजल्या असता {answer} एवढ्या आहेत.",
                    },
                7: {
                    "commentary": f"Therefore there are {answer} remaining {object}  and mathematically it can be written as, {num_01}   -   {num_02}   =   {answer} is the answer.म्हणजेच बाकी अशा त्या एकूण {answer} {marathi_obj_dict[object]} आहेत.आणि हे लिहिण्याची पद्धत {num_01} - {num_02} = {answer} अशी आहे.",
                },
                8: {
                        "commentary" : f"Method 2: Out of {num_01} {object}, it is given that {num_02} were sold.{num_01} {marathi_obj_dict[object]} पैकी, {num_02} विकले गेले असे दिले आहे.It means we still have some {object} left.याचा अर्थ आमच्याकडे अजून काही {marathi_obj_dict[object]} शिल्लक आहेत.So, we will start counting only non-crossed from {num_02} onwards till we count all.म्हणून, आपण फक्त बाकी सर्व {marathi_obj_dict[object]} मोजू ",
                    },
                9: {
                        "commentary" : f"Therefore there are {answer} {object} remained in the shop, is the answer.म्हणजे दुकानात {answer} {marathi_obj_dict[object]} शिल्लक आहेत, हे उत्तर आहे",      
                    },  
                10: {
                        "commentary" : f" It can be written mathematically as, {num_01}   -   {num_02}   =   {answer} is the answer.गणिती भाषेत हे खालील प्रमाणे लिहिता येते, {num_01} - {num_02} = {answer} हे उत्तर .",      
                    },                               
            } 
        if version == '5':
            extracted_objects = obj_extractor
            num_01 = extracted_objects['numbers'][0]
            num_02 = extracted_objects['numbers'][1]
            object = extracted_objects['objects'][0]
            

            ques = f"{num_01} - {num_02} = ?"

            text_exp ={
                0 : {
                        "commentary" : f"The minus Sign between {num_01} and {num_02} indicates that this is a subtraction problem.",
                        "commentary_marathi" : f"The minus Sign between {num_01} and {num_02} indicates that this is a subtraction problem.{num_01} आणि {num_02} मधील - हे चिन्ह, ही वजाबाकी आहे हे दाखवत आहे.",
                    },
                1 : {
                        "commentary" : f"We are asked to find out the result when {num_02} is subtracted from {num_01}.",
                        "commentary_marathi" : f"We are asked to find out the result when {num_02} is subtracted from {num_01}.या गणितात, जेव्हा {num_01} मधून {num_02} वजा करतो तेव्हा उत्तर (वजाबाकी) किती येते हे विचारले आहे.",
                    },  
                2 : {
                        "commentary" : f"Subtraction is an action which reduces, removes, decreases the original number.",
                        "commentary_marathi" : f"Subtraction is an action which reduces, removes, decreases the original number.वजाबाकी ही अशी क्रिया आहे की ज्यात मूळ संख्या ही आधीच्या पेक्षा कमी होते.",
                    
                    },        
                3 : {
                        "commentary" : f"Thus, we will remove {num_02} from {num_01}. By doing this {num_01} will get decreased by {num_02}.", 
                        "commentary_marathi" : f"Thus, we will remove {num_02} from {num_01}. By doing this {num_01} will get decreased by {num_02}.त्या नुसार आपण {num_01} मधून {num_02} कमी करणार आहोत.हे केल्याने {num_01} ही संख्या {num_02} ने कमी होईल.",      
                         
                    }, 
                4 : {
                        "commentary" : f"We have {num_01} numbers, say from 1 to {num_01} as {', '.join([str(num) for num in range(1, int(num_01))]) + ' and ' + str(num_01)} and {num_02} are to be removed from them.",
                        "commentary_marathi" : f"We have {num_01} numbers, say from 1 to {num_01} as {', '.join([str(num) for num in range(1, int(num_01))]) + ' and ' + str(num_01)} and {num_02} are to be removed from them.आपल्याकडे पुढे लिहिल्या प्रमाणे 1 ते {num_01} अशा {num_01} संख्या आहेत  {', '.join([str(num) for num in range(1, int(num_01))]) + ' आणि ' + str(num_01)}  आणि यातून {num_02} कमी करायचे आहेत.",             
                    }, 
                5 : {
                        "commentary" : f"It can be done in two ways. We can remove first {num_02} numbers beginning from 1 or last {num_02} numbers ending with {num_01}.",
                        "commentary_marathi" : f"It can be done in two ways. We can remove first {num_02} numbers beginning from 1 or last {num_02} numbers ending with {num_01}.हे 2 प्रकारे करता येते. आपण १ पासून सुरु करून पहिल्या {num_02} आकडे कमी करू शकतो किंवा {num_01} पाशी संपणारे शेवटचे {num_02} आकडे कमी करू शकतो.",      
                          
                    }, 
                6 : {
                        "commentary" : f"Method 1 is removing {num_02} numbers beginning from 1", 
                        "commentary_marathi" : f"Method 1 is removing {num_02} numbers beginning from 1.पद्धत 1 खाली दाखविल्या प्रमाणे १ पासून सुरु करून पहिल्या {num_02} संख्या काढून टाकणे",     
                    },
                7 : {
                        "commentary" : f"We have removed first {num_02} numbers. That is {','.join([str(num) for num in range(1,int(num_02))])+ ' and ' + str(num_02)}.",
                        "commentary_marathi" : f"We have removed first {num_02} numbers. That is {','.join([str(num) for num in range(1,int(num_02))])+ ' and ' + str(num_02)}.आपण {','.join([str(num) for num in range(1,int(num_02))])+ ' आणि ' + str(num_02)} असे पहिल्या {num_02} संख्या काढून टाकल्या आहेत "
                    
                    },
                8 : {
                        "commentary" : f"Now remaining numbers are ",
                        "commentary_marathi" : f"Now remaining numbers are.आता उरलेले आकडे असे आहेत."
                    },
                9 : {
                        "commentary" : f"Let us count the remaining numbers as",
                        "commentary_marathi" : f"Let us count the remaining numbers as,आता आपण उरलेल्या संख्या मोजुया"
                    },
                10 : {
                        "commentary" : f"So, from {int(num_02)+1} to {num_01} we can see that {answer} numbers are remaining and we get the answer as {answer} and is written as {num_01} minus {num_02} equals {answer}",
                        "commentary_marathi" : f"So, from {int(num_02)+1} to {num_01} we can see that {answer} numbers are remaining and we get the answer as {answer} and is written as {num_01} minus {num_02} equals {answer}.म्हणजेच {int(num_02)+1} ते {num_01} अशा {answer} संख्या शिल्लक आहेत.म्हणजेच आपल्याला {answer} असे उत्तर मिळाले आणि ते {num_01}-{num_02}={answer} असे लिहिले जाते." 
                    },  
                11 : {
                        "commentary" : f"Method 2 is {num_01} numbers which we have, are 1 to {num_01} as {', '.join([str(num) for num in range(1, int(num_01))]) + ' and ' + str(num_01)} and last {num_02} numbers are removed ending with {num_01}",
                        "commentary_marathi" : f"Method 2 is {num_01} numbers which we have, are 1 to {num_01} as {', '.join([str(num) for num in range(1, int(num_01))]) + ' and ' + str(num_01)} and last {num_02} numbers are removed ending with {num_01}.पद्धत 2,आपल्याकडे ज्या {num_01} संख्या आहेत त्या पुढील प्रमाणे 1 ते {num_01} अशा आहेत {', '.join([str(num) for num in range(1, int(num_01))]) + ' आणि ' + str(num_01)} आणि {num_01} पाशी संपणाऱ्या शेवटच्या {num_02} संख्या खाली दाखविल्या प्रमाणे काढून टाकायच्या आहेत "
                   
                    }, 
                12 : {
                        "commentary" : f"Then remaining numbers are {','.join([str(num) for num in range(1,int(answer))])+ ' and ' + str(answer)}",
                        "commentary_marathi" : f"Then remaining numbers are {','.join([str(num) for num in range(1,int(answer))])+ ' and ' + str(answer)}.आता उरलेल्या संख्या {','.join([str(num) for num in range(1,int(answer))])+ ' आणि ' + str(answer)} या आहेत."
                    }, 
                13 : {
                        "commentary" : f"Now we will count the remaining numbers",
                        "commentary_marathi" : f"Now we will count the remaining numbers.आपण उरलेल्या संख्या मोजू."
                    }, 
                14 : {
                        "commentary" : f"We can very easily see that 1 to {answer} are {answer} numbers remaining ",
                        "commentary_marathi" : f"We can very easily see that 1 to {answer} are {answer} numbers remaining.आपल्याला हे सहजरित्या कळू शकते की 1 ते {answer} या {answer} संख्या आहेत"
                    },
                15 : {
                        "commentary" : f"We get the answer as {answer} and is written as {num_01} minus {num_02} = {answer} ",
                        "commentary_marathi" : f"We get the answer as {answer} and is written as {num_01} minus {num_02} = {answer}.आपल्याला {answer} असे उत्तर मिळते आणि ते आपण {num_01} - {num_02} = {answer} असे लिहितो."
                    },                                                                    
            }  

        return ques,text_exp     
    
    if question_type == "multiplication":
        object = obj_extractor["objects"][0]
        num_01 = int(obj_extractor['numbers'][0])
        num_02 = int(obj_extractor['numbers'][1])

        number_word_list = ["first","second","third","fourth","fifth","sixth","Seventh","Eighth","Ninth","Tenth"]
        Dict = dict()
        num_list = list()
        for i in range(num_01):
                if i == 0:
                    num_list.append(str(num_02))
                else:    
                    num_list.append(f"+{num_02}")     

        for i in range(4):
            
            if i == 0 :
                Dict[i] = {"commentary":"The result of multiplication can be obtained by repeatative addition."}
            if i == 1 :
                Dict[i] = {"commentary":f"Each {object} costs {num_02} rupees .To find total cost we have to add {num_02}, {num_01} times ."} 
            if i == 2:
                Dict[i] = {"commentary":f"The total cost now is {''.join(num_list)} = {answer} "}
            if i == 3:
                Dict[i] = {"commentary":f"So, the total cost of all {object} is {answer} ruppees"}
                text_exp = Dict  

    if question_type == "division":
        object = obj_extractor["objects"][0]
        num_01 = int(obj_extractor['numbers'][0])
        num_02 = int(obj_extractor['numbers'][1])

        text_exp = dict()
        for i in range(3):
            if i == 0 :
                text_exp[i] = {"commentary":",The result of Division can be obtained by repeatative Subtraction and is represented by '%' sign"}
            if i == 1 :
                text_exp[i] = {"commentary":f"We shall make set of {num_02} {object}, and repeatedly, move it to the second mat, untill there remains 0 {object} on first mat"}
            else: 
                pass     
                                         
    return text_exp


def subs():
    """
    helper function for subtraction, it generate and returns the operands needed in subtraction.

    Output_param :
        Subtrahend : the number being subtracted
        Minuend    : the number from which we will subtract
    """
    Subtrahend  = random.randint(2,5)
    Minuend  = random.randint(6,10)
    return Subtrahend ,Minuend 

def division():
    """
    helper function for division, it generate and returns the operands needed in division.

    Output_param:
        Divisor  : Divisor
        Dividend : Divident
    """
    lst = [6,8,9,10,12,15,16,18,20,21,24,25]
    Dividend = random.choice(lst)
    while True:
        Divisor = random.randint(2,7)
        
        if Dividend%Divisor == 0:
            return Divisor,Dividend

def random_question_generator_add():
    """
    generating a random addition question by replacing its original numbers, objects and names

    Output_param: 
        text : generated addition question
        sum(lst) : answer of the addtion question
    """
    names_list = ["Anil","Sunil","Shyam","Ronit","Vinshnu","Fahad","Nitin","Josh","Rahul","Amit"]
    objects_list = ["Apples","Oranges","Bats","Balls","Pens","Books","Cupcakes","Donuts","Lanterns","Toys"]
  
    text = Add_question
    
    doc = nlp(Add_question)

    for token in doc:
        if token.pos_ == "PROPN":
            text = re.sub(token.text, names_list[random.randint(0,len(names_list)-1)], text)
        elif token.pos_ == "NUM": 
            text = re.sub(token.text, str(random.randint(2,8)), text)  
        elif token.pos_ == "NOUN" and token.dep_ == "dobj" :
            text = re.sub(token.text, objects_list[random.randint(0,len(objects_list)-1)], text) 
        else:
            pass   
    
    doc = nlp(text)
    lst = []
    for token in doc:
        if token.pos_ == "NUM":
            num = str(token)
            num = int(num)
            lst.append(num)   
    #multiplication = reduce((lambda x, y: x * y), lst)
    return text, sum(lst)

def random_question_generator_multi():
    """
    generating a random multiplication question by replacing its original numbers, objects and names

    Output_param: 
        text : generated multiplication question
        multiplication : answer of the multiplication question
    """
    names_list = ["Anil","Sunil","Shyam","Ronit","Vinshnu","Fahad","Nitin","Josh","Rahul","Amit"]
    objects_list = ["Apples","Oranges","Bats","Balls","Pens","Books","Cupcakes","Donuts","Lanterns","Toys"]
    text = Multi_question
    
    doc = nlp(Multi_question)

    for token in doc:
        if token.pos_ == "PROPN":
            text = re.sub(token.text, names_list[random.randint(0,len(names_list)-1)], text)
        elif token.pos_ == "NUM": 
            text = re.sub(token.text, str(random.randint(1,8)), text)  
        elif token.pos_ == "NOUN" and token.dep_ == "dobj" :
            text = re.sub(token.text, objects_list[random.randint(0,len(objects_list)-1)], text) 
        else:
            pass   
    
    doc = nlp(text)
    lst = []
    for token in doc:
        if token.pos_ == "NUM":
            num = str(token)
            num = int(num)
            lst.append(num)   
    multiplication = reduce((lambda x, y: x * y), lst)
    return text, multiplication  

def random_question_generator_subtract():
    """
    generating a random subtraction question by replacing its original numbers, objects and names

    Output_param: 
        text : generated subtraction question
        difference : answer of the subtraction question
    """
    names_list = ["Anil","Sunil","Shyam","Ronit","Vinshnu","Fahad","Nitin","Josh","Rahul","Amit"]
    objects_list = ["Apples","Oranges","Bats","Balls","Pens","Books","Cupcakes","Donuts","Lanterns","Toys"]
    text = Sub_question
    
    doc = nlp(Sub_question)
    Subtrahend , Minuend = subs()

    text = text.replace("27", str(Minuend)) 
    text = text.replace("5", str(Subtrahend)) 

    for token in doc:
        if token.pos_ == "PROPN":
            text = re.sub(token.text, names_list[random.randint(0,len(names_list)-1)], text)
        elif token.pos_ == "NOUN" and token.dep_ == "dobj" :
            text = re.sub(token.text, objects_list[random.randint(0,len(objects_list)-1)], text) 
        else:
            pass 

    difference = Minuend - Subtrahend   
    return text , difference

def random_question_generator_divide():
    """
    generating a random division question by replacing its original numbers, objects and names

    Output_param: 
        text : generated division question
        quotient : answer of the division question
    """
    names_list = ["Anil","Sunil","Shyam","Ronit","Vinshnu","Fahad","Nitin","Josh","Rahul","Amit"]
    # objects_list = ["Apples","Oranges","Bats","Balls","Pens","Books","Bears","Cupcakes","Donuts","Lanterns","Toys","Ducks"]
    objects_list = ["Apples","Oranges","Bats","Balls","Pens","Books","Cupcakes","Donuts","Lanterns","Toys"]
    text = Div_question
    
    Divisor, Dividend = division()
    #print(Dividend,Divisor)
    text = text.replace("9", str(Dividend)) 
    text = text.replace("3", str(Divisor))
    text = text.replace("Anand", names_list[random.randint(0,len(names_list)-1)]) 
    text = text.replace("stickers", objects_list[random.randint(0,len(objects_list)-1)])
    quotient = Dividend/Divisor  
    #print(quotient)
    return text, quotient

def question(question_type, question_number ):
    """
    generating question of given type 

    Input_param :
        question_type: operation of the question (i.e addition or subtraction)
        question_number: needed number of question

    Output_param: 
        lst_ : list contaiing info of question, answer and objects
    """
    if question_type == "addition":
        lst_add = []
        for i  in range(question_number):
            question_add = {}
            text, addition = random_question_generator_add()
            obj_extractor = numbers_and_object_extracor(text)
            question_add.update({'Question':text})
            question_add.update({'Answer':addition})
            
            question_add.update({'Objects':obj_extractor})
            lst_add.append(question_add)
        return lst_add
    elif question_type == "multiplication":
        lst_multi = []
        for i  in range(question_number):
            question_multi = {}
            text, multiplication = random_question_generator_multi()
            question_multi.update({'Question':text})
            question_multi.update({'Answer':multiplication})
            obj_extractor = numbers_and_object_extracor(text)
            question_multi.update({'Objects':obj_extractor})
            lst_multi.append(question_multi)
           
        return lst_multi
    elif question_type == "subtraction":
        lst_sub = []
        for i  in range(question_number):
            question_sub = {}
            text, difference = random_question_generator_subtract()
            question_sub.update({'Question':text})
            question_sub.update({'Answer':difference})
            obj_extractor = numbers_and_object_extracor(text)
            question_sub.update({'Objects':obj_extractor})
            lst_sub.append(question_sub)
            
        return lst_sub
    elif question_type == "division":
        lst_div = []
        for i  in range(question_number):
            question_div = {}
            text, quotient = random_question_generator_divide()
            quotient = int(quotient)
            question_div.update({'Question':text})
            question_div.update({'Answer':quotient})
            obj_extractor = numbers_and_object_extracor(text)
            question_div.update({'Objects':obj_extractor})
            lst_div.append(question_div)
            
        return lst_div

def question_with_text_exp(question_type, question_number, version = None ):
    """
    generating question along with their explanation of given type 

    Input_param :
        question_type: operation of the question (i.e addition or subtraction)
        question_number: needed number of question
        version : version of the question

    Output_param: 
        lst_ : list contaiing info of question, answer and objects, question_type, version and text_explanation
    """
    if question_type == "addition":
        lst_add = []
        for i  in range(question_number):
            question_add = {}
            text, addition = random_question_generator_add()
            obj_extractor = numbers_and_object_extracor(text)
            ques,txt_explanation = text_explanation(addition,question_type,obj_extractor,version)
            question_add.update({'Question':ques})
            question_add.update({'Answer':addition})
            question_add.update({'Version':version})
            question_add.update({'question_type':question_type})
            question_add.update({'Objects':obj_extractor})
            question_add.update({'Text_Explanation':txt_explanation})
            lst_add.append(question_add)
        return lst_add
    
    elif question_type == "subtraction":
        lst_sub = []
        for i  in range(question_number):
            question_sub = {}
            text, difference = random_question_generator_subtract()
            obj_extractor = numbers_and_object_extracor(text)
            ques,txt_explanation = text_explanation(difference,question_type,obj_extractor,version)
            question_sub.update({'Question':ques})
            question_sub.update({'Answer':difference})
            question_sub.update({'Version':version})
            question_sub.update({'question_type':question_type})
            question_sub.update({'Objects':obj_extractor})
            question_sub.update({'Text_Explanation':txt_explanation})
            lst_sub.append(question_sub)  
        return lst_sub
    
    elif question_type == "multiplication":
        lst_multi = []
        for i  in range(question_number):
            question_multi = {}
            text, multiplication = random_question_generator_multi()
            question_multi.update({'Question':text})
            question_multi.update({'Answer':multiplication})
            obj_extractor = numbers_and_object_extracor(text)
            question_multi.update({'Objects':obj_extractor})
            txt_explanation = text_explanation(multiplication,question_type,obj_extractor)
            question_multi.update({'Text_Explanation':txt_explanation})
            lst_multi.append(question_multi)
            
        return lst_multi
    
    elif question_type == "division":
        lst_div = []
        for i  in range(question_number):
            question_div = {}
            text, quotient = random_question_generator_divide()
            quotient = int(quotient)
            question_div.update({'Question':text})
            question_div.update({'Answer':quotient})
            obj_extractor = numbers_and_object_extracor(text)
            question_div.update({'Objects':obj_extractor})
            txt_explanation = text_explanation(quotient,question_type,obj_extractor)
            question_div.update({'Text_Explanation':txt_explanation})
            lst_div.append(question_div)
        return lst_div

############################################## Fahads Code-end #######################

################################################ number_and_object_extractor ###########
def numbers_and_object_extracor(question):
    """
    Given a question, extracting its numbers, names and objects

    Input_param : 
        question : input question in a form of sentence

    Output_param : 
        dicts : a dictionary containing information about numbers, names and objects within the question.    
    """
    doc = nlp(question)

    num_list = []
    object_list = []
    name_list = []
    dicts = {}

    for token in doc:
        
        if token.pos_ == "NUM": 
            num_list.append(token.text)  
        elif (token.pos_ == "PROPN" and token.dep_ == "dobj") or (token.pos_ == "NOUN" and token.dep_ == "dobj"):
            object_list.append(token.text) 
        elif (token.pos_ == "PROPN" and token.dep_ == "nsubj") or (token.pos_ == "PROPN" and token.dep_ == "pobj"):
            name_list.append(token.text)    
        else:
            pass  

    dicts['numbers'] = num_list
    dicts['objects'] = object_list 
    dicts['names'] = name_list  

    return dicts     
################################################ number_and_object_extractor-end #######

################################ Fraction_Section_Functions ################################
def fraction_question( ):
    question_set = {
        1:
        {
            1:{"question":"What fraction of people have Green hats?","option_01":"3/15","option_02":"1/5","option_03":"4/15","option_04":"3/16","ans":"3/15"},
            2:{"question":"What fraction of people have Red hats?","option_01":"3/15","option_02":"4/15","option_03":"5/15","option_04":"3/16","ans":"4/15"},
            3:{"question":"What fraction of people have Blue hats?","option_01":"4/15","option_02":"1/5","option_03":"4/16","option_04":"3/15","ans":"3/15"},
            4:{"question":"What fraction of people have Yellow hats?","option_01":"3/15","option_02":"1/5","option_03":"4/15","option_04":"3/16","ans":"3/15"},
            5:{"question":"What fraction of people have Black hats?","option_01":"3/15","option_02":"1/5","option_03":"2/15","option_04":"3/16","ans":"2/15"},
        },
        2:
        {
            1:{"question":"What fraction of people have Green hats?","option_01":"3/15","option_02":"1/5","option_03":"4/15","option_04":"None","ans":"None"},
            2:{"question":"What fraction of people have Red hats?","option_01":"3/15","option_02":"2/12","option_03":"5/15","option_04":"3/16","ans":"2/12"},
            3:{"question":"What fraction of people have Blue hats?","option_01":"4/15","option_02":"1/5","option_03":"5/12","option_04":"3/15","ans":"5/12"},
            4:{"question":"What fraction of people have Yellow hats?","option_01":"3/15","option_02":"1/5","option_03":"4/12","option_04":"3/16","ans":"4/12"},
            5:{"question":"What fraction of people have Orange hats?","option_01":"3/15","option_02":"1/12","option_03":"2/15","option_04":"3/16","ans":"2/15"},
        },
        3:
        {
            1:{"question":"What fraction of people have Green hats?","option_01":"3/13","option_02":"1/5","option_03":"4/13","option_04":"3/16","ans":"4/13"},
            2:{"question":"What fraction of people have Red hats?","option_01":"3/13","option_02":"1/13","option_03":"5/15","option_04":"3/16","ans":"1/13"},
            3:{"question":"What fraction of people have Blue hats?","option_01":"4/15","option_02":"4/13","option_03":"4/16","option_04":"3/15","ans":"4/13"},
            4:{"question":"What fraction of people have Yellow hats?","option_01":"1/13","option_02":"1/5","option_03":"4/13","option_04":"3/16","ans":"1/13"},
            5:{"question":"What fraction of people have Black hats?","option_01":"3/13","option_02":"1/5","option_03":"1/13","option_04":"3/16","ans":"1/13"},
        },
        4:
        {
            1:{"question":"What fraction of people have Green hats?","option_01":"3/14","option_02":"6/14","option_03":"4/14","option_04":"3/16","ans":"3/14"},
            2:{"question":"What fraction of people have Red hats?","option_01":"1/14","option_02":"1/13","option_03":"5/15","option_04":"3/16","ans":"1/14"},
            3:{"question":"What fraction of people have Blue hats?","option_01":"4/15","option_02":"6/14","option_03":"4/16","option_04":"3/15","ans":"6/14"},
            4:{"question":"What fraction of people have Yellow hats?","option_01":"1/13","option_02":"1/5","option_03":"2/14","option_04":"3/16","ans":"2/14"},
            5:{"question":"What fraction of people have Purple hats?","option_01":"2/14","option_02":"1/5","option_03":"1/13","option_04":"3/16","ans":"2/14"},
        }, }

    random_image = random.randint(1,4) 
    random_question = random.randint(1,5)    

    output_dict = {
        "image": random_image,
        "question":question_set[random_image][random_question],

    }
    return output_dict
################################ Fraction_Section_Functions_end ################################

################################# Sample_question_mahesh_sir #################################

################## Identifying shapes############################
def identify_the_shape(number):

    circle_obj = 0
    square_object = 0
    triangle_object = 0

    output_object_list = []

    object_list = ["circle","triangle","square"]

    circle = [{"object":"tire","url":"https://i.ibb.co/594FR44/tire.png","object_type":"circle"},{"object":"plate","url":"https://i.ibb.co/3mzn20R/plate.png","object_type":"circle"}]

    triangle = [{"object":"hanger","url":"https://i.ibb.co/0FKqYRM/hanger.png","object_type":"triangle"},{"object":"green_cap","url":"https://i.ibb.co/hLj6tyy/green-cap.png","object_type":"triangle"},{"object":"blue_cap","url":"https://i.ibb.co/y5hyKRX/blue-cap.png","object_type":"triangle"}]

    square = [{"object":"mobile","url":"https://i.ibb.co/rpT2J3N/mobile.png","object_type":"square"},{"object":"window","url":"https://i.ibb.co/Htp0dWx/window.png","object_type":"square"},{"object":"book","url":"https://i.ibb.co/W09pRjn/book.png","object_type":"square"}]

    for i in range(number):
        rand_num = random.randint(1,3)
        if rand_num == 1:
            circle_obj += 1
            rand_num =  random.randint(0,1)
            value = copy.copy(circle[rand_num])
            value["count"] = circle_obj
            output_object_list.append(value)
        elif rand_num == 2:
            triangle_object += 1
            rand_num =  random.randint(0,2)
            value = copy.copy(triangle[rand_num])
            value["count"] = triangle_object
            output_object_list.append(value)
        else:
            square_object += 1
            rand_num =  random.randint(0,2)
            value = copy.copy(square[rand_num])
            value["count"] = square_object
            output_object_list.append(value)

    output = {"objects":output_object_list,"answer":{"circle":circle_obj,"square":square_object,"triangle":triangle_object}}        

    return output  

@api_view(['GET'])
def identifying_shapes(request):
    try:
        num_of_ques = int(request.META.get('HTTP_NUMBERS'))
        if num_of_ques > 0 :
            dict_data = identify_the_shape(num_of_ques)
            response_obj = ResponseClass(200, "Add Successful",dict_data)
            return JsonResponse(response_obj.__dict__, status=200)
        else:
            response_obj = ResponseClass(400, "input cannot be zero")
            return JsonResponse(response_obj.__dict__, status=400)

    except KeyError as e:
            response_obj = ResponseClass(400, "no field specified")
            return JsonResponse(response_obj.__dict__, status=400) 
######################### Identifying Shapes ######################

######################### measuring angles ########################
def measuring_angle(number):
    question_list = []
    for i in range(number):
        angle_value = random.randrange(5,170,5)
        option_list = [
                        angle_value,
                        angle_value + 5,
                        angle_value - 5,
                        angle_value + 10
                      ]
        random.shuffle(option_list)
        data = {
                    "angle":angle_value,
                    "options":option_list,
               }
        question_list.append(data)
    return question_list    

@api_view(['GET'])
def measure_angle(request):
    try:
        num_of_ques = int(request.META.get('HTTP_NUMBERS'))
        if num_of_ques > 0 :
            dict_data = measuring_angle(num_of_ques)
            response_obj = ResponseClass(200, "Add Successful",dict_data)
            return JsonResponse(response_obj.__dict__, status=200)
        else:
            response_obj = ResponseClass(400, "input cannot be zero")
            return JsonResponse(response_obj.__dict__, status=400)
    except KeyError as e:
            response_obj = ResponseClass(400, "no field specified")
            return JsonResponse(response_obj.__dict__, status=400) 

######################### measuring angles ########################
def displaying_angle(number):
    question_list = []
    for i in range(number):
        angle_value = choice([i for i in range(5,75,5) if i not in [45]])
        option_list = [
                        angle_value,
                        180 - angle_value ,
                        "r "+str(180 - angle_value) ,
                        90 - angle_value
                      ]
        random.shuffle(option_list)
        data = {
                    "angle":angle_value,
                    "options":option_list,
               }
        question_list.append(data)
    return question_list  

@api_view(['GET'])
def display_angle(request):
    try:
        num_of_ques = int(request.META.get('HTTP_NUMBERS'))
        if num_of_ques > 0 :
            
            dict_data = displaying_angle(num_of_ques)
            response_obj = ResponseClass(200, "Add Successful",dict_data)
            return JsonResponse(response_obj.__dict__, status=200)
        else:
            response_obj = ResponseClass(400, "input cannot be zero")
            return JsonResponse(response_obj.__dict__, status=400)

    except KeyError as e:
            response_obj = ResponseClass(400, "no field specified")
            return JsonResponse(response_obj.__dict__, status=400) 
######################### Observing angle #########################

######################### Observing angle #########################

######################### Identifying Angles ########################
def angle_problem(number):
    question_list = []
    for i in range(number):
        obj = ["an acute angle","a complete angle","a obtuse angle","a reflex angle","a right angle","a straight angle",]
        object_list = [
    {0:{"acute_30":"https://i.ibb.co/NCc4yXm/acute-30.png"},
     1:{"acute_45":"https://i.ibb.co/W0kvMc7/acute-45.png"},
     2:{"acute_60":"https://i.ibb.co/V9JRyFg/acute-60.png"}
     },

    {0:{"complete_angle_01":"https://i.ibb.co/fMqscGL/complete-angle-01.png"},
     1:{"complete_angle_02":"https://i.ibb.co/f825TVC/complete-angle-02.png"},
     2:{"complete_angle_03":"https://i.ibb.co/DbDsJ0q/complete-angle-03.png"}
     },

    {0:{"obtuse_106":"https://i.ibb.co/pnkX6Sw/obtuse-106.png"},
     1:{"obtuse_110":"https://i.ibb.co/sjp7nnj/obtuse-110.png"},
     2:{"obtuse_120":"https://i.ibb.co/TtQ73kX/obtuse-120.png"}
     },
     
     {0:{"reflex_220":"https://i.ibb.co/0DT0tNr/reflex-220.png"},
     1:{"reflex_225":"https://i.ibb.co/tPSZy0d/reflex-225.png"},
     2:{"reflex_320":"https://i.ibb.co/gFxnxFZ/reflex-320.png"}
     },

    {0:{"rignt_angle_01":"https://i.ibb.co/TBKsBt1/rignt-angle-01.png"},
     1:{"rignt_angle_02":"https://i.ibb.co/Pr2tShZ/rignt-angle-02.png"},
     2:{"rignt_angle_03":"https://i.ibb.co/YTHNb6Q/rignt-angle-03.png"}
     },

    {0:{"straight_01":"https://i.ibb.co/0DscpnF/straight-01.png"},
     1:{"straight_02":"https://i.ibb.co/VBXnCZC/straight-02.png"},
     2:{"straight_03":"https://i.ibb.co/L6n9xqB/straight-03.png"}
     },
    ]
        rand_obj = random.randint(0,len(obj)-1)
        ques = "Which of the following is "+ obj[rand_obj]
        option = []
        answer = []
        qus_num = random.randint(0,2)
        for i in range(4):
            if i == 0:
                option.append(object_list[rand_obj][qus_num])
                answer.append(object_list[rand_obj][qus_num])
            else: 
                obj_selection = random.randint(0,len(obj)-1)
                obj_of_obj_selection = random.randint(0,2)
                if obj_selection == rand_obj:
                    option.append(object_list[rand_obj][obj_of_obj_selection])
                    answer.append(object_list[rand_obj][obj_of_obj_selection])
                else:
                    option.append(object_list[obj_selection][obj_of_obj_selection])

        random.shuffle(option)
        qus_dict = {
            "question":ques,
            "options":option,
            "answer":answer
        }
        question_list.append(qus_dict)
    return question_list

@api_view(['GET'])
def identifying_angle(request):
    try:
        num_of_ques = int(request.META.get('HTTP_NUMBERS'))
        if num_of_ques > 0 :
            dict_data = angle_problem(num_of_ques)
            response_obj = ResponseClass(200, "Add Successful",dict_data)
            return JsonResponse(response_obj.__dict__, status=200)
        else:
            response_obj = ResponseClass(400, "input cannot be zero")
            return JsonResponse(response_obj.__dict__, status=400)
    except KeyError as e:
            response_obj = ResponseClass(400, "no field specified")
            return JsonResponse(response_obj.__dict__, status=400) 

######################### Idntifying Angles #########################


######################### Naming Figures ############################
def naming_figures(numbers):
    question_list = []
    problem_list = [
    {
        "fig":"https://i.ibb.co/qR5QHrZ/fig-01.png",
        "coli_points":['MOT','RON',1],
        "rays":['OR','OM','OS','OT','ON','OP',0],
        "line_seg":['OP','ON','OT','OS','OR','OM','MT','RN',1],
        "lines":['MT','RN',1]
    },
    {
        "fig":"https://i.ibb.co/02RfmFs/fig-02.png",
        "coli_points":['XOA',1],
        "rays":['OB','OA','OE','OD','OX','OC',0],
        "line_seg":['OB','OA','OE','OD','OX','OC','XA',1],
        "lines":['XA',1]
    },
    {
        "fig":"https://i.ibb.co/0MHSCZN/fig-03.png",
        "coli_points":['BOD','AOC',1],
        "rays":['OE','OD','OC','OB','OA',0],
        "line_seg":['OE','OD','OC','OB','OA','BD','AC',1],
        "lines":['BD','AC',1]
    }]

    for num in range(numbers):
        random_question = random.randint(0,len(problem_list)-1)
        question_list.append(problem_list[random_question])
    return question_list    

@api_view(['GET'])
def naming_fig(request):
    try:
        num_of_ques = int(request.META.get('HTTP_NUMBERS'))
        if num_of_ques > 0 :
            dict_data = naming_figures(num_of_ques)
            response_obj = ResponseClass(200, "Add Successful",dict_data)
            return JsonResponse(response_obj.__dict__, status=200)
        else:
            response_obj = ResponseClass(400, "input cannot be zero")
            return JsonResponse(response_obj.__dict__, status=400)
    except KeyError as e:
            response_obj = ResponseClass(400, "no field specified")
            return JsonResponse(response_obj.__dict__, status=400)
    

def naming_figures_single_question(numbers):

    """function for naming figures into different categories"""
    question_list = []

    problem_list = [
    {
        "fig":"https://i.ibb.co/qR5QHrZ/fig-01.png",
        "coli_points":{"points":['MOT','RON'],"reverse":True},
        "rays":{"points":['OR','OM','OS','OT','ON','OP'],"reverse":False},
        "line_seg":{"points":['OP','ON','OT','OS','OR','OM','MT','RN'],"reverse":True},
        "lines":{"points":['MT','RN'],"reverse":True}
    },
    {
        "fig":"https://i.ibb.co/02RfmFs/fig-02.png",
        "coli_points":{"points":['XOA'],"reverse":True},
        "rays":{"points":['OB','OA','OE','OD','OX','OC'],"reverse":False},
        "line_seg":{"points":['OB','OA','OE','OD','OX','OC','XA'],"reverse":True},
        "lines":{"points":['XA'],"reverse":True}
    },
    {
        "fig":"https://i.ibb.co/0MHSCZN/fig-03.png",
        "coli_points":{"points":['BOD','AOC'],"reverse":True},
        "rays":{"points":['OE','OD','OC','OB','OA'],"reverse":False},
        "line_seg":{"points":['OE','OD','OC','OB','OA','BD','AC'],"reverse":True},
        "lines":{"points":['BD','AC'],"reverse":True}
    }]

    for num in range(numbers):
        random_question = random.randint(0,len(problem_list)-1)
        figure_components = ["Colinear Points", "Rays", "Line Segment","Lines"]
        key_list = ["coli_points","rays","line_seg","lines"]
        selected_fig_compnt = random.randint(0,3) 
        question = "Name "+str(figure_components[selected_fig_compnt])+" from the following figure" 
        question_dict = {
            "question": question,
            "figure": problem_list[random_question]["fig"],
            key_list[selected_fig_compnt]:problem_list[random_question][key_list[selected_fig_compnt]],
        }
        question_list.append(question_dict)
    return question_list  

@api_view(['GET'])
def naming_fig_single_ques(request):
    try:
        num_of_ques = int(request.META.get('HTTP_NUMBERS'))
        if num_of_ques > 0 :
            dict_data = naming_figures_single_question(num_of_ques)
            response_obj = ResponseClass(200, "Add Successful",dict_data)
            return JsonResponse(response_obj.__dict__, status=200)
        else:
            response_obj = ResponseClass(400, "input cannot be zero")
            return JsonResponse(response_obj.__dict__, status=400)
    except KeyError as e:
            response_obj = ResponseClass(400, "no field specified")
            return JsonResponse(response_obj.__dict__, status=400)
          

######################### Naming Figures-end ########################


################################# Sample_question_mahesh_sir #################################
@api_view(['GET'])
def convert_text_q_to_picture_q(request):
    try:
        question = request.META.get('HTTP_QUESTION')
        # question = request.data['question']
        if question:
            if text_to_picture.validate_question(question):
                img = text_to_picture.convert_text_to_pic(question)
                return img
            else:
                response_obj = ResponseClass(206, "Text is not proper")
                return JsonResponse(response_obj.__dict__, status=206)
        else:
            response_obj = ResponseClass(400, "Question can not be empty")
            return JsonResponse(response_obj.__dict__, status=400)
    except KeyError as e:
            response_obj = ResponseClass(400, "no field called question")
            return JsonResponse(response_obj.__dict__, status=400)


@api_view(['POST'])
def convert_pictorial_text_q_to_picture_q(request):
    try:
        image = request.data['image']
        question_text = text_to_picture.get_question_from_image(image)
        question_set = text_to_picture.get_all_questions(question_text)
        if question_set:
                img = text_to_picture.convert_set_of_text_to_pic(question_set)
                return img
        else:
            response_obj = ResponseClass(400, "Image does not have a question")
            return JsonResponse(response_obj.__dict__, status=400)
    except KeyError as e:
            response_obj = ResponseClass(400, "no field called image")
            return JsonResponse(response_obj.__dict__, status=400)
################################## Random_Number_Generator_Section ######################
@api_view(['GET'])
def rand_ques_generator(request):
    try:
        
        question_number  = int(request.META.get('HTTP_A'))
        question_type    = request.META.get('HTTP_TYPE')

        if question_number>0 and question_number<11 and question_type: 
            dict_data = question(question_type, question_number )
            response_obj = ResponseClass(200, "Add Successful",dict_data)
            return JsonResponse(response_obj.__dict__, status=200)
        else:
            response_obj = ResponseClass(400, "question and question type cannot be empty,or zero, or greater than 10")
            return JsonResponse(response_obj.__dict__, status=400)
    except KeyError as e:
            response_obj = ResponseClass(400, "no field called question and question_type")
            return JsonResponse(response_obj.__dict__, status=400)   


################################## Random_Number_Generator_Section ends #################

################################## Random_Number_Generator_with_text_explanation_Section ######################
@api_view(['GET'])
def rand_ques_generator_with_text_explanation(request):
    try:
        
        question_number  = int(request.META.get('HTTP_A'))
        question_type    = request.META.get('HTTP_TYPE')
        question_version = request.META.get('HTTP_VERSION')

        if question_number>0 and question_number<11 and question_type or question_version:
            dict_data = question_with_text_exp(question_type, question_number,question_version)
            response_obj = ResponseClass(200, "Add Successful",dict_data)
            return JsonResponse(response_obj.__dict__, status=200)
        else:
            response_obj = ResponseClass(400, "question and question type cannot be empty,or zero, or greater than 10")
            return JsonResponse(response_obj.__dict__, status=400)
    except KeyError as e:
            response_obj = ResponseClass(400, "no field called question and question_type")
            return JsonResponse(response_obj.__dict__, status=400)   


################################## Random_Number_Generator_with_text_explanation_Section ends #################
###################################### Count_pictures_and_add section ####################
@api_view(['GET'])
def counting_pictures(request):
    try:
        num_of_ques = int(request.META.get('HTTP_NUMBERS'))
        if num_of_ques>0 and num_of_ques<11:
            object_list =["Fish","Ball","Finger","Pen","Pencil","Rubber"]
            dict_data = [0]*num_of_ques
            for i in range(num_of_ques):
                num_01 = random.randint(1,10)
                num_02 = random.randint(1,10)
                object_num = random.randint(0,5)
                object = object_list[object_num]
                ans = num_01 + num_02
                dicct = {
                    "object":object,
                    "count":[num_01,num_02],
                    "answer":ans
                }
                dict_data[i] = dicct
            response_obj = ResponseClass(200, "Add Successful",dict_data)
            return JsonResponse(response_obj.__dict__, status=200)
        else:
            response_obj = ResponseClass(400, "input cannot be zero, or greater than 10")
            return JsonResponse(response_obj.__dict__, status=400)
    except KeyError as e:
            response_obj = ResponseClass(400, "no field for number")
            return JsonResponse(response_obj.__dict__, status=400)   

################################ Count_pictures_and_add_section end ######################

#################################### Fraction_Section ###################################
@api_view(['GET'])
def fraction_question_generator(request):
    try:
        num_of_ques = int(request.META.get('HTTP_NUMBERS'))
        if num_of_ques > 0 and num_of_ques <11:
            dict_data = {}
            for i in range(num_of_ques):
                fraction_output = fraction_question()
                dict_data[i] = fraction_output

            response_obj = ResponseClass(200, "Add Successful",dict_data)
            return JsonResponse(response_obj.__dict__, status=200)
        else:
            response_obj = ResponseClass(400, "input cannot be zero, or greater than 10")
            return JsonResponse(response_obj.__dict__, status=400)
    except KeyError as e:
            response_obj = ResponseClass(400, "no field specified")
            return JsonResponse(response_obj.__dict__, status=400) 

##################################### Fraction_Section_end ##############################

############################### API for generating qustions objects,numbers and operations #
@api_view(['GET'])
def obtaining_objects(request):
    try:
        question = str(request.META.get('HTTP_QUESTION'))
        if question:
            if text_to_picture.validate_question(question):
                operation = text_to_picture.find_operation(question)
                numbers =  text_to_picture.find_numbers(question)
                subjects =  text_to_picture.find_subject(question)
                dicct = {
                    "Question":question,
                    "Operation":operation,
                    "numbers":numbers,
                    "objects":subjects
                }
                response_obj = ResponseClass(200, "Add Successful",dicct)
                return JsonResponse(response_obj.__dict__, status=200)
            else:
                response_obj = ResponseClass(206, "Text is not proper")
                return JsonResponse(response_obj.__dict__, status=206)
        else:
            response_obj = ResponseClass(400, "Question can not be empty")
            return JsonResponse(response_obj.__dict__, status=400)
    except KeyError as e:
            response_obj = ResponseClass(400, "no field called question")
            return JsonResponse(response_obj.__dict__, status=400)

##################################### LCM ###########################################
def lcm_numbers(nums):
    """
    finding LCM of numbers

    Input_param :
        nums : list of numbers whose LCM needes to be fined

    Output_param :
        nums_base_copy: passed list
        storing_output_arr: vertical arrangements
        answer_set: answer set
        answer: answer
         
    """
    storing_output_arr = []
    increment_value = 2
    nums_base_copy = copy.deepcopy(nums)

    answer_set=[]
    answer = 1

    while(sum(nums)>len(nums)):
        nums_copy = copy.deepcopy(nums)
        value = [ True if i % increment_value == 0 else False for i in nums ]
        if True in value:
            storing_output_arr.append((increment_value,nums_copy))
            answer *= increment_value
            answer_set.append(increment_value)
            for i in range(len(nums)):
                if nums[i] % increment_value == 0:
                    nums[i] = nums[i] // increment_value  
                else:
                    nums[i] = nums[i]      

        else:
            increment_value += 1

    return nums_base_copy,storing_output_arr,answer_set,answer     

@api_view(['GET'])
def LCM_numbers(request):
    try:
        list_a ="".join(request.META.get('HTTP_LIST'))
        integer_list = ast.literal_eval(list_a)
        if len(integer_list)>1 and len(integer_list)<5:
            nums_base_copy,storing_output_arr,answer_set,answer  = lcm_numbers(integer_list)
            c = [
                {   "Passed_List":nums_base_copy,
                    "Vertical_Arrangement":storing_output_arr,
                    "Answer_Set":answer_set,
                    "Answer":answer
                }
            ] 
            response_obj = ResponseClass(200, "Add Successful",c)
            return JsonResponse(response_obj.__dict__, status=200)
        else:
            response_obj = ResponseClass(400, "list cannot be empty, pass two to four numbers list")
            return JsonResponse(response_obj.__dict__, status=400)
    except KeyError as e:
            response_obj = ResponseClass(400, "no field called list")
            return JsonResponse(response_obj.__dict__, status=400)


@api_view(['GET'])
def image_q(request):
    try:
        question_type = request.META.get('HTTP_TYPE')
        num1 = request.META.get('HTTP_NUM1')
        num2= request.META.get('HTTP_NUM2')
        img = text_to_picture.convert_q_pic([num1,num2],question_type)
        return img
    except KeyError as e:
            response_obj = ResponseClass(400, "no field called question_type and numbers")
            return JsonResponse(response_obj.__dict__, status=400)
            return JsonResponse(response_obj.__dict__, status=400)                     

