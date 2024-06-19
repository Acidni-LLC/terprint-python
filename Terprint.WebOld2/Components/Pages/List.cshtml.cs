using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.Extensions.Options;
using static Terprint.Pages.TableModel;


namespace Terprint.Pages
{
    public class ListModel : PageModel
    {
        public Terprint.Components.Components c { get; set; }

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
                c = new Components.Components();

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
