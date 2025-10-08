from pydoc import text
import fitz # PyMuPDF
import requests
import sys
import os

redownload = 0
my_list = ["19208_0007314750", "83669_0007745913", "80965_0007745916", "65053_0007733301", "83677_0007330088", "76618_0007768257", "79117_0007758380", "83669_0007685990", "83667_0007685819", "82456_0007758367", "82188_0007354943", "81684_0007685815", "76618_0007605401", "79441_0007540872", "69670_0007711628", "63991_0007630058", "61130_0007616599", "71035_0007673682", "83669_0007771992", "83536_0007475408", "76618_0007605405", "65197_0007758388", "32158_0007424997", "84994_0007673528", "84600_0007745786", "84573_0007673661", "83537_0007746082", "82462_0007768510", "82388_0007540963", "76757_0007746071", "81283_0007538669", "79080_0007653760", "80205_0007563253", "79099_0007629764", "76505_0007734156", "75785_0007290685", "75792_0007519660", "75567_0007673680", "74556_0007605467", "74576_0007771989", "73983_0007815080", "71320_0007465823", "72986_0007733531", "72985_0007653554", "72984_0007653555", "69669_0007711628", "70912_0007630058", "71029_0007509347", "68679_0007616627", "69353_0007514153", "67988_0007815114", "68683_0007405291", "68673_0007641972", "68920_0007514209", "59814_0007803308", "59703_0007828047", "67194_0007584970", "66760_0007519756", "65044_0007425721", "64813_0007584712", "63549_0007673675", "63534_0007519748", "61123_0007246497", "59663_0007366912", "58739_0007674831", "58723_0007426355", "57901_0007452411", "50657_0007757621", "43670_0007313365", "18275_0007402750", "79080_0007757408", "76505_0007734157", "72985_0007530225", "69661_0007758381", "68186_0007814913", "67542_0007450809", "67192_0007426356", "67335_0007377969", "67065_0007758388", "64813_0007614563", "64809_0007768258", "59663_0007453562", "57901_0007813111", "46768_0007826447", "18275_0007429612", "82187_0007673698", "82049_0007733517", "76757_0007768507", "81468_0007465823", "81283_0007516400", "79080_0007541026", "80205_0007562480", "79099_0007475608", "71223_0007595505", "75785_0007354936", "74556_0007711608", "74576_0007290699", "72985_0007562320", "69669_0007816069", "71030_0007354228", "68679_0007475377", "67988_0007687378", "68683_0007173428", "67661_0007689072", "59721_0007314474", "59814_0007353476", "59703_0007137826", "67542_0007485904", "67194_0007541009", "67342_0007641487", "66883_0007099065", "66760_0007403890", "60436_0007687376", "58723_0007442383", "50657_0007540652", "35299_0007814914", "18365_0007450194", "81283_0007616623", "68186_0007771990", "68686_0007771993", "59710_0007354081", "59721_0007815081", "67542_0007463774", "83537_0007475951", "67988_0007514131", "68186_0007378049", "64809_0007758366", "71320_0007758370", "69669_0007595504", "68679_0007575046", "59814_0007366578", "64813_0007548780", "58739_0007584969", "57901_0007366503", "79132_0007758376", "75567_0007757098", "74576_0007353492", "59721_0007509345", "60421_0007293728", "67340_0007489243", "67325_0007745914", "46768_0007673495", "18363_0007224250", "82187_0007653475", "67542_0007452774", "80205_0007813108", "59710_0007298356", "71232_0007711627", "64813_0007485370", "56976_0007711617", "58739_0007562483", "49447_0007426354", "18329_0007630532", "67330_0007519694", "82187_0007584922", "67342_0007641508", "69669_0007653121", "60421_0007161154", "24134_0007208753", "79376_0007381188", "67323_0006923509", "77745_0007074998", "74576_0007008133", "73983_0007653505", "72982_0007686034", "68677_0007313329", "68746_0007392420", "67192_0007101697", "67342_0007290175", "67336_0007197539", "67279_0007221337", "59663_0007185119", "49447_0007119352", "40866_0007119277"]
#my_list = ["COA_2504CBR0142-002",
# "COA_2505CBR0142-006",
# "COA_2507CBR0098-003",
# "COA_2508CBR0020-002",
# "COA_2508CBR0048-001",
# "COA_2508CBR0092-006",
# "COA_2508CBR0145-003",
# "COA_2508CBR0161-004",
# "COA_2509CBR0001-004",
# "COA_2509CBR0029-002",
# "COA_2509CBR0058-001",
# "COA_2509CBR0058-004",
# "COA_2509CBR0058-005",
# "COA_2509CBR0074-001",
# "COA_2509CBR0103-001",
# "COA_2509CBR0103-002",
# "COA_2509CBR0103-004",
# "COA_2509CBR0117-001",
# "COA_2509CBR0117-003",
# "COA_2509CBR0117-005",
# "COA_2509CBR0152-002",
# "COA_2509CBR0152-005",
# "COA_2509CBR0152-009",
# "COA_2509CBR0179-001",
# "COA_2509CBR0179-002",
# "COA_2509CBR0179-002"

