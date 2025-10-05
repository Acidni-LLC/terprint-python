from pydoc import text
import fitz # PyMuPDF
import requests
import sys
import os

redownload = 0
my_list = ["84600_0007745786", "76757_0007746071", "68679_0007575046", "60421_0007293728", "59703_0007137826", "84600_0007745786", "76757_0007746071", "68679_0007616627", "68677_0007355142", "59814_0007366578", "59703_0007137826", "67335_0007530209", "84600_0007745786", "76757_0007768507", "71030_0007354228", "68679_0007575046", "68683_0007173428", "60421_0007161154", "59814_0007353476", "59703_0007137826", "67335_0007530209", "84600_0007745786", "76757_0007746071", "68679_0007575046", "60421_0007293728", "59703_0007137826", "84600_0007745786", "82462_0007768510", "76757_0007746071", "68679_0007616627", "68683_0007173428", "60421_0007161154", "59814_0007366578", "59703_0007137826", "67335_0007530209", "84600_0007745786", "82462_0007768510", "76757_0007746071", "68679_0007575046", "60421_0007161154", "59814_0007366578", "59703_0007137826", "67335_0007530209", "84600_0007745786", "82462_0007768510", "76757_0007746071", "71030_0007354228", "68679_0007616627", "60421_0007293728", "59814_0007353476", "59703_0007137826", "67336_0007046808", "67335_0007530209", "84600_0007745786", "82462_0007768510", "76757_0007746071", "71030_0007354228", "68679_0007575046", "59814_0007366578", "59703_0007137826", "67336_0007046808", "67335_0007530209", "84600_0007745786", "82462_0007768510", "76757_0007746071", "71030_0007354228", "68679_0007575046", "68683_0007173428", "60421_0007293728", "59814_0007366578", "59703_0007137826", "67335_0007530209", "84600_0007745786", "82462_0007768510", "76757_0007746071", "71030_0007354228", "68679_0007575046", "59703_0007137826", "67335_0007530209", "84600_0007745786", "76757_0007746071", "68679_0007616627", "60421_0007293728", "59703_0007137826", "84600_0007745786", "82462_0007768510", "76757_0007746071", "68679_0007575046", "68683_0007173428", "60421_0007293728", "59703_0007137826", "67331_0007172821", "84600_0007745786", "76757_0007746071", "68679_0007575046", "60421_0007293728", "59814_0007366578", "59703_0007137826", "67335_0007530209", "84600_0007745786", "82462_0007768510", "76757_0007746071", "71030_0007354228", "68679_0007575046", "68683_0007173428", "60421_0007161154", "84600_0007745786", "76757_0007746071", "77745_0007074998", "71030_0007354228", "71029_0007689041", "69881_0007208736", "68679_0007575046", "68189_0007453659", "68677_0007313329", "60421_0007262150", "59814_0007353476", "59703_0007137826", "67335_0007530209", "80965_0007663473", "79441_0007630964", "63991_0007630058", "80965_0007663473", "76618_0007605405", "80965_0007489245", "76618_0007563508", "79441_0007540872", "63991_0007630058", "80965_0007663473", "71247_0007711627", "80965_0007663473", "76618_0007605405", "63991_0007630058", "83537_0007746082", "79376_0007381188", "81283_0007538669", "71219_0007757109", "74576_0007353492", "67988_0007687378", "65044_0007425721", "64813_0007584712", "58739_0007378977", "57901_0007366503", "56974_0007711629", "46768_0007673495", "18275_0007402750", "83537_0007746082", "81473_0007687379", "81283_0007538669", "71219_0007757109", "74576_0007353492", "71320_0007758370", "67988_0007687378", "64813_0007584712", "57901_0007366503", "18275_0007402750", "83537_0007687374", "81283_0007516400", "71219_0007757109", "73983_0007563660", "71320_0007758370", "67988_0007687378", "65044_0007425721", "64813_0007584712", "58739_0007685947", "58723_0007104565", "57901_0007366503", "35299_0007768512", "18275_0007402750", "83537_0007746082", "67988_0007687378", "64813_0007584712", "58739_0007685947", "58723_0007442383", "57901_0007366503", "18275_0007402750", "83537_0007746082", "79376_0007381188", "81283_0007538669", "71219_0007757109", "73983_0007563660", "71320_0007758370", "67988_0007687378", "64813_0007584712", "57901_0007366503", "18275_0007402750", "83537_0007687374", "71219_0007757109", "74576_0007353492", "73983_0007563660", "71320_0007758370", "69669_0007595504", "67988_0007687378", "64813_0007548780", "63715_0007758389", "58723_0007442383", "57901_0007366503", "56976_0007711617", "46768_0007673495", "18275_0007367106", "83537_0007687374", "71219_0007757109", "74576_0007353492", "73983_0007563660", "71320_0007758370", "67988_0007687378", "67279_0007353501", "65044_0007425721", "64813_0007548780", "58723_0007442383", "57901_0007489239", "56976_0007711617", "46768_0007673495", "18275_0007402750", "83537_0007687374", "81283_0007538669", "74576_0007353492", "71320_0007758370", "67988_0007687378", "64813_0007548780", "63715_0007758389", "58723_0007442383", "57901_0007366503", "56976_0007711617", "35299_0007768512", "18275_0007402750", "83537_0007687374", "71219_0007757109", "74576_0007353492", "73983_0007563660", "69669_0007595504", "67988_0007687378", "65044_0007425721", "64813_0007548780", "57901_0007366503", "56974_0007711629", "46768_0007673495", "18275_0007402750", "83537_0007746082", "74576_0007353492", "67988_0007687378", "65044_0007425721", "64813_0007584712", "57901_0007366503", "18275_0007402750", "83537_0007746082", "81283_0007538669", "71219_0007757109", "67988_0007514131", "64813_0007584712", "58739_0007378977", "58723_0007442383", "57901_0007366503", "46768_0007673495", "18275_0007402750", "83537_0007687374", "81283_0007516400", "67988_0007687378", "64813_0007614563", "58739_0007586424", "57901_0007452411", "46768_0007673495", "35299_0007768512", "18275_0007402750", "83537_0007475951", "81283_0007538669", "71219_0007757109", "73983_0007563660", "71320_0007758370", "67988_0007514131", "64813_0007584712", "58739_0007685947", "57901_0007366503", "56976_0007711617", "35299_0007768512", "18275_0007402750", "83537_0007475951", "81283_0007538669", "71219_0007757109", "74576_0007353492", "73983_0007563660", "67988_0007687378", "67279_0007380764", "65044_0007425721", "64813_0007584712", "57901_0007366503", "46768_0007673495", "24134_0007208753", "18275_0007402750", "83537_0007687374", "79376_0007381188", "81283_0007538669", "79132_0007653758", "71219_0007757109", "73983_0007563660", "67988_0007687378", "65044_0007425721", "64813_0007614563", "58723_0007104565", "57901_0007366503", "35299_0007768512", "18275_0007402750", "82462_0007746224", "79099_0007629764", "71223_0007595505", "71029_0007509347", "68186_0007378049", "67340_0007489243", "63534_0007519748", "49447_0007353503", "43670_0007313365", "82462_0007746224", "82049_0007487666", "71223_0007595505", "68186_0007771990", "67542_0007452774", "63534_0007519748", "82462_0007746224", "82049_0007701661", "79099_0007629764", "71223_0007595505", "71029_0007509347", "68186_0007771990", "59721_0007314474", "67542_0007487589", "67342_0007290175", "67340_0006877351", "63534_0007519748", "60436_0007687376", "49447_0007353503", "43670_0007313365", "18363_0007224250", "82462_0007746224", "82049_0007540999", "80205_0007516631", "71223_0007595505", "71029_0007509347", "68186_0007378049", "67542_0007475384", "63534_0007519748", "82049_0007487666", "79099_0007629764", "71029_0007509347", "68186_0007378049", "67542_0007475384", "67342_0007641487", "67340_0007489243", "63534_0007519748", "43670_0007313365", "82049_0007487666", "80205_0007516631", "79099_0007629764", "71029_0007509347", "68186_0007378049", "67542_0007450809", "67340_0007489243", "63534_0007519748", "60436_0007768511", "43670_0007313365", "18363_0007224250", "82049_0007487666", "79099_0007771988", "71223_0007595505", "71029_0007509347", "68186_0007378049", "67542_0007452774", "67340_0007489243", "63534_0007519748", "60436_0007768511", "18363_0007224250", "82049_0007487666", "80205_0007516631", "79099_0007641222", "71223_0007595505", "68186_0007771990", "67542_0007452774", "67340_0007489243", "63534_0007519748", "60436_0007768511", "43670_0007313365", "82049_0007487666", "79099_0007629764", "71223_0007595505", "71029_0007509347", "68186_0007771990", "67542_0007487589", "67340_0007489243", "63534_0007519748", "60436_0007687376", "82049_0007540999", "71223_0007595505", "71029_0007509347", "67542_0007452774", "67340_0007489243", "63534_0007519748", "43670_0007313365", "82049_0007487666", "71223_0007595505", "67542_0007475384", "63534_0007519748", "43670_0007313365", "82049_0007540999", "79099_0007629764", "68186_0007771990", "68746_0007173415", "68188_0007424399", "67542_0007366914", "67340_0007489243", "63534_0007519748", "43670_0007313365", "18363_0007224250", "83699_0007734155", "82462_0007746224", "82049_0007487666", "80205_0007516631", "79099_0007629764", "68186_0007378049", "59721_0007563266", "67542_0007475384", "67342_0007641487", "67340_0007489243", "63534_0007519748", "49447_0007119352", "43670_0007313365", "82049_0007487666", "79099_0007629764", "71223_0007595505", "68186_0007378049", "67542_0007450809", "67342_0007641487", "67340_0007489243", "63534_0007519748", "60436_0007768511", "49447_0007119352", "83699_0007734155", "82462_0007746224", "82049_0007745912", "67323_0006923509", "79099_0007629764", "71223_0007595505", "68186_0007378049", "68746_0007025018", "59721_0007314474", "67542_0007450809", "67342_0006923439", "67340_0007324753", "63534_0007519748", "60436_0007687376", "49447_0007119352", "40866_0007119277", "83667_0007685819", "83667_0007685819", "76621_0007593290", "79086_0007487656", "83667_0007685819", "83667_0007685819", "83536_0007475408", "81684_0007530207", "59763_0007162220", "75849_0007584968", "81684_0007530207", "59763_0007162115", "75849_0007584968", "71034_0007487610", "61128_0007514199", "83667_0007161156", "76625_0007485377", "82188_0007354943", "64821_0007313300", "81684_0007530207", "59763_0007162220", "75849_0007584968", "69670_0007711628", "71034_0007614543", "63551_0007530166", "61128_0007514199", "81684_0007673489", "59763_0007162220", "79836_0007517347", "75849_0007562320", "71034_0007614543", "61128_0007514199", "83536_0007475408", "82188_0007685952", "81684_0007530207", "59763_0007162220", "79836_0007517347", "66759_0007562368", "18329_0007630532", "67330_0007519694", "79080_0007541026", "80205_0007562480", "76505_0007734156", "75785_0007290685", "75792_0007519660", "75567_0007757098", "74556_0007605467", "71320_0007392356", "72985_0007562320", "69669_0007653122", "70912_0007630058", "68920_0007509336", "59710_0007298356", "67194_0007584970", "64809_0007758366", "61123_0007246497", "58723_0007426355", "50657_0007757621", "18365_0007450194", "67330_0007519694", "79080_0007653760", "80205_0007562480", "76505_0007734156", "75785_0007290685", "75792_0007519660", "75567_0007757098", "74556_0007605467", "72985_0007562320", "69669_0007653122", "70912_0007630058", "68920_0007509336", "67194_0007541009", "64809_0007584868", "61123_0007246497", "58723_0007426355", "50657_0007757621", "18365_0007450194", "18329_0007584963", "67330_0007519694", "79080_0007541026", "80205_0007562480", "76505_0007734157", "75785_0007354936", "75567_0007757098", "74556_0007605467", "74576_0007290699", "72985_0007562320", "69669_0007711628", "70912_0007630058", "68185_0007314406", "68920_0007701362", "59710_0007298356", "67661_0007689072", "67194_0007541009", "66883_0007099065", "64809_0007562333", "63868_0007404550", "61123_0007246497", "50657_0007540652", "18365_0007450194", "67330_0007519694", "79080_0007541026", "76505_0007734156", "75785_0007290685", "75567_0007757098", "74556_0007711608", "74576_0007771989", "72985_0007562320", "69669_0007653122", "70912_0007630058", "68920_0007509336", "59710_0007298356", "67194_0007584970", "64809_0007584868", "61123_0007246497", "50657_0007757621", "80205_0007562480", "76505_0007734157", "75785_0007290685", "74576_0007771989", "72985_0007562320", "69669_0007711628", "70912_0007630058", "68920_0007509336", "67194_0007541009", "64809_0007584868", "61123_0007246497", "58723_0007426355", "50657_0007757621", "18365_0007450194", "18329_0007630532", "82319_0007538671", "67330_0007519694", "79080_0007653760", "76505_0007734156", "75785_0007290685", "75792_0007519660", "74556_0007711608", "72985_0007562320", "70912_0007630058", "68920_0007745823", "59710_0007298356", "67194_0007541009", "64809_0007562333", "61123_0007246497", "58739_0007584969", "50657_0007757621", "18329_0007630532", "67330_0007519694", "79080_0007541026", "80205_0007562480", "76505_0007734157", "75785_0007290685", "75567_0007757099", "74556_0007605467", "73771_0007313354", "72985_0007562320", "69669_0007653121", "70912_0007630058", "68920_0007653509", "59710_0007562494", "67661_0007689072", "59721_0007509345", "67194_0007541009", "66883_0007007615", "64809_0007562333", "63868_0007404550", "61129_0007324624", "50657_0007757621", "18365_0007450194", "18329_0007630532", "67330_0007519694", "79080_0007541026", "76505_0007734157", "75785_0007290685", "75792_0007519660", "75567_0007757098", "74556_0007605467", "72985_0007562320", "69669_0007653121", "70912_0007630058", "68920_0007653509", "59710_0007298356", "67194_0007541009", "64809_0007584868", "61123_0007246497", "58739_0007584969", "50657_0007757621", "18365_0007450194", "67330_0007519694", "80205_0007562480", "76505_0007734157", "75785_0007290685", "75792_0007519660", "75567_0007757098", "74556_0007605467", "71320_0007392356", "72985_0007530225", "70912_0007630058", "59710_0007298356", "67194_0007541009", "64809_0007584868", "63868_0007404550", "61123_0007246497", "58739_0007584969", "58723_0007426355", "50657_0007757621", "18365_0007450194", "79080_0007541026", "80205_0007562480", "76505_0007734156", "75785_0007290685", "74556_0007605467", "71320_0007392356", "72985_0007562320", "69669_0007653121", "70912_0007630058", "68920_0007509336", "59710_0007298356", "67194_0007584970", "66883_0007355102", "64809_0007584868", "61123_0007246497", "58739_0007584969", "58723_0007426355", "50657_0007757621", "18365_0007450194", "79080_0007653760", "80205_0007562480", "76505_0007734156", "75785_0007290685", "74556_0007605467", "74576_0007771989", "72985_0007530225", "69669_0007711628", "70912_0007630058", "68920_0007745823", "59710_0007298356", "67194_0007584970", "67192_0007101697", "64809_0007584868", "61123_0007246497", "50657_0007757621", "18365_0007450194", "18329_0007584963", "82319_0007538671", "67330_0007519694", "80205_0007562480", "76505_0007734157", "75785_0007290685", "75567_0007757098", "74576_0007771989", "72985_0007562320", "70912_0007630058", "59710_0007298356", "59721_0007366918", "67194_0007584970", "64809_0007758366", "61123_0007246497", "58723_0007426355", "50657_0007757621", "18365_0007450194", "82319_0007538671", "67330_0007519694", "79080_0007653760", "76505_0007734156", "75785_0007290685", "75567_0007673680", "74576_0007771989", "72985_0007562320", "70912_0007630058", "68920_0007509336", "59710_0007298356", "67194_0007541009", "64809_0007584868", "61123_0007246497", "58723_0007426355", "50657_0007757621", "18365_0007450194", "67330_0007519694", "80205_0007562480", "76505_0007734156", "75785_0007290685", "75792_0007519660", "75567_0007757099", "74556_0007605467", "71320_0007392356", "72985_0007530225", "69669_0007653121", "70912_0007630058", "59710_0007247175", "59721_0007475993", "67194_0007584970", "64809_0007584868", "61123_0007246497", "58739_0007584969", "58723_0007426355", "50657_0007757621", "18365_0007450194", "18329_0007584963", "67330_0007519694", "79080_0007653760", "80205_0007562480", "76505_0007734157", "75785_0007290685", "75567_0007757098", "74556_0007605467", "74576_0006971502", "71320_0007392356", "72985_0007509355", "69669_0007653121", "70912_0007630058", "68678_0007247217", "68920_0007745823", "59710_0007298356", "67661_0007689072", "67194_0007541009", "67192_0007101697", "67336_0007197539", "67279_0007221337", "66883_0007036682", "64809_0007562333", "63868_0007404550", "61123_0007246497", "56967_0007757111", "50657_0007540652", "18365_0007450194"]
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
