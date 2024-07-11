using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Components;
using Terprint.Web.Models;
using System.Numerics;
using System.Drawing.Drawing2D;
using Microsoft.Identity.Client;


namespace Terprint.common
{
    public enum TerpeneList {   };
    public static class config
    {
        public static string appname = "Terptastic";
    }
    public static class Overrides
    {
        public static void ReloadPage(this NavigationManager manager)
        {
            manager.NavigateTo(manager.Uri, true);
        }
    }
    public class AppState
    {
        public RatingCategory ratingCategory { get; set; }
        public int batchid { get; set; }
        public int ratingcategoryid { get; set; }

        public class TerprintTable
        {
            public string batchId { get; set; }
            public int matrixId { get; set; }

            public int matrixSize { get; set; }
        }

    }
    public static class Strains
    {
        public static List<string> GetStrains()
        {
            Components c = new Components();
            c.loadStrains();
            return c.TerpValues.Select(t => t.Strain).OrderBy(t => t).Distinct().ToList();

        }
        public static List<string> GetBatches(string strain = "")
        {
            Components c = new Components();
            c.loadStrains();
            return c.TerpValues.Where(t => t.Strain == strain).Select(t => t.Batch).OrderBy(t => t).Distinct().ToList();

        }

    }
    public class Components : PageModel
    {

        public MarkupString outputrows { get; set; }

        [FromQuery(Name = "strain")]
        public string? strain
        {
            get; set;
        }

        public string? batch
        {
            get;
            //{

            //    try
            //    {
            //        if (HttpContext.Request.Query["strain"].ToString() != "")
            //        {
            //            return HttpContext.Request.Query["strain"].FirstOrDefault().Split("|")[1];

            //        }
            //        else
            //        {
            //            return currentStrain[0].Batch;

            //        }
            //    }
            //    catch (Exception)
            //    {
            //        return currentStrain[0].Batch;
            //        return null;

            //    }
            //}
            set;
            //{ }
        }

        [FromQuery(Name = "matrix")]
        public int? matrix { get; set; }

        [FromQuery(Name = "size")]
        public components.Ratings ratings { get; set; }
        public string? size { get; set; }
        public string? RequestId { get; set; }
        public int currentTerpenes { get; set; }
        public bool ShowRequestId => !string.IsNullOrEmpty(RequestId);

        // private readonly ILogger<ErrorModel> _logger;

        //public ListModel(ILogger<ErrorModel> logger)
        //{
        //    _logger = logger;
        //}

        public List<SelectListItem> Options { get; set; }
        public List<SelectListItem> OptionsMatrix { get; set; }
        public List<SelectListItem> OptionsSize { get; set; }
        public List<terpValue>? currentStrain { get; set; }
        public List<terpValue>? TerpValues { get; set; }
        public List<matrixes>? Matrixes { get; set; }


        public class matrixes
        {
            public matrixes(int a, string b, int c, int d, int e, string color, string name2 = "", string description = "")
            {
                Id = a;
                Name = b;
                Matrix = c;
                Row = d;
                Column = e;
                Color = "";
                Color = color;
                this.name2 = name2;
                this.description = description;
                NamesOther = new List<string>();
            }
            public List<string> NamesOther;
            public int Row;
            public int Column;
            public string Name;
            public int Id;
            public int Matrix;
            public string Color;
            public string name2;
            public string description;
        }

        public class terpValue
        {
            public terpValue(double value, string terpName, string strain, string batch)
            {
                // Date = date;
                components.Ratings r = new components.Ratings();
                Value = value;
                TerpName = terpName;
                Strain = strain;
                Batch = batch;
                Ratings = r.UserRatings.Where(t => t.batch == batch).ToList();
                Rating = (double)r.UserRatings.Where(t => t.batch == batch).Select(t => t.OverallRating).FirstOrDefault();
            }
            List<components.Ratings.UserRating> Ratings;
            public double Value;
            public string TerpName;
            public string Strain;
            public string Batch;
            public double Rating;
            public DateOnly Date;
        }
        public void OnGet()
        {
        }