# ]
#dispensary="Sunburn"
for item in my_list:
    missingfile = 0
    
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
            response = requests.get(url, stream=True)  # Use stream=True for large files
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

            with open(local_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"File '{local_filename}' downloaded successfully.")

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
        print("BEGIN format:" + str(format))
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

        print("END format:" + str(format))
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
                if skip == True:
                    outputlines ="Batch,Index,Terpene,Result,Percent"
                    skip = False
                    continue
                if counter  ==1 :
                    outputline =  batch + ","+str(position)+"," + line 
                    #outputline =   terp + "," + str(percent)+ "|" +  str(counter) + "|"
                elif counter  == 2:
                    outputline = outputline + ","+ line
                elif counter  == 3:
                    outputline = outputline + ","+ line
                    outputlines = outputlines+  "\n"+  outputline                     
                    outputline = ""
                    counter = 0                
                    position = position + 1                
                counter = counter  + 1
            # for line in terpenetext.splitlines():
            #     if counter == 3:
            #         outputline = "\n"+ outputline + " " + line  
            #         outputlines = outputlines + " " + outputline
            #         outputline=""
            #         counter  = 1
            #     elif counter == 1:                
            #         outputline =   outputline 
            #         outputline = outputline + " " + line 
            #         counter = counter + 1
            #     else:
            #         outputline = outputline + " " + line
            #         counter = counter + 1

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
                # if skip == True:
                #     outputlines ="Batch,Index,Cannabinoid,Dilution,LOD,LOQ,Result,Percent\n"
                #     skip = False
                #     outputline =   line 
                #     continue
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
                    if setheader == True:
                        outputlines ="Batch,Index,Cannabinoid,Dilution,LOD,LOQ,Result,Percent\n"
                        setheader=False
                    outputline = batch + ", "+str(position)+", " +line +" "+ outputline

                elif counter <6:
                    outputline = outputline + ", "+  line 
                elif counter ==6:
                    outputlines = outputlines +  outputline + ", "+  line + "\n"
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

            cannabinoidtext = extracted_text1.split("POTENCY SUMMARY (As Received)", maxsplit=1)[1]
            cannabinoidtext  =cannabinoidtext.split("TERPENES SUMMARY (Top Ten)", maxsplit=1)[0]

            outputlines = ""
            outputline = ""
            c= 1
            can=""
            percent=""
            outputlines = ""
            c= 1
            position = 1
            skipcount = 6
            index = 1
            for line in cannabinoidtext.splitlines():
                if position == skipcount:
                    outputlines ="Batch,Index,Cannabinoid,Percent,Milligrams\n"
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
                    outputline = batch + ", "+str(index)+", " +line 

                elif counter <3:
                    outputline = outputline + ", "+  line 
                elif counter ==3:
                    outputlines = outputlines +  outputline + ", "+  line + "\n"
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
                        outputlines ="Batch,Index,Terpene,Percent\n"
                        setheader=False
                    terp = batch + ", " + str(index)+", " + line
                    outputline =   terp + "," + percent
                    outputlines = outputlines+ outputline+  "\n"
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
                if position == skipcount:
                    outputlines ="Batch,Index,Cannabinoid,Dilution,LOD,LOQ,Result,Percent\n"
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
                    outputline = batch + ", "+str(index)+", " +line 

                elif counter <5:
                    outputline = outputline + ", "+  line 
                elif counter ==5:
                    outputlines = outputlines +  outputline + ", "+  line + "\n"
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
                # if skip == True:
                #     skip = False
                #     continue
                #  # print("Line:", line)
                #  # print("Counter:", counter)
                #  # print("Is number:", is_number)
                #  # print("-----")
                #  # Check if the line can be converted to a float
                #  # If it can, it's a number; otherwise, it's not
                # try:
                #     float(line)
                #     is_number = True
                # except ValueError:
                #     is_number = False
                #    # print("Not a number:", line)

                # if is_number == True :
                #     percent = line  
                #     outputline =  terp + ", " + percent
                #     # counter = counter  + 1
                # else:
                #     if setheader == True:
                #         outputlines ="Batch,Index,Terpene,Percent\n"
                #         setheader=False
                #     terp = batch + ", " + str(index)+", " + line
                #     outputline =   terp + "," + percent
                #     outputlines = outputlines+ outputline+  "\n"
                #     index = index + 1
                
                #     # if counter == 1:
                # #     percent = line
                # #     counter = counter  + 1
                # # elif counter == 2:
                # #     terp = line
                # #     counter = counter  + 1
                # # elif counter == 3:
                # #     outputline = terp + " " + percent + "\n"
                # #     outputlines = outputlines + outputline  
                # #     counter  =1
                if position == skipcount:
                    outputlines ="Batch,Index,Terpene,(ug/g),Percent\n"
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
                    outputline = batch + ", "+str(index)+", " +line 

                elif counter <3:
                    outputline = outputline + ", "+  line 
                elif counter ==3:
                    outputlines = outputlines +  outputline + ", "+  line + "\n"
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
        print(item + ":" + str(format) + ":"+str(exception_traceback.tb_lineno) +" Error:", e)
      # print("\n"+extracted_text)
        print("\n\n--------------------------------")
def has_decimal_places_str(number):
    return "." in str(number)
    
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
