using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.AspNetCore.Mvc.Rendering;
using System.ComponentModel.DataAnnotations.Schema;
using System.Diagnostics;
using System.Drawing;
using System.Reflection;
using static Terprint_3.Pages.TableModel;

namespace Terprint_3.Pages
{
    public class TableModel : PageModel
    {

        public Terprint_3.Components c { get; set; }

        [FromQuery(Name = "strain")]
        public string? strain
        {
            get
            {
                try
                {
                    if (HttpContext.Request.Query["strain"].FirstOrDefault() != null)
                    {

                        return HttpContext.Request.Query["strain"].FirstOrDefault().Split("|")[0];
                    }
                    else
                    {
                        if (c.currentStrain != null)
                        {

                            return c.currentStrain[0].Strain;

                        }
                        else { return ""; }
                    }
                }
                catch
                {
                    return null;
                }
            }
            set { }
        }


        public string? batch
        {
            get
            {

                try
                {
                    if (HttpContext.Request.Query["strain"].ToString() != "")
                    {
                        return HttpContext.Request.Query["strain"].FirstOrDefault().Split("|")[1];

                    }
                    else
                    {
                        if (c.currentStrain != null)
                        {
                            return c.currentStrain[0].Batch;
                        }
                        else { return null; }

                    }
                }
                catch (Exception)
                {

                    return null;

                }
            }
            set { }
        }
        [FromQuery(Name = "matrix")]
        public int? matrix { get; set; }

        [FromQuery(Name = "size")]
        public string? size { get; set; }
        public class strainModel : PageModel
        {
            [BindProperty]
            public string strain { get; set; }
            public void OnPost()
            {
                // posted value is assigned to the Number property automatically
            }
        }
        public void OnPost()
        {
            strain = Request.Form["strain"].ToString();
            c.setCurrentStrain();
        }
        public void OnGet()
        {

            //   loadData();

        }
        public void loadData()
        {
            try
            {
                c = new Components();
                c.size = size;
                c.matrix = matrix;
                c.strain = strain;
                c.batch = batch;
                c.loadmatrix();
                c.loadRatings();

                c.loadStrains();
                c.loadListBoxes();
                c.setCurrentStrain();
                if (c.currentStrain.Count == 0)
                {
                    c.terprintTable(c.Options[0].Value.Split('|')[1]);
                }
                else
                {
                    c.terprintTable();
                }

            }


            catch
            {

            }
        }


        public async Task<IActionResult> OnPostRegisterAsync()
        {
            //…
            return RedirectToPage();
        }
        public async Task<IActionResult> OnPostRequestInfo()
        {
            //…
            return RedirectToPage();
        }

    }
}
