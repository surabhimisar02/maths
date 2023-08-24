import re
import datetime
import time
from PIL import Image, ImageFont, ImageDraw

from django.http import HttpResponse
from pytesseract import pytesseract
from selenium import webdriver
from selenium.webdriver import Keys
from time import sleep
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path


def validate_question(statement):
    return re.search('(\\d).*(\\d).*(\\?)$', statement)


def find_numbers(statement):
    numbers = re.findall('(\\d+)', statement)
    for i in range(len(numbers)):
        numbers[i] = int(numbers[i])
    return numbers


def find_operation(statement):
    operator_required = ""
    if re.search('bought each for', statement, re.IGNORECASE):
        operator_required = 'multiplication'
    elif re.search('divided|distributed among|into', statement, re.IGNORECASE):
        operator_required = 'division'
    elif re.search(' together| combined| bought| added| all| total| times', statement):
        operator_required = 'addition'
    elif re.search('gave|took|sold|removed|how many more .* than', statement, re.IGNORECASE):
        operator_required = 'subtraction'
    return operator_required if operator_required else "not specified"


def find_subject(statement):
    # subject = re.findall('(\\d)[ ]{1,}(\\w+)',statement) //it matches number and subject list pair and return those pairs in list
    subject = re.findall('(?<=\\d) +((?!more|extra)\\w+)', statement)
    return subject


def get_image(subject_name: object):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.google.com")
    input_element = driver.find_element(By.TAG_NAME, "input")
    input_element.send_keys(" a " + subject_name[:-1] + " cartoon")
    input_element.send_keys(Keys.ENTER)
    image_tab = driver.find_elements(By.XPATH, "//*[contains(text(),\"Images\")]")
    image_tab[0].click()
    sleep(5)
    with open('myapp/downloaded_image/' + subject_name + '.png', 'wb') as file:
        # identify image to be captured
        l = driver.find_element(By.XPATH, "//*[@id=\"islrg\"]/div[1]/div[1]/a[1]/div[1]/img")
        # write file
        file.write(l.screenshot_as_png)
    driver.close()


