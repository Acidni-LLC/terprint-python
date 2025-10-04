from pydoc import text
import fitz # PyMuPDF
import requests
import sys
import os

redownload = 0
#my_list = ["18275_0007355234","18275_0007367106","18275_0007402750","18329_0007584963","18329_0007630532","18347_0007584866","18363_0007224250","18365_0007450194","19248_0007509364","24134_0007208753","39720_0007485377","40866_0007119277","41839_0007584621","43670_0007313365","46768_0007673495","49447_0007119352","49447_0007353503","50657_0007757621","55435_0007744647","56972_0007701664","56974_0007711629","56975_0007354956","56976_0007595513","57347_0007595471","57901_0007392371","58723_0007104565","58723_0007426355","58723_0007442383","58739_0007378977","58739_0007562483","58739_0007584969","59663_0007366912","59703_0006933913","59703_0007137826","59703_0007331673","59710_0006955393","59710_0007162218","59710_0007236544","59710_0007247175","59721_0007314474","59721_0007429464","59721_0007475993","59721_0007509345","59763_0007162220","59814_0007353476","59814_0007366578","60421_0007161154","60421_0007293728","60436_0007687376","61123_0007246497","61128_0007514199","61129_0007324624","61130_0007450580","63534_0007519748","63551_0007530166","63868_0007404550","63991_0007519793","63991_0007630058","64809_0007519751","64809_0007530144","64813_0007548780","64813_0007584712","64821_0007313300","65044_0007425721","65199_0007711629","65201_0007701664","65217_0007711601","65467_0007453660","66759_0007562368","66883_0007036682","66883_0007099065","66883_0007355102","67065_0007653467","67194_0007541009","67279_0007221337","67279_0007353501","67336_0007016880","67336_0007046808","67336_0007183857","67336_0007197539","67340_0006877351","67340_0007489243","67342_0007290175","67342_0007365528","67342_0007641487","67342_0007641508","67542_0007450809","67542_0007452774","67542_0007487589","67661_0007689072","67988_0007687378","68185_0007314406","68185_0007465874","68186_0007378049","68189_0007453659","68673_0007530137","68673_0007540970","68673_0007540977","68673_0007595480","68677_0007313329","68677_0007355142","68683_0007173428","68683_0007453658","68746_0007197842","68920_0007509336","68920_0007701362","69669_0007595504","69669_0007653121","69669_0007653122","69669_0007711628","69670_0007711628","71029_0007509347","71029_0007689041","71030_0007354228","71035_0007584619","71223_0007595505","71223_0007711623","71234_0007711604","71238_0007711623","71320_0007392356","72982_0007562482","72982_0007653556","72985_0007509355","72985_0007562320","73771_0007313354","73983_0007475606","73983_0007509340","74541_0007711608","74556_0007605467","74556_0007711608","74565_0007245657","74576_0007290699","74576_0007353492","75781_0007673684","75785_0007290685","75785_0007354936","75792_0007519660","75838_0007487647","75849_0007562320","75849_0007584968","76505_0007734156","76505_0007734157","76618_0007563508","76618_0007605405","76621_0007593290","76625_0007485377","76757_0007768507","79040_0007701649","79080_0007541026","79080_0007653760","79086_0007487656","79099_0007641222","79112_0007701650","79132_0007653758","79212_0007584846","79376_0007381188","80205_0007516631","80965_0007489245","81049_0007701652","81283_0007516400","81283_0007538669","81473_0007687379","81474_0007711741","81474_0007746068","82049_0007429610","82049_0007701661","82049_0007733517","82188_0007354943","82188_0007453524","82188_0007685952","82462_0007746224","82605_0007687375","83536_0007475408","83537_0007673850","83537_0007687374","83667_0007161156","83669_0007701657","83669_0007701660","83698_0007487607","83699_0007733873","83699_0007734155","84600_0007745786","84601_0007733248"]
my_list = ["COA_2509CBR0095-001","COA_2508CBR0124-009"]
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
