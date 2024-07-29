using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Components;
using Terprint.Web.Models;
using System.Numerics;
using System.Drawing.Drawing2D;
using Microsoft.Identity.Client;
using Microsoft.AspNetCore.WebUtilities;
using OpenTelemetry.Trace;
using Microsoft.AspNetCore.Components.Routing;
using Microsoft.Extensions.Caching.Distributed;
using Terprint.Web.Components;
using StackExchange.Redis;
using System.Composition.Convention;
using Microsoft.CodeAnalysis.CSharp.Syntax;


namespace Terprint.Web
{
    public class common
    {
        public static string? GetQueryValue(string key, NavigationManager NavManager)
        {
            try
            {
                ;
                var uri = NavManager.ToAbsoluteUri(NavManager.Uri);
                if (QueryHelpers.ParseQuery(uri.Query).TryGetValue(key, out var outval))
                {
                    return outval;
                }
                else
                {
                    return "";
                    return null;
                }
            }
            catch
            {
                return null;
            }
        }
        public static string CreateStrainLink(string strain)
        {
            string s = "";
            try
            {
                s = "<a href=\"/StrainProfile?strain=" + System.Web.HttpUtility.UrlEncode(strain) + "\">" + strain + "</a>";
            }
            catch (Exception ex)
            {

            }
            return s;
        }
        public static string CreateBatchLink(string batch)
        {
            string s = "";
            try
            {
                s = "<a href=\"/BatchProfile?batch=" + System.Web.HttpUtility.UrlEncode(batch) + "\">" + batch + "</a>";
            }
            catch (Exception ex)
            {

            }
            return s;
        }
        public static string CreateRatingCategoryLink(string ratingcategory, int ratingcategoryid)
        {
            string s = "";
            try
            {
                s = "<a href=\"/ratingcategoryprofile?ratingcategory="
                    + System.Web.HttpUtility.UrlEncode(ratingcategory)
                    + "&ratingcategoryid="
                    + ratingcategoryid + "\">"
                    + ratingcategory + "</a>";
                s = " " + ratingcategory + " ";
            }
            catch (Exception ex)
            {

            }
            return s;
        }
        public class Matrixes
        {
            public Matrixes()
            {
                MatrixList = new List<Matrix>();
                MatrixDefinitionList = new List<MatrixDefinition>();
                LoadMatrixDefinitions();
                LoadMatrixes();
            }
            private void LoadMatrixes()
            {
                Terpenes Terpenes = new Terpenes();
                foreach (var md in MatrixDefinitionList)
                {
                    int id = 1;
                    int row = 1;
                    while (row <= md.rows)
                    {
                        int col = 1;

                        while (col <= md.columns)
                        {
                            if (Terpenes.TerpeneList.Where(t => t.Id == id).FirstOrDefault() != null)
                            {
                                Terpenes.Terpene t = Terpenes.TerpeneList.Where(t => t.Id == id).FirstOrDefault();
                                MatrixList.Add(new Matrix()
                                {
                                    Terpene = t,
                                    MatrixDefinitionid = md.id,
                                    id = id,
                                    column = col,
                                    row = row

                                });

                            }
                            id++;


                            col++;
                        }
                        row++;
                    }
                }
            }
            private void LoadMatrixDefinitions()
            {
                MatrixDefinitionList.Add(new MatrixDefinition() { id = 1, rows = 6, columns = 6 });
                MatrixDefinitionList.Add(new MatrixDefinition() { id = 2, rows = 11, columns = 3 });
                MatrixDefinitionList.Add(new MatrixDefinition() { id = 3, rows = 17, columns = 2 });
                MatrixDefinitionList.Add(new MatrixDefinition() { id = 4, rows = 34, columns = 1 });
                MatrixDefinitionList.Add(new MatrixDefinition() { id = 5, rows = 1, columns = 34 });
            }
            public List<Matrix> MatrixList { get; set; }
            public List<MatrixDefinition> MatrixDefinitionList { get; set; }
            public class Matrix
            {
                public int id { get; set; }
                public int MatrixDefinitionid { get; set; }
                public int row { get; set; }
                public int column { get; set; }
                public Terpenes.Terpene Terpene { get; set; }
            }
            public class MatrixDefinition
            {
                public int id { get; set; }
                public int rows { get; set; }
                public int columns { get; set; }
            }
        }
        public class Terpenes
        {
            public List<Terpene> TerpeneList { get; set; }
            public Terpenes()
            {
                TerpeneList = new List<Terpene>();

                //TerpeneList.Add(new Terpene() { TerpeneName = "(R)-(+)-Limonene", Color = "#008000", Id = 1, OtherNames = { } });
                TerpeneList.Add(new Terpene() { TerpeneName = "Camphene", Color = "#33CC33", Id = 2, OtherNames = { } });
                TerpeneList.Add(new Terpene() { TerpeneName = "Caryophyllene Oxide", Color = "#66FF66", Id = 3, OtherNames = { } });
                TerpeneList.Add(new Terpene() { TerpeneName = "Eucalyptol", Color = "#CCFFCC", Id = 4, OtherNames = { }, Description = "Minty, camphor aroma" });
                TerpeneList.Add(new Terpene() { TerpeneName = "Fenchyl Alcohol", Color = "#FFCCFF", Id = 5, OtherNames = { "endo-fenchyl alcohol" } });
                TerpeneList.Add(new Terpene() { TerpeneName = "Geraniol", Color = "#FF99FF", Id = 6, OtherNames = { }, Description = "Tobacco like aroma" });
                TerpeneList.Add(new Terpene() { TerpeneName = "Guaiol", Color = "#CC00CC", Id = 7, OtherNames = { } });
                TerpeneList.Add(new Terpene() { TerpeneName = "Isopulegol", Color = "#FFCCCC", Id = 8, OtherNames = { } });
                TerpeneList.Add(new Terpene() { TerpeneName = "Linalool", Color = "#FF7C80", Id = 9, OtherNames = { }, Description = "Floral, lavender aroma" });
                TerpeneList.Add(new Terpene() { TerpeneName = "Menthol", Color = "#CC0000", Id = 10, OtherNames = { } });
                TerpeneList.Add(new Terpene() { TerpeneName = "δ-Limonene", Color = "#66CCFF", Id = 11, OtherNames = { "d-limonene", "(r)-(+)-limonene", "limonene", "(r)-( )-limonene" }, Description = "Second most abundant, citrus" });
                TerpeneList.Add(new Terpene() { TerpeneName = "Terpineol", Color = "#0066FF", Id = 12, OtherNames = { "total terpineol", "alpha-terpineol" }, Description = "Lilac, floral aroma" });
                TerpeneList.Add(new Terpene() { TerpeneName = "Terpinolene", Color = "#0000CC", Id = 13, OtherNames = { "alpha-terpinolene" } });
                TerpeneList.Add(new Terpene() { TerpeneName = "Valencene", Color = "#006666", Id = 14, OtherNames = { }, Description = "Tropical, citrus aroma" });
                TerpeneList.Add(new Terpene() { TerpeneName = "cis-Nerolidol", Color = "#339966", Id = 15, OtherNames = { "e-nerolidol", "trans-nerolidol" } });
                TerpeneList.Add(new Terpene() { TerpeneName = "Ocimene", Color = "#00CC00", Id = 16, OtherNames = { "ocimenes", "cis-ocimene", "trans-ocimene" }, Description = "Tropical, musky aroma" });
                TerpeneList.Add(new Terpene() { TerpeneName = "p-Cymene", Color = "#FF6699", Id = 17, OtherNames = { } });
                TerpeneList.Add(new Terpene() { TerpeneName = "trans-Caryophyllene", Color = "#FF3399", Id = 18, OtherNames = { } });
                TerpeneList.Add(new Terpene() { TerpeneName = "trans-Nerolidol", Color = "#CC3399", Id = 19, OtherNames = { } });
                TerpeneList.Add(new Terpene() { TerpeneName = "α-Bisabolol", Color = "#002060", Id = 20, OtherNames = { "alpha-bisabolol" } });
                TerpeneList.Add(new Terpene() { TerpeneName = "α-Humulene", Color = "#0070C0", Id = 21, OtherNames = { "alpha-humulene" }, Description = "Hoppy, herbal aroma" });
                TerpeneList.Add(new Terpene() { TerpeneName = "α-Pinene", Color = "#00B0F0", Id = 22, OtherNames = { "alpha-pinene" }, Description = "Pine, fir aroma" });
                TerpeneList.Add(new Terpene() { TerpeneName = "α-Terpinene", Color = "#00B050", Id = 23, OtherNames = { "alpha-terpinene", "γ-terpinene", "alpha-terpinene", "gamma-terpinene" } });
                TerpeneList.Add(new Terpene() { TerpeneName = "β-Caryophyllene", Color = "#92D050", Id = 24, OtherNames = { "e-caryophyllene", "beta-caryophyllene" }, Description = "Spicy, peppery aroma" });
                TerpeneList.Add(new Terpene() { TerpeneName = "β-Myrcene", Color = "#FFFF00", Id = 25, OtherNames = { "beta-myrcene" }, Description = "The most abundant terpene in modern commercial cannabis and gives it a peppery, spicy, balsam fragrance." });
                TerpeneList.Add(new Terpene() { TerpeneName = "β-Pinene", Color = "#FFC000", Id = 26, OtherNames = { "beta-pinene" } });
                TerpeneList.Add(new Terpene() { TerpeneName = "δ-3-Carene", Color = "#C00000", Id = 27, OtherNames = { } });
                TerpeneList.Add(new Terpene() { TerpeneName = "Borneol", Color = "#99FF33", Id = 28, OtherNames = { "isoborneol" } });
                TerpeneList.Add(new Terpene() { TerpeneName = "Sabinene", Color = "#C0C0C0", Id = 29, OtherNames = { } });
                TerpeneList.Add(new Terpene() { TerpeneName = "Farnesene", Color = "#00CC99", Id = 30, OtherNames = { } });
                TerpeneList.Add(new Terpene() { TerpeneName = "Geranyl Acetate", Color = "#996633", Id = 31, OtherNames = { } });
                TerpeneList.Add(new Terpene() { TerpeneName = "Phellandrene", Color = "#54065A", Id = 32, OtherNames = { "alpha-phellandrene" } });




            }
            public class Terpene
            {
                public Terpene()
                {
                    OtherNames = new List<string>();
                }
                public string TerpeneName { get; set; }
                public string Description { get; set; }
                public string Color { get; set; }
                public int Id { get; set; }
                public List<string> OtherNames { get; set; }


            }
        }
        public static class config
        {
            public static string appname = "Terptastic";
        }

