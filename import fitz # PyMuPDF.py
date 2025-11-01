from pydoc import text
import fitz # PyMuPDF
import requests
import sys
import os
from bs4 import BeautifulSoup
import batchFromUrl

from sqlConnection import insertcannabinoids, insertterpenes,checkTerpene,checkCannabinoid
from bcolors import bcolors
#from downloadFile import downloadfile

separator ="|"
redownload = 0
#my_list = ["73881_0007916126","82057_0007827833","82115_0007827419","76555_0007938946","76692_0007595523","70485_0007815066","70475_0007552442","70455_0007850495","70483_0007826254","74941_0007782358","74940_0007745817","73345_0007487585","66469_0007827816","41743_0006970031","35471_0007723033","35163_0007723031","17699_0007247919","17611_0007773276","17552_0007365581","17551_0007585074","17550_0007324717","17496_0007723032","76692_0007605476","70485_0007814456","78022_0006993920","70483_0007896426","47993_0007425018","35163_0007774147","73877_0007916125","75265_0007848664","77008_0007825590","76555_0007849441","76692_0007326955","70485_0007721957","70455_0007840147","70483_0007895795","74941_0007641946","74940_0007701106","17611_0007353100","76692_0007927817","70483_0007850491","17552_0007838248","17551_0007937998","17550_0007653493","17496_0007782247","81867_0007511894","70475_0007105140","70478_0007026451","74941_0007653489","47993_0006162867","35471_0007782246","17550_0006945103","76692_0007838379","70475_0007757083","80356_0007828495","80354_0007828494","74940_0007803301","17551_0007086534","82057_0007916183","82115_0007916172","70483_0007838370","74941_0007838378","70485_0007746233","74940_0007732801","17699_0007563884","17611_0007641949","74940_0007749037","70487_0007548776","70481_0007541027","70475_0007290332","74941_0007757087","74940_0007685829","67357_0007162123","70475_0007489472","70475_0007529648","70455_0007871718","17552_0007261921","80355_0007828496","80374_0007817803","73997_0007630961","77047_0007771193","77106_0007329103","77124_0007275926","74863_0007277906","76555_0007510590","77132_0007248959","73994_0007223617","77614_0007209427","77078_0007313346","70477_0007136957","70475_0007062037","70455_0007775012","70483_0007208801","70478_0007023639","17611_0007137975"]
my_list = ["47993_0006162867"]
dispensary="Trulieve"
dispensaryid=1
# my_list = ["gbxxJoq4GqJcnLw","3LpRC3Ckz5XjF6w","WQiipC7sQpiyojx","czKcWBWzTDyCPdT","8K4kMmg8nsTGFxt","FW3xYKXr7WnzAWq","gFAcXTRYpnfkSfk","g47exX3f769D7Np","6z63Dpn43BwkggY","QpgabPXJzZM7StD","sGgQEA54cQ3Y9JW","rqrTmqqezwBGipR","SrGCCkbd2AobjjY","g852X8ybqn7w2pL","LngeNzi2cfXKMiX","33k3sMwNY5TKXTg","Ay2ZkZyeQNDjyfa","JPqWAsffRt99ySJ","nP7REAQ5aQ4RYW2","6DMQwXFGMqs8zX5","jKdbRbwgKFijRtc","rbbr8Ep3qAoPj5y","cZLTKTn3yTTJe7P","eWDcrrGNLEmzbs9","meg9ZNWmCGESgsC","dnyP2drMTRyw87E","SnFSY86MjSfXyB8","gZYK5idR4KdJqma","SfWBtnDxrN9qs2t"]
# # #my_list = ["SfWBtnDxrN9qs2t"]
# dispensary="Sunburn"
# dispensaryid=2
totalbatches = my_list.__len__()
batchescount = 0

