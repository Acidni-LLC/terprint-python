
using System.ComponentModel.DataAnnotations;

namespace Terprint.Web.Models
{
    public class THCValue
    {
        public DateTime created { get; set; } = DateTime.Now;
        public string? createdby { get; set; }

        public int THCValueId { get; set; }
        [Required]
        public int? BatchID { get; set; }

        public string Analyte { get; set; }
        public string? Dilution { get; set; }
        public string? LOD { get; set; }
        public string? LOQ { get; set; }

        public string Result { get; set; }

        public string Percent { get; set; }


    }
}