        public class AppState
        {
            public class StateContainer
            {
                public class TerpeneValue
                {
                    private List<Models.TerpeneValue> terpenevalues;

                    public List<Models.TerpeneValue> TerpeneValues
                    {
                        get => terpenevalues ?? null;
                        set
                        {
                            IConnectionMultiplexer connectionMultiplexer;
                            terpenevalues = value;

                            NotifyStateChanged();
                        }
                    }
                    public event Action? OnChange;

                    private void NotifyStateChanged() => OnChange?.Invoke();

                }
                public class THCValue
                {
                    private List<Models.THCValue> thcvalues;

                    public List<Models.THCValue> THCValues
                    {
                        get => thcvalues ?? null;
                        set
                        {
                            thcvalues = value;
                            NotifyStateChanged();
                        }
                    }
                    public event Action? OnChange;

                    private void NotifyStateChanged() => OnChange?.Invoke();

                }
                public class Grower
                {
                    private List<Models.Grower> growers;

                    public List<Models.Grower> Growers
                    {
                        get => growers ?? null;
                        set
                        {
                            growers = value;
                            NotifyStateChanged();
                        }
                    }
                    public event Action? OnChange;

                    private void NotifyStateChanged() => OnChange?.Invoke();

                }
                public class Strain
                {
                    private List<Models.Strain> strains;

