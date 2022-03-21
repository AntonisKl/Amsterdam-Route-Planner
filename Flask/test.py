# import speech_recognition as sr
# import pyaudio
#
# def speech():
#
#     r = sr.Recognizer()
#     # text = ""
#     with sr.Microphone() as source:
#         r.adjust_for_ambient_noise(source)
#         print("Listening......")
#         audio = r.listen(source)
#
#         try:
#             print("Recognizing...")
#             query = r.recognize_google(audio, language='nl-NL')
#             # print(f"USER: {query}\n")
#
#         except Exception:
#             print("Did not catch that")
#     return query
#
#
#
# # r = sr.Recognizer()
# #     # text = ""
# # with sr.Microphone() as source:
# #     r.adjust_for_ambient_noise(source)
# #     print("Listening......")
# #     audio = r.listen(source)
# #
# #     try:
# #         print("Recognizing...")
# #         query = r.recognize_google(audio, language='nl-NL')
# #         print(f"USER: {query}\n")
# #
# #     except Exception:
# #         print("Did not catch that")
#
#
#     # r = sr.Recognizer()
#     # text = ""
#     # with sr.Microphone() as source:
#     #     r.adjust_for_ambient_noise(source)
#     #
#     #     print("Please say something")
#     #
#     #     audio = r.listen(source)
#     #
#     #     print("Recognizing Now .... ")
#     #
#     #
#     #     # recognize speech using google
#     #
#     #     try:
#     #         text =  r.recognize_google(audio)
#     #
#     #
#     #     except Exception as e:
#     #         print("Error :  " + str(e))
#     # return text
