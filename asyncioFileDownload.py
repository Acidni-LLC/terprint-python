import asyncio
import os

local_filename = 'COA_2509CBR0194-005.pdf'
url='https://mete.labdrive.net/s/SfWBtnDxrN9qs2t/download/COA_2509CBR0194-005.pdf'

def downloadfile(url,local_filename):
    PYPPETEER_CHROMIUM_REVISION = '1263111'

    os.environ['PYPPETEER_CHROMIUM_REVISION'] = PYPPETEER_CHROMIUM_REVISION

    from pyppeteer import launch


    async def generate_pdf(url, pdf_path):
        browser = await launch()
        page = await browser.newPage()
        
        await page.goto(url)
        
        await page.pdf({'path': pdf_path})
        
        await browser.close()

    # Run the function
    asyncio.get_event_loop().run_until_complete(generate_pdf(url,local_filename))


downloadfile(url,local_filename)