                    public List<Models.Strain> Strains
                    {
                        get => strains ?? null;
                        set
                        {
                            strains = value;
                            NotifyStateChanged();
                        }
                    }
                    public event Action? OnChange;

                    private void NotifyStateChanged() => OnChange?.Invoke();

                }

                public class Batch
                {
                    private List<Models.Batch> batches;
                    public List<Models.Batch> Batches
                    {
                        get => batches ?? null;
                        set
                        {
                            batches = value;
                            NotifyStateChanged();
                        }
                    }
                    public event Action? OnChange;

                    private void NotifyStateChanged() => OnChange?.Invoke();
                }
                public class RatingCategory
                {
                    private List<Models.RatingCategory> ratingcategories;
                    public List<Models.RatingCategory> RatingCategories
                    {
                        get => ratingcategories ?? null;
                        set
                        {
                            ratingcategories = value;
                            NotifyStateChanged();
                        }
                    }
                    public event Action? OnChange;

                    private void NotifyStateChanged() => OnChange?.Invoke();
                }

            }
            public static class menuItems
            {

                public static List<Strain> Strains
                {
                    get
                    {
                        if (strains is null)
                        { }
                        return strains;
                    }
                    set { strains = value; }
                }
                public static List<Grower> Growers { get; set; }
                public static List<Batch> Batches { get; set; }
                private static List<Strain> strains { get; set; }
                private static List<Grower> growers { get; set; }
                private static List<Batch> batches { get; set; }
            }
            public RatingCategory ratingCategory { get; set; }
            public int batchid { get; set; }
            public int ratingcategoryid { get; set; }

