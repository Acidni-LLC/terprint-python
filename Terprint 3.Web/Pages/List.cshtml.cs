using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.Extensions.Options;
using static Terprint_3.Pages.TableModel;


namespace Terprint_3.Pages
{
    public class ListModel : PageModel
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


        [FromQuery(Name = "matrix")]
        public int? matrix { get; set; }

        [FromQuery(Name = "size")]
        public string? size { get; set; }
        public void OnGet()
        {
        }

        public void loadData()
        {
            try
            {
                c = new Components();

                c.matrix = matrix;
                c.strain = strain;
                c.loadmatrix();
                c.loadRatings();

                c.loadStrains();
                c.setCurrentStrain();
                c.loadListBoxes();


            }


            catch
            {

            }
        }
    }
}
