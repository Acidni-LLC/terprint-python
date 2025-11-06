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
#my_list = ["83677_0007673514","82188_0007746062","81684_0007732559","81143_0007687420","81131_0007687687","76642_0007838512","65053_0007733301","61128_0007614549","83536_0007540972","80965_0007871794","71035_0007701647","75837_0007782313","83669_0007771992","82188_0007453524","80965_0007838513","76618_0007653473","79441_0007605403","76642_0007825663","79086_0007392383","69670_0007816069","71247_0007816068","71034_0007685949","61128_0007653200","83536_0007771203","79041_0007757408","76506_0007814988","88373_0007768322","84573_0007917595","79112_0007861686","41839_0007673539","83537_0007584635","82462_0007768510","82049_0007871793","76757_0007641641","81283_0007616623","79080_0007757408","80205_0007563253","76505_0007722540","75785_0007429590","75781_0007812531","75838_0007792608","75567_0007939541","74556_0007815392","74576_0007826214","73983_0007782311","73727_0007711677","71320_0007770949","72986_0007616857","72985_0007653554","72984_0007541011","69669_0007711628","70912_0007630058","71029_0007584610","68679_0007616627","68684_0007711699","69353_0007514153","68187_0007894511","67988_0007815114","68682_0007452924","68673_0007769184","68686_0007894512","59710_0007916124","67990_0007861292","59725_0007630100","59721_0007894089","59703_0007828047","67194_0007614543","67192_0007530233","67342_0007849586","67340_0007562321","67325_0007871796","18347_0007653567","66760_0007519756","64813_0007485370","64809_0007813112","63549_0007673675","61129_0007424983","61123_0007246497","59680_0007685956","59663_0007453562","58723_0007426355","56975_0007814983","50657_0007514205","49447_0007541022","46768_0007838611","24134_0007313363","18363_0007530174","18275_0007463761","83699_0007828103","81283_0007689754","79137_0007861291","79080_0007861679","80205_0007848631","70912_0007771215","69353_0007598101","67988_0007616849","68188_0007673697","59721_0007848417","67065_0007860767","58739_0007733523","58723_0007541012","50657_0007757621","18275_0007450575","84573_0007689763","83537_0007746082","82049_0007429610","79080_0007541026","80205_0007813108","79099_0007629764","71223_0007814973","75785_0007290685","73983_0007711504","71320_0007465823","72985_0007562320","72984_0007653555","72982_0007798034","69669_0007816069","71030_0007354228","71029_0007509347","68679_0007475377","68684_0007732567","68683_0007405291","68682_0007861296","68673_0007641972","68686_0007848415","59814_0007353476","67194_0007584970","67342_0007641487","67335_0007530209","64813_0007595473","64809_0007768258","63534_0007519748","50657_0007540652","49447_0007838367","46768_0007826447","43670_0007313365","18275_0007402750","84605_0007768331","82049_0007861297","79080_0007653760","76505_0007734156","71320_0007892812","72985_0007530225","72984_0007745899","67342_0007861293","57901_0007813111","81283_0007538669","80205_0007616847","76505_0007734157","67194_0007541009","83537_0007771994","76757_0007768507","79099_0007475608","75567_0007616845","67988_0007584874","68673_0007746253","59721_0007575033","49447_0007803309","46768_0007927735","79132_0007861294","76505_0007757622","74556_0007605467","74576_0007771989","68684_0007711717","67988_0007514131","68186_0007814913","59814_0007366578","67325_0007745914","58723_0007442383","56976_0007814985","75792_0007519660","68673_0007905940","82049_0007905680","81474_0007701644","71320_0007758370","67340_0007673898","66760_0007403890","64809_0007643290","82803_0007860766","79137_0007653480","71232_0007816068","74556_0007711608","71320_0007848413","59814_0007803308","76757_0007746071","18275_0007429612","82049_0007674240","68683_0007173428","58739_0007861611","18329_0007630532","68186_0007378049","68677_0007355142","59721_0007314474","60421_0007293728","67192_0007101697","67342_0007290175","67279_0007221337","49447_0007119352"]
#my_list = ["47993_0006162867"]
#dispensary="Trulieve"
#dispensaryid=1
my_list = ["gbxxJoq4GqJcnLw","WQiipC7sQpiyojx","XF4zAKoQj8yCx3p","fmNHWqZYycqDAgd","j5XgcqBirTe85nG","zpyWAj3mMeADHCt","dfA63am93BqkAeR","ABbmjHwkrRK5F4e","iCm33pB7LjWnd5q","zDF5f7E6ggrca73","Ay2ZkZyeQNDjyfa","nP7REAQ5aQ4RYW2","6DMQwXFGMqs8zX5","4REmwgHG6A5fwcL","9yWQQm4aaRsgHNa","cZLTKTn3yTTJe7P","LF66JqZy3mMr4wy","r87Bi5xrLPpCSfo","xCZ57p6SmP4GkFP","dS6zKbP9cGmtNEY","y8YBxxsizxsCHRE","dnyP2drMTRyw87E","Yad7LeWTiqZc3Jm","je5X9ECWdoC6w4o","NgBasfHjWkQecKP"]
# # #my_list = ["SfWBtnDxrN9qs2t"]
dispensary="Sunburn"
dispensaryid=2
totalbatches = my_list.__len__()
batchescount = 0
#if dispensaryid ==2:
#       downloadfile(my_list,dispensaryid)
for item in my_list:
    batch = ""
    batchescount = batchescount + 1
    print (f"{bcolors.OKBLUE} batch {str(batchescount)} {item+bcolors.ENDC} of {bcolors.OKBLUE}  {str(totalbatches)} : {item+bcolors.ENDC}")
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
        
        local_path ='C:/Users/JamiesonGill/source/repos/Acidni-LLC/Terprint/Terprint.Python/files/test_output'
        local_pathandPDFfile = local_path +'/'+ local_filename
        if os.path.exists(local_pathandPDFfile):
            print(f"File '{local_pathandPDFfile}' already exists.")
        # continue
            # If you want to redownload the file even if it exists, set redownload to 1
            # redownload = 1
        else:
            print(f"File '{local_pathandPDFfile}' does not exist. It will be downloaded.")
            missingfile = 1


        if redownload == 1 or missingfile == 1:
            try:
                headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
                }
                response = requests.get(url, headers=headers, stream=True, timeout=10)  # Use stream=True for large files
                response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
                with open(local_pathandPDFfile, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"File '{local_pathandPDFfile}' downloaded successfully.")
 

            except requests.exceptions.RequestException as e:
                print(f"Error downloading file: {local_pathandPDFfile} {e}")


        #https://www.trulieve.com/content/dam/trulieve/en/lab-reports/84573_0007311573.pdf?download=true
        backslashpath = "C:\\Users\\JamiesonGill\\source\\repos\\Acidni-LLC\\Terprint\\Terprint.Python\\files\\test_output\\"
        pdf_path = "C:\\Users\\JamiesonGill\\source\\repos\\Acidni-LLC\\Terprint\\Terprint.Python\\files\\test_output\\"+batch+".pdf"
       # pdf_path = local_path
        def extract_text_from_pdf(local_pathandfile):
            print("extracting text from " +pdf_path)
            """Extracts all text from a PDF file."""
            text = ""
            try:
                with fitz.open(pdf_path) as doc:
                    for page in doc:
                        text += page.get_text()
                print("text extracted")
            except Exception as e:
                print(f"Error extracting text: {e}")
            return text


        try:
            

            format = 0
            print(bcolors.OKGREEN + "BEGIN format:" + str(format) + bcolors.ENDC)
            #Example usage
            extracted_text = extract_text_from_pdf(local_pathandPDFfile)
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
            local_pathandExtractAllfile =local_path+"/"+ batch+"_extractall.txt"
            with open(local_pathandExtractAllfile, "w", encoding='utf-8') as f:
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

                with open(backslashpath+str(format)+"\\terpenes\\"+batch+"_terpenes.txt", "w", encoding='utf-8') as f:
                    outputtext =  terpenetext            
                    f.write(outputtext)
                with open(backslashpath+str(format)+"\\cannabinoids\\"+batch+"_cannabinoids.txt", "w", encoding='utf-8') as f:
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
        
                with open(backslashpath+str(format)+"\\terpenes\\"+batch+"_terpenes.txt", "w", encoding='utf-8') as f:
                    outputtext =  terpenetext            
                    f.write(outputtext)
                with open(backslashpath+str(format)+"\\cannabinoids\\"+batch+"_cannabinoids.txt", "w", encoding='utf-8') as f:
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
        
                with open(backslashpath+str(format)+"\\terpenes\\"+batch+"_terpenes.txt", "w", encoding='utf-8') as f:
                    outputtext =  terpenetext            
                    f.write(outputtext)
                with open(backslashpath+str(format)+"\\cannabinoids\\"+batch+"_cannabinoids.txt", "w", encoding='utf-8') as f:
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
        
                with open(backslashpath+str(format)+"\\terpenes\\"+batch+"_terpenes.txt", "w", encoding='utf-8') as f:
                    outputtext =  terpenetext            
                    f.write(outputtext)
                with open(backslashpath+str(format)+"\\cannabinoids\\"+batch+"_cannabinoids.txt", "w", encoding='utf-8') as f:
                    outputtext = cannabinoidtext            
                    f.write(outputtext)
                                    

        except Exception as e:
            exception_message = str(e)
            exception_type, exception_object, exception_traceback = sys.exc_info() 
            print  (item + ":" + str(format) + ":"+str(exception_traceback.tb_lineno) +" Error:", e  )
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
