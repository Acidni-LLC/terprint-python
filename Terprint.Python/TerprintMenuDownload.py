from pydoc import text
import fitz # PyMuPDF
import requests
import sys
import os
from bs4 import BeautifulSoup
import batchFromUrl
import COADataModel
from COA_MethodDataExtractor import COA
from COA_ACS_Simple import ACS_COA_Simple
from COA_ModernCanna01 import ModernCanna_COA

from sqlConnection import insertcannabinoids, insertterpenes, checkTerpene, checkCannabinoid, insertBatch
from bcolors import bcolors

#from downloadFile import downloadfile

separator ="|"
redownload = 0
my_list = ["88373_0007976197","84605_0007838588","83537_0007771994","82049_0007871793","76757_0007641641","81283_0007616623","79080_0007757408","80205_0007584617","71223_0007917546","76505_0007734157","75785_0007429590","75781_0007812531","75838_0007826259","75084_0007768280","74556_0007815392","74576_0007826214","73727_0007745861","71320_0007905682","72985_0007653554","72984_0007745899","71209_0007803305","70912_0007630058","71029_0007584610","67988_0007828086","68186_0007653750","68682_0007452924","68673_0007771213","68677_0007976196","68686_0007861609","67990_0007782363","59725_0007630100","59721_0007916123","67194_0007614543","67192_0007530233","67342_0007849586","67340_0007562321","67325_0007871796","67236_0007861610","18347_0007653567","66760_0007519756","64809_0007616625","63549_0007673675","58739_0007927439","58723_0007826261","56975_0007814983","50657_0007514205","49447_0007541022","46768_0007965176","24134_0007313363","18275_0007463761","82803_0007917542","84573_0007746218","83537_0007563272","81283_0007689754","79080_0007861679","80205_0007848631","76505_0007771991","75785_0007487330","75084_0007937997","71320_0007770949","72986_0007616857","69669_0007917621","70912_0007771215","69353_0007598101","68187_0007451732","68686_0007711509","59721_0007848417","67342_0007861293","67340_0007673898","67325_0007745914","63868_0007562376","61123_0007246497","59664_0007965308","58723_0007541012","56976_0007917548","56974_0007917544","50657_0007540652","49447_0007803309","46768_0007927735","84573_0007814969","83537_0007746082","82049_0007674240","80205_0007563253","79099_0007475608","76505_0007722540","75785_0007290685","75838_0007792608","75567_0007939541","73983_0007782311","71320_0007848413","72985_0007530225","72984_0007541011","69669_0007816069","71029_0007509347","68679_0007575046","69353_0007514153","67988_0007916422","68673_0007905940","68686_0007894512","59710_0007509349","67990_0007746016","59721_0007575033","59814_0007353476","67194_0007584970","67236_0007895791","67065_0007860767","59663_0007453562","58739_0007711502","58723_0007426355","46768_0007826447","43670_0007313365","18275_0007429612","80205_0007616847","75084_0007562476","69661_0007861700","68679_0007616627","67988_0007616849","68673_0007953957","59725_0007687418","67325_0007892809","18275_0007976638","81283_0007538669","67194_0007541009","79112_0007861686","83537_0007927819","81312_0007614538","76505_0007734156","75781_0007848428","75838_0007848659","18363_0007530174","84605_0007768331","82049_0007905680","79099_0007629764","71218_0007815394","76505_0007757622","75838_0007769182","74556_0007605467","71030_0007354228","67988_0007514131","68682_0007861296","59703_0007828047","61129_0007450580","56976_0007814985","82462_0007768510","59814_0007366578","67342_0007509324","63534_0007519748","46768_0007838611","41839_0007673539","76757_0007768507","75792_0007519660","74576_0007771989","69669_0007711628","68186_0007814913","59680_0007685956","50657_0007564075","69665_0007861694","66760_0007403890","58723_0007442383","18275_0007450575","61129_0007424983","59814_0007803308","67342_0007641508","58739_0007861611","50657_0007220619","18329_0007630532","74556_0007711608","71320_0007892812","68186_0007378049","68686_0007848415","59721_0007475993","67342_0007641487","57901_0007813111"]
#my_list = ["47993_0006162867"]
dispensary="Trulieve"
dispensaryid=1      
#my_list = ["AfCP8Lj3XkzHems","REYxZB8sRQ4KwKG","NJiRDgnPDYBtAnX","XF4zAKoQj8yCx3p","fmNHWqZYycqDAgd","dfA63am93BqkAeR","ABbmjHwkrRK5F4e","ERHxaFsjM9pyotE","iCm33pB7LjWnd5q","KTcZ6JgHdpqoAEx","zDF5f7E6ggrca73","Ay2ZkZyeQNDjyfa","nP7REAQ5aQ4RYW2","5RzcEb3k8B4ALo4","dxDjCKX2xmAwYtW","6DMQwXFGMqs8zX5","4REmwgHG6A5fwcL","6T5P2wJxs4sBAR4","9yWQQm4aaRsgHNa","cZLTKTn3yTTJe7P","r87Bi5xrLPpCSfo","xCZ57p6SmP4GkFP","y8YBxxsizxsCHRE","mj6WiyWX8HiAFxE","Yad7LeWTiqZc3Jm"]
#my_list = ["AfCP8Lj3XkzHems"]
# dispensary="Sunburn"
# dispensaryid=2
productType ="Flower"
totalbatches = my_list.__len__()
batchescount = 0
#if dispensaryid ==2:
#       downloadfile(my_list,dispensaryid)ter

