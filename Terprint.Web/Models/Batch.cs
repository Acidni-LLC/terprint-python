
using NuGet.Common;
using System.ComponentModel.DataAnnotations;

namespace Terprint.Web.Models
{
    public class Batch
    {
        public int? BatchId { get; set; }
        [Required]
        //Terpene	Matrix	Row	Column	Color
        public string Name { get; set; }
        public string Type
        { get; set; }
        [DataType(DataType.Date)]
        [DisplayFormat(DataFormatString = "{0:yyyy-MM-dd}", ApplyFormatInEditMode = true)]

        public DateOnly Date { get; set; }
        public ICollection<TerpeneValue> TerpeneValues { get;  }
        public ICollection<Rating> Ratings { get; }
        public ICollection<THCLevel> THCLevels { get; }
        public Grower? Grower { get; set; }
        public int? GrowerID { get; set; }
        public int? StrainID { get; set; }



        public Batch()
        {
            BatchId = null;
            Grower = new Grower();
            Date =  new DateOnly( DateTime.Now.Year,DateTime.Now.Month,DateTime.Now.Day);
        }
    }
}
