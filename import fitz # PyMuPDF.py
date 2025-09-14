import fitz # PyMuPDF
import requests

my_list = ["18275_0007355234","18275_0007367106","18275_0007402750","18329_0007584963","18329_0007630532","18347_0007584866","18363_0007224250","18365_0007450194","19248_0007509364","24134_0007208753","39720_0007485377","40866_0007119277","41839_0007584621","43670_0007313365","46768_0007673495","49447_0007119352","49447_0007353503","50657_0007757621","55435_0007744647","56972_0007701664","56974_0007711629","56975_0007354956","56976_0007595513","57347_0007595471","57901_0007392371","58723_0007104565","58723_0007426355","58723_0007442383","58739_0007378977","58739_0007562483","58739_0007584969","59663_0007366912","59703_0006933913","59703_0007137826","59703_0007331673","59710_0006955393","59710_0007162218","59710_0007236544","59710_0007247175","59721_0007314474","59721_0007429464","59721_0007475993","59721_0007509345","59763_0007162220","59814_0007353476","59814_0007366578","60421_0007161154","60421_0007293728","60436_0007687376","61123_0007246497","61128_0007514199","61129_0007324624","61130_0007450580","63534_0007519748","63551_0007530166","63868_0007404550","63991_0007519793","63991_0007630058","64809_0007519751","64809_0007530144","64813_0007548780","64813_0007584712","64821_0007313300","65044_0007425721","65199_0007711629","65201_0007701664","65217_0007711601","65467_0007453660","66759_0007562368","66883_0007036682","66883_0007099065","66883_0007355102","67065_0007653467","67194_0007541009","67279_0007221337","67279_0007353501","67336_0007016880","67336_0007046808","67336_0007183857","67336_0007197539","67340_0006877351","67340_0007489243","67342_0007290175","67342_0007365528","67342_0007641487","67342_0007641508","67542_0007450809","67542_0007452774","67542_0007487589","67661_0007689072","67988_0007687378","68185_0007314406","68185_0007465874","68186_0007378049","68189_0007453659","68673_0007530137","68673_0007540970","68673_0007540977","68673_0007595480","68677_0007313329","68677_0007355142","68683_0007173428","68683_0007453658","68746_0007197842","68920_0007509336","68920_0007701362","69669_0007595504","69669_0007653121","69669_0007653122","69669_0007711628","69670_0007711628","71029_0007509347","71029_0007689041","71030_0007354228","71035_0007584619","71223_0007595505","71223_0007711623","71234_0007711604","71238_0007711623","71320_0007392356","72982_0007562482","72982_0007653556","72985_0007509355","72985_0007562320","73771_0007313354","73983_0007475606","73983_0007509340","74541_0007711608","74556_0007605467","74556_0007711608","74565_0007245657","74576_0007290699","74576_0007353492","75781_0007673684","75785_0007290685","75785_0007354936","75792_0007519660","75838_0007487647","75849_0007562320","75849_0007584968","76505_0007734156","76505_0007734157","76618_0007563508","76618_0007605405","76621_0007593290","76625_0007485377","76757_0007768507","79040_0007701649","79080_0007541026","79080_0007653760","79086_0007487656","79099_0007641222","79112_0007701650","79132_0007653758","79212_0007584846","79376_0007381188","80205_0007516631","80965_0007489245","81049_0007701652","81283_0007516400","81283_0007538669","81473_0007687379","81474_0007711741","81474_0007746068","82049_0007429610","82049_0007701661","82049_0007733517","82188_0007354943","82188_0007453524","82188_0007685952","82462_0007746224","82605_0007687375","83536_0007475408","83537_0007673850","83537_0007687374","83667_0007161156","83669_0007701657","83669_0007701660","83698_0007487607","83699_0007733873","83699_0007734155","84600_0007745786","84601_0007733248"]
for item in my_list:
    print(item)

    batch = item

    url ="https://www.trulieve.com/content/dam/trulieve/en/lab-reports/"+batch+".pdf?download=true"  # Replace with the actual URL of the file
    local_filename = batch+".pdf"  # Replace with your desired local filename

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
        #Example usage
        pdf_file = "sample.pdf"
        extracted_text = extract_text_from_pdf(pdf_path)
        with open(batch+"_extractall.txt", "w", encoding='utf-8') as f:
            f.write(extracted_text)
        splittext = extracted_text.split("Terpenes Summary", maxsplit=1)[1]
        splittext  =splittext.split("Detailed Terpenes Analysis is on the following page", maxsplit=1)[0]
        print(splittext)
        #print(extracted_text)
        splittext1 = extracted_text.split("This product is tested at this moisture level, not at dry weight.", maxsplit=1)[1]
        splittext1 = splittext1.split("Terpenes Summary", maxsplit=1)[0]
        print("1\n"+splittext1)
        with open(batch+".txt", "w", encoding='utf-8') as f:
            f.write(splittext + "\n----------------------" + splittext1)

    except Exception as e:
        extracted_text = extract_text_from_pdf(pdf_path)
        with open(batch+"_extractall.txt", "w", encoding='utf-8') as f:
            f.write(extracted_text)
        splittext = extracted_text.split("%\nAnalyte\nmg", maxsplit=1)[1]
        splittext  =splittext.split("TERPENES SUMMARY (Top Ten)", maxsplit=1)[0]
        print(splittext)
        #print(extracted_text)
        splittext1 = extracted_text.split("TERPENES SUMMARY (Top Ten)", maxsplit=1)[1]
        splittext1 = splittext1.split("Completed", maxsplit=1)[0]
        print("2\n"+splittext1)
        with open(batch+".txt", "w", encoding='utf-8') as f:
            f.write(splittext + "\n----------------------" + splittext1)
