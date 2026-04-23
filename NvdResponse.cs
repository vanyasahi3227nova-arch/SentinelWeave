using System.Collections.Generic;

namespace CyberRiskAPI.Models
{
    public class NvdResponse
    {
        public List<VulnerabilityItem> vulnerabilities { get; set; }
    }

    public class VulnerabilityItem
    {
        public Cve cve { get; set; }
    }

    public class Cve
    {
        public string id { get; set; }
        public List<Description> descriptions { get; set; }
        public Metrics metrics { get; set; }
    }

    public class Description
    {
        public string value { get; set; }
    }

    public class Metrics
    {
        public List<CvssMetricV31> cvssMetricV31 { get; set; }
    }

    public class CvssMetricV31
    {
        public CvssData cvssData { get; set; }
    }

    public class CvssData
    {
        public double baseScore { get; set; }
        public string baseSeverity { get; set; }
    }
}