using System.ComponentModel;
using System.ComponentModel.DataAnnotations;

namespace Terprint.Web.Models
{
    public class TerpeneValue
    {

        public DateTime created { get; set; } = DateTime.Now;
        public int TerpeneValueId { get; set; }
        
        [Required]
        public double Value { get; set; }
        [Display(Name = "Terpene Name")]
        [Required]
        public string TerpeneName { get; set; }
        [Required]
        public int? BatchID { get; set; }
        public string? Scale { get; set; }
    }
}
