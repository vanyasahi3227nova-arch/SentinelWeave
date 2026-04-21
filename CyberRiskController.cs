using CyberRiskAPI.Models;
using CyberRiskAPI.Services;
using Microsoft.AspNetCore.Mvc;

namespace CyberRiskAPI.Controllers
{
    public class CyberRiskController : Controller
    {
        private readonly CyberRiskService _service;
        private readonly NvdService _nvdService;

        public CyberRiskController(
            CyberRiskService service,
            NvdService nvdService)
        {
            _service = service;
            _nvdService = nvdService;
        }

        // LIST
        public async Task<IActionResult> Index()
        {
            
            var risks = await _service.GetAllAsync();
            return View(risks);
        }

        // DETAILS
        public async Task<IActionResult> Details(string id)
        {
            var risk = await _service.GetByIdAsync(id);
            if (risk == null) return NotFound();
            return View(risk);
        }

        // CREATE (GET)
        public IActionResult Create() => View();

        // CREATE (POST) 
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create(CyberRisk risk)
        {
            
            risk.Id = null;

            
            ModelState.Remove("Id");

            if (!ModelState.IsValid)
            {
                
                foreach (var entry in ModelState)
                {
                    if (entry.Value.Errors.Any())
                        Console.WriteLine(
                            $"[ModelState] {entry.Key}: " +
                            string.Join(", ", entry.Value.Errors
                                .Select(e => e.ErrorMessage)));
                }
                return View(risk);
            }

            risk.UpdateRiskLevel();
            await _service.CreateAsync(risk);

            
            return RedirectToAction("Index", "CyberRisk");
        }

        // EDIT (GET)
        public async Task<IActionResult> Edit(string id)
        {
            var risk = await _service.GetByIdAsync(id);
            if (risk == null) return NotFound();
            return View(risk);
        }

        // EDIT (POST)
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Edit(string id, CyberRisk risk)
        {
            // ✅ Same fix — ensure Id is set from route, not form body
            risk.Id = id;
            ModelState.Remove("Id");

            if (!ModelState.IsValid)
                return View(risk);

            risk.UpdateRiskLevel();

            if (!await _service.UpdateAsync(id, risk))
                return NotFound();

            return RedirectToAction("Index", "CyberRisk");
        }

        // DELETE (GET)
        public async Task<IActionResult> Delete(string id)
        {
            var risk = await _service.GetByIdAsync(id);
            if (risk == null) return NotFound();
            return View(risk);
        }

        // DELETE (POST)
        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> DeleteConfirmed(string id)
        {
            await _service.DeleteAsync(id);
            return RedirectToAction("Index", "CyberRisk");
        }

        // NVD VIEW
        public async Task<IActionResult> Vulnerabilities(string assetName)
        {
            var data = await _nvdService.GetCvesAsync(assetName);
            return View(data);
        }
    }
}