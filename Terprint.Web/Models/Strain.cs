
using System.ComponentModel.DataAnnotations;

namespace Terprint.Web.Models
{
    public class Strain
    {
        public DateTime created { get; set; } = DateTime.Now;
        public string? createdby { get; set; }
        public int StrainId { get; set; }
        //Terpene	Matrix	Row	Column	Color
        [Required]
        public string StrainName { get; set; }
        public string StrainDescription { get; set; }
        public ICollection<Batch> Batches { get;  }



    }
}
