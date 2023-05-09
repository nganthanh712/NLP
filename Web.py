

from bs4 import BeautifulSoup
import requests
import openai
from fpdf import FPDF

def translate(lang, content):
    max_tokens = 900
    token_list = []
    tokens = [s.split() for s in content]
    # Split the input list into arrays of 1000 elements
    token_arrays = [tokens[i:i+max_tokens] for i in range(0, len(tokens), max_tokens)]
    #print (token_arrays)
    for token_slice in token_arrays:
        for i in token_slice:
           
            openai.api_key = "openAIkey"
            prompt=f"Please translate each {i} into {lang} and keep content olny. Please don't return anything esle "

            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt,
                temperature=0.7,
                max_tokens=1024,
                n=1,
                timeout=10,
                stop=None
                )

            val_trans = set()
            translated_text = response.choices[0].text.strip()
            translated_text = translated_text.replace('\n', '')
            if translated_text not in val_trans:
                val_trans.add(translated_text)
                token_list.append(translated_text)
                translated_text= ''.join(token_list)                   

    return translated_text

#def save_to_file(lang, title, content, content_trans):
    

def crawlData(nPage):
    
    req = requests.get('https://vnexpress.net/')
    soup = BeautifulSoup(req.content, 'html.parser', from_encoding='utf-8')

    links =[a['href'] for i, a in enumerate(soup.select('h3.title-news a[href]')) if i<nPage]
    f = open('English.txt', 'w', encoding="utf-8")
    
    for link in links:
        print(link, '\n')
        link_req = requests.get(link)
        link_soup = BeautifulSoup(link_req.content,'html.parser')

        contents = link_soup.find_all('p')
        
        titles = link_soup.find_all('title')
        spans = link_soup.find_all('span')
        title_list=[]
        content_list=[]
        for title in titles:
            ti = title.get_text().strip()
            ti = ti.replace('\n', '')  # remove newline characters
            ti = ' '.join(ti.split())  # remove multiple consecutive spaces
            title_list.append(ti)
            title_string = ''.join(title_list)
        val = set()
        for content in contents:
            for span in spans:
                des = span.extract()
                des = content.get_text().strip()
            
           
                des = ' '.join(des.split())  # remove multiple consecutive spaces
                if des not in val:
                    val.add(des)
                    content_list.append(des)
                    content_string = ''.join(content_list)

       
        
        print("Title: ",  title_string)
        print('Content: ',content_string) 

        print('\n')
        
        lang = input("Enter language to translate: ")
        print(translate(lang, title_list))
        print(translate(lang, content_list))
        #save_to_file(lang, title, content, content_list)
        
        
        f.write("Translate: ")
        f.write("\n")
        f.writelines("Title: ")
        f.writelines(translate(lang, title_list))
        f.write("\n")
        f.writelines("Content: ")
        f.writelines(translate(lang, content_list))
        f.write("\n")
    f.close()

def export_to_pdf():
    pdf= FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=14)
    f = open("English.txt", "r",encoding="UTF-8") 
    text = f.read()
    pdf.multi_cell(0, 10, text)
    pdf.output("Data.pdf")  

if __name__ == "__main__":
    #nPage = int(input("Enter N page: "))
    #crawlData(nPage)
    export_to_pdf()
