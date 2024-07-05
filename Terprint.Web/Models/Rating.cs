using System.ComponentModel.DataAnnotations;

namespace Terprint.Web.Models
{
    public class Rating
    {
        public int RatingId { get; set; }
        public string userid { get; set; }
        [Required]
        public int? OverallRating
 { get; set; }
        public int? Taste
    { get; set; }
        public int? Effect
        { get; set; }
        public string? Notes
        { get; set; }
        public bool BuyAgain
        { get; set; }

    }
}
