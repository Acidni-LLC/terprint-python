using System.ComponentModel.DataAnnotations;

namespace Terprint.Web.Models
{
    public class Rating
    {
        public DateTime created { get; set; } = DateTime.Now;
        public int RatingId { get; set; }
        public string userid { get; set; }
        [Required]
        public int RatingCategoryID
 { get; set; }
        public string Value
        { get; set; }
        public string? Notes
        { get; set; }
        [Required]
        public int? BatchID { get; set; }

    }
}
