using CyberRiskAPI.Models;
using Microsoft.AspNetCore.Mvc;
using System.Diagnostics;

namespace CyberRiskAPI.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;

        public HomeController(ILogger<HomeController> logger)
        {
            _logger = logger;
        }

        
        public IActionResult Index()
        {
            
            if (HttpContext.Session.GetString("Username") == null)
            {
                return RedirectToAction("Index", "Login");
            }

            ViewData["Title"] = "CyberRiskLingo Dashboard";
            ViewData["User"] = HttpContext.Session.GetString("Username");

            return View();
        }

        
        public IActionResult Privacy()
        {
            if (HttpContext.Session.GetString("Username") == null)
            {
                return RedirectToAction("Index", "Login");
            }

            ViewData["Title"] = "Privacy Policy";
            return View();
        }

        
        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel
            {
                RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier
            });
        }
    }
}