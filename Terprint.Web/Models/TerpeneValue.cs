using System.ComponentModel;
using System.ComponentModel.DataAnnotations;

namespace Terprint.Web.Models
{
    public class TerpeneValue
    {

        public int Id { get; set; }
        public string Grower
        { get; set; }
        [Required]
        public double Value { get; set; }
        public string Material { get; set; }
        [Display(Name="Terpene Name")]
        [Required]
        public string TerpeneName { get; set; }
        public string Strain { get; set; }
        public static string Batch { get; set; }
        public int BatchID { get; set; }
        public double Rating { get; set; }
        public string Scale {  get; set; }
        public DateOnly Date { get; set; }
    }
}
