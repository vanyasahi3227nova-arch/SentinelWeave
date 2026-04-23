using System.ComponentModel.DataAnnotations;

namespace WebsiteLogin.Models
{
    public class UserModel
    {
        public int ID { get; set; }

        [Required(ErrorMessage = "Username is required.")]
        public string? Username { get; set; }

        [Required(ErrorMessage = "Password is required.")]
        [DataType(DataType.Password)]
        public string? Password { get; set; }
    }
}

