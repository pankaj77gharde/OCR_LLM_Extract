import os
import re
import shutil
import fitz
import json
import sys

def pdf_to_images(pdf_path, output_folder):
    try:
        os.makedirs(output_folder, exist_ok=True)
        os.makedirs(f"{output_folder}/images", exist_ok=True)
        doc = fitz.open(pdf_path)

        for i, page in enumerate(doc):
            pix = page.get_pixmap()
            pix.save(f"{output_folder}/images/page_{i+1}.png")
        print("done")
    except:
        print(" Error : Issue in PDF to Image conversion")

    return i+1


def extract_data(pdf_path):
    folder_path = './temp_data' #images

    if os.path.exists(folder_path) and os.path.isdir(folder_path):

      shutil.rmtree(folder_path)

      pag_count = pdf_to_images(pdf_path, folder_path)
      file_name = re.findall(r"[\w\s]*.pdf",pdf_path)[0]
      dict_out = {"Total_page_count" : pag_count, "file_name" : file_name}

      os.makedirs(f"{folder_path}/file_info", exist_ok=True)
      with open(f"{folder_path}/file_info/uploded_file.json", "w") as json_file:
        json.dump(dict_out, json_file, indent=4)

    else:
      pag_count = pdf_to_images(pdf_path, folder_path)
      file_name = re.findall(r"[\w\s]*.pdf",pdf_path)[0]
      dict_out = {"Total_page_count" : pag_count, "file_name" : file_name}

      os.makedirs(f"{folder_path}/file_info", exist_ok=True)
      with open(f"{folder_path}/file_info/uploded_file.json", "w") as json_file:
        json.dump(dict_out, json_file, indent=4)

    return dict_out

# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Use: python lode_data.py <pdf_path>")
#         sys.exit(1)
        
#     pdf_path = sys.argv[1]
#     dispvar = extract_data(pdf_path)
#     print(dispvar)
    
# conda env : python 3.11.9 conda