        public void loadData()
        {
            try
            {
                //try
                //{
                //    if (HttpContext.Request.Query["strain"] != "" && HttpContext.Request.Query["strain"].ToString().Contains("|"));
                //    {
                //        batch = HttpContext.Request.Query["strain"].FirstOrDefault().Split("|")[1];
                //    }
                //}
                //catch (Exception ex)
                //{

                //}
                loadmatrix();
                loadRatings();

                loadStrains();
                loadListBoxes();
                setCurrentStrain();


            }


            catch
            {

            }
        }
        public void loadRatings()
        {
            ratings = new components.Ratings();
            //  ratings.UserRatings = new List<Ratings.UserRating>();

        }
        public void loadListBoxes()
        {
            Options = TerpValues.GroupBy(a => a.Batch).Select(grp =>
                                   new SelectListItem
                                   {
                                       Value = grp.First().Strain + "|" + grp.First().Batch,
                                       Text = grp.First().Strain + "|" + grp.First().Batch //,
                                                                                           //  Selected = grp.First().Strain == strain ? true : false

                                   }).OrderBy(t => t.Text).ToList();

            OptionsMatrix = Matrixes.GroupBy(a => a.Matrix).Select(grp =>
            new SelectListItem
            {
                Value = grp.First().Matrix.ToString(),
                Text = grp.First().Matrix.ToString()
            }).ToList();

            List<SelectListItem> sizes = new List<SelectListItem>();
            sizes.Add(new SelectListItem
            {
                Value = "Micro",
                Text = "Micro"
            });
            sizes.Add(new SelectListItem
            {
                Value = "Small",
                Text = "Small"
            });
            sizes.Add(new SelectListItem
            {
                Value = "Medium",
                Text = "Medium"
            });
            sizes.Add(new SelectListItem
            {
                Value = "Large",
                Text = "Large"
            });
            OptionsSize = sizes;
        }
        public void loadStrains()
        {


            if (TerpValues is null)
            {
                TerpValues = new List<terpValue>();

                #region data strains
                TerpValues.Add(new terpValue(0, "3-Carene", "Z-Mintz", "3370 0970 3898 2532"));
                TerpValues.Add(new terpValue(0.3, "Camphene", "Z-Mintz", "3370 0970 3898 2532"));
                TerpValues.Add(new terpValue(0, "Caryophyllene Oxide", "Z-Mintz", "3370 0970 3898 2532"));
                TerpValues.Add(new terpValue(0, "cis-Nerolidol", "Z-Mintz", "3370 0970 3898 2532"));
                TerpValues.Add(new terpValue(0, "Eucalyptol", "Z-Mintz", "3370 0970 3898 2532"));
                TerpValues.Add(new terpValue(0.27, "Geraniol", "Z-Mintz", "3370 0970 3898 2532"));
                TerpValues.Add(new terpValue(1.67, "Guaiol", "Z-Mintz", "3370 0970 3898 2532"));
                TerpValues.Add(new terpValue(0, "Isopulegol", "Z-Mintz", "3370 0970 3898 2532"));
                TerpValues.Add(new terpValue(5.9, "Linalool", "Z-Mintz", "3370 0970 3898 2532"));
                TerpValues.Add(new terpValue(0, "Menthol", "Z-Mintz", "3370 0970 3898 2532"));
                TerpValues.Add(new terpValue(0, "Ocimene", "Z-Mintz", "3370 0970 3898 2532"));
                TerpValues.Add(new terpValue(0, "p-Cymene", "Z-Mintz", "3370 0970 3898 2532"));
                TerpValues.Add(new terpValue(0.13, "Terpinolene", "Z-Mintz", "3370 0970 3898 2532"));
                TerpValues.Add(new terpValue(1.57, "trans-Nerolidol", "Z-Mintz", "3370 0970 3898 2532"));
                TerpValues.Add(new terpValue(1.65, "α-Bisabolol", "Z-Mintz", "3370 0970 3898 2532"));
                TerpValues.Add(new terpValue(2.12, "α-Humulene", "Z-Mintz", "3370 0970 3898 2532"));
                TerpValues.Add(new terpValue(0.82, "α-Pinene", "Z-Mintz", "3370 0970 3898 2532"));
                TerpValues.Add(new terpValue(0, "α-Terpinene", "Z-Mintz", "3370 0970 3898 2532"));
                TerpValues.Add(new terpValue(6.5, "β-Caryophyllene", "Z-Mintz", "3370 0970 3898 2532"));
                TerpValues.Add(new terpValue(0.68, "β-Myrcene", "Z-Mintz", "3370 0970 3898 2532"));
                TerpValues.Add(new terpValue(1.32, "β-Pinene", "Z-Mintz", "3370 0970 3898 2532"));
                TerpValues.Add(new terpValue(0, "γ-Terpinene", "Z-Mintz", "3370 0970 3898 2532"));
                TerpValues.Add(new terpValue(9.07, "δ-Limonene", "Z-Mintz", "3370 0970 3898 2532"));
                TerpValues.Add(new terpValue(0, "3-Carene", "Purple Eclipse", "5152 6368 4561 8754"));
                TerpValues.Add(new terpValue(0.16, "Camphene", "Purple Eclipse", "5152 6368 4561 8754"));
                TerpValues.Add(new terpValue(0.12, "Caryophyllene Oxide", "Purple Eclipse", "5152 6368 4561 8754"));
                TerpValues.Add(new terpValue(0, "cis-Nerolidol", "Purple Eclipse", "5152 6368 4561 8754"));
                TerpValues.Add(new terpValue(0.04, "Eucalyptol", "Purple Eclipse", "5152 6368 4561 8754"));
                TerpValues.Add(new terpValue(0, "Geraniol", "Purple Eclipse", "5152 6368 4561 8754"));
                TerpValues.Add(new terpValue(0, "Guaiol", "Purple Eclipse", "5152 6368 4561 8754"));
                TerpValues.Add(new terpValue(0, "Isopulegol", "Purple Eclipse", "5152 6368 4561 8754"));
                TerpValues.Add(new terpValue(0.67, "Linalool", "Purple Eclipse", "5152 6368 4561 8754"));
                TerpValues.Add(new terpValue(0, "Menthol", "Purple Eclipse", "5152 6368 4561 8754"));
                TerpValues.Add(new terpValue(3.96, "Ocimene", "Purple Eclipse", "5152 6368 4561 8754"));
                TerpValues.Add(new terpValue(0, "p-Cymene", "Purple Eclipse", "5152 6368 4561 8754"));
                TerpValues.Add(new terpValue(0.08, "Terpinolene", "Purple Eclipse", "5152 6368 4561 8754"));
                TerpValues.Add(new terpValue(0.35, "trans-Nerolidol", "Purple Eclipse", "5152 6368 4561 8754"));
                TerpValues.Add(new terpValue(1.56, "α-Bisabolol", "Purple Eclipse", "5152 6368 4561 8754"));
                TerpValues.Add(new terpValue(1.1, "α-Humulene", "Purple Eclipse", "5152 6368 4561 8754"));
                TerpValues.Add(new terpValue(7.19, "α-Pinene", "Purple Eclipse", "5152 6368 4561 8754"));
                TerpValues.Add(new terpValue(0, "α-Terpinene", "Purple Eclipse", "5152 6368 4561 8754"));
                TerpValues.Add(new terpValue(3.53, "β-Caryophyllene", "Purple Eclipse", "5152 6368 4561 8754"));
                TerpValues.Add(new terpValue(18.49, "β-Myrcene", "Purple Eclipse", "5152 6368 4561 8754"));
                TerpValues.Add(new terpValue(2.06, "β-Pinene", "Purple Eclipse", "5152 6368 4561 8754"));
                TerpValues.Add(new terpValue(0, "γ-Terpinene", "Purple Eclipse", "5152 6368 4561 8754"));
                TerpValues.Add(new terpValue(0.89, "δ-Limonene", "Purple Eclipse", "5152 6368 4561 8754"));
                TerpValues.Add(new terpValue(7.603, "(R)-(+)-Limonene", "Krypto Chronic", "56966_0005029379"));
                TerpValues.Add(new terpValue(2.287, "Borneol", "Krypto Chronic", "56966_0005029379"));
                TerpValues.Add(new terpValue(0.713, "Fenchyl Alcohol", "Krypto Chronic", "56966_0005029379"));
                TerpValues.Add(new terpValue(2.651, "Linalool", "Krypto Chronic", "56966_0005029379"));
                TerpValues.Add(new terpValue(3.919, "trans-Caryophyllene", "Krypto Chronic", "56966_0005029379"));
                TerpValues.Add(new terpValue(0.92, "α-Humulene", "Krypto Chronic", "56966_0005029379"));
                TerpValues.Add(new terpValue(0.655, "α-Pinene", "Krypto Chronic", "56966_0005029379"));
                TerpValues.Add(new terpValue(1.303, "β-Myrcene", "Krypto Chronic", "56966_0005029379"));
                TerpValues.Add(new terpValue(0.914, "β-Pinene", "Krypto Chronic", "56966_0005029379"));
                TerpValues.Add(new terpValue(0.7689, "(R)-(+)-Limonene", "Space Age Cake", "59727_0005068301"));
                TerpValues.Add(new terpValue(0.2604, "Borneol", "Space Age Cake", "59727_0005068301"));
                TerpValues.Add(new terpValue(0.0692, "Fenchyl Alcohol", "Space Age Cake", "59727_0005068301"));
                TerpValues.Add(new terpValue(0.4693, "Linalool", "Space Age Cake", "59727_0005068301"));
                TerpValues.Add(new terpValue(1.5846, "trans-Caryophyllene", "Space Age Cake", "59727_0005068301"));
                TerpValues.Add(new terpValue(0.0855, "α-Bisabolol", "Space Age Cake", "59727_0005068301"));
                TerpValues.Add(new terpValue(0.3631, "α-Humulene", "Space Age Cake", "59727_0005068301"));
                TerpValues.Add(new terpValue(0.0551, "α-Pinene", "Space Age Cake", "59727_0005068301"));
                TerpValues.Add(new terpValue(0.6157, "β-Myrcene", "Space Age Cake", "59727_0005068301"));
                TerpValues.Add(new terpValue(0.0821, "β-Pinene", "Space Age Cake", "59727_0005068301"));


                TerpValues.Add(new terpValue(2.374, "Borneol", "DieselDough", "63424_0004931218"));
                TerpValues.Add(new terpValue(0.64, "Fenchyl", "DieselDough", "63424_0004931218"));
                TerpValues.Add(new terpValue(1.44, "Guaiol", "DieselDough", "63424_0004931218"));
                TerpValues.Add(new terpValue(2.682, "Linalool", "DieselDough", "63424_0004931218"));
                TerpValues.Add(new terpValue(6.974, "trans-Caryophyllene", "DieselDough", "63424_0004931218"));
                TerpValues.Add(new terpValue(0.704, "trans-Nerolidol", "DieselDough", "63424_0004931218"));
                TerpValues.Add(new terpValue(0.619, "α-Bisabolol", "DieselDough", "63424_0004931218"));
                TerpValues.Add(new terpValue(1.591, "α-Humulene", "DieselDough", "63424_0004931218"));
                TerpValues.Add(new terpValue(0.529, "α-Pinene", "DieselDough", "63424_0004931218"));
                TerpValues.Add(new terpValue(6.004, "β-Myrcene", "DieselDough", "63424_0004931218"));
                TerpValues.Add(new terpValue(0.77, "β-Pinene", "DieselDough", "63424_0004931218"));
                TerpValues.Add(new terpValue(3.01, "(R)-(+)-Limonene", "DieselDough", "63424_0004999768"));
                TerpValues.Add(new terpValue(0.86, "Fenchyl Alcohol", "DieselDough", "63424_0004999768"));
                TerpValues.Add(new terpValue(0.5, "Geranyl Acetate", "DieselDough", "63424_0004999768"));
                TerpValues.Add(new terpValue(1.24, "Guaiol", "DieselDough", "63424_0004999768"));
                TerpValues.Add(new terpValue(2.1, "Linalool", "DieselDough", "63424_0004999768"));
                TerpValues.Add(new terpValue(0.6, "Total Terpineol", "DieselDough", "63424_0004999768"));
                TerpValues.Add(new terpValue(5.13, "trans-Caryophyllene", "DieselDough", "63424_0004999768"));
                TerpValues.Add(new terpValue(0.51, "trans-Nerolidol", "DieselDough", "63424_0004999768"));
                TerpValues.Add(new terpValue(0.38, "Valencene", "DieselDough", "63424_0004999768"));
                TerpValues.Add(new terpValue(0.64, "α-Bisabolol", "DieselDough", "63424_0004999768"));
                TerpValues.Add(new terpValue(1, "α-Humulene", "DieselDough", "63424_0004999768"));
                TerpValues.Add(new terpValue(0.31, "α-Pinene", "DieselDough", "63424_0004999768"));
                TerpValues.Add(new terpValue(0.48, "β-Myrcene", "DieselDough", "63424_0004999768"));
                TerpValues.Add(new terpValue(2.96, "β-Pinene", "DieselDough", "63424_0004999768"));
                TerpValues.Add(new terpValue(6.556, "(R)-(+)-Limonene", " Cake Face", "67317_0005141914"));
                TerpValues.Add(new terpValue(2.379, "Borneol", " Cake Face", "67317_0005141914"));
                TerpValues.Add(new terpValue(0.841, "Fenchyl Alcohol", " Cake Face", "67317_0005141914"));
                TerpValues.Add(new terpValue(4.079, "Linalool", " Cake Face", "67317_0005141914"));
                TerpValues.Add(new terpValue(14.132, "trans-Caryophyllene", " Cake Face", "67317_0005141914"));
                TerpValues.Add(new terpValue(1.061, "trans-Nerolidol", " Cake Face", "67317_0005141914"));
                TerpValues.Add(new terpValue(0.591, "α-Bisabolol", " Cake Face", "67317_0005141914"));
                TerpValues.Add(new terpValue(3.139, "α-Humulene", " Cake Face", "67317_0005141914"));
                TerpValues.Add(new terpValue(0.478, "α-Pinene", " Cake Face", "67317_0005141914"));
                TerpValues.Add(new terpValue(3.255, "β-Myrcene", " Cake Face", "67317_0005141914"));
                TerpValues.Add(new terpValue(0.7, "β-Pinene", " Cake Face", "67317_0005141914"));
                TerpValues.Add(new terpValue(7.277, "(R)-(+)-Limonene", "LA Kush Cake", "67335_0005165631"));
                TerpValues.Add(new terpValue(2.94, "Borneol", "LA Kush Cake", "67335_0005165631"));
                TerpValues.Add(new terpValue(0.901, "Fenchyl Alcohol", "LA Kush Cake", "67335_0005165631"));
                TerpValues.Add(new terpValue(5.52, "Linalool", "LA Kush Cake", "67335_0005165631"));
                TerpValues.Add(new terpValue(6.094, "trans-Caryophyllene", "LA Kush Cake", "67335_0005165631"));
                TerpValues.Add(new terpValue(1.371, "α-Humulene", "LA Kush Cake", "67335_0005165631"));
                TerpValues.Add(new terpValue(0.567, "α-Pinene", "LA Kush Cake", "67335_0005165631"));
                TerpValues.Add(new terpValue(0.481, "β-Myrcene", "LA Kush Cake", "67335_0005165631"));
                TerpValues.Add(new terpValue(0.84, "β-Pinene", "LA Kush Cake", "67335_0005165631"));
                TerpValues.Add(new terpValue(0, "3-Carene", "Witch D.", "6953 2390 9886 2373"));
                TerpValues.Add(new terpValue(0.31, "Camphene", "Witch D.", "6953 2390 9886 2373"));
                TerpValues.Add(new terpValue(0, "Caryophyllene Oxide", "Witch D.", "6953 2390 9886 2373"));
                TerpValues.Add(new terpValue(0, "cis-Nerolidol", "Witch D.", "6953 2390 9886 2373"));
                TerpValues.Add(new terpValue(0, "Eucalyptol", "Witch D.", "6953 2390 9886 2373"));
                TerpValues.Add(new terpValue(0, "Geraniol", "Witch D.", "6953 2390 9886 2373"));
                TerpValues.Add(new terpValue(0, "Guaiol", "Witch D.", "6953 2390 9886 2373"));
                TerpValues.Add(new terpValue(0, "Isopulegol", "Witch D.", "6953 2390 9886 2373"));
                TerpValues.Add(new terpValue(2.36, "Linalool", "Witch D.", "6953 2390 9886 2373"));
                TerpValues.Add(new terpValue(0, "Menthol", "Witch D.", "6953 2390 9886 2373"));
                TerpValues.Add(new terpValue(0, "Ocimene", "Witch D.", "6953 2390 9886 2373"));
                TerpValues.Add(new terpValue(0, "p-Cymene", "Witch D.", "6953 2390 9886 2373"));
                TerpValues.Add(new terpValue(0.12, "Terpinolene", "Witch D.", "6953 2390 9886 2373"));
                TerpValues.Add(new terpValue(0.22, "trans-Nerolidol", "Witch D.", "6953 2390 9886 2373"));
                TerpValues.Add(new terpValue(0.43, "α-Bisabolol", "Witch D.", "6953 2390 9886 2373"));
                TerpValues.Add(new terpValue(1.6, "α-Humulene", "Witch D.", "6953 2390 9886 2373"));
                TerpValues.Add(new terpValue(0.81, "α-Pinene", "Witch D.", "6953 2390 9886 2373"));
                TerpValues.Add(new terpValue(0, "α-Terpinene", "Witch D.", "6953 2390 9886 2373"));
                TerpValues.Add(new terpValue(5.04, "β-Caryophyllene", "Witch D.", "6953 2390 9886 2373"));
                TerpValues.Add(new terpValue(3.63, "β-Myrcene", "Witch D.", "6953 2390 9886 2373"));
                TerpValues.Add(new terpValue(1.18, "β-Pinene", "Witch D.", "6953 2390 9886 2373"));
                TerpValues.Add(new terpValue(0, "γ-Terpinene", "Witch D.", "6953 2390 9886 2373"));
                TerpValues.Add(new terpValue(7.69, "δ-Limonene", "Witch D.", "6953 2390 9886 2373"));
                TerpValues.Add(new terpValue(0, "3-Carene", "G. Mints", "9436 5391 1236 0974"));
                TerpValues.Add(new terpValue(0.18, "Camphene", "G. Mints", "9436 5391 1236 0974"));
                TerpValues.Add(new terpValue(0, "Caryophyllene Oxide", "G. Mints", "9436 5391 1236 0974"));
                TerpValues.Add(new terpValue(0, "cis-Nerolidol", "G. Mints", "9436 5391 1236 0974"));
                TerpValues.Add(new terpValue(0.04, "Eucalyptol", "G. Mints", "9436 5391 1236 0974"));
                TerpValues.Add(new terpValue(0, "Geraniol", "G. Mints", "9436 5391 1236 0974"));
                TerpValues.Add(new terpValue(0, "Guaiol", "G. Mints", "9436 5391 1236 0974"));
                TerpValues.Add(new terpValue(0.11, "Isopulegol", "G. Mints", "9436 5391 1236 0974"));
                TerpValues.Add(new terpValue(1.98, "Linalool", "G. Mints", "9436 5391 1236 0974"));
                TerpValues.Add(new terpValue(0, "Menthol", "G. Mints", "9436 5391 1236 0974"));
                TerpValues.Add(new terpValue(0.2, "Ocimene", "G. Mints", "9436 5391 1236 0974"));
                TerpValues.Add(new terpValue(0, "p-Cymene", "G. Mints", "9436 5391 1236 0974"));
                TerpValues.Add(new terpValue(0.08, "Terpinolene", "G. Mints", "9436 5391 1236 0974"));
                TerpValues.Add(new terpValue(0.54, "trans-Nerolidol", "G. Mints", "9436 5391 1236 0974"));
                TerpValues.Add(new terpValue(1.39, "α-Bisabolol", "G. Mints", "9436 5391 1236 0974"));
                TerpValues.Add(new terpValue(3.3, "α-Humulene", "G. Mints", "9436 5391 1236 0974"));
                TerpValues.Add(new terpValue(0.53, "α-Pinene", "G. Mints", "9436 5391 1236 0974"));
                TerpValues.Add(new terpValue(0, "α-Terpinene", "G. Mints", "9436 5391 1236 0974"));
                TerpValues.Add(new terpValue(9.01, "β-Caryophyllene", "G. Mints", "9436 5391 1236 0974"));
                TerpValues.Add(new terpValue(4.32, "β-Myrcene", "G. Mints", "9436 5391 1236 0974"));
                TerpValues.Add(new terpValue(0.96, "β-Pinene", "G. Mints", "9436 5391 1236 0974"));
                TerpValues.Add(new terpValue(0, "γ-Terpinene", "G. Mints", "9436 5391 1236 0974"));
                TerpValues.Add(new terpValue(4.51, "δ-Limonene", "G. Mints", "9436 5391 1236 0974"));
                TerpValues.Add(new terpValue(0, "3-Carene", "Blueberry Headba0", "9628 5341 3355 9561"));
                TerpValues.Add(new terpValue(0.23, "Camphene", "Blueberry Headba0", "9628 5341 3355 9561"));
                TerpValues.Add(new terpValue(0, "Caryophyllene Oxide", "Blueberry Headba0", "9628 5341 3355 9561"));
                TerpValues.Add(new terpValue(0, "cis-Nerolidol", "Blueberry Headba0", "9628 5341 3355 9561"));
                TerpValues.Add(new terpValue(0, "Eucalyptol", "Blueberry Headba0", "9628 5341 3355 9561"));
                TerpValues.Add(new terpValue(0, "Geraniol", "Blueberry Headba0", "9628 5341 3355 9561"));
                TerpValues.Add(new terpValue(0, "Guaiol", "Blueberry Headba0", "9628 5341 3355 9561"));
                TerpValues.Add(new terpValue(0, "Isopulegol", "Blueberry Headba0", "9628 5341 3355 9561"));
                TerpValues.Add(new terpValue(1.23, "Linalool", "Blueberry Headba0", "9628 5341 3355 9561"));
                TerpValues.Add(new terpValue(0, "Menthol", "Blueberry Headba0", "9628 5341 3355 9561"));
                TerpValues.Add(new terpValue(2, "Ocimene", "Blueberry Headba0", "9628 5341 3355 9561"));
                TerpValues.Add(new terpValue(0, "p-Cymene", "Blueberry Headba0", "9628 5341 3355 9561"));
                TerpValues.Add(new terpValue(0.06, "Terpinolene", "Blueberry Headba0", "9628 5341 3355 9561"));
                TerpValues.Add(new terpValue(0.43, "trans-Nerolidol", "Blueberry Headba0", "9628 5341 3355 9561"));
                TerpValues.Add(new terpValue(0.77, "α-Bisabolol", "Blueberry Headba0", "9628 5341 3355 9561"));
                TerpValues.Add(new terpValue(0.87, "α-Humulene", "Blueberry Headba0", "9628 5341 3355 9561"));
                TerpValues.Add(new terpValue(15.45, "α-Pinene", "Blueberry Headba0", "9628 5341 3355 9561"));
                TerpValues.Add(new terpValue(0, "α-Terpinene", "Blueberry Headba0", "9628 5341 3355 9561"));
                TerpValues.Add(new terpValue(1.9, "β-Caryophyllene", "Blueberry Headba0", "9628 5341 3355 9561"));
                TerpValues.Add(new terpValue(1.75, "β-Myrcene", "Blueberry Headba0", "9628 5341 3355 9561"));
                TerpValues.Add(new terpValue(4.72, "β-Pinene", "Blueberry Headba0", "9628 5341 3355 9561"));
                TerpValues.Add(new terpValue(0, "γ-Terpinene", "Blueberry Headba0", "9628 5341 3355 9561"));
                TerpValues.Add(new terpValue(3.1, "δ-Limonene", "Blueberry Headba0", "9628 5341 3355 9561"));
                TerpValues.Add(new terpValue(12.443, "trans-Caryophyllene", "Traffic Jam", "68675_0005224528"));
                TerpValues.Add(new terpValue(6.081, "(R)-(+)-Limonene", "Traffic Jam", "68675_0005224528"));
                TerpValues.Add(new terpValue(3.803, "α-Humulene", "Traffic Jam", "68675_0005224528"));
                TerpValues.Add(new terpValue(3.115, "Linalool", "Traffic Jam", "68675_0005224528"));
                TerpValues.Add(new terpValue(1.727, "β-Myrcene", "Traffic Jam", "68675_0005224528"));
                TerpValues.Add(new terpValue(1.524, "Borneol", "Traffic Jam", "68675_0005224528"));
                TerpValues.Add(new terpValue(1.126, "trans-Nerolidol", "Traffic Jam", "68675_0005224528"));
                TerpValues.Add(new terpValue(0.628, "α-Bisabolol", "Traffic Jam", "68675_0005224528"));
                TerpValues.Add(new terpValue(0.555, "β-Pinene", "Traffic Jam", "68675_0005224528"));
                TerpValues.Add(new terpValue(0.537, "Fenchyl Alcohol", "Traffic Jam", "68675_0005224528"));
                TerpValues.Add(new terpValue(0.415, "α-Pinene", "Traffic Jam", "68675_0005224528"));
                TerpValues.Add(new terpValue(10.284, "trans-Caryophyllene", "Wedding Crasher", "59731_0005856782"));
                TerpValues.Add(new terpValue(4.16, "β-Myrcene", "Wedding Crasher", "59731_0005856782"));
                TerpValues.Add(new terpValue(4.072, "(R)-(+)-Limonene", "Wedding Crasher", "59731_0005856782"));
                TerpValues.Add(new terpValue(2.552, "Linalool", "Wedding Crasher", "59731_0005856782"));
                TerpValues.Add(new terpValue(2.3, "α-Humulene", "Wedding Crasher", "59731_0005856782"));
                TerpValues.Add(new terpValue(1.713, "trans-Nerolidol", "Wedding Crasher", "59731_0005856782"));
                TerpValues.Add(new terpValue(0.957, "Fenchyl Alcohol", "Wedding Crasher", "59731_0005856782"));
                TerpValues.Add(new terpValue(0.582, "β-Pinene", "Wedding Crasher", "59731_0005856782"));
                TerpValues.Add(new terpValue(0.571, "α-Bisabolol", "Wedding Crasher", "59731_0005856782"));
                TerpValues.Add(new terpValue(0.382, "α-Pinene", "Wedding Crasher", "59731_0005856782"));
                TerpValues.Add(new terpValue(10.58, "trans-Caryophyllene", "Space Age Cake", "19233_0005737034"));
                TerpValues.Add(new terpValue(6.409, "(R)-(+)-Limonene", "Space Age Cake", "19233_0005737034"));
                TerpValues.Add(new terpValue(5.987, "Linalool", "Space Age Cake", "19233_0005737034"));
                TerpValues.Add(new terpValue(3.378, "α-Humulene", "Space Age Cake", "19233_0005737034"));
                TerpValues.Add(new terpValue(3.042, "β-Myrcene", "Space Age Cake", "19233_0005737034"));
                TerpValues.Add(new terpValue(0.000871, "Fenchyl Alcohol", "Space Age Cake", "19233_0005737034"));
                TerpValues.Add(new terpValue(0.714, "α-Bisabolol", "Space Age Cake", "19233_0005737034"));
                TerpValues.Add(new terpValue(0.564, "β-Pinene", "Space Age Cake", "19233_0005737034"));
                TerpValues.Add(new terpValue(7.24, "β-Myrcene", "iCa0y", "67279_0005905658"));
                TerpValues.Add(new terpValue(6.054, "(R)-(+)-Limonene", "iCa0y", "67279_0005905658"));
                TerpValues.Add(new terpValue(4.906, "trans-Caryophyllene", "iCa0y", "67279_0005905658"));
                TerpValues.Add(new terpValue(3.962, "Linalool", "iCa0y", "67279_0005905658"));
                TerpValues.Add(new terpValue(1.534, "Fenchyl Alcohol", "iCa0y", "67279_0005905658"));
                TerpValues.Add(new terpValue(1.362, "α-Humulene", "iCa0y", "67279_0005905658"));
                TerpValues.Add(new terpValue(1.093, "trans-Nerolidol", "iCa0y", "67279_0005905658"));
                TerpValues.Add(new terpValue(0.741, "β-Pinene", "iCa0y", "67279_0005905658"));
                TerpValues.Add(new terpValue(0.636, "α-Bisabolol", "iCa0y", "67279_0005905658"));
                TerpValues.Add(new terpValue(0.511, "α-Pinene", "iCa0y", "67279_0005905658"));
                TerpValues.Add(new terpValue(10.635, "trans-Caryophyllene", "Ice Cream Cake", "64811_0005937028"));
                TerpValues.Add(new terpValue(6.449, "Linalool", "Ice Cream Cake", "64811_0005937028"));
                TerpValues.Add(new terpValue(6.448, "(R)-(+)-Limonene", "Ice Cream Cake", "64811_0005937028"));
                TerpValues.Add(new terpValue(3.382, "α-Humulene", "Ice Cream Cake", "64811_0005937028"));
                TerpValues.Add(new terpValue(2.729, "β-Myrcene", "Ice Cream Cake", "64811_0005937028"));
                TerpValues.Add(new terpValue(0.871, "Fenchyl Alcohol", "Ice Cream Cake", "64811_0005937028"));
                TerpValues.Add(new terpValue(0.646, "α-Bisabolol", "Ice Cream Cake", "64811_0005937028"));
                TerpValues.Add(new terpValue(0.513, "β-Pinene", "Ice Cream Cake", "64811_0005937028"));
                TerpValues.Add(new terpValue(12.955, "trans-Caryophyllene", "Shiprweck", "19290_0006067427"));
                TerpValues.Add(new terpValue(3.786, "α-Humulene", "Shiprweck", "19290_0006067427"));
                TerpValues.Add(new terpValue(3.455, "(R)-(+)-Limonene", "Shiprweck", "19290_0006067427"));
                TerpValues.Add(new terpValue(2.444, "Linalool", "Shiprweck", "19290_0006067427"));
                TerpValues.Add(new terpValue(1.907, "trans-Nerolidol", "Shiprweck", "19290_0006067427"));
                TerpValues.Add(new terpValue(1.15, "β-Myrcene", "Shiprweck", "19290_0006067427"));
                TerpValues.Add(new terpValue(0.802, "α-Bisabolol", "Shiprweck", "19290_0006067427"));
                TerpValues.Add(new terpValue(0.405, "β-Pinene", "Shiprweck", "19290_0006067427"));
                TerpValues.Add(new terpValue(6.84, "trans-Caryophyllene", "Boston Rntz #5 (H)", "PRPFLW100054-2405-28099"));
                TerpValues.Add(new terpValue(3.85, "δ-Limonene", "Boston Rntz #5 (H)", "PRPFLW100054-2405-28099"));
                TerpValues.Add(new terpValue(1.9, "β-Humulene", "Boston Rntz #5 (H)", "PRPFLW100054-2405-28099"));
                TerpValues.Add(new terpValue(1.53, "beta-Myrcene", "Boston Rntz #5 (H)", "PRPFLW100054-2405-28099"));
                TerpValues.Add(new terpValue(1.5, "Linalool", "Boston Rntz #5 (H)", "PRPFLW100054-2405-28099"));
                TerpValues.Add(new terpValue(1.08, "α-Bisabolol", "Boston Rntz #5 (H)", "PRPFLW100054-2405-28099"));
                TerpValues.Add(new terpValue(0.85, "Terpineol", "Boston Rntz #5 (H)", "PRPFLW100054-2405-28099"));
                TerpValues.Add(new terpValue(0.763, "trans-Nerolidol", "Boston Rntz #5 (H)", "PRPFLW100054-2405-28099"));
                TerpValues.Add(new terpValue(0.697, "Fenchyl Alcohol", "Boston Rntz #5 (H)", "PRPFLW100054-2405-28099"));
                TerpValues.Add(new terpValue(0.559, "β-Pinene", "Boston Rntz #5 (H)", "PRPFLW100054-2405-28099"));
                TerpValues.Add(new terpValue(0.551, "α-Pinene", "Boston Rntz #5 (H)", "PRPFLW100054-2405-28099"));


                try
                {

                }
                catch (Exception ex)
                {

                }

                if (strain != null)
                { currentStrain = TerpValues.Where(t => t.Strain == strain).ToList(); }
                else
                { currentStrain = TerpValues.Where(t => t.Strain == TerpValues[0].Strain).ToList(); }





                #endregion
            }

        }
        private void replaceCharacters()
        {

        }
        public string GetTerpeneColor(string terpene)
        {
            string color = "";

            loadmatrix();
            try
            {
                var r = Matrixes.Where(t => t.Name == terpene.Trim() ||   t.NamesOther.Contains(terpene.Trim())).FirstOrDefault();
                if (r is not null)
                {
                    color = r.Color;
                }
                else
                {
                    ; Console.WriteLine ( "Add terpene->" +terpene);
                }

            }
            catch (Exception ex)
            {

            }
            return color;

        }
        public string GetTerpeneDescription(string terpene)
        {
            string details = "";

            loadmatrix();
            try
            {
                var r = Matrixes.Where(t => t.Name == terpene.Trim() || t.NamesOther.Contains(terpene.Trim())).FirstOrDefault();
                if (r is not null)
                {
                    details = r.description;
                }
                else
                {
                    ; Console.WriteLine("Add terpene->" + terpene);
                }
            }
            catch (Exception ex)
            {

            }
            
            return details;

        }

