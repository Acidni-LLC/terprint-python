using NuGet.Common;
using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace Terprint.Web.Models
{
    public class Batch
    {
        public DateTime created { get; set; } = DateTime.Now;
        public string? createdby { get; set; }
        public int? BatchId { get; set; }
        [Required]
        //Terpene	Matrix	Row	Column	Color
        public string Name { get; set; }
        public string Type { get; set; }
        [DataType(DataType.Date)]
        [DisplayFormat(DataFormatString = "{0:yyyy-MM-dd}", ApplyFormatInEditMode = true)]
        public DateOnly Date { get; set; }
        public IList<TerpeneValue> TerpeneValues { get; } = new List<TerpeneValue>();
        public IList<Rating> Ratings { get; } = new List<Rating>();
        public IList<THCValue> THCValues { get; } = new List<THCValue>();
        [JsonIgnore] // Ignore to prevent cycle during serialization
        public Grower? Grower { get; set; }
        public int? GrowerID { get; set; }
        public int? StrainID { get; set; }

        public Batch()
        {
            BatchId = null;
            // Removed: Grower = new Grower(); to avoid creating default instances unnecessarily
            Date = new DateOnly(DateTime.Now.Year, DateTime.Now.Month, DateTime.Now.Day);
        }
    }
}
