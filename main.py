import sys
from load_data import extract_data
from text_extract import gemini_smart
from manaul_update import update_prompt_referance


def pdf_referance_extract(pdf_path=None, img_no=None, file_type=None, referance_list=None):
    try:
        if pdf_path != None:
            out_var = extract_data(pdf_path)
        elif img_no!=None and file_type!=None:
            out_var = gemini_smart(img_no, file_type)
        elif file_type!=None and referance_list!=None:
            out_var = update_prompt_referance(file_type, referance_list)
        # else:
        #     print("Error : Please check your input parameter")
        return out_var 
            
    except Exception as error:
        print(f"Error in pdf_referance_extract function: {error}")

    
if __name__ == "__main__":
    pdf_path = input("pdf_path (leave blank if not applicable): ").strip() or None
    img_no = input("img_no (leave blank if not applicable): ").strip() or None
    file_type = input("file_type: ").strip() or None
    referance_list = input("Manual referan (provide values Comma Seperated),  (leave blank if not applicable): ").strip() or None
    referance_list = referance_list.split(",")
    # print(referance_list)
    
    dispvar = pdf_referance_extract(pdf_path=pdf_path, img_no=img_no, file_type=file_type, referance_list=referance_list)
    
    if dispvar is not None:
        print(dispvar)
# conda env : python 3.11.9 conda