            //public class TerprintTable
            //{
            //    public string batchId { get; set; }
            //    public int matrixId { get; set; }

            //    public int matrixSize { get; set; }
            //}

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
            public class StrainComparer
            {
                public class TerpList
                {
                    public string strain1;
                    public string strain2;
                    public string terpene;
                    public double terpeneValue;

                }
                common.Matrixes m = new Matrixes();
                public string strain1;
                public string strain2;
                public List<KeyValuePair<string, double>> TerpsinBoth;
                public List<KeyValuePair<string, double>> TerpsOnlyin1;
                public List<KeyValuePair<string, double>> TerpsOnlyin2;

                public List<TerpeneValue> strain1Terps;
                public List<TerpeneValue> strain2Terps;

                public List<TerpList> terplistboth;

                public class TerpCompareData
                {
                    public int terplist { get; set; }
                    public string originalTerpName { get; set; }
                    public string dbTerpName { get; set; }
                    public bool in1 { get; set; }
                    public bool in2 { get; set; }
                    public bool inboth { get; set; }
                    public double value { get; set; }
                }
                public StrainComparer(string strain1, string strain2, List<TerpeneValue> strain1Terps,
                List<TerpeneValue> strain2Terps)
                {
                    List<TerpCompareData> tcd = new List<TerpCompareData>();
                    List<string> terpenes = new List<string>();
                    common.Components c = new common.Components();
                    terplistboth = new List<TerpList>();
                    TerpsinBoth = new List<KeyValuePair<string, double>>();
                    TerpsOnlyin1 = new List<KeyValuePair<string, double>>();
                    TerpsOnlyin2 = new List<KeyValuePair<string, double>>();
                    foreach (var r in strain1Terps)
                    {
                        tcd.Add(new TerpCompareData()
                        {
                            terplist = 1,
                            originalTerpName = r.TerpeneName,
                            dbTerpName = c.GetDBTerpName(r.TerpeneName),
                            value = r.Value,
                            in1 = true
                        });

                    }
                    foreach (var r in strain2Terps)
                    {
                        tcd.Add(new TerpCompareData()
                        {
                            terplist = 2,
                            originalTerpName = r.TerpeneName,
                            dbTerpName = c.GetDBTerpName(r.TerpeneName),
                            value = r.Value,
                            in2 = true
                        });

                    }
                    terpenes = tcd.Select(t => t.dbTerpName).Distinct().ToList();
                    foreach (string s in terpenes)
                    {
                        if (tcd.Where(t => t.dbTerpName == s).Count() ==2)
                        {

                            TerpsinBoth.Add(new KeyValuePair<string, double>(s, 0));
                        }
                       else if (tcd.Where(t => t.dbTerpName == s).Where(t => t.terplist == 1).Count() == 1)
                        {

                            TerpsOnlyin1.Add(new KeyValuePair<string, double>(s, 0));
                        }
                       else if (tcd.Where(t => t.dbTerpName == s).Where(t => t.terplist == 2).Count() == 1)
                        {

                            TerpsOnlyin2.Add(new KeyValuePair<string, double>(s,0));
                        }
                    } 

                }
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

                }

            }
            private void replaceCharacters()
            {

            }
            public string GetTerpeneColor(string terpene)
            {
                string color = "";
                common.Matrixes m = new Matrixes();
                loadmatrix();
                try
                {
                    var r = m.MatrixList.Where(t => t.Terpene.TerpeneName == terpene.Trim() || t.Terpene.OtherNames.Contains(terpene.Trim())).FirstOrDefault();
                    if (r is not null)
                    {
                        color = r.Terpene.Color;
                    }
                    else
                    {
                        ; Console.WriteLine("Add terpene->" + terpene);
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
                common.Matrixes m = new Matrixes();
                try
                {
                    var r = m.MatrixList.Where(t => t.Terpene.TerpeneName == terpene.Trim() || t.Terpene.OtherNames.Contains(terpene.Trim())).FirstOrDefault();
                    if (r is not null)
                    {
                        details = r.Terpene.Description;
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
                common.Matrixes m = new Matrixes();
                List<string> terpenes = new List<string>();


                terpenes = m.MatrixList.Select(t => t.Terpene.TerpeneName).Distinct().ToList();

                return terpenes;

            }
            public string GetDBTerpName(string terpene)
            {
                string terpenes = "";
                
                common.Matrixes m = new Matrixes();
                common.Terpenes t = new Terpenes();
                foreach (var terp in t.TerpeneList)
                {
                    if (terp.TerpeneName.ToLower()  == terpene.ToLower() )
                    {
                        terpenes = terp.TerpeneName;
                    }
                    if (terp.OtherNames.Contains(terpene.ToLower()))
                    {
                        terpenes = terp.TerpeneName;
                    }
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

                    Matrixes.Add(new matrixes(150, "Farnesene", 1, 7, 1, "#3AE6F8"));

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
                    Matrixes.Add(new matrixes(150, "Farnesene", 2, 11, 1, "#3AE6F8"));
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
                    Matrixes.Add(new matrixes(150, "Farnesene", 3, 16, 2, "#3AE6F8"));
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
                    Matrixes.Add(new matrixes(150, "Farnesene", 4, 30, 1, "#3AE6F8"));
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
                    Matrixes.Add(new matrixes(150, "Farnesene", 5, 1, 31, "#3AE6F8"));

                    //add FARNESENE, Geranyl Acetate

                    #endregion
                    #region add alternate names
                    foreach (matrixes m in Matrixes)
                    {

                        if (m.Name == "Fenchyl Alcohol") { m.NamesOther.Add("endo-fenchyl alcohol"); }
                        else if (m.Name == "cis-Nerolidol") { m.NamesOther.Add("e-nerolidol"); m.NamesOther.Add("trans-nerolidol"); }
                        else if (m.Name == "δ-Limonene") { m.NamesOther.Add("limonene"); m.NamesOther.Add("d-limonene"); m.NamesOther.Add("limonene"); m.NamesOther.Add("(r)-(+)-limonene"); m.NamesOther.Add("(r)-( )-limonene"); }
                        else if (m.Name == "borneol") { m.NamesOther.Add("isoborneol"); }
                        else if (m.Name == "Terpinolene") { m.NamesOther.Add("alpha-terpinolene"); }
                        else if (m.Name == "Terpineol") { m.NamesOther.Add("total terpineol"); m.NamesOther.Add("alpha-terpineol"); m.NamesOther.Add("terpineol"); }
                        else if (m.Name == "cis-Ocimene") { m.NamesOther.AddRange(["ocimenes", "ocimene"]); }
                        else if (m.Name == "α-Bisabolol") { m.NamesOther.Add("alpha-bisabolol"); }
                        else if (m.Name == "α-Humulene") { m.NamesOther.Add("alpha-humulene"); }
                        else if (m.Name == "α-Pinene") { m.NamesOther.Add("alpha-pinene"); }
                        else if (m.Name == "β-Caryophyllene") { m.NamesOther.Add("e-caryophyllene"); m.NamesOther.Add("beta-caryophyllene"); }
                        else if (m.Name == "β-Myrcene") { m.NamesOther.Add("beta-myrcene"); }
                        else if (m.Name == "β-Pinene") { m.NamesOther.Add("beta-pinene"); }
                        else if (m.Name == "α-Terpinene") { m.NamesOther.Add("alpha-terpinene"); }
                        else if (m.Name == "α-Terpinene") { m.NamesOther.Add("gamma-terpinene"); }
                        else if (m.Name == "δ-3-Carene") { m.NamesOther.Add("3-carene"); }

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

}