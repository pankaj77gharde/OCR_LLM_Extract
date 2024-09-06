import sys
import os 
import json
import numpy as np
import google.generativeai as genai
from paddleocr import PaddleOCR

# to get gemini acess use use env file , need to add gemini key there
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def extract_text_from_image(image_no, lang='en'):
  image_path = f'./temp_data/images/page_{image_no}.png'
  ocr = PaddleOCR(lang=lang, use_gpu=False)  # will get GPU then process wil be fast jut by making it true
  result = ocr.ocr(image_path, rec=True, cls=True)
  return result

def out2json(mdata):
  mdata = mdata.replace("```", "",2)
  mdata = mdata.replace("json", "")
  final_dictionary = eval(mdata)
  return final_dictionary

def extractme(image_info, file_type):#,img_no):

  with open("./prompt_referances.json", "r") as json_file:
    json_ref_prompt = json.load(json_file)

  uase_referance = json_ref_prompt[file_type]

  generation_config = {
    "temperature": 0.8,
    # "top_p": 0.95,
    # "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
  }

  model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
  )

  chat_session = model.start_chat(
    history=[
    ]
  )

  response = chat_session.send_message(f"""
  following is the nested list having coordinates of text at zero index of inside list, in same list at index one having tuple with text and confidence score.

  You are an AI model tasked with processing insurance related documents and extracting structured information from them. The goal is to generate a JSON object where each key is a Reference point only representing a specific area in the document, and the corresponding value is a list that captures the extracted information along with a confidence score.

  The JSON should be structured as follows for all the set of values :
  main key : Provide output in JSON format with main key as Page_data with each set of informetion as nested dict.
  Nested json : json must be nested if more  than one set of values are there for refernace point .
  Reference Points: The keys should be each specific reference points within the document, including {uase_referance}.
                    If referance points related informetion not present in follwing data then just provide NAN as value. Only use referance points as key, strictly do not generate new key in json.
  Extracted Text and Confidence Score: The values must be in tuple where the first element is the extracted text, and the second element is a confidence score (ranging from 0.0 to 1.0) representing the accuracy of the extraction.
   Do not provide nested values for referance point keys in json, if you came across such neseted value then convert into proper (extracted informetion, confidance score) this format.

  Do not provide any explnetion or code just provide json format informetion. if you don’t get value or text for key then just provide 'NAN'.: \n {image_info}""")

  try:
    json_ = out2json(response.text)
    return json_
  except:
    print(f""" Error in text_extract.py line no 62 : issue with converting model output to json 
             \n getting follwing output : \n {response.text}""")


def chk_ext_perc(extractocr,file_type):
  with open("./prompt_referances.json", "r") as json_file:
    json_ref_prompt = json.load(json_file)

  uase_referance = json_ref_prompt[file_type]

  finlis = []
  for i in range(len(extractocr[0]))[:]:
    finlis.append(extractocr[0][i][1][0])

  generation_config = {
    "temperature": 0.1,
    "top_p": 0.2,
    "top_k": 20,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
  }

  model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
  )

  chat_session = model.start_chat(
    history=[
    ]
  )
  # response = chat_session.send_message(f"""
  # In terms of percentage check presence of contextually similar referance points in follwing data. Is referances ponts given in list {uase_referance} present in follwing data. Just provide overall  persentage value in json foramt. Dont generate any explnetion or code. : : \n {finlis}""")

  # response = chat_session.send_message(f"""
  # in terms of percentage how many referances ponts from list {uase_referance} are present in follwing list of data, check similar text semantically. Just provide referance point and its persentage value in json foramt. Dont generate any explnetion or code, just give JSON as output. : : \n {finlis}""")
  #   Give overall avarge accuracy of presence of refrance points in Data, but check each rerance points induvijvaly first.
  response = chat_session.send_message(f"""
  Task:
  Evaluate the presence of specified reference points in given data. Check presence of each referance points induvijvaly first and get indivjval accuracy, finaly take mean of all the accuracys and provide overall accuracy.

  You can first detect for eaxct refrance text present or not, if its present you can consider it as 100% for that particular refrance point.
  If excat refrance text not present then you can use semantical and contextual understanding of data and referance points to detect the presens.

  Data:
    - Reference Text/Points: {uase_referance}
    - Data: {finlis}

  Output:
  JSON format with an "accuracy" key containing the overall percentage of reference points found in the data.
  Do not generate any code or explnetion just give JSON as output.""")

  # print(response.text)

  try:
    json_ = out2json(response.text)
    lis_accu = json_.values()
    avg_accu = np.mean(list(lis_accu))
    # print(avg_accu)
    return avg_accu
  except:
    print(f""" Error in text_extract.py line no 119 : issue with converting model output to json 
             \n getting follwing output : \n {response.text}""")

  
def gemini_smart(img_no, file_type): # select page no count_page
  img_info = extract_text_from_image(img_no, lang='en')
  extracted_percentage = chk_ext_perc(img_info, file_type)

  if extracted_percentage >= 70:
    json_out = extractme(img_info, file_type)
    json_out["Page_accuracy"] = extracted_percentage
    # json_out["Page_count"] = count_page

    with open("output.json", "w") as json_file:
      json.dump(json_out, json_file, indent=4)

  else: # saving unnessary token consumption !!!!
    json_out = {"Error" : "\n Current referances not performing good on current file type, please try with a different refrances."}
    json_out["Page_accuracy"] = extracted_percentage
    with open("output.json", "w") as json_file:
      json.dump(json_out, json_file, indent=4)

  return json_out

# if __name__ == "__main__":
#     if len(sys.argv) != 3:
#       print("Use: python text_extract.py <img_no> <file_type>")
#       sys.exit(1)
    
#     try:
#       img_no = int(sys.argv[1])
#       file_type = sys.argv[2]
#     except:
#       print("Error : provide valide img_no not string")
#       sys.exit(1)

#     dispvar = gemini_smart(img_no, file_type)
#     print(dispvar)
    
# conda env : python 3.11.9 conda