        public List<string> GetTerpeneList()
        {
            List<string> terpenes = new List<string>();

            loadmatrix();

            terpenes = Matrixes.Select(t => t.Name).Distinct().ToList();

            return terpenes;

        }
        public string GetDBTerpName(string terpene)
        {
            string terpenes ="";

            loadmatrix();
            
                var r = Matrixes.Where(t => t.Name == terpene.Trim() || t.NamesOther.Contains(terpene.Trim())).FirstOrDefault();
                if (r is not null)
            if (Matrixes
                .Where(t => t.Name == terpene && t.name2.Length > 0)
                .Count() > 0)
            {
                terpenes = Matrixes
                .Where(t => t.Name == terpene)
                .FirstOrDefault().name2;
            }
            else
            {
                terpenes = terpene;
            }
            return terpenes;

        }
        public void loadmatrix(string strain = "")
        {
            if (Matrixes == null)
            {
                Matrixes = new List<matrixes>();
                #region data matrix
                Matrixes.Add(new matrixes(1, "(R)-(+)-Limonene", 1, 1, 1, "#008000"));
                Matrixes.Add(new matrixes(2, "Camphene", 1, 1, 2, "#33CC33"));
                Matrixes.Add(new matrixes(3, "Caryophyllene Oxide", 1, 1, 3, "#66FF66"));
                Matrixes.Add(new matrixes(4, "Eucalyptol", 1, 1, 4, "#CCFFCC", "", "Minty, camphor aroma"));
                Matrixes.Add(new matrixes(5, "Fenchyl Alcohol", 1, 1, 5, "#FFCCFF", "Endo-Fenchyl Alcohol"));
                Matrixes.Add(new matrixes(6, "Geraniol", 1, 1, 6, "#FF99FF", "", "Tobacco like aroma"));
                Matrixes.Add(new matrixes(7, "Guaiol", 1, 2, 1, "#CC00CC"));
                Matrixes.Add(new matrixes(8, "Isopulegol", 1, 2, 2, "#FFCCCC"));
                Matrixes.Add(new matrixes(9, "Linalool", 1, 2, 3, "#FF7C80", "", "Floral, lavender aroma"));
                Matrixes.Add(new matrixes(10, "Menthol", 1, 2, 4, "#CC0000"));
                Matrixes.Add(new matrixes(11, "δ-Limonene", 1, 2, 5, "#99FF33", "D-Limonene", "Second most abundant, citrus"));
                Matrixes.Add(new matrixes(12, "Terpineol", 1, 2, 6, "#0066FF", "Total Terpineol", "Lilac, floral aroma"));
                Matrixes.Add(new matrixes(13, "Terpinolene", 1, 3, 1, "#FF6699"));
                Matrixes.Add(new matrixes(14, "Valencene", 1, 3, 2, "#7030A0", "", "Tropical, citrus aroma"));
                Matrixes.Add(new matrixes(15, "cis-Nerolidol", 1, 3, 3, "#339966"));
                Matrixes.Add(new matrixes(16, "cis-Ocimene", 1, 3, 4, "#99FF33", "Ocimenes", "Tropical, musky aroma"));
                Matrixes.Add(new matrixes(17, "p-Cymene", 1, 3, 5, "#FF6699"));
                Matrixes.Add(new matrixes(18, "trans-Caryophyllene", 1, 3, 6, "#FF3399"));
                Matrixes.Add(new matrixes(19, "trans-Nerolidol", 1, 4, 1, "#CC3399"));
                Matrixes.Add(new matrixes(20, "trans-Ocimene", 1, 4, 2, "#7030A0"));
                Matrixes.Add(new matrixes(21, "α-Bisabolol", 1, 4, 3, "#002060", "alpha-Bisabolol"));
                Matrixes.Add(new matrixes(22, "α-Humulene", 1, 4, 4, "#0070C0", "alpha-Humulene", "foppy, herbal aroma"));
                Matrixes.Add(new matrixes(23, "α-Pinene", 1, 4, 5, "#00B0F0", "alpha-Pinene", "Pine, fir aroma"));
                Matrixes.Add(new matrixes(24, "α-Terpinene", 1, 4, 6, "#99FF33"));
                Matrixes.Add(new matrixes(25, "β-Caryophyllene", 1, 5, 1, "#92D050", "E-Caryophyllene", "Spicy, peppery aroma"));
                Matrixes.Add(new matrixes(26, "β-Myrcene", 1, 5, 2, "#FFFF00", "beta-Myrcene", "The most abundant terpene in modern commercial cannabis and gives it a peppery, spicy, balsam fragrance."));
                Matrixes.Add(new matrixes(27, "β-Pinene", 1, 5, 3, "#FFC000", "beta-Pinene"));
                Matrixes.Add(new matrixes(28, "γ-Terpinene", 1, 5, 4, "#99FF33"));
                Matrixes.Add(new matrixes(29, "δ-3-Carene", 1, 5, 5, "#C00000"));
                Matrixes.Add(new matrixes(30, "Borneol", 1, 5, 6, "#99FF33"));


                Matrixes.Add(new matrixes(31, "(R)-(+)-Limonene", 2, 1, 1, "#008000"));
                Matrixes.Add(new matrixes(32, "Camphene", 2, 1, 2, "#33CC33"));
                Matrixes.Add(new matrixes(33, "Caryophyllene Oxide", 2, 1, 3, "#66FF66"));
                Matrixes.Add(new matrixes(34, "Eucalyptol", 2, 6, 1, "#CCFFCC"));
                Matrixes.Add(new matrixes(35, "Fenchyl Alcohol", 2, 6, 2, "#FFCCFF"));
                Matrixes.Add(new matrixes(36, "Geraniol", 2, 6, 3, "#FF99FF"));
                Matrixes.Add(new matrixes(37, "Guaiol", 2, 2, 1, "#CC00CC"));
                Matrixes.Add(new matrixes(38, "Isopulegol", 2, 2, 2, "#FFCCCC"));
                Matrixes.Add(new matrixes(39, "Linalool", 2, 2, 3, "#FF7C80"));
                Matrixes.Add(new matrixes(40, "Menthol", 2, 7, 1, "#CC0000"));
                Matrixes.Add(new matrixes(41, "δ-Limonene", 2, 7, 2, "#66CCFF"));
                Matrixes.Add(new matrixes(42, "Terpineol", 2, 7, 3, "#0066FF"));
                Matrixes.Add(new matrixes(43, "Terpinolene", 2, 3, 1, "#FF6699"));
                Matrixes.Add(new matrixes(44, "Valencene", 2, 3, 2, "#7030A0"));
                Matrixes.Add(new matrixes(45, "cis-Nerolidol", 2, 3, 3, "#339966"));
                Matrixes.Add(new matrixes(46, "cis-Ocimene", 2, 9, 1, "#00CC00"));
                Matrixes.Add(new matrixes(47, "p-Cymene", 2, 9, 2, "#FF6699"));
                Matrixes.Add(new matrixes(48, "trans-Caryophyllene", 2, 9, 3, "#FF3399"));
                Matrixes.Add(new matrixes(49, "trans-Nerolidol", 2, 4, 1, "#CC3399"));
                Matrixes.Add(new matrixes(50, "trans-Ocimene", 2, 4, 2, "#7030A0"));
                Matrixes.Add(new matrixes(51, "α-Bisabolol", 2, 4, 3, "#002060"));
                Matrixes.Add(new matrixes(52, "α-Humulene", 2, 8, 1, "#0070C0"));
                Matrixes.Add(new matrixes(53, "α-Pinene", 2, 8, 2, "#00B0F0"));
                Matrixes.Add(new matrixes(54, "α-Terpinene", 2, 8, 3, "#00B050"));
                Matrixes.Add(new matrixes(55, "β-Caryophyllene", 2, 5, 1, "#92D050"));
                Matrixes.Add(new matrixes(56, "β-Myrcene", 2, 5, 2, "#FFFF00"));
                Matrixes.Add(new matrixes(57, "β-Pinene", 2, 5, 3, "#FFC000"));
                Matrixes.Add(new matrixes(58, "γ-Terpinene", 2, 10, 1, "#FF0000"));
                Matrixes.Add(new matrixes(59, "δ-3-Carene", 2, 10, 2, "#C00000"));
                Matrixes.Add(new matrixes(60, "Borneol", 2, 10, 3, "#99FF33"));
                Matrixes.Add(new matrixes(61, "(R)-(+)-Limonene", 3, 1, 1, "#008000"));
                Matrixes.Add(new matrixes(62, "Camphene", 3, 1, 2, "#33CC33"));
                Matrixes.Add(new matrixes(63, "Caryophyllene Oxide", 3, 10, 1, "#66FF66"));
                Matrixes.Add(new matrixes(64, "Eucalyptol", 3, 6, 1, "#CCFFCC"));
                Matrixes.Add(new matrixes(65, "Fenchyl Alcohol", 3, 6, 2, "#FFCCFF"));
                Matrixes.Add(new matrixes(66, "Geraniol", 3, 10, 2, "#FF99FF"));
                Matrixes.Add(new matrixes(67, "Guaiol", 3, 2, 1, "#CC00CC"));
                Matrixes.Add(new matrixes(68, "Isopulegol", 3, 2, 2, "#FFCCCC"));
                Matrixes.Add(new matrixes(69, "Linalool", 3, 11, 1, "#FF7C80"));
                Matrixes.Add(new matrixes(70, "Menthol", 3, 7, 1, "#CC0000"));
                Matrixes.Add(new matrixes(71, "δ-Limonene", 3, 7, 2, "#66CCFF"));
                Matrixes.Add(new matrixes(72, "Terpineol", 3, 11, 2, "#0066FF"));
                Matrixes.Add(new matrixes(73, "Terpinolene", 3, 3, 1, "#FF6699"));
                Matrixes.Add(new matrixes(74, "Valencene", 3, 3, 2, "#7030A0"));
                Matrixes.Add(new matrixes(75, "cis-Nerolidol", 3, 12, 1, "#339966"));
                Matrixes.Add(new matrixes(76, "cis-Ocimene", 3, 14, 1, "#00CC00"));
                Matrixes.Add(new matrixes(77, "p-Cymene", 3, 14, 2, "#FF6699"));
                Matrixes.Add(new matrixes(78, "trans-Caryophyllene", 3, 12, 2, "#FF3399"));
                Matrixes.Add(new matrixes(79, "trans-Nerolidol", 3, 4, 1, "#CC3399"));
                Matrixes.Add(new matrixes(80, "trans-Ocimene", 3, 4, 2, "#7030A0"));
                Matrixes.Add(new matrixes(81, "α-Bisabolol", 3, 13, 1, "#002060"));
                Matrixes.Add(new matrixes(82, "α-Humulene", 3, 8, 1, "#0070C0"));
                Matrixes.Add(new matrixes(83, "α-Pinene", 3, 8, 2, "#00B0F0"));
                Matrixes.Add(new matrixes(84, "α-Terpinene", 3, 13, 2, "#00B050"));
                Matrixes.Add(new matrixes(85, "β-Caryophyllene", 3, 5, 1, "#92D050"));
                Matrixes.Add(new matrixes(86, "β-Myrcene", 3, 5, 2, "#FFFF00"));
                Matrixes.Add(new matrixes(87, "β-Pinene", 3, 15, 1, "#FFC000"));
                Matrixes.Add(new matrixes(88, "γ-Terpinene", 3, 9, 1, "#FF0000"));
                Matrixes.Add(new matrixes(89, "δ-3-Carene", 3, 9, 2, "#C00000"));
                Matrixes.Add(new matrixes(90, "Borneol", 3, 15, 2, "#99FF33"));
                Matrixes.Add(new matrixes(91, "(R)-(+)-Limonene", 4, 1, 1, "#008000"));
                Matrixes.Add(new matrixes(92, "Camphene", 4, 2, 1, "#33CC33"));
                Matrixes.Add(new matrixes(93, "Caryophyllene Oxide", 4, 3, 1, "#66FF66"));
                Matrixes.Add(new matrixes(94, "Eucalyptol", 4, 4, 1, "#CCFFCC"));
                Matrixes.Add(new matrixes(95, "Fenchyl Alcohol", 4, 5, 1, "#FFCCFF"));
                Matrixes.Add(new matrixes(96, "Geraniol", 4, 6, 1, "#FF99FF"));
                Matrixes.Add(new matrixes(97, "Guaiol", 4, 7, 1, "#CC00CC"));
                Matrixes.Add(new matrixes(98, "Isopulegol", 4, 8, 1, "#FFCCCC"));
                Matrixes.Add(new matrixes(99, "Linalool", 4, 9, 1, "#FF7C80"));
                Matrixes.Add(new matrixes(100, "Menthol", 4, 10, 1, "#CC0000"));
                Matrixes.Add(new matrixes(101, "δ-Limonene", 4, 11, 1, "#66CCFF"));
                Matrixes.Add(new matrixes(102, "Terpineol", 4, 12, 1, "#0066FF"));
                Matrixes.Add(new matrixes(103, "Terpinolene", 4, 13, 1, "#FF6699"));
                Matrixes.Add(new matrixes(104, "Valencene", 4, 14, 1, "#7030A0"));
                Matrixes.Add(new matrixes(105, "cis-Nerolidol", 4, 15, 1, "#339966"));
                Matrixes.Add(new matrixes(106, "cis-Ocimene", 4, 16, 1, "#00CC00"));
                Matrixes.Add(new matrixes(107, "p-Cymene", 4, 17, 1, "#FF6699"));
                Matrixes.Add(new matrixes(108, "trans-Caryophyllene", 4, 18, 1, "#FF3399"));
                Matrixes.Add(new matrixes(109, "trans-Nerolidol", 4, 19, 1, "#CC3399"));
                Matrixes.Add(new matrixes(110, "trans-Ocimene", 4, 20, 1, "#7030A0"));
                Matrixes.Add(new matrixes(111, "α-Bisabolol", 4, 21, 1, "#002060"));
                Matrixes.Add(new matrixes(112, "α-Humulene", 4, 22, 1, "#0070C0"));
                Matrixes.Add(new matrixes(113, "α-Pinene", 4, 23, 1, "#00B0F0"));
                Matrixes.Add(new matrixes(114, "α-Terpinene", 4, 24, 1, "#00B050"));
                Matrixes.Add(new matrixes(115, "β-Caryophyllene", 4, 25, 1, "#92D050"));
                Matrixes.Add(new matrixes(116, "β-Myrcene", 4, 26, 1, "#FFFF00"));
                Matrixes.Add(new matrixes(117, "β-Pinene", 4, 27, 1, "#FFC000"));
                Matrixes.Add(new matrixes(118, "γ-Terpinene", 4, 28, 1, "#FF0000"));
                Matrixes.Add(new matrixes(119, "δ-3-Carene", 4, 29, 1, "#C00000"));
                Matrixes.Add(new matrixes(120, "Borneol", 4, 30, 1, "#99FF33"));
                Matrixes.Add(new matrixes(121, "(R)-(+)-Limonene", 5, 1, 1, "#008000"));
                Matrixes.Add(new matrixes(122, "Camphene", 5, 1, 2, "#33CC33"));
                Matrixes.Add(new matrixes(123, "Caryophyllene Oxide", 5, 1, 3, "#66FF66"));
                Matrixes.Add(new matrixes(124, "Eucalyptol", 5, 1, 4, "#CCFFCC"));
                Matrixes.Add(new matrixes(125, "Fenchyl Alcohol", 5, 1, 5, "#FFCCFF"));
                Matrixes.Add(new matrixes(126, "Geraniol", 5, 1, 6, "#FF99FF"));
                Matrixes.Add(new matrixes(127, "Guaiol", 5, 1, 7, "#CC00CC"));
                Matrixes.Add(new matrixes(128, "Isopulegol", 5, 1, 8, "#FFCCCC"));
                Matrixes.Add(new matrixes(129, "Linalool", 5, 1, 9, "#FF7C80"));
                Matrixes.Add(new matrixes(130, "Menthol", 5, 1, 10, "#CC0000"));
                Matrixes.Add(new matrixes(131, "δ-Limonene", 5, 1, 11, "#66CCFF"));
                Matrixes.Add(new matrixes(132, "Terpineol", 5, 1, 12, "#0066FF"));
                Matrixes.Add(new matrixes(133, "Terpinolene", 5, 1, 13, "#FF6699"));
                Matrixes.Add(new matrixes(134, "Valencene", 5, 1, 14, "#7030A0"));
                Matrixes.Add(new matrixes(135, "cis-Nerolidol", 5, 1, 15, "#339966"));
                Matrixes.Add(new matrixes(136, "cis-Ocimene", 5, 1, 16, "#00CC00"));
                Matrixes.Add(new matrixes(137, "p-Cymene", 5, 1, 17, "#FF6699"));
                Matrixes.Add(new matrixes(138, "trans-Caryophyllene", 5, 1, 18, "#FF3399"));
                Matrixes.Add(new matrixes(139, "trans-Nerolidol", 5, 1, 19, "#CC3399"));
                Matrixes.Add(new matrixes(140, "trans-Ocimene", 5, 1, 20, "#7030A0"));
                Matrixes.Add(new matrixes(141, "α-Bisabolol", 5, 1, 21, "#002060"));
                Matrixes.Add(new matrixes(142, "α-Humulene", 5, 1, 22, "#0070C0"));
                Matrixes.Add(new matrixes(143, "α-Pinene", 5, 1, 23, "#00B0F0"));
                Matrixes.Add(new matrixes(144, "α-Terpinene", 5, 1, 24, "#00B050"));
                Matrixes.Add(new matrixes(145, "β-Caryophyllene", 5, 1, 25, "#92D050"));
                Matrixes.Add(new matrixes(146, "β-Myrcene", 5, 1, 26, "#FFFF00"));
                Matrixes.Add(new matrixes(147, "β-Pinene", 5, 1, 27, "#FFC000"));
                Matrixes.Add(new matrixes(148, "γ-Terpinene", 5, 1, 28, "#FF0000"));
                Matrixes.Add(new matrixes(149, "δ-3-Carene", 5, 1, 29, "#C00000"));
                Matrixes.Add(new matrixes(150, "Borneol", 5, 1, 30, "#99FF33"));


                #endregion
                #region add alternate names
                foreach (matrixes m in Matrixes)
                {

                    if (m.Name == "Fenchyl Alcohol") { m.NamesOther.Add("Endo-Fenchyl Alcohol"); }
                    else if (m.Name == "cis-Nerolidol") { m.NamesOther.Add("E-Nerolidol"); }
                    
                    else if (m.Name == "(R)-(+)-Limonene") { m.NamesOther.Add("(R)-( )-Limonene"); }
                    else if (m.Name == "δ-Limonene") { m.NamesOther.Add("D-Limonene"); }
                    else if (m.Name == "Terpineol") { m.NamesOther.Add("Total Terpineol"); }
                    else if (m.Name == "cis-Ocimene") { m.NamesOther.AddRange([ "Ocimenes","Ocimene"]); }
                    else if (m.Name == "α-Bisabolol") { m.NamesOther.Add("alpha-Bisabolol"); }
                    else if (m.Name == "α-Humulene") { m.NamesOther.Add("alpha-Humulene"); }
                    else if (m.Name == "α-Pinene") { m.NamesOther.Add("alpha-Pinene"); }
                    else if (m.Name == "β-Caryophyllene") { m.NamesOther.Add("E-Caryophyllene"); }
                    else if (m.Name == "β-Myrcene") { m.NamesOther.Add("beta-Myrcene"); }
                    else if (m.Name == "β-Pinene") { m.NamesOther.Add("beta-Pinene"); }

                }

                #endregion
            }

        }
        public void terprintTable(string batchin = "", string sortorder = "")
        {

            if (batchin != "")

            {

                currentStrain = TerpValues.Where(t => t.Batch == batchin).ToList();
                size = "Micro";

            }
            else
            {

                // size = Request.Form["size"].ToString();
                // strain = Request.Form["strain"].ToString();
                //  matrix = Convert.ToInt32(Request.Form["matrix"].ToString());
                //test
            }
            string temprow = "";
            string temprows = "";
            int currentRow = 1;
            int maxRow = Matrixes.Max(t => t.Row);
            Random rnd = new Random();
            string width = "";
            if (size == "Micro")
            {
                width = "width: 10px; height: 10px;";
                temprows += "<table border=\"1 px gray;\"><tr>";
                //  temprows += "<table style='width: 15px'><tr>";
            }
            if (size == "Small")
            {
                width = "width: 25px;height: 25px;";
                temprows += "<table ><tr>";
                //  temprows += "<table style='width: 15px'><tr>";
            }
            else if (size == "Medium")
            {
                width = "width: 50px;height: 50px;";
                temprows += "<table ><tr>";
                // temprows += "<table style='width: 300px'><tr>";
            }
            else if (size == "Large")
            {
                width = "width: 100px;height: 100px;";
                temprows += "<table ><tr>";
            };
            List<matrixes> localmatrix = Matrixes;
            // if(sortorder =="name")
            {
                //    localmatrix = Matrixes.Where(t => t.Matrix == matrix).OrderBy(t=>t.Name).ToList();
            }
            // else
            {
                localmatrix = Matrixes.Where(t => t.Matrix == matrix).OrderBy(t => t.Column).OrderBy(t => t.Row).ToList();
            }
            foreach (var o in localmatrix)
            {
                if (o.Matrix == matrix)
                {
                    if (o.Row > currentRow)
                    {
                        currentRow += 1;
                        temprows += "</tr>";
                        temprows += "<tr>";
                    }
                    if (currentStrain.Where(t => t.TerpName == o.Name).ToList().Count > 0 && currentStrain.Where(t => t.TerpName == o.Name).FirstOrDefault().Value > 0)
                    {
                        ///not zero value output formatted cell 

                        string terpnamecurrent = o.Name;
                        string terpnamestrain = currentStrain.Where(t => t.TerpName == o.Name).FirstOrDefault().TerpName;

                        double op = currentStrain.Where(t => t.TerpName.ToLower() == o.Name.ToLower()).FirstOrDefault().Value;



                        string opp = Math.Round((op * .1), 4).ToString() + "%";
                        double opacity = Math.Round((op * .1), 3);
                        double opacitynondec = Math.Round((op * 10), 2);
                        temprow = "";

                        string tooltip = o.Name + " " + opp;

                        //set table cell colors and sizes
                        if (size != "Micro")
                        {
                            temprow += string.Format("<td title=\"{5}\" style='{3}border:solid;border-color:{1};background-color:{1};opacity:{2}'> <div  style=\"z-index:{4};opacity:1\"> ", o.Id, o.Color, opacity, width, opacitynondec, tooltip);
                        }
                        else
                        {
                            temprow += string.Format("<td title=\"{5}\" style='{3}background-color:{1};opacity:{2}'>  ", o.Id, o.Color, opacity, width, opacitynondec, tooltip);


                        }
                        //set writing

                        if (size == "Micro" || size == "Small")
                        {

                            temprow += string.Format(" ", opp, o.Name);
                        }
                        else
                        {
                            temprow += string.Format("<span style=\"z-index:100\" class='badge bg-black text-bg-info'>{0}</span>", o.Name, opacity, o.Color);

                            temprow += string.Format("<span class=\"badge bg-black rounded-pill text-bg-info\">{1}</span>", op, opp);

                        }

                        temprow += "</td>";

                    }

                    else
                    {
                        ///zero value output blank cell 
                        temprow = "";
                        //temprow += string.Format("<tr >", o.Color);// "<tr bgcolor="">";
                        temprow += string.Format("<td  style='{3}opacity:{2}'>  ", o.Id, o.Color, 0, width);
                        //temprow += string.Format(" {0}   ", o.Name);
                        //temprow += string.Format(" {0} , ", o.Matrix);
                        //  temprow += string.Format(" Row {0}, Column {1} ", o.Row,o.Column );
                        //temprow += string.Format(" {0} , ", o.Column);
                        //temprow += string.Format(" {0} ", o.Color);

                        temprow += string.Format("  </td>", "");
                    }

                    temprows = temprows + temprow;

                }
            }

            temprows += "</tr></table>";

            outputrows = (MarkupString)temprows;
            // batchin = "";





        }

        public void setCurrentStrain()
        {
            if (strain != null && strain != "")
            {
                currentStrain = TerpValues.Where(t => t.Strain == strain).Where(t => t.Batch == batch).Where(t => t.Value > 0).ToList();
                strain = currentStrain[0].Strain;
                currentTerpenes = currentStrain.Where(t => t.Value > 0).ToList().Count;
            }
            else
            {

                currentStrain = TerpValues.Where(t => t.Strain == Options.First().Value).ToList();
                strain = Options.First().Value;
                currentTerpenes = currentStrain.Where(t => t.Value > 0).ToList().Count;

            }
        }
    }
}

