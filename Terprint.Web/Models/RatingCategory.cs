using System.ComponentModel.DataAnnotations;

namespace Terprint.Web.Models
{
    public class RatingCategory
    {
        public int RatingCategoryId { get; set; }
        [Required]
        public string CategoryName { get; set; }

        public string CategoryDescription { get; set; }
        public string CategoryTitle { get; set; }
        public ICollection<Rating> Ratings { get;  }

    }
}
