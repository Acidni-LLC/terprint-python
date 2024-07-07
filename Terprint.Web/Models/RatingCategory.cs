using System.ComponentModel.DataAnnotations;

namespace Terprint.Web.Models
{
    public class RatingCategory
    {
        public int RatingCategoryId { get; set; }
        [Display(Name = "Rating Category Type"), DataType(DataType.Text)]
        public string RatingCategoryType { get; set; }
        [Required]
        [Display(Name = "Category Name"), DataType(DataType.Text)]
        public string CategoryName { get; set; }

        [Display(Name = "Category Description"), DataType(DataType.Text)]
        public string CategoryDescription { get; set; }
        [Display(Name = "Category Title"), DataType(DataType.Text)]
        public string CategoryTitle { get; set; }
        public IList<Rating> Ratings { get;  }

    }
}