bigindex = 0

for item in my_list:
    batchin = item
    batch = batchin
    batchescount = batchescount + 1
    print (f"{bcolors.OKGREEN} batch {batchin}  {bcolors.ENDC}- {bcolors.OKBLUE}{str(batchescount)} {bcolors.ENDC} of {bcolors.OKBLUE}  {str(totalbatches)}  {bcolors.ENDC}")
    missingfile = 0
    bigindex=bigindex+1
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
                format = 1  # ACS  81410_0007711669  #ACS_COA_Simple.py  trulieve 
            elif "Accreditation #102020" in extracted_text:
                #mcs 
                if "Total Cannabinoids" in extracted_text:
                    format = 2  # example 74941_0007653489  ModernCanna_COA trulieve
                elif "Total Active Cannabinoids" in extracted_text:
                    format = 4  # example 47993_0006162867  trulieve  COA_ModernCanna01.py
            elif "Method Testing Laboratories" in extracted_text: #sunburn sample 6DMQwXFGMqs8zX5 
                format = 3
                #Method Testing Laboratories COAMethodDataExtractor.py   COA_2510CBR0031-006

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

            if format == 1:  # ACS  81410_0007711669  #COA_ACS_Simple.py

            #FORMAT 111111111111111111111111111
                coa = ACS_COA_Simple.from_text(extracted_text)
                
                json_text = coa.to_json1() 
                #print("\n\n"+json_text+"\n\n")
                batchName = coa.order_number +"_"+ batchin
                batchid =  insertBatch(
                    coa, productType, 
                    dispensaryid, "jgill@acidnillc.onmicrosoft.com",json_text, batchin,coa.total_terpenes_percent,coa.total_cannabinoids_percent,coa.batch_date,coa.cultivar)
            # print("1\n"+terpenetext)
                #print(extracted_text)
                counter =1
                outputline = ""
                outputlines = ""
                newcan = 0 
                
                counter = 1
                position = 1
                index=1
            # print(terpenetext)
                skip = True
                outputlines ="Batch"+separator+"Index"+separator+"Terpene"+separator+"Result"+separator+"Percent"
                for line in coa.terpenes:    
                    
                    
                        outputline =  batch + "|"+str(index)+"|" + line.name + "|" + str(line.result_mg_per_g) + "|" + str(line.result_percent)
                        
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
                                    "jgill@acidnillc.onmicrosoft.com",
                                    batchid)
                        outputlines = outputlines+  "\n"+  outputline                     
                        outputline = ""
                        counter = 0                
                        position = position + 1                
                        index = index +1
            
                

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
                for line in coa.potency_analytes:
                    
                    outputlines ="Batch"+separator+"Index"+separator+"Cannabinoid"+separator+"Dilution"+separator+"LOD"+separator+"LOQ"+separator+"Result"+separator+"Percent\n"
                    setheader=False
                    outputline = batchin + separator+str(position)+separator+line.name +separator+ str(line.dilution)+separator+ str(line.lod_percent)+separator+ str(line.loq_percent)+separator+ str(line.result_mg_per_g)+separator+ str(line.result_percent) +"\n"

                        
                    print("-----")
                    print (outputline)
                    print("-----") 
                    insertcannabinoids(
                                    outputline.split(separator)[0],
                                    outputline.split(separator)[1],
                                    outputline.split(separator)[2],
                                    outputline.split(separator)[7],
                                    outputline.split(separator)[6], 
                                    dispensaryid,
                                    "jgill@acidnillc.onmicrosoft.com",
                                    batchid)
                    outputlines = outputlines + outputline
                    outputline=""
                    counter = 0
                    position = position + 1
                    counter = counter + 1

                with open(backslashpath+str(format)+"\\terpenes\\"+batch+"_terpenes.txt", "w", encoding='utf-8') as f:
                    outputtext =  terpenetext            
                    f.write(outputtext)
                with open(backslashpath+str(format)+"\\cannabinoids\\"+batch+"_cannabinoids.txt", "w", encoding='utf-8') as f:
                    outputtext = cannabinoidtext            
                    f.write(outputtext)
            
            ###FORMAT 2222222222222222222222222222


            elif format == 2:  # example 74941_0007653489  COA_ModernCanna01.py


            ###FORMAT 222222222222222222222222222


                coa2 = ModernCanna_COA.from_text(extracted_text)
                
                json_text = coa2.to_json() 
                #print("\n\n"+json_text+"\n\n")
                batchName =  batchin
                batchid =  insertBatch(
                    coa2, productType, 
                    dispensaryid, "jgill@acidnillc.onmicrosoft.com",json_text, batchName,coa2.total_terpenes_percent,coa2.total_active_cannabinoids_percent,coa2.received_date,coa2.cultivar)
                
           
                index = 1
                outputlines ="Batch"+separator+"Index"+separator+"Cannabinoid"+separator+"Percent"+separator+"Milligrams\n"
                for line in coa2.cannabinoids:
                  
                        outputline = batch + "|"+str(index)+"|" +line.name + "|" +str(line.percent) + "|" + str(line.mg)   +"\n"
                        # print ("+++++++++++++++++++++++++++++++++++++++++++++++\n")
                        # print(outputline+"\n")
                        # print ("-----------------------------------------------\n")
                    # outputline = outputline.split(separator)[0] +    "," + outputline.split(separator)[1] +    "," + outputline.split(separator)[2]+    "," + outputline.split(separator)[3] +    "," + outputline.split(separator)[4]      
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
                                        "jgill@acidnillc.onmicrosoft.com",
                                        batchid)
                        outputline=""
                        counter = 0
                        index=index+1 
 
                    
    
                outputlines=""
                counter = 1
                skip = True
                terp = ""
                skip = True
                index = 1
                setheader = True
                for line in coa2.terpenes:    
                    outputlines ="Batch"+separator+"Index"+separator+"Terpene"+separator+"Percent\n"
                    
                                            
                    outputline = batch + "|" + str(index)+"|" + line.name + "|" + str(line.percent)
                    insertterpenes(
                                    outputline.split(separator)[0],
                                    outputline.split(separator)[1],
                                    outputline.split(separator)[2],
                                    outputline.split(separator)[3], 
                                    0,                                        
                                    dispensaryid,
                                    "jgill@acidnillc.onmicrosoft.com",
                                    batchid)
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


            elif format == 3: # COA_MethodDataExtractor.py    sunburn


                 #new code to use extractor class

                extracted_text = extract_text_from_pdf(pdf_path)
                coa3 = COADataModel.Batch.from_text(extracted_text) 
                json_text = coa.to_json() 
                print("\n\n"+json_text+"\n\n")
                batchName = coa3.order_number +"_"+ batchin
                batchid =  insertBatch(
                    coa3, productType, 
                    dispensaryid, "jgill@acidnillc.onmicrosoft.com",json_text, batchName,
                    coa3.total_terpenes_percent,
                    coa3.total_cannabinoids_percent,
                    coa3.batch_date,
                    coa3.cultivars[0] if coa3.cultivars else "")
            # print(extracted_text)
            # with open(batch+"_extractall.txt", "w", encoding='utf-8') as f:
                # f.write(extracted_text)
                    
            # # print("2wrote text:\n")
            #     terpenetext = extracted_text.split("(ug/g)\n%", maxsplit=1)[1]
            #     terpenetext = terpenetext.split("                              Total Terpenes", maxsplit=1)[0]    

            # #  print("3found terpenes:\n")
                
            #     #terpenetext = extract_text_from_pdf(terpenetext)

            #     cannabinoidtext = extracted_text1.split("mg/unit", maxsplit=1)[1]
            #     cannabinoidtext  =cannabinoidtext.split("Sample Analyzed By", maxsplit=1)[0]

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
                
        #CANNABINOIDS
                outputlines = ""
                
                for cannabinoid in coa3.potency_analytes:
                    outputline = ""
                    outputline = batch +"_"+ batchin +separator+  str(index) + separator+ cannabinoid.name + separator + str(cannabinoid.percent) + separator + str(cannabinoid.mg_per_unit) +    "\n"
                    # print(cannabinoid.name + " " + str(cannabinoid.percent) + " " + str(cannabinoid.mg_per_unit))
                    
                    outputlines = outputlines +  outputline 
                    
                    index = index+ 1
                    print ("+++++++++++++++++++++++++++++++++++++++++++++++\n")
                    print(bcolors.OKCYAN + outputline + bcolors.ENDC +"\n")
                    print ("-----------------------------------------------\n")
                    insertcannabinoids(
                                    outputline.split(separator)[0],
                                    outputline.split(separator)[1],
                                    outputline.split(separator)[2],
                                    outputline.split(separator)[4],
                                    outputline.split(separator)[3],           
                                    dispensaryid,
                                    "jgill@acidnillc.onmicrosoft.com",
                                    batchid)
                 

                cannabinoidtext = outputlines
                    
    
        #TERPS
                outputlines=""
                counter = 1
                skip = True
                terp = ""
                position = 1
                skip = True
                index = 1
                setheader = True
                outputlines ="Batch"+separator+"Index"+separator+"Terpene"+separator+"(ug/g)"+separator+"Percent\n"
                for terp in coa3.terpenes:
                    outputline = ""
                    outputline =  batch +"_"+ batchin +separator+  str(index) + separator+ terp.name + separator + str(terp.result_ug_per_g) + separator + str(terp.percent) +    "\n"
                    # print(terp.name + " " + str(terp.ug_per_g) + " " + str(terp.percent_of_total))
                    
                    print ("+++++++++++++++++++++++++++++++++++++++++++++++\n")
                    print(bcolors.OKGREEN + outputline + bcolors.ENDC +"\n")
                    print ("-----------------------------------------------\n")
                    insertterpenes(
                                    outputline.split(separator)[0],
                                    outputline.split(separator)[1],
                                    outputline.split(separator)[2],
                                    outputline.split(separator)[4], 
                                    outputline.split(separator)[3],
                                    dispensaryid,
                                    "jgill@acidnillc.onmicrosoft.com",
                                    batchid)
                    outputlines = outputlines + outputline
                    index=index+1
                terpenetext = outputlines
        
                with open(backslashpath+str(format)+"\\terpenes\\"+batch+"_terpenes.txt", "w", encoding='utf-8') as f:
                    outputtext =  terpenetext            
                    f.write(outputtext)
                with open(backslashpath+str(format)+"\\cannabinoids\\"+batch+"_cannabinoids.txt", "w", encoding='utf-8') as f:
                    outputtext = cannabinoidtext            
                    f.write(outputtext)


    ###FORMAT 444444444444444444
            
            elif format == 4:  #  COA_ModernCanna01.py   47993_0006162867 trulieve

                
                extracted_text = extract_text_from_pdf(pdf_path)
                extracted_text1 = extracted_text
                coa4 = ModernCanna_COA.from_text(extracted_text) 
                
                json_text = coa4.to_json() 
                print("\n\n"+json_text+"\n\n")
                
                batchid =  insertBatch(
                    coa4, productType, 
                    dispensaryid, "jgill@acidnillc.onmicrosoft.com",json_text, batch,
                    coa4.total_terpenes_percent,
                    coa4.total_cannabinoids_percent,
                    coa4.sample_date,
                    coa4.sample_alias)
                
                index = 1
                outputlines ="Batch"+separator+"Index"+separator+"Cannabinoid"+separator+"Percent"+separator+"Milligrams\n"
                for line in coa4.cannabinoids:
                    outputline = ""
                    outputline = batch + "|"+str(index)+"|" +line.name + "|" +line.percent + "|" + line.mg   +"\n"
                    # print ("+++++++++++++++++++++++++++++++++++++++++++++++\n")
                    
                    outputlines = outputlines + outputline
                    
                    insertcannabinoids(
                                    outputline.split(separator)[0],
                                    outputline.split(separator)[1],
                                    outputline.split(separator)[2],
                                    outputline.split(separator)[3],
                                    0, 
                                    dispensaryid,
                                    "jgill@acidnillc.onmicrosoft.com",
                                    batchid,
                                    coa)
                    outputline=""
                    counter = 0
                    position = position + 1
                    index=index+1
                    
                    counter = counter + 1

    
                outputlines=""
                counter = 1
                skip = True
                terp = ""
                position = 1
                skip = True
                index = 1
                outputlines ="Batch"+separator+"Index"+separator+"Terpene"+separator+"Percent\n"
                percent=""
                setheader = True
                for line in coa4.terpenes :   
                                          
                    outputline = batch + "|"+str(index)+"|" +line.name + "|" + str(line.percent)+"\n"
                    
                    outputlines = outputlines + outputline
                
                    insertterpenes(
                                    outputline.split(separator)[0],
                                    outputline.split(separator)[1],
                                    outputline.split(separator)[2],
                                    outputline.split(separator)[3],
                                    0, 
                                    dispensaryid,
                                    "jgill@acidnillc.onmicrosoft.com",
                                    batchid)
                    outputline="" 
                    position = position + 1
                    index=index+1 
                     
        
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
