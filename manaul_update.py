import sys
import json

def update_prompt_referance(file_type, referance_list):
  with open("./prompt_referances.json", "r") as json_file:
    json_ref_prompt = json.load(json_file)

  if file_type in json_ref_prompt.keys() and type(referance_list)==list:
    json_ref_prompt[file_type] = json_ref_prompt[file_type] + referance_list
    msg = "Update in current Referance successful !"
  elif type(referance_list)==list:
      json_ref_prompt[file_type] =  referance_list
      msg = "New Referance Update successful !"
  else :
    msg = f"Error : File type {file_type} not get updated with referances {referance_list} !"

  with open("./prompt_referances.json", "w") as json_file:
    json.dump(json_ref_prompt,json_file, indent=4)
    
  return msg

    
# if __name__ == "__main__":
#     if len(sys.argv) < 3:
#         print("Use : python manaul_update.py <file type> <referance1> <referance2> ....")
#         sys.exit(1)
        
#     file_type = sys.argv[1]      
#     referance_list = []
#     for arg in sys.argv[2:]:
#         referance_list.append(arg)
    
#     dispvar = update_prompt_referance(file_type, referance_list)
#     print(dispvar)
    
# conda env : python 3.11.9 conda
