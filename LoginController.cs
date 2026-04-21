using Microsoft.AspNetCore.Mvc;
using WebsiteLogin.Models;
using System.Collections.Generic;
using System.Linq;
using Microsoft.AspNetCore.Http;

namespace WebsiteLogin.Controllers
{
    public class LoginController : Controller
    {
        private static readonly List<UserModel> ValidUsers = new()
        {
            new UserModel { ID = 1, Username = "samantha.morris@cyberrisklingo.com", Password = "password12" },
            new UserModel { ID = 2, Username = "brian.clark@cyberrisklingo.com", Password = "password_62" },
            new UserModel { ID = 3, Username = "victor.thomas@cyberrisklingo.com", Password = "password02!" },
            new UserModel { ID = 4, Username = "ava.brown@cyberrisklingo.com", Password = "Password01!" },
            new UserModel { ID = 5, Username = "chris.davis@cyberrisklingo.com", Password = "Password53!" },
            new UserModel { ID = 6, Username = "emily.foster@cyberrisklingo.com", Password = "Password03!" },
            new UserModel { ID = 7, Username = "george.harris@cyberrisklingo.com", Password = "Password04!" },
            new UserModel { ID = 8, Username = "isabella.jones@cyberrisklingo.com", Password = "Password05!" },
            new UserModel { ID = 9, Username = "kevin.lewis@cyberrisklingo.com", Password = "Password06!" },
            new UserModel { ID = 10, Username = "nina.martin@cyberrisklingo.com", Password = "Password07!" },
            new UserModel { ID = 11, Username = "oliver.white@cyberrisklingo.com", Password = "Password08!" },
            new UserModel { ID = 12, Username = "quinn.roberts@cyberrisklingo.com", Password = "Password09!" },
            new UserModel { ID = 13, Username = "steven.taylor@cyberrisklingo.com", Password = "Password10!" },
            new UserModel { ID = 14, Username = "uma.wilson@cyberrisklingo.com", Password = "Password11!" },
            new UserModel { ID = 15, Username = "william.xavier@cyberrisklingo.com", Password = "Password12!" },
            new UserModel { ID = 16, Username = "zoe.young@cyberrisklingo.com", Password = "Password13!" },
            new UserModel { ID = 17, Username = "liam.morgan@cyberrisklingo.com", Password = "Password14!" },
            new UserModel { ID = 18, Username = "nathan.phillips@cyberrisklingo.com", Password = "Password15!" }
        };

        [HttpGet]
        public IActionResult Index()
        {
            if (!string.IsNullOrEmpty(HttpContext.Session.GetString("Username")))
            {
                return RedirectToAction("Index", "Home");
            }

            ViewBag.PageTitle = "CyberRiskLingo Login Portal";
            return View(new UserModel());
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult ProcessLogin(UserModel user)
        {
            if (!ModelState.IsValid)
            {
                TempData["Message"] = "Please complete all fields.";
                return View("Index", user);
            }

            var match = ValidUsers.FirstOrDefault(u =>
                u.Username == user.Username &&
                u.Password == user.Password);

            if (match != null)
            {
                HttpContext.Session.SetString("Username", match.Username);

                TempData["Message"] = $"Welcome {match.Username}";
                return RedirectToAction("Index", "Home");
            }

            TempData["Message"] = "Invalid corporate credentials. Access denied.";
            user.Password = "";
            return View("Index", user);
        }

        [HttpPost]
        public IActionResult Logout()
        {
            HttpContext.Session.Clear();
            return RedirectToAction("Index", "Login");
        }
    }
}