def create_image(number_list, subject_list, question_operator, question_statement):
    subject_set = set(subject_list)
    if len(subject_set) == len(subject_list) and len(subject_set) > 1:
        for subject in subject_list:
            my_file = Path('myapp/downloaded_image/' + subject + '.png')
            if not my_file.is_file():
                get_image(subject)

        object_image_1 = Image.open('myapp/downloaded_image/' + subject_list[0] + '.png')
        object_image_2 = Image.open('myapp/downloaded_image/' + subject_list[1] + '.png')
    else:
        my_file = Path('myapp/downloaded_image/' + subject_list[0] + '.png')
        if not my_file.is_file():
            get_image(subject_list[0])
        object_image_1 = Image.open('myapp/downloaded_image/' + subject_list[0] + '.png')
        object_image_2 = object_image_1
    if question_operator == "addition":
        operator_image = Image.open(r'myapp/source_image/plus-sign.png')
    elif question_operator == "subtraction":
        operator_image = Image.open(r'myapp/source_image/minus-sign.png')
    elif question_operator == "multiplication":
        operator_image = Image.open(r'myapp/source_image/multiplication-sign.png')
    elif question_operator == "division":
        operator_image = Image.open(r'myapp/source_image/division-sign.png')
    equals_image = Image.open(r'myapp/source_image/equals-sign.png')
    whitespace_image = Image.open(r'myapp/source_image/white-background-block.png')
    question_mark_image = Image.open(r'myapp/source_image/question_mark.png')
    # keep multiplying number odd as 1 or 3
    multiplying_number = 3
    image_height = 225 * multiplying_number
    vertical_middle = 225 * ((multiplying_number - 1) // 2)
    question_image = Image.new('RGB', ((number_list[0] + number_list[1] + 4) * 225, image_height), (250, 250, 250))
    image_quantity_list = [{"image": object_image_1,
                            "count": number_list[0]},
                           {"image": operator_image,
                            "count": 1},
                           {"image": object_image_2,
                            "count": number_list[1]},
                           {"image": equals_image,
                            "count": 1},
                           {"image": whitespace_image,
                            "count": 1},
                           {"image": question_mark_image,
                            "count": 1}]
    p = 0
    for im_q in image_quantity_list:
        for i in range(im_q["count"]):
            question_image.paste(im_q["image"], (p, vertical_middle))
            p += 225
    title_font = ImageFont.truetype('myapp/font/Roman Regular.ttf', 20)
    image_editable = ImageDraw.Draw(question_image)
    constant = 0
    for i in range(len(number_list)):
        title_text = str(number_list[i]) + " " + (subject_list[i] if len(subject_list) > i else subject_list[0])
        image_editable.text((constant + 225*(number_list[i]//2), vertical_middle+225), title_text, (0, 0, 0), font=title_font)
        constant = constant + 225*(number_list[i]+1)
    image_editable.text((constant + 100, vertical_middle + 225), subject_list[0], (0, 0, 0), font=title_font)
    title_font = ImageFont.truetype('myapp/font/Roman Regular.ttf', 60)
    image_editable.text((50, 50), question_statement, (0, 0, 0), font=title_font)
    ts = time.time()
    dt = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H-%M-%S')
    question_image.save("myapp/questions/question" + dt+ ".jpg", "JPEG")
    return dt


def get_question_from_image(question_image):
    path_to_tesseract = r"C:\\Users\\Amit.K\\AppDataLocal\\Programs\\Tesseract-OCR"

    # Opening the image & storing it in an image object
    img = Image.open(question_image)

    # Providing the tesseract executable
    # location to pytesseract library
    pytesseract.tesseract_cmd = path_to_tesseract

    # Passing the image object to image_to_string() function
    # This function will extract the text from the image
    text = pytesseract.image_to_string(img)

    # Displaying the extracted text
    print(text[:-1])
    # new_text = text.replace("'", "").replace("\n", " ").replace("’","").strip()
    new_text = text.replace("\n", " ")
    print(new_text)
    return new_text


def get_all_questions(scrapped_text):
    first_aray = [e+"?" for e in scrapped_text.split("?") if e]
    all_question = []
    for sentence in first_aray:
        if validate_question(sentence):
            all_question.append(sentence)
    return all_question
    # return re.findall("([A-Z].*\\d.*\\d.*?\\?)|(\\d.*\\d.*?\\?)", scrapped_text)


def convert_text_to_pic(question_statement):
    question_numbers = find_numbers(statement=question_statement)
    question_subject = find_subject(question_statement)
    question_operator = find_operation(statement=question_statement)
    dt = create_image(question_numbers, question_subject, question_operator, question_statement)
    with open("myapp/questions/question" + dt + ".jpg", "rb") as image2string:
        return HttpResponse(image2string.read(), content_type="image/jpeg")


def convert_set_of_text_to_pic(question_list):
    output_image = Image.new('RGB', (225*20, 225*3*len(question_list)), (250, 250, 250))
    y = 0
    for question in question_list:
        question_numbers = find_numbers(statement=question)
        question_subject = find_subject(question)
        question_operator = find_operation(statement=question)

        dt = create_image(question_numbers, question_subject, question_operator, question)
        new_image = Image.open("myapp/questions/question" + dt + ".jpg")
        output_image.paste(new_image, (0, y))
        y = y + 3 * 225
    ts = time.time()
    dt = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    output_image.save("myapp/questions/question" + dt + ".jpg", "JPEG")
    with open("myapp/questions/question" + dt + ".jpg", "rb") as image2string:
        return HttpResponse(image2string.read(), content_type="image/jpeg")


def create_q_image(number_list, question_operator):
    basket_image= Image.open('myapp/source_image/Basket2.png')
    apple_image = Image.open('myapp/source_image/apple2.png').resize(size=(30, 30))
    if question_operator == "addition":
        operator_image = Image.open(r'myapp/source_image/plus-sign.png').resize(size=(125, 125))
    elif question_operator == "subtraction":
        operator_image = Image.open(r'myapp/source_image/minus-sign.png').resize(size=(125, 125))
    elif question_operator == "multiplication":
        operator_image = Image.open(r'myapp/source_image/multiplication-sign.png').resize(size=(125, 125))
    elif question_operator == "division":
        operator_image = Image.open(r'myapp/source_image/division-sign.png').resize(size=(125, 125))
    equals_image = Image.open(r'myapp/source_image/equals-sign.png').resize(size=(125, 125))
    whitespace_image = Image.open(r'myapp/source_image/white-background-block.png').resize(size=(125, 125))
    question_mark_image = Image.open(r'myapp/source_image/question_mark.png').resize(size=(125, 125))
    # keep multiplying number odd as 1 or 3
    multiplying_number = 1
    image_height = 225 * multiplying_number
    vertical_middle = 225 * ((multiplying_number - 1) // 2)
    question_image = Image.new('RGB', (5 * 225, image_height), (250, 250, 250))
    image_quantity_list = [{"image": apple_image,
                            "count": int(number_list[0]),
                            "isObject":True},
                           {"image": operator_image,
                            "count": 1,
                            "isObject":False},
                           {"image": apple_image,
                            "count": int(number_list[1]),
                            "isObject": True},
                           {"image": equals_image,
                            "count": 1,
                            "isObject": False},
                           # {"image": whitespace_image,
                           #  "count": 1,
                           #  "isObject": False},
                           {"image": question_mark_image,
                            "count": 1,
                            "isObject":False}
                           ]
    p = 0
    q = 0

    for im_q in image_quantity_list:
        q=p
        z = vertical_middle
        for i in range(im_q["count"]):
            if im_q["isObject"]:
                if i ==0 :
                    question_image.paste(basket_image, (q, z))
                    z = z + 50
                    q = q + 30
                question_image.paste(im_q["image"], (q, z))
                q = q+33
                if (i+1) % 4 == 0:
                    z = z + 53
                    q = p + 30
                if i == im_q["count"] - 1:
                    p += 225
            else:
                question_image.paste(im_q["image"], (p+50, vertical_middle+50))
                p += 225

    ts = time.time()
    dt = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H-%M-%S')
    question_image.save("myapp/questions/question" + dt+ ".jpg", "jpeg")
    return dt


def convert_q_pic(numbers, operation):
    dt = create_q_image(numbers, operation)
    with open("myapp/questions/question" + dt + ".jpg", "rb") as image2string:
        return HttpResponse(image2string.read(), content_type="image/jpeg")