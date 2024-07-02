namespace Terprint.Web.Models
{
    public class Ratings
    {
        public int Id { get; set; }
        public string userid { get; set; }
        public string batch { get; set; }
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
