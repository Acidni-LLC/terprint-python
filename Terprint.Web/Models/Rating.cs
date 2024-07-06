using System.ComponentModel.DataAnnotations;

namespace Terprint.Web.Models
{
    public class Rating
    {

        public int RatingId { get; set; }
        public int Growerid { get; set; }
        public string userid { get; set; }
        [Required]
        public int RatingCategoryID
 { get; set; }
        public int Value
        { get; set; }
        public string? Notes
        { get; set; }
        [Required]
        public int? BatchID { get; set; }

    }
}
