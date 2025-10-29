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
my_list = ["88372_0007733521","83669_0007814909","82188_0007746062","80965_0007838513","59765_0007826464","76642_0007825663","79086_0007392383","71035_0007701647","65053_0007733301","65045_0007653393","61128_0007614549","79081_0007814998","83669_0007814910","83536_0007540972","76642_0007838512","71247_0007816068","76506_0007814988","74541_0007815392","65217_0007814983","83669_0007685990","83536_0007475961","82188_0007453524","80965_0007514146","76618_0007653473","79041_0007757408","79441_0007605403","75839_0007653555","69670_0007816069","65219_0007814985","63991_0007701090","59765_0007519732","65201_0007815003","83536_0007475408","84605_0007768331","84994_0007685832","24127_0007894509","41839_0007673539","83537_0007584635","82462_0007768510","82049_0007871793","76757_0007768507","81474_0007701644","81283_0007616623","79137_0007861291","79080_0007757408","80205_0007563253","71223_0007814973","76505_0007722540","75785_0007429590","75781_0007768294","75567_0007616845","74556_0007815392","74576_0007826214","73983_0007782311","73727_0007711677","71320_0007848413","72985_0007653554","72984_0007541011","69669_0007711628","70912_0007630058","68679_0007616627","68684_0007732567","69353_0007514153","67988_0007584874","68683_0007405291","68682_0007861296","68673_0007641972","68686_0007826463","68188_0007673697","59710_0007475372","67990_0007861292","59725_0007630100","59721_0007848417","59703_0007828047","67194_0007584970","67342_0007849586","67340_0007562321","18347_0007653567","66760_0007519756","64813_0007595473","64809_0007768258","63549_0007673675","61129_0007424983","61123_0007246497","59680_0007685956","59663_0007453562","58723_0007426355","57901_0007813111","56975_0007814983","56967_0007860769","50657_0007514205","49447_0007541022","46768_0007838611","24134_0007313363","18363_0007530174","18275_0007463761","83699_0007828103","76757_0007746071","79099_0007475608","71219_0007860768","71320_0007465823","72984_0007653555","70912_0007771215","68679_0007425739","68682_0007452924","67542_0007475384","67192_0007530233","67329_0007130897","63715_0007860770","63534_0007519748","58739_0007733523","58723_0007541012","56976_0007814985","56972_0007815003","50657_0007757621","18275_0007450575","88347_0007871804","84994_0007871798","83537_0007746082","82049_0007429610","81468_0007465823","79080_0007541026","80205_0007813108","79099_0007629764","75785_0007354936","75567_0007673680","74576_0007353492","73983_0007711504","72986_0007733531","72985_0007562320","72982_0007798034","69669_0007816069","71030_0007354228","71029_0007509347","68679_0007475377","68684_0007711717","68920_0007687076","68686_0007771993","59721_0007894089","59814_0007353476","67194_0007541009","67342_0007641487","67335_0007530209","67325_0007871796","65044_0007425721","64813_0007584712","60436_0007687376","58739_0007861611","58723_0007442383","50657_0007540652","49447_0007838367","46768_0007826447","43670_0007313365","18275_0007402750","82049_0007861297","76757_0007641641","79080_0007653760","80205_0007848631","76505_0007734156","75785_0007290685","72985_0007530225","68679_0007221624","68684_0007711699","67988_0007815114","81283_0007538669","80205_0007584617","76505_0007734157","68683_0007173428","68673_0007746253","68686_0007848415","64809_0007813112","59664_0007711650","71232_0007816068","75792_0007519660","71320_0007892812","67988_0007828086","68682_0006969917","68673_0007732574","59721_0007575033","59814_0007803308","67325_0007745914","83537_0007475951","74556_0007605467","74576_0007771989","73983_0007848416","67988_0007514131","68186_0007771990","59814_0007366578","18275_0007429612","68186_0007814913","71320_0007758370","66760_0007403890","79137_0007653480","74556_0007711608","83699_0007746079","67342_0007861293","18363_0007224250","81283_0007689754","71223_0007711623","69669_0007653121","68679_0007342760","18329_0007630532","67330_0007519694","80205_0007562480","68186_0007378049","68677_0007355142","59721_0007314474","60421_0007293728","67192_0007101697","67342_0007290175","67279_0007221337","57901_0007452411","49447_0007119352"]
#my_list = ["19208_0007314750"]
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
                format = 2
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

    ###FORMAT 2222222222222222222222222222


            elif format == 3:


            ###FORMAT 222222222222222222222222222

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
