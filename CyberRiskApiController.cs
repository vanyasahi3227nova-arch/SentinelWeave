using CyberRiskAPI.Models;
using CyberRiskAPI.Services;
using Microsoft.AspNetCore.Mvc;

namespace CyberRiskAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class CyberRiskApiController : ControllerBase
    {
        private readonly CyberRiskService _service;
        private readonly NvdService _nvdService;

        public CyberRiskApiController(
            CyberRiskService service,
            NvdService nvdService)
        {
            _service = service;
            _nvdService = nvdService;
        }

        // GET ALL
        [HttpGet]
        public ActionResult<List<CyberRisk>> GetAll()
            => _service.GetAll();

        // GET BY ID
        [HttpGet("{id}")]
        public ActionResult<CyberRisk> GetById(string id)
        {
            var risk = _service.GetById(id);
            if (risk == null) return NotFound();
            return risk;
        }

        // CREATE
        [HttpPost]
        public ActionResult<CyberRisk> Create(CyberRisk risk)
        {
            risk.UpdateRiskLevel();

            var created = _service.Create(risk);

            return CreatedAtAction(nameof(GetById), new { id = created.Id }, created);
        }

        // UPDATE
        [HttpPut("{id}")]
        public IActionResult Update(string id, CyberRisk risk)
        {
            risk.UpdateRiskLevel();

            if (!_service.Update(id, risk))
                return NotFound();

            return NoContent();
        }

        // DELETE
        [HttpDelete("{id}")]
        public IActionResult Delete(string id)
        {
            if (!_service.Delete(id))
                return NotFound();

            return NoContent();
        }

        // NVD API
        [HttpGet("vulnerabilities/{assetName}")]
        public async Task<IActionResult> GetVulnerabilities(string assetName)
        {
            var result = await _nvdService.GetCvesAsync(assetName);

            if (result == null)
                return NotFound();

            return Ok(result);
        }
    }
}