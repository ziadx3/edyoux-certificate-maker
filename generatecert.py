
import io
import shutil
from docxtpl import DocxTemplate
from msoffice2pdf import convert
import json
import sys
import qrcode
import os
import firebase_admin
from firebase_admin import credentials , storage
from dotenv import load_dotenv,dotenv_values




env_variables = dotenv_values(dotenv_path="env." + os.getenv("ENVOIRMENT"))

jsonText = ""
studentData = ""

try:

    jsonText = sys.argv[1]
    studentData = json.loads(jsonText)
    os.mkdir(studentData['userInfo']['id'],mode=0o777)

except Exception as error:
    print("error")
    sys.exit()

try:
    
    cred = credentials.Certificate("./cred/" + env_variables['FIREBASE_CRED_NAME'] + ".json")

    firebase = firebase_admin.initialize_app(cred,
                                            {
    'storageBucket' : env_variables["STORAGE_BUCKET"]
                                            })

    store = storage.bucket()



    parentPath = '/root/server'

    # studentData = {
        
    #     "userInfo": {
    #         "ar": "زياد فواز المطيري",
    #         "en": "ziad al-mutairi2",
    #         "id" : 'ojidawoijdowjadijgawo'
    #     },
    #     "stats": {
    #         "likesReceived": 0,
    #         "commentsCount": 4,
    #         "repliesReceived": 0,
            
    #     },
    #     "completedCourses": [
    #         {
    #             "topicsIds": [
    #                 "42prj2ZLfn3PzO0SnNDR"
    #             ],
    #             "totalDuration": 214.882,
    #             "featured": True,
    #             "topics": [
    #                 {
    #                     "ar": "تصميم",
    #                     "en": "Design"
    #                 }
    #             ],
    #             "published": True,
    #             "type": {
    #                 "ar": "دورة قصيرة",
    #                 "en": "Short course"
    #             },
    #             "title": {
    #                 "ar": "تجربة الكورس",
    #                 "en": "تجربة الكورس"
    #             },
    #             "trailerUrl": "27oiot60xo",
    #             "version": 1,
    #             "lessonsCount": 1,
    #             "sections": [
    #                 {
    #                     "duration": 214.882,
    #                     "title": {
    #                         "ar": "عنوان",
    #                         "en": "title"
    #                     },
    #                     "version": 1,
    #                     "goals": {
    #                         "ar": " اهداف",
    #                         "en": "section desc"
    #                     },
    #                     "lessons": [
    #                         {
    #                             "vid": "oow0q6bkh7",
    #                             "hasFile": False,
    #                             "quizId": None,
    #                             "vidDuration": 214.882,
    #                             "title": {
    #                                 "ar": "عنوان",
    #                                 "en": "lesson title"
    #                             },
    #                             "desc": {
    #                                 "ar": "وصف الدرس",
    #                                 "en": "lesson desc"
    #                             }
    #                         }
    #                     ]
    #                 }
    #             ],
    #             "tags": {
    #                 "ar": [],
    #                 "en": [
    #                     "تجربة الكروس"
    #                 ]
    #             },
    #             "cover": "",
    #             "demoUrl": "oow0q6bkh7",
    #             "createdAt": {
    #                 "seconds": 1681722013,
    #                 "nanoseconds": 619000000
    #             },
    #             "comingSoon": False,
    #             "teachers": [
    #                 {
    #                     "createdAt": {
    #                         "seconds": 1667117750,
    #                         "nanoseconds": 199000000
    #                     },
    #                     "name": {
    #                         "ar": "احمد عبد الله",
    #                         "en": "Ahmed Abdullah"
    #                     },
    #                     "cCount": 12,
    #                     "photo": "",
    #                     "bio": {
    #                         "ar": "مطور العاب",
    #                         "en": "Games developer"
    #                     },
    #                     "id": "5bJ6OYJs0urYolfC7DKk",
    #                     "title": {
    #                         "ar": "تقنية معلومات",
    #                         "en": "IT"
    #                     }
    #                 }
    #             ],
    #             "price": 10,
    #             "typeId": "6zuTysLMVbAGHW0WTeTG",
    #             "wistiaProject": "ellar3khz7",
    #             "teachersIds": [
    #                 "5bJ6OYJs0urYolfC7DKk"
    #             ],
    #             "desc": {
    #                 "ar": "تجربة",
    #                 "en": "تجربة الكورس"
    #             },
    #             "goals": {
    #                 "ar": "تجربة",
    #                 "en": "تجربة الكورس"
    #             },
    #             "invoicingId": 21,
    #             "id": "ZEop73tm7b6EBLpodSiO",
    #             "stats": {
    #                 "purchasesCount": 3,
    #                 "commentsCount": 4,
    #                 "avgRate": 0,
    #                 "totalSales": 30,
    #                 "ratesCount": 0,
    #                 "views": 0
    #             }
    #         }
    #     ]
    # }

    def generateGeneralCert(lang):
        doc = DocxTemplate('certem' + lang + '.docx')


        coursesNames = []

        for name in studentData["completedCourses"]:

            coursesNames.append(name["title"][lang])
        


        context = {
                'studentName' : str(studentData["userInfo"][lang]),
                'coursesNames' : coursesNames,
                'sNum' : str(studentData["stats"]['likesReceived'] + studentData["stats"]["commentsCount"]),
                'commentsN' : str(studentData["stats"]["commentsCount"]),
                'coursesN' : str(len(studentData["completedCourses"])),
                'reactN' : str(studentData["stats"]["likesReceived"]),
                'certId': studentData["userInfo"]["id"],
                'trofy' : "مجتهد" if lang == "ar" else "diligent",
            }
        
        doc.render(context=context)

        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
        )

        qr.add_data('https://' + env_variables["ORIGIN"] +'/certificates/' + studentData["userInfo"]["id"] + '/' + lang)
        

        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="transparent")
        img.save(studentData["userInfo"]["id"] + lang + '.png')

        shutil.move("/root/server/" + studentData["userInfo"]["id"] + lang + '.png', "/root/server/" + studentData["userInfo"]["id"] + '/')

        doc.replace_pic('qrcode','/root/server/' + studentData["userInfo"]["id"] + '/' + studentData["userInfo"]["id"] + lang + '.png')

        
        source = studentData["userInfo"]["id"]

        doc.save(filename= source + '/cert' + lang + '.docx' )

        pdfFilename = convert(source='/root/server/' + source + '/cert' + lang + '.docx', output_dir='/root/server/' + source , soft=1)

        

        os.rename(os.path.join(parentPath + "/" +  source, pdfFilename), os.path.join(parentPath  + "/" + source,'certifcate' + lang + '.pdf'))

    def generateCertificate(course,lang):

        doc = DocxTemplate('certem' + lang + '.docx')

        context = {
                'studentName' : str(studentData["userInfo"][lang]),
                'coursesNames' : [
                    str(course['title'][lang])
                                ],
                'sNum' : str(studentData["stats"]['likesReceived'] + studentData["stats"]["commentsCount"]),
                'commentsN' : str(studentData["stats"]["commentsCount"]),
                'coursesN' : str(len(studentData["completedCourses"])),
                'reactN' : str(studentData["stats"]["likesReceived"]),
                'certId': studentData["userInfo"]["id"] + course["id"],
                'trofy' : "مجتهد" if lang == "ar" else "diligent",
            }
        
        doc.render(context=context)

        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
        )

        qr.add_data('https://' + env_variables["ORIGIN"] + '/certificates/' + studentData["userInfo"]["id"] + "-" + course['id'] + '/' + lang)
        

        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="transparent")
        img.save(studentData["userInfo"]["id"] + course["id"] + lang + ".png")

        os.makedirs(name=os.path.join(parentPath , studentData["userInfo"]["id"]  + "/" + course["id"] + "/" + lang),mode=0o777)
        shutil.move("/root/server/" + studentData["userInfo"]["id"] + course["id"] + lang + '.png', "/root/server/" + studentData["userInfo"]["id"] + '/' + course["id"] + "/" + lang + "/")

        doc.replace_pic('qrcode','/root/server/' + studentData["userInfo"]["id"] + '/' + course["id"] + "/" + lang + '/' + studentData["userInfo"]["id"] + course["id"] + lang + ".png")

        


        
        source = studentData["userInfo"]["id"] + "/" + course["id"] + "/" + lang

        doc.save(filename= source + '/cert.docx')

        pdfFilename = convert(source='/root/server/' + source + '/cert.docx', output_dir='/root/server/' + source , soft=1)

        

        os.rename(os.path.join(parentPath + "/" +  source, pdfFilename), os.path.join(parentPath  + "/" + source,'certifcate.pdf'))


    for course in studentData['completedCourses']:


        for round in range(2):
            
            lang = ''

            if round == 0:
                lang = 'en'
            else:
                lang = 'ar'
            
            generateCertificate(course=course,lang=lang)

            blob = store.blob('users/' + studentData["userInfo"]['id'] + '/certifcates/' + course['id'] + '/certificate' + lang + '.pdf')

            blob.upload_from_filename(studentData["userInfo"]['id'] + '/' + course['id'] + '/' + lang + '/certifcate.pdf')
            blob.make_public()



    for round in range(2):
            
        lang = ''

        if round == 0:
            lang = 'en'
        else:
            lang = 'ar'
            
        generateGeneralCert(lang=lang)
        blob = store.blob('users/' + studentData["userInfo"]['id'] + '/certifcates/' + 'certificate' + lang + '.pdf')
        blob.upload_from_filename(studentData["userInfo"]['id'] + '/'  + '/certifcate' + lang + '.pdf')
        blob.make_public()
    
    shutil.rmtree('/root/server/' + studentData["userInfo"]['id'], ignore_errors=True)   
    print("Succsseed")
except Exception as error:
    print("error")
    shutil.rmtree('/root/server/' + studentData["userInfo"]['id'], ignore_errors=True)


# convert('cert.docx','ziad.pdf')
# output = 

