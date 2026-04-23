using CyberRiskAPI.Models;
using System.Net.Http;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace CyberRiskAPI.Services
{
    public class NvdService
    {
        private readonly HttpClient _httpClient;

        public NvdService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<NvdResponse> GetCvesAsync(string keyword)
        {
            
            var url = $"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={keyword}&resultsPerPage=5";

            var response = await _httpClient.GetAsync(url);

            if (!response.IsSuccessStatusCode)
            {
                return null;
            }

            var json = await response.Content.ReadAsStringAsync();

            return JsonConvert.DeserializeObject<NvdResponse>(json);
        }
    }
}