for item in my_list:
    batch = ""
    batchescount = batchescount + 1
    print (bcolors.OKBLUE+ "batch " + str(batchescount) + " of " + str(totalbatches) + " : " + item+bcolors.ENDC)
    missingfile = 0
    
    if(checkTerpene(item)==True):
        print(bcolors.OKCYAN + item +" terpene record exisits" + bcolors.ENDC)        
    else:
        batch = ""
        if dispensary == "Sunburn":
            batch =batchFromUrl.batch_from_url(item)
            url ="https://mete.labdrive.net/s/"+item  # Replace with the actual URL of the file
            print(url)
        elif dispensary == "Trulieve":
            batch = item
            url ="https://www.trulieve.com/content/dam/trulieve/en/lab-reports/"+batch+".pdf?download=true"  # Replace with the actual URL of the file
            
        #url = "https://mete.labdrive.net/s/g47exX3f769D7Np"
        local_filename = batch+".pdf"  # Replace with your desired local filename

        if os.path.exists(local_filename):
            print(f"File '{batch}' already exists.")
        # continue
            # If you want to redownload the file even if it exists, set redownload to 1
            # redownload = 1
        else:
            print(f"File '{batch}' does not exist. It will be downloaded.")
            missingfile = 1


        if redownload == 1 or missingfile == 1:
            try:
                headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
                }
                response = requests.get(url, headers=headers, stream=True, timeout=10)  # Use stream=True for large files
                response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
                local_path ='C:/Users/JamiesonGill/source/repos/Terprint/test_output/'
                local_path = local_path + local_filename
                with open(local_filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"File '{local_path}' downloaded successfully.")
 

            except requests.exceptions.RequestException as e:
                print(f"Error downloading file: {e}")


        #https://www.trulieve.com/content/dam/trulieve/en/lab-reports/84573_0007311573.pdf?download=true
        pdf_path = "C:\\JamiesonGill\\source\\repos\\Terprint\\test_output\\"+batch+".pdf"
        pdf_path = local_filename
        print("PDF Path:" + pdf_path)
        def extract_text_from_pdf(pdf_path):
            """Extracts all text from a PDF file."""
            text = ""
            try:
                with fitz.open(pdf_path) as doc:
                    for page in doc:
                        text += page.get_text()
            except Exception as e:
                print(f"Error extracting text: {e}")
            return text


        try:
            

            format = 0
            print(bcolors.OKGREEN + "BEGIN format:" + str(format) + bcolors.ENDC)
            #Example usage
            extracted_text = extract_text_from_pdf(pdf_path)
            #DETERMINE IF NEW OR OLD FORMAT
            if "RA0571996" in extracted_text:
                format = 1
            elif "Accreditation #102020" in extracted_text:
                #mcs 
                if "Total Cannabinoids" in extracted_text:
                    format = 2  # example 74941_0007653489
                elif "Total Active Cannabinoids" in extracted_text:
                    format = 4  # example 47993_0006162867
            elif "Method Testing Laboratories" in extracted_text:
                format = 3
                #Method Testing Laboratories

            print(bcolors.OKGREEN + "END format:" + str(format) + bcolors.ENDC)
            print(item+":"+str(format))

            with open(batch+"_extractall.txt", "w", encoding='utf-8') as f:
                f.write(extracted_text)

            outputline = ""
            outputlines = ""
            terp = ""
            percent = ""
            counter = 1
            
            #FORMAT 1111111111111111111111111111

            if format == 1:

            #FORMAT 111111111111111111111111111

                if "Result " in extracted_text:
                    terpenetext = extracted_text.split("Result ", maxsplit=1)[1]
                elif "Result\n(mg/g)\n%" in extracted_text:
                    terpenetext = extracted_text.split("Result\n(mg/g)\n%\n", maxsplit=1)[1]
                elif "Result (mg/g)\n" in extracted_text:
                    terpenetext = extracted_text.split("Result (mg/g)\n", maxsplit=1)[1]
    
                terpenetext  =terpenetext.split("Total Terpenes:", maxsplit=1)[0]
                terpenetext  =terpenetext.replace("(mg/g)\n(%)","")#(mg/g) (%)
                terpenetext  =terpenetext.replace("(mg/g) (%)","")#
            # print("1\n"+terpenetext)
                #print(extracted_text)
                counter =1
                outputline = ""
                outputlines = ""
                newcan = 0 
                
                counter = 1
                position = 1
            # print(terpenetext)
                skip = True
                for line in terpenetext.splitlines():    
                    line = line.strip()
                    if line=="Ocimene, Total" :
                        line = "Ocimene"
                    if skip == True:
                        outputlines ="Batch"+separator+"Index"+separator+"Terpene"+separator+"Result"+separator+"Percent"
                        skip = False
                        continue
                    if counter  ==1 :
                        outputline =  batch + "|"+str(position)+"|" + line 
                        #outputline =   terp + "," + str(percent)+ "|" +  str(counter) + "|"
                    elif counter  == 2:
                        outputline = outputline + separator  + line
                    elif counter  == 3:
                        outputline = outputline + separator + line   
                        
                        # print("-----\n")
                        # print (outputline+"\n")
                        # print("-----\n") 
                        insertterpenes(
                                    outputline.split(separator)[0],
                                    outputline.split(separator)[1],
                                    outputline.split(separator)[2],
                                    outputline.split(separator)[4], 
                                    outputline.split(separator)[3],           
                                    dispensaryid,
                                    "jgill@acidnillc.onmicrosoft.com")
                        outputlines = outputlines+  "\n"+  outputline                     
                        outputline = ""
                        counter = 0                
                        position = position + 1                
                    counter = counter  + 1
            
                

                terpenetext = outputlines#.replace(",Analyte,Result (mg/g)\n%,","")
                outputlines = ""
                outputline = ""
                cannabinoidtext = extracted_text.split("Result\n(mg/g)\n(%)\n", maxsplit=1)[1]
        
                cannabinoidtext = cannabinoidtext.split("\nPrep. By: ", maxsplit=1)[0]
            # print("1\n"+cannabinoidtext)
                counter =1
                newcan = 0 
                position =1
                setheader = True
                for line in cannabinoidtext.splitlines():
                    
                    if "Total Active" in line:
                        break 
                    # if skip == True:
                    #     outputlines ="Batch,Index,Cannabinoid,Dilution,LOD,LOQ,Result,Percent\n"
                    #     skip = False
                    #     outputline =   line 
                    #     continue
                    # if "mg/g" in line:    
                    # if line == "THCA-A" or line == "Delta-9 THC" or line == "CBDA" or line == "CBD" or line == "CBN" or line == "CBG" or line == "CBC" or line == "THCV" or line == "CBDV" or line == "CBGA" or line == "THC-A" or line == "Delta-9-THC" or line =="Total Active CBD"or line =="Total Active THC" or line =="Delta-8 THC":
                    #     outputline =  outputline + line  
                    #     outputlines = outputlines +  outputline
                    #     outputline=""
                    # else:
                    #     outputline = outputline + "," + line  
                    if counter ==1:
                        if setheader == True:
                            outputlines ="Batch"+separator+"Index"+separator+"Cannabinoid"+separator+"Dilution"+separator+"LOD"+separator+"LOQ"+separator+"Result"+separator+"Percent\n"
                            setheader=False
                        outputline = batch + separator+str(position)+separator+line +separator+ outputline

                    elif counter <6:
                        outputline = outputline + separator+  line 
                    elif counter ==6:
                        outputline =  outputline + separator+  line + "\n"
                        outputlines = outputlines +  outputline 
                        
                        print("-----")
                        print (outputline)
                        print("-----") 
                        insertcannabinoids(
                                        outputline.split(separator)[0],
                                        outputline.split(separator)[1],
                                        outputline.split(separator)[2],
                                        outputline.split(separator)[8],
                                        outputline.split(separator)[7], 
                                        dispensaryid,
                                        "jgill@acidnillc.onmicrosoft.com")
                        outputline=""
                        counter = 0
                        position = position + 1
                    counter = counter + 1

                cannabinoidtext = outputlines.replace(",Analyte,Result (mg/g) (%)\n","")
                # print("__________________________________________________")      
                # print(batch)            
                # print("1\n"+terpenetext)
                # print("1\n"+cannabinoidtext) 

                with open(str(format)+"\\terpenes\\"+batch+"_terpenes.txt", "w", encoding='utf-8') as f:
                    outputtext =  terpenetext            
                    f.write(outputtext)
                with open(str(format)+"\\cannabinoids\\"+batch+"_cannabinoids.txt", "w", encoding='utf-8') as f:
                    outputtext = cannabinoidtext            
                    f.write(outputtext)
            
            ###FORMAT 2222222222222222222222222222


            elif format == 2:


            ###FORMAT 222222222222222222222222222

                extracted_text = extract_text_from_pdf(pdf_path)
                extracted_text1 = extracted_text
            # print(extracted_text)
            # with open(batch+"_extractall.txt", "w", encoding='utf-8') as f:
                # f.write(extracted_text)
                    
            # print("2wrote text:\n")
                terpenetext = extracted_text.split("TERPENES SUMMARY (Top Ten)", maxsplit=1)[1]
                terpenetext = terpenetext.split("Completed", maxsplit=1)[0]
                terpenetext  =terpenetext.split("Total CBD", maxsplit=1)[0]
                terpenetext  =terpenetext.split("%\n ", maxsplit=1)[1]

            #  print("3found terpenes:\n")
                
                #terpenetext = extract_text_from_pdf(terpenetext)

                cannabinoidtext = extracted_text1.split("Analyte\nmg\n", maxsplit=1)[1]
                cannabinoidtext  =cannabinoidtext.split("TERPENES SUMMARY (Top Ten)", maxsplit=1)[0]
                
                
                counter =1
                outputlines = ""
                outputline = ""
                c= 1
                can=""
                percent=""
                outputlines = ""
                c= 1
                position = 1
                skipcount = 1
                index = 1
                outputlines ="Batch"+separator+"Index"+separator+"Cannabinoid"+separator+"Percent"+separator+"Milligrams\n"
                for line in cannabinoidtext.splitlines():
                
                    if "Total Active" in line:
                        break 
                    # line = line.strip()
                    # print ("-----------------------------------------------\n")
                    # print (str(counter)+"\n")
                    # print (line+"\n")
                    # print ("+++++++++++++++++++++++++++++++++++++++++++++++\n")
                    # #print(cannabinoidtext+"\n")
                    # print ("-----------------------------------------------\n")
                
                    # if "mg/g" in line:    
                    # if line == "THCA-A" or line == "Delta-9 THC" or line == "CBDA" or line == "CBD" or line == "CBN" or line == "CBG" or line == "CBC" or line == "THCV" or line == "CBDV" or line == "CBGA" or line == "THC-A" or line == "Delta-9-THC" or line =="Total Active CBD"or line =="Total Active THC" or line =="Delta-8 THC":
                    #     outputline =  outputline + line  
                    #     outputlines = outputlines +  outputline
                    #     outputline=""
                    # else:
                    #     outputline = outputline + "," + line  
                    if counter ==1:
                        outputline = batch + "|"+str(index)+"|" +line 
                    elif counter ==2:
                        outputline =  outputline + "|" +line 
                    elif counter ==3:                             
                        outputline =  outputline + "|"+  line +"\n"
                        # print ("+++++++++++++++++++++++++++++++++++++++++++++++\n")
                        # print(outputline+"\n")
                        # print ("-----------------------------------------------\n")
                    # outputline = outputline.split(separator)[0] +    "," + outputline.split(separator)[1] +    "," + outputline.split(separator)[2]+    "," + outputline.split(separator)[3] +    "," + outputline.split(separator)[4]   
                        inpercent = ""
                        inanalyte = ""    
                        print(str(index) +"---"+outputline+"----")            
                    #  if index == 1:
                        # else:
                        #     inpercent = outputline.split(separator)[3]
                        #     inanalyte = outputline.split(separator)[2]
                        outputlines = outputlines + outputline
                    
                        insertcannabinoids(
                                        outputline.split(separator)[0],
                                        outputline.split(separator)[1],
                                        outputline.split(separator)[2],
                                        outputline.split(separator)[3],
                                        outputline.split(separator)[4], 
                                        dispensaryid,
                                        "jgill@acidnillc.onmicrosoft.com")
                        outputline=""
                        counter = 0
                        position = position + 1
                        index=index+1
                    counter = counter + 1

                cannabinoidtext = outputlines.replace(",,,%,,%,Analyte,,%,Analyte,mg,,%,Analyte,mg,","") 
                    
    
                outputlines=""
                counter = 1
                skip = True
                terp = ""
                position = 1
                skip = True
                index = 1
                setheader = True
                for line in terpenetext.splitlines():    
                    if skip == True:
                        skip = False
                        continue
                    
                    if line=="Ocimene, Total" :
                        line = "Ocimene"
                    # print("Line:", line)
                    # print("Counter:", counter)
                    # print("Is number:", is_number)
                    # print("-----")
                    # Check if the line can be converted to a float
                    # If it can, it's a number; otherwise, it's not
                    try:
                        float(line)
                        is_number = True
                    except ValueError:
                        is_number = False
                    # print("Not a number:", line)

                    if is_number == True :
                        percent = line  
                        outputline =  terp + ", " + percent
                        # counter = counter  + 1
                    else:
                        if setheader == True:
                            outputlines ="Batch"+separator+"Index"+separator+"Terpene"+separator+"Percent\n"
                            setheader=False
                                            
                        terp = batch + "|" + str(index)+"|" + line
                        outputline =   terp + "|" + percent
                        if setheader == False:                            
                            outputline =  outputline + "\n"
                            # #outputlines = outputlines +  outputline 
                            # print("-----\n")
                            # print (outputline+"\n")
                            # print("-----\n")
                            insertterpenes(
                                            outputline.split(separator)[0],
                                            outputline.split(separator)[1],
                                            outputline.split(separator)[2],
                                            outputline.split(separator)[3], 
                                            0,                                        
                                            dispensaryid,
                                            "jgill@acidnillc.onmicrosoft.com")
                        outputlines = outputlines+ outputline 
                        index = index + 1
                    
                        # if counter == 1:
                    #     percent = line
                    #     counter = counter  + 1
                    # elif counter == 2:
                    #     terp = line
                    #     counter = counter  + 1
                    # elif counter == 3:
                    #     outputline = terp + " " + percent + "\n"
                    #     outputlines = outputlines + outputline  
                    #     counter  =1
                terpenetext = outputlines

                # print("__________________________________________________")        
                # print(batch)            
                # print("2\n"+terpenetext)
                # print("2\n"+cannabinoidtext)
        
                with open(str(format)+"\\terpenes\\"+batch+"_terpenes.txt", "w", encoding='utf-8') as f:
                    outputtext =  terpenetext            
                    f.write(outputtext)
                with open(str(format)+"\\cannabinoids\\"+batch+"_cannabinoids.txt", "w", encoding='utf-8') as f:
                    outputtext = cannabinoidtext            
                    f.write(outputtext)

            ###FORMAT 3333333333333333333333333333


            elif format == 3:


            ###FORMAT 4444444444444444444444444444

                extracted_text = extract_text_from_pdf(pdf_path)
                extracted_text1 = extracted_text
            # print(extracted_text)
            # with open(batch+"_extractall.txt", "w", encoding='utf-8') as f:
                # f.write(extracted_text)
                    
            # print("2wrote text:\n")
                terpenetext = extracted_text.split("(ug/g)\n%", maxsplit=1)[1]
                terpenetext = terpenetext.split("                              Total Terpenes", maxsplit=1)[0]    

            #  print("3found terpenes:\n")
                
                #terpenetext = extract_text_from_pdf(terpenetext)

                cannabinoidtext = extracted_text1.split("mg/unit", maxsplit=1)[1]
                cannabinoidtext  =cannabinoidtext.split("Sample Analyzed By", maxsplit=1)[0]

                outputlines = ""
                outputline = ""
                c= 1
                can=""
                percent=""
                outputlines = ""
                c= 1
                position = 1
                skipcount = 4
                index = 1
                for line in cannabinoidtext.splitlines():
                    line = line.strip()
                    if position == skipcount:
                        outputlines ="Batch"+separator+"Index"+separator+"Cannabinoid"+separator+"Dilution"+separator+"LOD"+separator+"LOQ"+separator+"Result"+separator+"Percent\n"
                        position = position + 1
                        skip = False 
                        continue
                    elif position < skipcount:
                        position = position + 1
                        continue
                    if "Total " in line:
                        break 
                    # if "mg/g" in line:    
                    # if line == "THCA-A" or line == "Delta-9 THC" or line == "CBDA" or line == "CBD" or line == "CBN" or line == "CBG" or line == "CBC" or line == "THCV" or line == "CBDV" or line == "CBGA" or line == "THC-A" or line == "Delta-9-THC" or line =="Total Active CBD"or line =="Total Active THC" or line =="Delta-8 THC":
                    #     outputline =  outputline + line  
                    #     outputlines = outputlines +  outputline
                    #     outputline=""
                    # else:
                    #     outputline = outputline + "," + line  
                    if counter ==1:
                        outputline = batch +"_"+item + "|"+str(index)+"|" +line 

                    elif counter <5:
                        outputline = outputline + "|"+  line 
                    elif counter ==5:
                        outputline =  outputline + "|"+  line + "\n"
                        outputlines = outputlines +  outputline 
                        
                        print ("+++++++++++++++++++++++++++++++++++++++++++++++\n")
                        print(bcolors.OKCYAN + outputline + bcolors.ENDC+"\n")
                        print ("-----------------------------------------------\n")
                        insertcannabinoids(
                                        outputline.split(separator)[0],
                                        outputline.split(separator)[1],
                                        outputline.split(separator)[2],
                                        outputline.split(separator)[6],
                                        outputline.split(separator)[5], 
                                        dispensaryid,
                                        "jgill@acidnillc.onmicrosoft.com")
                        
                        outputline=""
                        counter = 0
                        position = position + 1
                        index=index+1
                    counter = counter + 1

                cannabinoidtext = outputlines.replace(",,,%,,%,Analyte,,%,Analyte,mg,,%,Analyte,mg,","") 
                    
    
                outputlines=""
                counter = 1
                skip = True
                terp = ""
                position = 1
                skip = True
                index = 1
                setheader = True
                for line in terpenetext.splitlines():     
                    if position == skipcount:
                        outputlines ="Batch"+separator+"Index"+separator+"Terpene"+separator+"(ug/g)"+separator+"Percent\n"
                        position = position + 1
                        skip = False 
                        continue
                    elif position < skipcount:
                        position = position + 1
                        continue
                    if "Total " in line:
                        break  
                    if counter ==1:
                        outputline = batch +"_"+item + separator+str(index)+separator +line 

                    elif counter <3:
                        outputline = outputline + separator+  line 
                    elif counter ==3:
                        outputline =  outputline +separator+  line + "\n"
                        outputlines = outputlines +  outputline 
                        
                        print ("+++++++++++++++++++++++++++++++++++++++++++++++\n")
                        print(bcolors.OKCYAN + outputline + bcolors.ENDC +"\n")
                        print ("-----------------------------------------------\n")
                        insertterpenes(
                                        outputline.split(separator)[0],
                                        outputline.split(separator)[1],
                                        outputline.split(separator)[2],
                                        outputline.split(separator)[4], 
                                        outputline.split(separator)[3],
                                        dispensaryid,
                                        "jgill@acidnillc.onmicrosoft.com")
                        outputline=""
                        counter = 0
                        position = position + 1
                        index=index+1
                    counter = counter + 1
                terpenetext = outputlines

                # print("__________________________________________________")        
                # print(batch)            
                # print("2\n"+terpenetext)
                # print("2\n"+cannabinoidtext)
        
                with open(str(format)+"\\terpenes\\"+batch+"_terpenes.txt", "w", encoding='utf-8') as f:
                    outputtext =  terpenetext            
                    f.write(outputtext)
                with open(str(format)+"\\cannabinoids\\"+batch+"_cannabinoids.txt", "w", encoding='utf-8') as f:
                    outputtext = cannabinoidtext            
                    f.write(outputtext)


            ###FORMAT 444444444444444444
            
            elif format == 4:

            ###FORMAT 444444444444444444

                extracted_text = extract_text_from_pdf(pdf_path)
                extracted_text1 = extracted_text
            # print(extracted_text)
            # with open(batch+"_extractall.txt", "w", encoding='utf-8') as f:
                # f.write(extracted_text)
                    
            # print("2wrote text:\n")
                terpenetext = extracted_text
                terpenetext = terpenetext.split("Analyte", maxsplit=1)[1]
                terpenetext = terpenetext.split("%\n", maxsplit=1)[1]
                terpenetext = terpenetext.split("Total THC", maxsplit=1)[0]

                print("TERPENES-----------------------")
                print(terpenetext)
            #  print("3found terpenes:\n")
                
                #terpenetext = extract_text_from_pdf(terpenetext)
                cannabinoidtext =  extracted_text1
                cannabinoidtext = cannabinoidtext.split("POTENCY DETAILS", maxsplit=1)[1]
                cannabinoidtext  =cannabinoidtext.split("Total Terpenes:", maxsplit=1)[0]
                print("CANNABINOIDS-----------------------")
                print(cannabinoidtext)
                ###  Cannabinoid
                counter =1
                outputlines = ""
                outputline = ""
                c= 1
                can=""
                percent=""
                outputlines = ""
                c= 1
                position = 1
                skipcount = 1
                index = 1
                outputlines ="Batch"+separator+"Index"+separator+"Cannabinoid"+separator+"Percent"+separator+"Milligrams\n"
                for line in cannabinoidtext.splitlines():
                    print(line)
                    line = line.strip()
                    if "Total Active" in line:
                        break 
                    if line.strip() == "":
                        continue
                    
                    if counter ==1:
                        percent = line
                        outputline = batch + "|"+str(index)+"|" +line 
                    elif counter ==2: 
                        can = line                      
                        outputline = batch + "|"+str(index)+"|" +can         
                        outputline =  outputline + "|"+  percent +"\n"
                        # print ("+++++++++++++++++++++++++++++++++++++++++++++++\n")
                        # print(outputline+"\n")
                        # print ("-----------------------------------------------\n")
                    # outputline = outputline.split(separator)[0] +    "," + outputline.split(separator)[1] +    "," + outputline.split(separator)[2]+    "," + outputline.split(separator)[3] +    "," + outputline.split(separator)[4]   
                        inpercent = ""
                        inanalyte = ""    
                        print(str(index) +"---"+outputline+"----")            
                    #  if index == 1:
                        # else:
                        #     inpercent = outputline.split(separator)[3]
                        #     inanalyte = outputline.split(separator)[2]
                        outputlines = outputlines + outputline
                    
                        insertcannabinoids(
                                        outputline.split(separator)[0],
                                        outputline.split(separator)[1],
                                        outputline.split(separator)[2],
                                        outputline.split(separator)[3],
                                        0, 
                                        dispensaryid,
                                        "jgill@acidnillc.onmicrosoft.com")
                        outputline=""
                        counter = 0
                        position = position + 1
                        index=index+1
                        
                    counter = counter + 1

                cannabinoidtext = outputlines.replace(",,,%,,%,Analyte,,%,Analyte,mg,,%,Analyte,mg,","") 
                    
    
                outputlines=""
                counter = 1
                skip = True
                terp = ""
                position = 1
                skip = True
                index = 1
                percent=""
                setheader = True
                for line in terpenetext.splitlines():    
                    print(line)
                    line = line.strip()
                    if skip == True:
                        skip = False
                        continue
                    
                    if line=="Ocimene, Total" :
                        line = "Ocimene"
                    # print("Line:", line)
                    # print("Counter:", counter)
                    # print("Is number:", is_number)
                    # print("-----")
                    # Check if the line can be converted to a float
                    # If it can, it's a number; otherwise, it's not
                    if counter ==1:
                        terp = line
                    elif counter ==2: 
                        percent = line                      
                        outputline = batch + "|"+str(index)+"|" +terp
                        outputline =  outputline + "|"+  percent +"\n"
                        # print ("+++++++++++++++++++++++++++++++++++++++++++++++\n")
                        # print(outputline+"\n")
                        # print ("-----------------------------------------------\n")
                    # outputline = outputline.split(separator)[0] +    "," + outputline.split(separator)[1] +    "," + outputline.split(separator)[2]+    "," + outputline.split(separator)[3] +    "," + outputline.split(separator)[4]   
                        inpercent = ""
                        inanalyte = ""    
                        print(str(index) +"---"+outputline+"----")            
                    #  if index == 1:
                        # else:
                        #     inpercent = outputline.split(separator)[3]
                        #     inanalyte = outputline.split(separator)[2]
                        outputlines = outputlines + outputline
                    
                        insertterpenes(
                                        outputline.split(separator)[0],
                                        outputline.split(separator)[1],
                                        outputline.split(separator)[2],
                                        outputline.split(separator)[3],
                                        0, 
                                        dispensaryid,
                                        "jgill@acidnillc.onmicrosoft.com")
                        outputline=""
                        counter = 0
                        position = position + 1
                        index=index+1
                    counter = counter + 1
                    
                        # if counter == 1:
                    #     percent = line
                    #     counter = counter  + 1
                    # elif counter == 2:
                    #     terp = line
                    #     counter = counter  + 1
                    # elif counter == 3:
                    #     outputline = terp + " " + percent + "\n"
                    #     outputlines = outputlines + outputline  
                    #     counter  =1
                terpenetext = outputlines

                # print("__________________________________________________")        
                # print(batch)            
                # print("2\n"+terpenetext)
                # print("2\n"+cannabinoidtext)
        
                with open(str(format)+"\\terpenes\\"+batch+"_terpenes.txt", "w", encoding='utf-8') as f:
                    outputtext =  terpenetext            
                    f.write(outputtext)
                with open(str(format)+"\\cannabinoids\\"+batch+"_cannabinoids.txt", "w", encoding='utf-8') as f:
                    outputtext = cannabinoidtext            
                    f.write(outputtext)
                                    

        except Exception as e:
            exception_message = str(e)
            exception_type, exception_object, exception_traceback = sys.exc_info() 
            print(bcolors.FAIL  +  item + ":" + str(format) + ":"+str(exception_traceback.tb_lineno) +" Error:", e + bcolors.ENDC)
        # print("\n"+extracted_text)
            print("\n\n--------------------------------")
