namespace Terprint.Web.Models
{
    public class TerpeneValues
    {

        public int Id { get; set; }
        public string Grower
        { get; set; }
        public string Type
        { get; set; }
        public double Value { get; set; }
        public string Material { get; set; }
        public string TerpName { get; set; }
        public string Strain { get; set; }
        public static string Batch { get; set; }
        public double Rating { get; set; }
        public DateOnly Date { get; set; }
    }
}
