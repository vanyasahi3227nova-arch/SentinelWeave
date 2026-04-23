using System.Text.Json.Serialization;
using System.ComponentModel.DataAnnotations;
using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace CyberRiskAPI.Models
{
    public class CyberRisk
    {
        [BsonId]
        [BsonRepresentation(BsonType.ObjectId)]
        [JsonPropertyName("id")]
      
        public string Id { get; set; } = string.Empty;

        [Required]
        [JsonPropertyName("riskName")]
        public string RiskName { get; set; } = string.Empty;

        [JsonPropertyName("description")]
        public string Description { get; set; } = string.Empty;

        [Required]
        [JsonPropertyName("assetName")]
        public string AssetName { get; set; } = string.Empty;

        [Required]
        [JsonPropertyName("industry")]
        public string Industry { get; set; } = string.Empty;

        [Required]
        [JsonPropertyName("category")]
        public string Category { get; set; } = string.Empty;

        [Required]
        [Range(1, 10, ErrorMessage = "Impact must be between 1 and 10.")]
        [JsonPropertyName("impact")]
        public int Impact { get; set; }

        [Required]
        [Range(1, 10, ErrorMessage = "Likelihood must be between 1 and 10.")]
        [JsonPropertyName("likelihood")]
        public int Likelihood { get; set; }

        [JsonPropertyName("riskLevel")]
        public string RiskLevel { get; set; } = string.Empty;

        [JsonPropertyName("score")]
        public int Score { get; set; }

        [JsonPropertyName("mitigationStrategy")]
        public string MitigationStrategy { get; set; } = string.Empty;

        
        public void UpdateRiskLevel()
        {
            Score = Impact * Likelihood;

            RiskLevel = Score switch
            {
                >= 50 => "High",
                >= 25 => "Medium",
                _ => "Low"
            };

            MitigationStrategy = RiskLevel switch
            {
                "High" => "Implement immediate security controls, " +
                            "monitor assets closely, and plan incident response.",
                "Medium" => "Review security measures, apply best practices, " +
                            "and regularly monitor risks.",
                "Low" => "Maintain standard security procedures " +
                            "and periodically review risks.",
                _ => "Assess risk and define mitigation strategy."
            };
        }
    }
}