def has_decimal_places_str(number):
    return "." in str(number)
def batch_from_url(url):
    # URL of the webpage containing the download link
    webpage_url = "https://mete.labdrive.net/s/" + url

    # Fetch the webpage content
    response = requests.get(webpage_url)
    response.raise_for_status() # Raise an exception for bad status codes

    # Parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the download link (adjust selector as needed)
    # Example: finding a link with specific text or class
    download_link_tag = soup.find('a',attrs={'class': 'primary button'}) 
    # Or, if the link has a specific attribute:
    # download_link_tag = soup.find('a', {'id': 'download-button'})

    if download_link_tag:
        file_url = download_link_tag['href']
        # If the href is a relative path, you might need to construct the full URL
        # from urllib.parse import urljoin
        # file_url = urljoin(webpage_url, file_url)
        print("Download link found:", file_url)
        coa = file_url.split('download/')[-1]
        print("File name:", coa)
        batch = coa.split('.')[0]
        print("Batch name:", batch)
        return batch
    else:
        print("Download link not found on the page.")
        file_url = None
    
def extract_text_from_pdf2(textin):
    text = ""
    percent = ""
    terp = ""
    counter =1
    for line in textin.splitlines():
        if counter == 1:
            percent = line
            counter = counter  + 1
        elif counter == 2:
            terp = line
            counter = counter  + 1
        elif counter == 3:
            outputline = terp + " " + percent + "\n"
            text = text + outputline  
            counter  =1
    return text
